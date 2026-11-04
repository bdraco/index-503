import logging
from pathlib import Path
from typing import Optional
from zipfile import BadZipFile

from dist_meta import distributions
from packaging.utils import InvalidWheelFilename

_LOGGER = logging.getLogger(__name__)


def extract_metadata_from_wheel_file(wheel_path: Path) -> Optional[str]:
    """Extract the METADATA file from a wheel file.

    Returns :py:obj:`None` if the file is not a valid wheel (corrupt zip,
    malformed filename, or missing ``METADATA``). The caller is expected to
    skip the file rather than abort the whole index build.
    """
    try:
        with distributions.WheelDistribution.from_path(wheel_path) as wd:
            if not wd.has_file("METADATA"):
                _LOGGER.warning("METADATA file not found in %s", wheel_path)
                return None
            return wd.read_file("METADATA")
    except (BadZipFile, InvalidWheelFilename) as exc:
        _LOGGER.warning("Skipping invalid wheel %s: %s", wheel_path, exc)
        return None
