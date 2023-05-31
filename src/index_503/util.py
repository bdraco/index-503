import json
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict


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
