from pathlib import Path

import click
from consolekit import click_command

from .index import make_index


@click.argument(
    "origin",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click_command()
def main_cli(origin: Path) -> None:
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
    target_path = make_index(sanitize_path)
    print(f"Index generated at {target_path}")
