import json
import logging
from pathlib import Path
from typing import Any, Dict, Set

from .file import write_utf8_file
from .util import load_json_file

_LOGGER = logging.getLogger(__name__)

CACHE_FILE = "cache.json"


class IndexCache:
    def __init__(self, target_path: Path) -> None:
        """Cache of WheelFiles between runs."""
        cache_file = target_path.joinpath(CACHE_FILE)
        self.cache_file = cache_file
        self.cache: Dict[str, Dict[str, Any]] = {}

    def load(self) -> None:
        """Load the cache from a file."""
        if self.cache_file.exists():
            self.cache = load_json_file(self.cache_file)

    def write_to_new(self, target: Path) -> None:
        """Write the cache to a new file."""
        new_cache_file = target.joinpath(CACHE_FILE)
        write_utf8_file(new_cache_file, json.dumps(self.cache))

    def remove_stale_keys(self, all_wheel_files: Set[str]) -> None:
        """Remove any wheel file names that no longer exist."""
        removed_wheels = set(self.cache.keys()) - all_wheel_files
        for old_wheel_file in removed_wheels:
            del self.cache[old_wheel_file]
