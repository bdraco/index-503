from pathlib import Path

import pytest
from click.testing import CliRunner

from index_503.main import main_cli

from .test_index import TEST_WHEELS, setup_wheels


def test_main_cli():
    assert main_cli is not None


def test_main_cli_relative_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a plain relative directory name generates the sibling index."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["musllinux"])

    assert result.exit_code == 0, result.output
    assert f"Index generated at {origin_path_index}" in result.output
    assert origin_path_index.joinpath("index.html").exists()


@pytest.mark.parametrize("origin", [".", "./"])
def test_main_cli_dot_resolves_to_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, origin: str
) -> None:
    """Test '.' from inside the wheel dir indexes it as a named directory.

    Path(".").name is empty, so without resolving to an absolute path the
    index would be written to a bogus "-index" directory.
    """
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    monkeypatch.chdir(origin_path)

    result = CliRunner().invoke(main_cli, [origin])

    assert result.exit_code == 0, result.output
    assert f"Index generated at {origin_path_index}" in result.output
    assert origin_path_index.joinpath("index.html").exists()
    assert not tmp_path.joinpath("-index").exists()
    assert not origin_path.joinpath("-index").exists()


def test_main_cli_root_rejected() -> None:
    """Test '/' is rejected since its parent is itself."""
    result = CliRunner().invoke(main_cli, ["/"])

    assert isinstance(result.exception, FileNotFoundError)
    assert "Directory / same as parent of /" in str(result.exception)


def test_main_cli_missing_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a missing directory reports both the input and resolved path."""
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["missing"])

    assert isinstance(result.exception, FileNotFoundError)
    assert str(result.exception) == (
        f"Directory missing does not exist as {tmp_path / 'missing'}"
    )
    assert list(tmp_path.iterdir()) == []
