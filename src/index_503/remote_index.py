"""Fetch and parse remote PEP 503 simple indexes for merging."""

import logging
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from typing import Optional
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from airium import Airium

from .util import canonicalize_name

_LOGGER = logging.getLogger(__name__)

_USER_AGENT = "index-503"
_DEFAULT_TIMEOUT = 30


@dataclass
class RemoteEntry:
    """A wheel entry parsed from a remote PEP 503 project page."""

    filename: str
    href: str  # absolute URL, may include ``#sha256=...`` fragment
    requires_python: Optional[str] = None
    dist_info_metadata: Optional[str] = None  # raw PEP 658 attribute value
    core_metadata: Optional[str] = None  # raw PEP 714 attribute value

    def as_anchor(self, page: Airium) -> None:
        """Emit an anchor tag preserving the remote attributes."""
        kwargs: dict[str, str] = {"href": self.href}
        if self.requires_python is not None:
            kwargs["data-requires-python"] = escape(self.requires_python)
        if self.dist_info_metadata is not None:
            kwargs["data-dist-info-metadata"] = self.dist_info_metadata
        if self.core_metadata is not None:
            kwargs["data-core-metadata"] = self.core_metadata
        with page.a(**kwargs):
            page(self.filename)


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
    """Fetch a URL and return the decoded body."""
    request = Request(url, headers={"User-Agent": _USER_AGENT, "Accept": "text/html"})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _parse_anchors(html: str) -> list[tuple[dict[str, str], str]]:
    parser = _AnchorParser()
    parser.feed(html)
    parser.close()
    return parser.anchors


def _parse_top_index(html: str) -> list[str]:
    """Return the list of project hrefs from a top-level simple index page."""
    return [attrs["href"] for attrs, _ in _parse_anchors(html) if "href" in attrs]


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


def fetch_remote_index(
    base_url: str, timeout: int = _DEFAULT_TIMEOUT
) -> dict[str, list[RemoteEntry]]:
    """Fetch a remote PEP 503 index and return entries grouped by canonical name.

    Returns an empty dict if the index cannot be reached.
    """
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    try:
        index_html = _fetch(base_url, timeout)
    except (URLError, OSError) as exc:
        _LOGGER.warning("Failed to fetch remote index %s: %s", base_url, exc)
        return {}

    result: dict[str, list[RemoteEntry]] = {}
    for project_href in _parse_top_index(index_html):
        project_url = urljoin(base_url, project_href)
        if not project_url.endswith("/"):
            project_url = project_url + "/"
        try:
            page_html = _fetch(project_url, timeout)
        except (URLError, OSError) as exc:
            _LOGGER.warning(
                "Failed to fetch remote project page %s: %s", project_url, exc
            )
            continue
        entries = _parse_project_page(page_html, project_url)
        if not entries:
            continue
        # Use the filename's canonical project name when possible so we match
        # local projects even if the remote uses a non-canonical directory name.
        project_name = project_href.strip("/").split("/")[-1]
        canonical = canonicalize_name(project_name)
        # Deduplicate by filename within the same project.
        seen: set[str] = set()
        unique: list[RemoteEntry] = []
        for entry in entries:
            if entry.filename in seen:
                continue
            seen.add(entry.filename)
            unique.append(entry)
        result.setdefault(canonical, []).extend(unique)
    return result
