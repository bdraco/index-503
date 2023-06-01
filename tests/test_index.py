import json
from pathlib import Path
from shutil import copyfile

from index_503.index import make_index
from index_503.wheel_file import WHEEL_FILE_VERSION

from . import FIXTURES

TEST_WHEELS = (
    "sphinxcontrib.applehelp-1.0.3-py3-none-any.whl",
    "CO2Signal-0.4.2-py3-none-any.whl",
)


def test_make_index_end_to_end(tmp_path: Path) -> None:
    """Test make_index() end to end."""
    origin_path = tmp_path.joinpath("musllinux")
    origin_path.mkdir()
    origin_path_index = tmp_path.joinpath("musllinux-index")

    for test_wheel in TEST_WHEELS:
        fixture_wheel_path = FIXTURES.joinpath(test_wheel)
        origin_wheel_path = origin_path.joinpath(test_wheel)
        copyfile(fixture_wheel_path, origin_wheel_path)

    for _ in range(2):
        assert make_index(origin_path) == origin_path_index

        json_cache_path = origin_path_index.joinpath("cache.json")
        assert json_cache_path.exists()
        assert origin_path_index.joinpath(
            "CO2Signal-0.4.2-py3-none-any.whl.metadata"
        ).exists()
        project_index_path = origin_path_index.joinpath("index.html")
        assert project_index_path.exists()
        project_index_html = project_index_path.read_text()
        assert "CO2Signal" in project_index_html
        assert "/co2signal/" in project_index_html
        assert origin_path_index.joinpath("CO2Signal").exists()
        co2signal_index_path = origin_path_index.joinpath("CO2Signal", "index.html")
        assert co2signal_index_path.exists()
        assert json.loads(json_cache_path.read_text()) == {
            "CO2Signal-0.4.2-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "co2signal",
                "filename": "CO2Signal-0.4.2-py3-none-any.whl",
                "metadata_name": "CO2Signal",
                "wheel_hash": "23976d5df4ac7b4b85210e4f334382d65b759a2c3795121f9688e64365ef4790",
                "requires_python": None,
                "metadata_hash": "a6e73c9cf4f9469c5b308830afbc000bb806df5d894598dd499737e94974c27c",
            }
        }

        co2signal_index_html = co2signal_index_path.read_text()
        assert (
            "CO2Signal-0.4.2-py3-none-any.whl#sha256=23976d5df4ac7b4b85210e4f334382d65b759a2c3795121f9688e64365ef4790"
            in co2signal_index_html
        )
        assert (
            'data-dist-info-metadata="sha256=a6e73c9cf4f9469c5b308830afbc000bb806df5d894598dd499737e94974c27c"'
            in co2signal_index_html
        )
