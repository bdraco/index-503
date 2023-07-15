import logging
from pathlib import Path
from typing import Optional

from dist_meta import distributions

_LOGGER = logging.getLogger(__name__)


def extract_metadata_from_wheel_file(wheel_path: Path) -> Optional[str]:
    """Extract the METADATA file from a wheel file."""
    with distributions.WheelDistribution.from_path(wheel_path) as wd:
        if not wd.has_file("METADATA"):  # pragma: no cover
            _LOGGER.warning(f"METADATA file not found in {wheel_path}")
            return None
        return wd.read_file("METADATA")
