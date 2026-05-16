"""Tests for the remote PEP 503 index fetcher and the merge integration."""
from io import BytesIO
from pathlib import Path
from typing import Any
from unittest.mock import patch

from index_503.index import make_index
from index_503.remote_index import (
    RemoteEntry,
    _parse_project_page,
    _parse_top_index,
    fetch_remote_index,
)

from . import FIXTURES
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


def _fake_urlopen_factory(pages: dict[str, str]) -> Any:
    def _fake_urlopen(request: Any, timeout: int = 30) -> _FakeResponse:
        url = request.full_url if hasattr(request, "full_url") else str(request)
        body = pages[url].encode("utf-8")
        return _FakeResponse(body)

    return _fake_urlopen


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


def test_fetch_remote_index_returns_empty_on_error() -> None:
    def _boom(*args: Any, **kwargs: Any) -> Any:
        raise OSError("nope")

    with patch("index_503.remote_index.urlopen", side_effect=_boom):
        assert fetch_remote_index("https://example.invalid/simple/") == {}


def test_make_index_merges_remote_only_wheels(tmp_path: Path) -> None:
    """Remote-only wheels are added as absolute-URL anchors; local ones win."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
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
    te_page = origin_path_index.joinpath(
        "typing-extensions", "index.html"
    ).read_text()
    assert "remote-te-hash" not in te_page


def test_remote_entry_as_anchor_emits_attributes() -> None:
    from airium import Airium

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
