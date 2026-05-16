from pathlib import Path
from typing import Optional

import click
from consolekit import click_command

from .index import make_index


@click.argument(
    "origin",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--merge-with",
    "merge_with",
    type=click.STRING,
    default=None,
    help=(
        "URL of a remote PEP 503 index to merge with. Wheels present locally "
        "take precedence; remote-only wheels are linked via their absolute "
        "URL so 'pip' can fetch them directly. Useful when rsync'ing a "
        "partial wheel set to a host that already serves additional wheels."
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
    target_path = make_index(sanitize_path, merge_with=merge_with)
    print(f"Index generated at {target_path}")
