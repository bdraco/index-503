from pathlib import Path

import click
from consolekit import click_command

from .index import make_index


@click.argument("origin", type=click.STRING)
@click_command()
def main_cli(origin: str) -> None:
    origin_path = Path(origin)
    if not origin_path.exists():
        raise FileNotFoundError(f"Directory {origin_path} does not exist")
    target_path, projects = make_index(origin_path)
    print(f"Index generated at {target_path} with {len(projects)} projects.")
