from pathlib import Path

from index_503.cache import IndexCache


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
