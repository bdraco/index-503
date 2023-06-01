from pathlib import Path

import pytest

from index_503.file import write_utf8_file


def test_write_utf8_file(tmp_path: Path) -> None:
    write_utf8_file(tmp_path.joinpath("foo.txt"), "foo")
    assert tmp_path.joinpath("foo.txt").read_text() == "foo"

    with pytest.raises(OSError):
        write_utf8_file(Path("/not-writable"), "bar")
