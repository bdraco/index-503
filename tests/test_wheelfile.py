from pathlib import Path
from unittest.mock import ANY

from index_503.util import get_mtime_and_size_from_path
from index_503.wheel_file import WHEEL_FILE_VERSION, WheelFile

from . import FIXTURES


def test_wheel_file(tmp_path: Path) -> None:
    """Test WheelFile.from_wheel() and WheelFile.as_dict()"""
    metadata_path = tmp_path.joinpath("metadata")
    wheel_path = FIXTURES.joinpath("CO2Signal-0.4.2-py3-none-any.whl")
    wheel_file_obj = WheelFile.from_wheel(wheel_path, metadata_path)
    assert wheel_file_obj is not None
    assert wheel_file_obj.as_dict() == {
        "version": WHEEL_FILE_VERSION,
        "canonical_name": "co2signal",
        "filename": "CO2Signal-0.4.2-py3-none-any.whl",
        "metadata_name": "CO2Signal",
        "wheel_hash": "23976d5df4ac7b4b85210e4f334382d65b759a2c3795121f9688e64365ef4790",
        "requires_python": None,
        "size": 2841,
        "mtime": ANY,
        "metadata_hash": "a6e73c9cf4f9469c5b308830afbc000bb806df5d894598dd499737e94974c27c",
    }
    to_cache = wheel_file_obj.as_dict()
    mtime, size = get_mtime_and_size_from_path(wheel_path)
    assert WheelFile.from_cache(to_cache, mtime, size) == wheel_file_obj

    # Wrong mtime should not use the cache
    assert WheelFile.from_cache(to_cache, 42, size) is None

    to_cache["version"] = 0
    assert WheelFile.from_cache(to_cache, mtime, size) is None


def test_wheel_file_with_missing_metadata(tmp_path: Path) -> None:
    """Test WheelFile.from_wheel() with missing metadata"""
    metadata_path = tmp_path.joinpath("metadata")
    wheel_path = FIXTURES.joinpath("sphinxcontrib.applehelp-1.0.3-py3-none-any.whl")
    wheel_file_obj = WheelFile.from_wheel(wheel_path, metadata_path)
    assert wheel_file_obj is None
