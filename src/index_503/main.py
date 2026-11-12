from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

import click
from consolekit import click_command

from .index import make_index
from .remote_index import RemoteIndexError


def _validate_merge_with(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[str]:
    """Require an http(s) URL so a typo fails before any filesystem work."""
    if value is None:
        return None
    if urlsplit(value).scheme not in {"http", "https"}:
        raise click.BadParameter(f"expected an http(s) URL, got {value!r}")
    return value


@click.argument(
    "origin",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--merge-with",
    "merge_with",
    type=click.STRING,
    default=None,
    callback=_validate_merge_with,
    help=(
        "URL of a remote PEP 503 index to merge with. Wheels present locally "
        "take precedence; remote-only wheels are linked via their absolute "
        "URL so 'pip' can fetch them directly. Useful when rsync'ing a "
        "partial wheel set to a host that already serves additional wheels. "
        "The command fails if the remote index cannot be fetched."
    ),
)
@click_command()
def main_cli(origin: Path, merge_with: Optional[str] = None) -> None:
    # A trailing ".." has to be resolved to get a real directory name. Anything
    # else only goes through absolute() so a symlinked origin keeps its own
    # name and the index is written next to the symlink.
    sanitize_path = origin.resolve() if origin.name == ".." else origin.absolute()
    # Check the resolved path so a symlink to "/" is rejected too.
    resolved = origin.resolve()
    if resolved.parent == resolved:
        raise click.BadParameter(
            f"Refusing to index filesystem root: {origin}",
            param_hint="'ORIGIN'",
        )
    try:
        target_path = make_index(sanitize_path, merge_with=merge_with)
    except RemoteIndexError as exc:
        raise click.ClickException(str(exc)) from exc
    print(f"Index generated at {target_path}")
