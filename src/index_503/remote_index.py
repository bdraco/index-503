"""Fetch and parse remote PEP 503 simple indexes for merging."""

import logging
import re
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from http.client import HTTPException
from typing import Optional
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from airium import Airium

from .util import canonicalize_name

_LOGGER = logging.getLogger(__name__)

_USER_AGENT = "index-503"
_DEFAULT_TIMEOUT = 30

# A canonicalized (PEP 503) project name only ever contains these characters.
_CANONICAL_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


class RemoteIndexError(Exception):
    """Raised when a remote index cannot be fetched or decoded."""


@dataclass
class RemoteEntry:
    """A wheel entry parsed from a remote PEP 503 project page."""

    filename: str
    href: str  # absolute URL, may include ``#sha256=...`` fragment
    requires_python: Optional[str] = None
    dist_info_metadata: Optional[str] = None  # raw PEP 658 attribute value
    core_metadata: Optional[str] = None  # raw PEP 714 attribute value

    def as_anchor(self, page: Airium) -> None:
        """Emit an anchor tag preserving the remote attributes.

        Every value came from a remote page and was entity-decoded by the
        parser, so each one is escaped exactly once here (Airium does not
        escape attribute values or text).
        """
        kwargs: dict[str, str] = {"href": escape(self.href, quote=True)}
        if self.requires_python is not None:
            kwargs["data-requires-python"] = escape(self.requires_python, quote=True)
        if self.dist_info_metadata is not None:
            kwargs["data-dist-info-metadata"] = escape(
                self.dist_info_metadata, quote=True
            )
        if self.core_metadata is not None:
            kwargs["data-core-metadata"] = escape(self.core_metadata, quote=True)
        with page.a(**kwargs):
            page(escape(self.filename))


class _AnchorParser(HTMLParser):
    """Collect anchor tags (href + attrs + text) from a simple index page."""

    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[tuple[dict[str, str], str]] = []
        self._current_attrs: Optional[dict[str, str]] = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag == "a":
            self._current_attrs = {k: v for k, v in attrs if v is not None}
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_attrs is not None:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current_attrs is not None:
            text = "".join(self._current_text).strip()
            self.anchors.append((self._current_attrs, text))
            self._current_attrs = None
            self._current_text = []


def _fetch(url: str, timeout: int) -> str:
    """Fetch a URL and return the decoded body.

    :raises RemoteIndexError: if the request fails or the body cannot be
        decoded with the charset the server advertised.
    """
    try:
        request = Request(
            url, headers={"User-Agent": _USER_AGENT, "Accept": "text/html"}
        )
        with urlopen(request, timeout=timeout) as response:  # noqa: S310  # nosec B310
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except (URLError, OSError, HTTPException, ValueError, LookupError) as exc:
        # URLError covers HTTPError and network failures; OSError covers
        # socket timeouts; HTTPException covers IncompleteRead; ValueError
        # covers a URL without a scheme and UnicodeDecodeError; LookupError
        # covers an unknown charset.
        raise RemoteIndexError(f"Failed to fetch {url}: {exc}") from exc


def _parse_anchors(html: str) -> list[tuple[dict[str, str], str]]:
    parser = _AnchorParser()
    parser.feed(html)
    parser.close()
    return parser.anchors


def _parse_top_index(html: str) -> list[str]:
    """Return the list of project hrefs from a top-level simple index page.

    Anchors whose text is a wheel filename are not project links (a plain
    directory listing of wheels has them on the top page) and are skipped;
    :func:`_parse_project_page` collects those from the same page instead.
    """
    return [
        attrs["href"]
        for attrs, text in _parse_anchors(html)
        if "href" in attrs and not text.endswith(".whl")
    ]


def _parse_project_page(html: str, page_url: str) -> list[RemoteEntry]:
    """Return the wheel entries from a project page, with absolute hrefs."""
    entries: list[RemoteEntry] = []
    for attrs, text in _parse_anchors(html):
        href = attrs.get("href")
        if not href or not text:
            continue
        # Only collect wheel entries — skip sdists and other formats.
        if not text.endswith(".whl"):
            continue
        entries.append(
            RemoteEntry(
                filename=text,
                href=urljoin(page_url, href),
                requires_python=attrs.get("data-requires-python"),
                dist_info_metadata=attrs.get("data-dist-info-metadata"),
                core_metadata=attrs.get("data-core-metadata"),
            )
        )
    return entries


def _project_name_from_filename(filename: str) -> Optional[str]:
    """Return the canonical project name of a wheel filename, or None.

    PEP 427: the distribution name is the first dash-separated field. The
    result is validated against the canonical-name alphabet because it is
    used as a directory name in the generated index.
    """
    canonical = canonicalize_name(filename.split("-", 1)[0])
    if not _CANONICAL_NAME_RE.match(canonical):
        return None
    return canonical


def _resolve_project_url(
    base_url: str, project_href: str, directories_only: bool
) -> Optional[str]:
    """Return the absolute project page URL for a top-level link, or None.

    Links that cannot be project pages are dropped: sort links of a plain
    directory listing (query string), fragment-only links and anything that
    resolves outside ``base_url`` such as a parent-directory link. With
    ``directories_only`` (the top page is a file listing) only links that
    already end in ``/`` are followed, so sdists and other files are never
    requested as project pages.
    """
    if directories_only and not project_href.endswith("/"):
        return None
    project_url = urljoin(base_url, project_href)
    parts = urlsplit(project_url)
    if parts.query or parts.fragment:
        return None
    if not project_url.endswith("/"):
        project_url = project_url + "/"
    if project_url == base_url or not project_url.startswith(base_url):
        return None
    return project_url


def fetch_remote_index(
    base_url: str, timeout: int = _DEFAULT_TIMEOUT
) -> dict[str, list[RemoteEntry]]:
    """Fetch a remote PEP 503 index and return entries grouped by canonical name.

    Wheel links on the top-level page itself are collected too, so a plain
    web server directory listing of wheels works as well as a generated index.
    Entries are grouped by the project name parsed from the wheel filename
    (the same name local wheels are grouped by), never by the remote link
    text or path.

    :raises RemoteIndexError: if the top-level index or any project page
        cannot be fetched. Nothing is returned on partial failure so a
        transient error can never publish an index missing remote wheels.
    """
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    index_html = _fetch(base_url, timeout)
    index_anchors = _parse_anchors(index_html)
    if not index_anchors:
        _LOGGER.warning(
            "Remote index %s contains no links; is it a simple index?", base_url
        )

    # canonical project name -> {filename: entry}. Keying on the filename
    # deduplicates a page that is reachable through several links.
    result: dict[str, dict[str, RemoteEntry]] = {}

    def _add_entries(page_url: str, entries: list[RemoteEntry]) -> None:
        for entry in entries:
            canonical = _project_name_from_filename(entry.filename)
            if canonical is None:
                _LOGGER.warning(
                    "Skipping remote file %r on %s: not a valid wheel filename",
                    entry.filename,
                    page_url,
                )
                continue
            result.setdefault(canonical, {}).setdefault(entry.filename, entry)

    top_entries = _parse_project_page(index_html, base_url)
    _add_entries(base_url, top_entries)
    # Wheel links on the top page mean it is a file listing, not a generated
    # index, so only its sub-directories can hold further wheels.
    is_listing = bool(top_entries)

    seen_urls: set[str] = set()
    for project_href in _parse_top_index(index_html):
        project_url = _resolve_project_url(base_url, project_href, is_listing)
        if project_url is None:
            _LOGGER.debug("Skipping non-project link %r on %s", project_href, base_url)
            continue
        if project_url in seen_urls:
            continue
        seen_urls.add(project_url)
        page_html = _fetch(project_url, timeout)
        entries = _parse_project_page(page_html, project_url)
        if not entries:
            _LOGGER.debug("Remote page %s contains no wheel links", project_url)
            continue
        _add_entries(project_url, entries)
    return {name: list(entries.values()) for name, entries in result.items()}
