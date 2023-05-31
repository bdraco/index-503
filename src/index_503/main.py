import logging
from pathlib import Path

import click
from consolekit import click_command

from .index import make_index

_LOGGER = logging.getLogger(__name__)


@click.argument("origin", type=click.STRING)
@click_command()
def main_cli(origin: str) -> None:
    origin_path = Path(origin)
    if not origin_path.exists():
        raise FileNotFoundError(f"Directory {origin_path} does not exist")
    make_index(origin_path)
