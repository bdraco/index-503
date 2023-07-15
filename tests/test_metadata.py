from index_503.metadata import extract_metadata_from_wheel_file

from . import FIXTURES


def test_extract_metadata_missing():
    wheel_path = FIXTURES.joinpath("sphinxcontrib.applehelp-1.0.3-py3-none-any.whl")
    extract_metadata_from_wheel_file(wheel_path) is None


def test_extract_metadata():
    wheel_path = FIXTURES.joinpath("CO2Signal-0.4.2-py3-none-any.whl")
    extract_metadata_from_wheel_file(wheel_path) is not None
