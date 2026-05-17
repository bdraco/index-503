import json
from pathlib import Path

import pytest

from index_503.cache import CACHE_FILE, IndexCache


def test_cache(tmp_path: Path) -> None:
    source_path = tmp_path.joinpath("source")
    source_path.mkdir()
    target_path = tmp_path.joinpath("target")
    target_path.mkdir()

    cache = IndexCache(source_path)
    cache.load()
    assert cache.cache == {}
    cache.cache["foo"] = {"bar": "baz"}
    cache.cache["baz"] = {"qux": "quux"}
    cache.write_to_new(target_path)

    cache2 = IndexCache(target_path)
    cache2.load()
    assert cache2.cache == {"foo": {"bar": "baz"}, "baz": {"qux": "quux"}}
    target_path2 = tmp_path.joinpath("target2")
    target_path2.mkdir()
    cache2.remove_stale_keys({"foo"})
    cache2.write_to_new(target_path2)

    cache3 = IndexCache(target_path2)
    cache3.load()
    assert cache3.cache == {"foo": {"bar": "baz"}}


def test_cache_write_is_sorted_and_compact(tmp_path: Path) -> None:
    """Cache is written with sorted keys and no whitespace.

    A stable byte representation makes diffs between runs reflect real
    changes rather than dict ordering.
    """
    source_path = tmp_path.joinpath("source")
    source_path.mkdir()
    target_path = tmp_path.joinpath("target")
    target_path.mkdir()

    cache = IndexCache(source_path)
    cache.cache["zzz"] = {"b": 2, "a": 1}
    cache.cache["aaa"] = {"d": 4, "c": 3}
    cache.write_to_new(target_path)

    on_disk = target_path.joinpath(CACHE_FILE).read_text()
    # sorted, no whitespace, no trailing newline -> compact + deterministic
    assert on_disk == '{"aaa":{"c":3,"d":4},"zzz":{"a":1,"b":2}}'


def test_cache_load_corrupt_json_recovers(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A corrupt cache file is treated as empty, not fatal."""
    target_path = tmp_path.joinpath("target")
    target_path.mkdir()
    target_path.joinpath(CACHE_FILE).write_text("{not json")

    cache = IndexCache(target_path)
    with caplog.at_level("WARNING"):
        cache.load()

    assert cache.cache == {}
    assert "unreadable" in caplog.text


def test_cache_load_non_object_recovers(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A valid-JSON but non-object cache file is treated as empty."""
    target_path = tmp_path.joinpath("target")
    target_path.mkdir()
    target_path.joinpath(CACHE_FILE).write_text(json.dumps([1, 2, 3]))

    cache = IndexCache(target_path)
    with caplog.at_level("WARNING"):
        cache.load()

    assert cache.cache == {}
    assert "not a JSON object" in caplog.text
