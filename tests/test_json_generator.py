from typing import Any

from index_503.json_generator import (
    API_VERSION,
    generate_index_json,
    generate_project_page_json,
)
from index_503.wheel_file import WHEEL_FILE_VERSION, WheelFile


def _wheel(**overrides: Any) -> WheelFile:
    base: dict[str, Any] = dict(
        version=WHEEL_FILE_VERSION,
        canonical_name="example",
        filename="example-1.0-py3-none-any.whl",
        metadata_name="Example",
        wheel_hash="a" * 64,
        requires_python=">=3.8",
        metadata_hash="b" * 64,
        mtime=1.0,
        size=1234,
    )
    base.update(overrides)
    return WheelFile(**base)


def test_generate_index_json_canonicalizes_and_sorts() -> None:
    payload = generate_index_json(["Foo_Bar", "alpha", "Zeta", "alpha"])
    assert payload["meta"] == {"api-version": API_VERSION}
    names = [p["name"] for p in payload["projects"]]
    # canonicalized + natsort case-insensitive ordering
    assert names == ["alpha", "alpha", "foo-bar", "zeta"]


def test_generate_project_page_json_full_entry() -> None:
    wheel = _wheel()
    payload = generate_project_page_json("Example", [wheel], "../")
    assert payload["meta"] == {"api-version": API_VERSION}
    assert payload["name"] == "example"
    [entry] = payload["files"]
    assert entry == {
        "filename": "example-1.0-py3-none-any.whl",
        "url": "../example-1.0-py3-none-any.whl",
        "hashes": {"sha256": "a" * 64},
        "requires-python": ">=3.8",
        "core-metadata": {"sha256": "b" * 64},
        "size": 1234,
    }


def test_generate_project_page_json_omits_optional_fields() -> None:
    wheel = _wheel(requires_python=None, metadata_hash=None, size=None)
    [entry] = generate_project_page_json("example", [wheel], "/")["files"]
    assert "requires-python" not in entry
    assert "core-metadata" not in entry
    assert "size" not in entry


def test_generate_project_page_json_core_metadata_true_passthrough() -> None:
    wheel = _wheel(metadata_hash=True)
    [entry] = generate_project_page_json("example", [wheel], "/")["files"]
    assert entry["core-metadata"] is True


def test_generate_project_page_json_no_files() -> None:
    payload = generate_project_page_json("example", [], "/")
    assert payload["files"] == []
    assert payload["name"] == "example"
