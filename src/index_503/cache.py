import json
import logging
from pathlib import Path
from typing import Any

from .file import write_utf8_file
from .util import load_json_file

_LOGGER = logging.getLogger(__name__)

CACHE_FILE = "cache.json"


class IndexCache:
    def __init__(self, target_path: Path) -> None:
        """Cache of WheelFiles between runs."""
        cache_file = target_path.joinpath(CACHE_FILE)
        self.cache_file = cache_file
        self.cache: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        """Load the cache from a file.

        A corrupt or unreadable cache is treated as empty — the next run
        will rebuild it by re-hashing every wheel. This is slower, but
        avoids aborting the whole index build because of a stale or
        truncated cache file.
        """
        if not self.cache_file.exists():
            return
        try:
            loaded = load_json_file(self.cache_file)
        except (OSError, ValueError) as err:
            _LOGGER.warning(
                "Cache %s is unreadable (%s); rebuilding from scratch",
                self.cache_file,
                err,
            )
            return
        if not isinstance(loaded, dict):
            _LOGGER.warning(
                "Cache %s is not a JSON object; rebuilding from scratch",
                self.cache_file,
            )
            return
        self.cache = loaded

    def write_to_new(self, target: Path) -> None:
        """Write the cache to a new file.

        Sorted keys + compact separators keep the on-disk file small and
        produce a stable byte representation, so diffs between two runs
        reflect real changes rather than dict ordering.
        """
        new_cache_file = target.joinpath(CACHE_FILE)
        write_utf8_file(
            new_cache_file,
            json.dumps(self.cache, sort_keys=True, separators=(",", ":")),
        )

    def remove_stale_keys(self, all_wheel_files: set[str]) -> None:
        """Remove any wheel file names that no longer exist."""
        removed_wheels = set(self.cache.keys()) - all_wheel_files
        for old_wheel_file in removed_wheels:
            del self.cache[old_wheel_file]
