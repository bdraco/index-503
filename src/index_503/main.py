from pathlib import Path
from typing import Optional

import click
from consolekit import click_command

from .index import make_index


@click.argument("origin", type=click.STRING)
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
def main_cli(origin: str, merge_with: Optional[str] = None) -> None:
    origin_path = Path(origin)
    if not origin_path.exists():
        raise FileNotFoundError(f"Directory {origin_path} does not exist")
    target_path = make_index(origin_path, merge_with=merge_with)
    print(f"Index generated at {target_path}")
