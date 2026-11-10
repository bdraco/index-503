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


def test_main_cli_parent_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test '..' resolves to the parent's real name instead of '..-index'."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    subdir = origin_path.joinpath("subdir")
    subdir.mkdir()
    monkeypatch.chdir(subdir)

    result = CliRunner().invoke(main_cli, [".."])

    assert result.exit_code == 0, result.output
    assert f"Index generated at {origin_path_index}" in result.output
    assert origin_path_index.joinpath("index.html").exists()
    assert not origin_path.joinpath("..-index").exists()
    assert not subdir.joinpath("..-index").exists()


def test_main_cli_symlink_keeps_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a symlinked origin is indexed under the symlink's own name."""
    origin_path, origin_path_index = setup_wheels(tmp_path, TEST_WHEELS)
    tmp_path.joinpath("alias").symlink_to(origin_path, target_is_directory=True)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["alias"])

    alias_index = tmp_path.joinpath("alias-index")
    assert result.exit_code == 0, result.output
    assert f"Index generated at {alias_index}" in result.output
    assert alias_index.joinpath("index.html").exists()
    assert not origin_path_index.exists()


def test_main_cli_root_rejected() -> None:
    """Test '/' is rejected with a usage error since its parent is itself."""
    result = CliRunner().invoke(main_cli, ["/"])

    assert result.exit_code == 2
    assert "Refusing to index filesystem root: /" in result.output


def test_main_cli_symlink_to_root_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a symlink to '/' is rejected like '/' itself."""
    tmp_path.joinpath("rootlink").symlink_to("/", target_is_directory=True)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["rootlink"])

    assert result.exit_code == 2
    assert "Refusing to index filesystem root: rootlink" in result.output
    assert not tmp_path.joinpath("rootlink-index").exists()


def test_main_cli_missing_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a missing directory is a usage error and creates nothing."""
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["missing"])

    assert result.exit_code == 2
    assert "'missing' does not exist" in result.output
    assert list(tmp_path.iterdir()) == []


def test_main_cli_file_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a regular file is rejected instead of indexed."""
    tmp_path.joinpath("some.whl").write_bytes(b"")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main_cli, ["some.whl"])

    assert result.exit_code == 2
    assert "is a file" in result.output
    assert not tmp_path.joinpath("some.whl-index").exists()
