from pathlib import Path
from shutil import copyfile

from index_503.metadata import repair_metadata_file

FIXTURES = Path(__file__).parent.joinpath("fixtures")


def test_repair_metadata_file(tmp_path: Path) -> None:
    metadata_path = FIXTURES.joinpath("METADATA")
    original_metadata = metadata_path.read_text()
    temp_metadata_path = tmp_path.joinpath("METADATA")
    copyfile(metadata_path, temp_metadata_path)
    assert "Requires-Dist: IntelHex" in original_metadata
    assert repair_metadata_file(temp_metadata_path, {"intelhex": "intelhex"}) is True
    repaired_metadata = temp_metadata_path.read_text()
    assert "Requires-Dist: intelhex" in repaired_metadata
    assert original_metadata != repaired_metadata
    assert repair_metadata_file(temp_metadata_path, {"intelhex": "intelhex"}) is False
