import json
from pathlib import Path
from shutil import copyfile
from unittest.mock import ANY, patch

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

TEST_WHEELS_NAME_CHANGE = (
    "alexapy-1.26.8-py3-none-any.whl",
    "alexapy-1.26.9-py3-none-any.whl",
    "alexapy-1.27.0-py3-none-any.whl",
)


def install_wheels(origin_path: Path, files: tuple[str, ...]) -> None:
    """Install wheels for testing."""
    for test_wheel in files:
        fixture_wheel_path = FIXTURES.joinpath(test_wheel)
        origin_wheel_path = origin_path.joinpath(test_wheel)
        copyfile(fixture_wheel_path, origin_wheel_path)


def setup_wheels(tmp_path: Path, files: tuple[str, ...]) -> tuple[Path, Path]:
    """Setup wheels for testing."""
    origin_path = tmp_path.joinpath("musllinux")
    origin_path.mkdir()

    install_wheels(origin_path, files)

    origin_path_index = tmp_path.joinpath("musllinux-index")

    return origin_path, origin_path_index


def test_make_index_fails(tmp_path: Path) -> None:
    """Test make index cleans up on failure."""
    origin_path, _ = setup_wheels(tmp_path, TEST_WHEELS)
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
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)

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
        assert "co2signal" in project_index_html
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
                "mtime": ANY,
                "size": 2841,
            },
            "typing_extensions-4.2.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "typing-extensions",
                "filename": "typing_extensions-4.2.0-py3-none-any.whl",
                "metadata_name": "typing_extensions",
                "wheel_hash": "6657594ee297170d19f67d55c05852a874e7eb634f4f753dbd667855e07c1708",
                "requires_python": ">=3.7",
                "metadata_hash": "dfeedfcc1c0d79841471fb3b186d85747256e14d425b50af2514fe2cf0c2ded9",
                "mtime": ANY,
                "size": 24207,
            },
            "bleak-0.17.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "bleak",
                "filename": "bleak-0.17.0-py3-none-any.whl",
                "metadata_name": "bleak",
                "wheel_hash": "be243ced0132b02d43738411d7e5f210fb536905a867d26c339085b4f976ddb2",
                "requires_python": ">=3.7,<4.0",
                "metadata_hash": "b826a4a16ef36e8a2165b16cec9b46d2956930a66046e977a499a418388e33d1",
                "mtime": ANY,
                "size": 126632,
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

        # Now replace "CO2Signal-0.4.2-py3-none-any.whl" with a different wheel
        fixture_wheel_path = FIXTURES.joinpath(
            "replace_wheel", "CO2Signal-0.4.2-py3-none-any.whl"
        )
        origin_wheel_path = origin_path.joinpath("CO2Signal-0.4.2-py3-none-any.whl")
        copyfile(fixture_wheel_path, origin_wheel_path)
        assert make_index(origin_path) == origin_path_index
        print(json_cache_path.read_text())
        # The replacement CO2Signal-0.4.2-py3-none-any.whl wheel should have a different hash
        # and mtime, but the metadata hash should be the same
        assert json.loads(json_cache_path.read_text()) == {
            "CO2Signal-0.4.2-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "co2signal",
                "filename": "CO2Signal-0.4.2-py3-none-any.whl",
                "metadata_name": "CO2Signal",
                "wheel_hash": "1efad0734066e28058e8a41d480284fad398d36c94f32fb456feca8d219e4fcf",
                "requires_python": None,
                "metadata_hash": "a6e73c9cf4f9469c5b308830afbc000bb806df5d894598dd499737e94974c27c",
                "mtime": ANY,
                "size": 3673,
            },
            "typing_extensions-4.2.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "typing-extensions",
                "filename": "typing_extensions-4.2.0-py3-none-any.whl",
                "metadata_name": "typing_extensions",
                "wheel_hash": "6657594ee297170d19f67d55c05852a874e7eb634f4f753dbd667855e07c1708",
                "requires_python": ">=3.7",
                "metadata_hash": "dfeedfcc1c0d79841471fb3b186d85747256e14d425b50af2514fe2cf0c2ded9",
                "mtime": ANY,
                "size": 24207,
            },
            "bleak-0.17.0-py3-none-any.whl": {
                "version": WHEEL_FILE_VERSION,
                "canonical_name": "bleak",
                "filename": "bleak-0.17.0-py3-none-any.whl",
                "metadata_name": "bleak",
                "wheel_hash": "be243ced0132b02d43738411d7e5f210fb536905a867d26c339085b4f976ddb2",
                "requires_python": ">=3.7,<4.0",
                "metadata_hash": "b826a4a16ef36e8a2165b16cec9b46d2956930a66046e977a499a418388e33d1",
                "mtime": ANY,
                "size": 126632,
            },
        }
        # Now put back the original wheels
        # to make sure the next run will regenerate the index
        # and hashes along with size
        install_wheels(origin_path, TEST_WHEELS)


def test_make_index_with_name_change(tmp_path: Path) -> None:
    """Test make_index() end to end with a name change in the wheel."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS_NAME_CHANGE)

    for _ in range(2):
        assert make_index(origin_path) == origin_path_index

        json_cache_path = origin_path_index.joinpath("cache.json")
        assert json_cache_path.exists()
        assert origin_path_index.joinpath(
            "alexapy-1.26.8-py3-none-any.whl.metadata"
        ).exists()
        assert origin_path_index.joinpath(
            "alexapy-1.26.9-py3-none-any.whl.metadata"
        ).exists()
        assert origin_path_index.joinpath(
            "alexapy-1.27.0-py3-none-any.whl.metadata"
        ).exists()
        project_index_path: Path = origin_path_index.joinpath("index.html")
        assert project_index_path.exists()
        assert project_index_path.stat().st_mode & 0o0777 == 0o644
        parent_path: Path = project_index_path.parent
        assert parent_path.stat().st_mode & 0o0777 == 0o755
        project_index_html = project_index_path.read_text()
        assert "alexapy" in project_index_html
        assert "/alexapy/" in project_index_html
        alexapy_path: Path = origin_path_index.joinpath("alexapy")
        assert alexapy_path.stat().st_mode & 0o0777 == 0o755
        assert alexapy_path.exists()
        alexapy_index_path: Path = origin_path_index.joinpath("alexapy", "index.html")
        assert alexapy_index_path.exists()
        assert alexapy_index_path.stat().st_mode & 0o0777 == 0o644
        print(json_cache_path.read_text())
        assert json.loads(json_cache_path.read_text()) == {
            "alexapy-1.26.9-py3-none-any.whl": {
                "version": 10,
                "canonical_name": "alexapy",
                "filename": "alexapy-1.26.9-py3-none-any.whl",
                "metadata_name": "alexapy",
                "wheel_hash": "dd4eed7a53f4932156ba779c73c5bd64286ee4d0f714028401e8f9acd9cd6afd",
                "requires_python": ">=3.10,<4",
                "metadata_hash": "dc54cefafe6853e984d9651f0f69c61eb1c292cb94677a3766b605692fb5c126",
                "mtime": ANY,
                "size": 45566,
            },
            "alexapy-1.27.0-py3-none-any.whl": {
                "version": 10,
                "canonical_name": "alexapy",
                "filename": "alexapy-1.27.0-py3-none-any.whl",
                "metadata_name": "AlexaPy",
                "wheel_hash": "a6dc55daac51d0f8f423b85cec346fd012b2f58a5b05493524a93156585c5110",
                "requires_python": ">=3.11,<4",
                "metadata_hash": "6c989ef90d200a9105d6e2dcd9c32c1caa84022061f6d0160a2d9fb7d442a816",
                "mtime": ANY,
                "size": 49851,
            },
            "alexapy-1.26.8-py3-none-any.whl": {
                "version": 10,
                "canonical_name": "alexapy",
                "filename": "alexapy-1.26.8-py3-none-any.whl",
                "metadata_name": "alexapy",
                "wheel_hash": "f17ac40d033ca869706f899fe0ab518c3c44459c951c7141d3be0117158c0fe2",
                "requires_python": ">=3.10,<4",
                "metadata_hash": "8ea579b5b6ebc80657f3bc3d5046af91a208f342b4dae19966d52eafacf82fec",
                "mtime": ANY,
                "size": 45560,
            },
        }
        alexapy_index_html = alexapy_index_path.read_text()
        assert (
            "alexapy-1.26.8-py3-none-any.whl#sha256=f17ac40d033ca869706f899fe0ab518c3c44459c951c7141d3be0117158c0fe2"
            in alexapy_index_html
        )
        assert (
            "alexapy-1.26.9-py3-none-any.whl#sha256=dd4eed7a53f4932156ba779c73c5bd64286ee4d0f714028401e8f9acd9cd6afd"
            in alexapy_index_html
        )
        assert (
            "alexapy-1.27.0-py3-none-any.whl#sha256=a6dc55daac51d0f8f423b85cec346fd012b2f58a5b05493524a93156585c5110"
            in alexapy_index_html
        )
