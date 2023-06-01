import logging
from pathlib import Path
from typing import Dict, Optional

from dist_meta import distributions

from .util import canonicalize_name

_LOGGER = logging.getLogger(__name__)


def repair_metadata_file(
    metadata_file: Path, canonical_name_to_metadata_name: Dict[str, str]
) -> bool:
    """Repair the metadata file."""
    metadata_file_content = metadata_file.read_text().splitlines()
    # We have to parse the metadata file manually because the dist_meta library
    # doesn't support every version of the METADATA file.
    modified = False

    for index, line in enumerate(metadata_file_content):
        if line.startswith("Requires-Dist: "):
            items = line.split(" ")
            original_name = items[1]
            canonical_name = canonicalize_name(original_name)
            metadata_name = canonical_name_to_metadata_name.get(canonical_name)
            if metadata_name and metadata_name != original_name:
                _LOGGER.warning(
                    "Repairing %s Requires-Dist %s -> %s",
                    metadata_file,
                    original_name,
                    metadata_name,
                )
                items[1] = metadata_name
                metadata_file_content[index] = " ".join(items)
                modified = True
        if line == "":
            break

    if modified:
        metadata_file.write_text("\n".join(metadata_file_content))

    return modified


def extract_metadata_from_wheel_file(wheel_path: Path) -> Optional[str]:
    """Extract the METADATA file from a wheel file."""
    with distributions.WheelDistribution.from_path(wheel_path) as wd:
        if not wd.has_file("METADATA"):  # pragma: no cover
            _LOGGER.warning(f"METADATA file not found in {wheel_path}")
            return None
        return wd.read_file("METADATA")
