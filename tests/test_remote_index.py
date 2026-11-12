"""Tests for the remote PEP 503 index fetcher and the merge integration."""

from io import BytesIO
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import URLError

import pytest
from airium import Airium
from click.testing import CliRunner

from index_503.index import make_index
from index_503.main import main_cli
from index_503.remote_index import (
    RemoteEntry,
    RemoteIndexError,
    _parse_project_page,
    _parse_top_index,
    fetch_remote_index,
)

from .test_index import setup_wheels

TEST_WHEELS = (
    "bleak-0.17.0-py3-none-any.whl",
    "typing_extensions-4.2.0-py3-none-any.whl",
)


_TOP_INDEX_HTML = """<!DOCTYPE html>
<html><body>
<a href="bleak/">bleak</a><br>
<a href="other-pkg/">other-pkg</a><br>
<a href="typing-extensions/">typing-extensions</a><br>
</body></html>
"""

_BLEAK_PAGE_HTML = """<!DOCTYPE html>
<html><body>
<a href="../bleak-0.17.0-py3-none-any.whl#sha256=remote-hash-A"
   data-requires-python="&gt;=3.7,&lt;4.0"
   data-dist-info-metadata="sha256=meta-hash-A">bleak-0.17.0-py3-none-any.whl</a><br>
<a href="../bleak-0.18.0-py3-none-any.whl#sha256=remote-hash-B"
   data-requires-python="&gt;=3.7"
   data-core-metadata="sha256=meta-hash-B">bleak-0.18.0-py3-none-any.whl</a><br>
</body></html>
"""

_OTHER_PAGE_HTML = """<!DOCTYPE html>
<html><body>
<a href="../other_pkg-1.2.3-py3-none-any.whl#sha256=other-hash">other_pkg-1.2.3-py3-none-any.whl</a><br>
<a href="../other_pkg-1.2.3.tar.gz#sha256=sdist-hash">other_pkg-1.2.3.tar.gz</a><br>
</body></html>
"""

_TYPING_EXT_PAGE_HTML = """<!DOCTYPE html>
<html><body>
<a href="../typing_extensions-4.2.0-py3-none-any.whl#sha256=remote-te-hash">typing_extensions-4.2.0-py3-none-any.whl</a><br>
</body></html>
"""

# A plain Apache-style directory listing of the wheel directory itself (not a
# generated index): sort links with query strings, a parent link and the wheel
# files as anchors on the top page.
_DIR_LISTING_HTML = """<!DOCTYPE html>
<html><body><h1>Index of /musllinux</h1>
<a href="?C=N;O=D">Name</a> <a href="?C=M;O=A">Last modified</a>
<a href="/">Parent Directory</a>
<a href="bleak-0.18.0-py3-none-any.whl">bleak-0.18.0-py3-none-any.whl</a>
<a href="other_pkg-1.2.3-py3-none-any.whl">other_pkg-1.2.3-py3-none-any.whl</a>
<a href="other_pkg-1.2.3.tar.gz">other_pkg-1.2.3.tar.gz</a>
<a href="-1.0-py3-none-any.whl">-1.0-py3-none-any.whl</a>
</body></html>
"""


class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self._body = BytesIO(body)
        self.headers = type(
            "H", (), {"get_content_charset": staticmethod(lambda: "utf-8")}
        )()

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: Any) -> None:
        self._body.close()

    def read(self) -> bytes:
        return self._body.read()


def _fake_urlopen_factory(pages: dict[str, Any]) -> Any:
    """Serve ``pages`` by URL; a value that is an exception is raised instead."""

    def _fake_urlopen(request: Any, timeout: int = 30) -> _FakeResponse:
        url = request.full_url if hasattr(request, "full_url") else str(request)
        page = pages[url]
        if isinstance(page, Exception):
            raise page
        return _FakeResponse(page.encode("utf-8"))

    return _fake_urlopen


def _generated_index_pages(base: str) -> dict[str, Any]:
    return {
        base: _TOP_INDEX_HTML,
        base + "bleak/": _BLEAK_PAGE_HTML,
        base + "other-pkg/": _OTHER_PAGE_HTML,
        base + "typing-extensions/": _TYPING_EXT_PAGE_HTML,
    }


def test_parse_top_index_returns_project_hrefs() -> None:
    hrefs = _parse_top_index(_TOP_INDEX_HTML)
    assert hrefs == ["bleak/", "other-pkg/", "typing-extensions/"]


def test_parse_project_page_only_keeps_wheels_with_absolute_href() -> None:
    entries = _parse_project_page(
        _OTHER_PAGE_HTML, "https://example.com/simple/other-pkg/"
    )
    assert len(entries) == 1
    entry = entries[0]
    assert entry.filename == "other_pkg-1.2.3-py3-none-any.whl"
    assert entry.href == (
        "https://example.com/simple/other_pkg-1.2.3-py3-none-any.whl#sha256=other-hash"
    )


def test_parse_project_page_preserves_metadata_attrs() -> None:
    entries = _parse_project_page(_BLEAK_PAGE_HTML, "https://example.com/simple/bleak/")
    assert {e.filename for e in entries} == {
        "bleak-0.17.0-py3-none-any.whl",
        "bleak-0.18.0-py3-none-any.whl",
    }
    by_name = {e.filename: e for e in entries}
    older = by_name["bleak-0.17.0-py3-none-any.whl"]
    assert older.requires_python == ">=3.7,<4.0"
    assert older.dist_info_metadata == "sha256=meta-hash-A"
    assert older.core_metadata is None
    newer = by_name["bleak-0.18.0-py3-none-any.whl"]
    assert newer.core_metadata == "sha256=meta-hash-B"
    assert newer.dist_info_metadata is None


def test_fetch_remote_index_groups_by_canonical_name() -> None:
    base = "https://example.com/simple/"
    pages = {
        base: _TOP_INDEX_HTML,
        base + "bleak/": _BLEAK_PAGE_HTML,
        base + "other-pkg/": _OTHER_PAGE_HTML,
        base + "typing-extensions/": _TYPING_EXT_PAGE_HTML,
    }
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        result = fetch_remote_index(base)

    assert set(result) == {"bleak", "other-pkg", "typing-extensions"}
    assert {e.filename for e in result["bleak"]} == {
        "bleak-0.17.0-py3-none-any.whl",
        "bleak-0.18.0-py3-none-any.whl",
    }
    assert [e.filename for e in result["other-pkg"]] == [
        "other_pkg-1.2.3-py3-none-any.whl"
    ]


def test_fetch_remote_index_raises_on_top_level_error() -> None:
    def _boom(*args: Any, **kwargs: Any) -> Any:
        raise OSError("nope")

    with patch("index_503.remote_index.urlopen", side_effect=_boom), pytest.raises(
        RemoteIndexError, match="https://example.invalid/simple/.*nope"
    ):
        fetch_remote_index("https://example.invalid/simple/")


def test_fetch_remote_index_raises_on_project_page_error() -> None:
    """A single failed project page fails the whole fetch, never a partial result."""
    base = "https://example.com/simple/"
    pages = _generated_index_pages(base)
    pages[base + "other-pkg/"] = URLError("connection reset")
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ), pytest.raises(RemoteIndexError, match="other-pkg/.*connection reset"):
        fetch_remote_index(base)


def test_fetch_remote_index_raises_on_missing_scheme() -> None:
    with pytest.raises(RemoteIndexError, match="unknown url type"):
        fetch_remote_index("wheels.example.com/simple/")


def test_fetch_remote_index_raises_on_undecodable_body() -> None:
    def _fake_urlopen(request: Any, timeout: int = 30) -> _FakeResponse:
        return _FakeResponse(b"<a href='x/'>\xff\xfe</a>")

    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen
    ), pytest.raises(RemoteIndexError, match="utf-8"):
        fetch_remote_index("https://example.com/simple/")


def test_fetch_remote_index_deduplicates_filenames() -> None:
    base = "https://example.com/simple/"
    pages = _generated_index_pages(base)
    pages[base + "bleak/"] = _BLEAK_PAGE_HTML + _BLEAK_PAGE_HTML
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        result = fetch_remote_index(base)

    assert sorted(e.filename for e in result["bleak"]) == [
        "bleak-0.17.0-py3-none-any.whl",
        "bleak-0.18.0-py3-none-any.whl",
    ]


def test_fetch_remote_index_groups_by_wheel_filename_not_href() -> None:
    """The project name comes from the wheel, even if the remote path differs."""
    base = "https://example.com/simple/"
    pages = {
        base: '<a href="weird-dir/">weird-dir</a>',
        base + "weird-dir/": _BLEAK_PAGE_HTML,
    }
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        result = fetch_remote_index(base)

    assert set(result) == {"bleak"}


def test_fetch_remote_index_from_directory_listing() -> None:
    """A plain directory listing of wheels (no generated index) merges cleanly."""
    base = "https://example.com/musllinux/"
    pages = {base: _DIR_LISTING_HTML}
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        result = fetch_remote_index(base)

    # Sort links, the parent link, the sdist and the wheel files themselves are
    # never fetched as project pages; the unparseable "-1.0-..." wheel is skipped.
    assert set(result) == {"bleak", "other-pkg"}
    assert [e.href for e in result["bleak"]] == [
        "https://example.com/musllinux/bleak-0.18.0-py3-none-any.whl"
    ]
    assert [e.filename for e in result["other-pkg"]] == [
        "other_pkg-1.2.3-py3-none-any.whl"
    ]


def test_fetch_remote_index_warns_on_page_without_links(
    caplog: pytest.LogCaptureFixture,
) -> None:
    base = "https://example.com/simple/"
    pages = {base: "<html><body>Please log in</body></html>"}
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        assert fetch_remote_index(base) == {}
    assert "contains no links" in caplog.text


def test_make_index_merges_remote_only_wheels(tmp_path: Path) -> None:
    """Remote-only wheels are added as absolute-URL anchors; local ones win."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    base = "https://example.com/simple/"
    pages = _generated_index_pages(base)
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ):
        assert make_index(origin_path, merge_with=base) == origin_path_index

    top = origin_path_index.joinpath("index.html").read_text()
    assert "/bleak/" in top
    assert "/other-pkg/" in top
    assert "/typing-extensions/" in top

    bleak_page = origin_path_index.joinpath("bleak", "index.html").read_text()
    # Local bleak 0.17.0 keeps its true sha256 from the actual wheel.
    assert "remote-hash-A" not in bleak_page
    # Remote-only 0.18.0 is appended with its absolute URL.
    assert (
        "https://example.com/simple/bleak-0.18.0-py3-none-any.whl#sha256=remote-hash-B"
        in bleak_page
    )
    assert "data-core-metadata" in bleak_page

    # Remote-only project gets its own page with absolute links.
    other_page = origin_path_index.joinpath("other-pkg", "index.html").read_text()
    assert (
        "https://example.com/simple/other_pkg-1.2.3-py3-none-any.whl#sha256=other-hash"
        in other_page
    )

    # typing-extensions has only a local wheel with the same filename as remote,
    # so the project page must not contain the remote hash.
    te_page = origin_path_index.joinpath("typing-extensions", "index.html").read_text()
    assert "remote-te-hash" not in te_page


def test_make_index_fetch_failure_keeps_existing_index(tmp_path: Path) -> None:
    """A fetch error fails the build and leaves the previous index untouched."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    assert make_index(origin_path) == origin_path_index
    before = origin_path_index.joinpath("bleak", "index.html").read_text()
    assert not origin_path_index.joinpath("other-pkg").exists()

    base = "https://example.com/simple/"
    pages = _generated_index_pages(base)
    pages[base + "other-pkg/"] = URLError("timed out")
    with patch(
        "index_503.remote_index.urlopen", side_effect=_fake_urlopen_factory(pages)
    ), pytest.raises(RemoteIndexError):
        make_index(origin_path, merge_with=base)

    assert origin_path_index.joinpath("bleak", "index.html").read_text() == before
    assert not origin_path_index.joinpath("other-pkg").exists()
    assert {p.name for p in tmp_path.iterdir()} == {
        "musllinux",
        "musllinux-index",
        ".musllinux.index_503.lock",
    }


def test_main_cli_merge_with_is_passed_through(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    monkeypatch.chdir(tmp_path)
    base = "https://example.com/simple/"
    with patch(
        "index_503.remote_index.urlopen",
        side_effect=_fake_urlopen_factory(_generated_index_pages(base)),
    ):
        result = CliRunner().invoke(main_cli, ["musllinux", "--merge-with", base])

    assert result.exit_code == 0, result.output
    assert origin_path_index.joinpath("other-pkg", "index.html").exists()


def test_main_cli_merge_with_fetch_failure_is_clean_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    monkeypatch.chdir(tmp_path)
    base = "https://example.invalid/simple/"
    with patch(
        "index_503.remote_index.urlopen",
        side_effect=_fake_urlopen_factory({base: URLError("name or service")}),
    ):
        result = CliRunner().invoke(main_cli, ["musllinux", "--merge-with", base])

    assert result.exit_code == 1, result.output
    assert "Error: Failed to fetch https://example.invalid/simple/" in result.output
    assert "Traceback" not in result.output
    assert not origin_path_index.exists()


@pytest.mark.parametrize("url", ["wheels.example.com/simple", "file:///tmp/x"])
def test_main_cli_merge_with_rejects_non_http_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, url: str
) -> None:
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["musllinux", "--merge-with", url])

    assert result.exit_code == 2, result.output
    assert "expected an http(s) URL" in result.output
    assert not origin_path_index.exists()


def test_remote_entry_as_anchor_escapes_remote_values() -> None:
    """Values arrive entity-decoded from the parser and must be escaped once."""
    entries = _parse_project_page(
        '<a href="../foo-1.0-py3-none-any.whl?a=1&amp;b=2#sha256=abc"'
        ' data-core-metadata="sha256=abc&quot; onclick=&quot;x">'
        "foo-1.0-py3-none-any.whl</a>",
        "https://example.com/simple/foo/",
    )
    assert entries[0].href == (
        "https://example.com/simple/foo-1.0-py3-none-any.whl?a=1&b=2#sha256=abc"
    )
    page = Airium()
    entries[0].as_anchor(page)
    html = str(page)
    assert (
        'href="https://example.com/simple/foo-1.0-py3-none-any.whl'
        '?a=1&amp;b=2#sha256=abc"' in html
    )
    assert 'data-core-metadata="sha256=abc&quot; onclick=&quot;x"' in html
    assert ' onclick="x"' not in html


def test_remote_entry_as_anchor_emits_attributes() -> None:
    page = Airium()
    RemoteEntry(
        filename="foo-1.0-py3-none-any.whl",
        href="https://example.com/foo-1.0-py3-none-any.whl#sha256=abc",
        requires_python=">=3.9",
        dist_info_metadata="sha256=def",
    ).as_anchor(page)
    html = str(page)
    assert 'href="https://example.com/foo-1.0-py3-none-any.whl#sha256=abc"' in html
    assert 'data-requires-python="&gt;=3.9"' in html
    assert 'data-dist-info-metadata="sha256=def"' in html
    assert "foo-1.0-py3-none-any.whl" in html
    assert "</a>" in html
