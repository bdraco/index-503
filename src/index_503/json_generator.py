"""PEP 691 JSON-based Simple Repository API generation.

Writes ``index.v1_json`` files alongside the legacy PEP 503 ``index.html``
files. Web servers can use content negotiation (matching the ``Accept``
header ``application/vnd.pypi.simple.v1+json``) to serve the JSON variant
to pip 22.0+ clients.
"""

from collections.abc import Iterable
from typing import Any, Union

from natsort import natsorted
from yarl import URL

from .util import canonicalize_name
from .wheel_file import HASH_FORMAT, WheelFile

# PEP 691 baseline; ``size`` is a forward-compatible field that
# clients ignore when unsupported.
API_VERSION = "1.0"

JSON_INDEX_FILENAME = "index.v1_json"


def generate_index_json(projects: Iterable[str]) -> dict[str, Any]:
    """Generate the top-level PEP 691 project index payload."""
    return {
        "meta": {"api-version": API_VERSION},
        "projects": [
            {"name": canonicalize_name(p)}
            for p in natsorted(projects, key=str.lower)
        ],
    }


def generate_project_page_json(
    name: str,
    files: Iterable[WheelFile],
    base_url: Union[str, URL] = "/",
) -> dict[str, Any]:
    """Generate the per-project PEP 691 page payload."""
    base = URL(base_url)
    return {
        "meta": {"api-version": API_VERSION},
        "name": canonicalize_name(name),
        "files": [_file_entry(f, base) for f in files],
    }


def _file_entry(wheel: WheelFile, base_url: URL) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "filename": wheel.filename,
        "url": str(base_url / wheel.filename),
        "hashes": {HASH_FORMAT: wheel.wheel_hash},
    }
    if wheel.requires_python is not None:
        entry["requires-python"] = wheel.requires_python
    if wheel.metadata_hash is not None:
        if wheel.metadata_hash is True:
            entry["core-metadata"] = True
        else:
            entry["core-metadata"] = {HASH_FORMAT: wheel.metadata_hash}
    if wheel.size is not None:
        entry["size"] = wheel.size
    return entry
