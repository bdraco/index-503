import fcntl
import json
import logging
import re
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Generator

_LOGGER = logging.getLogger(__name__)

_canonicalize_regex = re.compile(r"[-_.]+")


# PEP 427: The build number must start with a digit.
def canonicalize_name(name: str) -> str:
    """Canonicalize a name."""
    # This is taken from PEP 503.
    return _canonicalize_regex.sub("-", name).lower()


def get_sha256_hash(filename: Path) -> str:
    """Get SHA256 hash of a file."""
    with filename.open("rb") as f:
        bytes = f.read()  # read entire file as bytes
        return sha256(bytes).hexdigest()


def load_json_file(filename: Path) -> Dict[str, Dict[str, Any]]:
    """Get a json file."""
    with filename.open("rb") as f:
        bytes = f.read()  # read entire file as bytes
        return json.loads(bytes)


@contextmanager
def exclusive_lock(origin_path: Path) -> Generator[None, None, None]:
    parent = origin_path.parent
    lock_file = parent / (origin_path.name + ".index_503.lock")
    with lock_file.open("a") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
            return
        except OSError:
            # Another instance is running, wait for it to finish
            _LOGGER.warning("Another instance is running, waiting")
        fcntl.flock(fh, fcntl.LOCK_EX)
        _LOGGER.warning("Another instance finished, continuing")
        yield
