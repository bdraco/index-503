import json
from pathlib import Path
from shutil import copyfile
from typing import Tuple
from unittest.mock import patch

import pytest

from index_503.index import make_index
from index_503.wheel_file import WHEEL_FILE_VERSION

from . import FIXTURES

TEST_WHEELS = (
    "bleak-0.17.0-py3-none-any.whl",
    "typing_extensions-4.2.0-py3-none-any.whl",
    "sphinxcontrib.applehelp-1.0.3-py3-none-any.whl",
    "CO2Signal-0.4.2-py3-none-any.whl",
)


def setup_wheels(tmp_path: Path) -> Tuple[Path, Path]:
    """Setup wheels for testing."""
    origin_path = tmp_path.joinpath("musllinux")
    origin_path.mkdir()

    for test_wheel in TEST_WHEELS:
        fixture_wheel_path = FIXTURES.joinpath(test_wheel)
        origin_wheel_path = origin_path.joinpath(test_wheel)
        copyfile(fixture_wheel_path, origin_wheel_path)

    origin_path_index = tmp_path.joinpath("musllinux-index")

    return origin_path, origin_path_index


def test_make_index_fails(tmp_path: Path) -> None:
    """Test make index cleans up on failure."""
    origin_path, _ = setup_wheels(tmp_path)
    parent_dir = origin_path.parent

    with pytest.raises(ValueError), patch(
        "index_503.index.IndexMaker._atomic_replace_old_index", side_effect=ValueError
    ):
        make_index(origin_path)

    parent_dir_contents = {path.name for path in parent_dir.iterdir()}
    assert len(parent_dir_contents) == 2
    # The lock file should always exist
    assert parent_dir_contents == {"musllinux", ".musllinux.index_503.lock"}


def test_make_index_end_to_end(tmp_path: Path) -> None:
    """Test make_index() end to end."""
    origin_path, origin_path_index = setup_wheels(tmp_path)

    for _ in range(2):
        assert make_index(origin_path) == origin_path_index

        json_cache_path = origin_path_index.joinpath("cache.json")
        assert json_cache_path.exists()
        assert origin_path_index.joinpath(
            "CO2Signal-0.4.2-py3-none-any.whl.metadata"
        ).exists()
        project_index_path: Path = origin_path_index.joinpath("index.html")
        assert project_index_path.exists()
        assert project_index_path.stat().st_mode & 0o0777 == 0o644
        parent_path: Path = project_index_path.parent
        assert parent_path.stat().st_mode & 0o0777 == 0o755
        project_index_html = project_index_path.read_text()
        assert "CO2Signal" in project_index_html
        assert "/co2signal/" in project_index_html
        co2_signal_path: Path = origin_path_index.joinpath("co2signal")
        assert co2_signal_path.stat().st_mode & 0o0777 == 0o755
        assert co2_signal_path.exists()
        co2signal_index_path: Path = origin_path_index.joinpath(
            "co2signal", "index.html"
        )
        assert co2signal_index_path.exists()
        assert co2signal_index_path.stat().st_mode & 0o0777 == 0o644
        print(json_cache_path.read_text())
        assert json.loads(json_cache_path.read_text()) == {
            "CO2Signal-0.4.2-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "co2signal",
                "filename": "CO2Signal-0.4.2-py3-none-any.whl",
                "metadata_name": "CO2Signal",
                "wheel_hash": "23976d5df4ac7b4b85210e4f334382d65b759a2c3795121f9688e64365ef4790",
                "requires_python": None,
                "metadata_hash": "a6e73c9cf4f9469c5b308830afbc000bb806df5d894598dd499737e94974c27c",
            },
            "typing_extensions-4.2.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "typing-extensions",
                "filename": "typing_extensions-4.2.0-py3-none-any.whl",
                "metadata_name": "typing_extensions",
                "wheel_hash": "6657594ee297170d19f67d55c05852a874e7eb634f4f753dbd667855e07c1708",
                "requires_python": ">=3.7",
                "metadata_hash": "dfeedfcc1c0d79841471fb3b186d85747256e14d425b50af2514fe2cf0c2ded9",
            },
            "bleak-0.17.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "bleak",
                "filename": "bleak-0.17.0-py3-none-any.whl",
                "metadata_name": "bleak",
                "wheel_hash": "be243ced0132b02d43738411d7e5f210fb536905a867d26c339085b4f976ddb2",
                "requires_python": ">=3.7,<4.0",
                "metadata_hash": "b826a4a16ef36e8a2165b16cec9b46d2956930a66046e977a499a418388e33d1",
            },
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

        bleak_metadata_path = origin_path_index.joinpath(
            "bleak-0.17.0-py3-none-any.whl.metadata"
        )
        assert bleak_metadata_path.exists()
        bleak_metadata = bleak_metadata_path.read_text()
        assert "Requires-Dist: typing-extensions" in bleak_metadata
