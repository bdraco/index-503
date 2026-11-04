from pathlib import Path

import click
from consolekit import click_command

from .index import make_index


@click.argument("origin", type=click.STRING)
@click_command()
def main_cli(origin: str) -> None:
    origin_path = Path(origin)
    sanitize_path = (
        origin_path.resolve() if origin_path.name == ".." else origin_path.absolute()
    )
    if not origin_path.exists():
        raise FileNotFoundError(f"Directory {origin} does not exist as {sanitize_path}")
    if origin_path.resolve().parent == origin_path.resolve():
        raise FileNotFoundError(f"Directory {origin} same as parent of {sanitize_path}")
    target_path = make_index(sanitize_path)
    print(f"Index generated at {target_path}")
