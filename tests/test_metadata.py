from pathlib import Path

from index_503.metadata import extract_metadata_from_wheel_file

from . import FIXTURES


def test_extract_metadata_missing():
    wheel_path = FIXTURES.joinpath("sphinxcontrib.applehelp-1.0.3-py3-none-any.whl")
    extract_metadata_from_wheel_file(wheel_path) is None


def test_extract_metadata():
    wheel_path = FIXTURES.joinpath("CO2Signal-0.4.2-py3-none-any.whl")
    extract_metadata_from_wheel_file(wheel_path) is not None


def test_extract_metadata_corrupt_zip(tmp_path: Path) -> None:
    """A wheel with a well-formed name but corrupt zip body returns None."""
    bad_wheel = tmp_path.joinpath("brokenpkg-1.0-py3-none-any.whl")
    bad_wheel.write_bytes(b"not a zip file")
    assert extract_metadata_from_wheel_file(bad_wheel) is None


def test_extract_metadata_invalid_filename(tmp_path: Path) -> None:
    """A file with a non-PEP-427 wheel name returns None."""
    bad_wheel = tmp_path.joinpath("not-a-real-wheel.whl")
    bad_wheel.write_bytes(b"not a zip file either")
    assert extract_metadata_from_wheel_file(bad_wheel) is None
