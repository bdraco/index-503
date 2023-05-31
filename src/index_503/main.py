import glob
import logging
from collections import defaultdict
from hashlib import _Hash, sha256
from operator import attrgetter
from pathlib import Path
from typing import Dict, List

from dist_meta import distributions, metadata

# 3rd party
from natsort import natsorted

from .file import write_utf8_file
from .page_generator import canonicalize_name, generate_index, generate_project_page
from .wheel_file import WheelFile

_LOGGER = logging.getLogger(__name__)


def main_cli() -> None:
    make_index("wheels", "wheels-index", "/wheels/")


def get_sha256_hash(filename: Path) -> _Hash:
    """Get SHA256 hash of a file."""
    with filename.open("rb") as f:
        bytes = f.read()  # read entire file as bytes
        return sha256(bytes)


def make_index(origin: str, target: str, base_url: str) -> Dict[str, List["WheelFile"]]:
    """
    Generate a simple repository of Python wheels.

    :param origin: A directory containing wheels. The wheels may be arranged in subdirectories.
    :param target: The directory to create the repository in.
        The directory structure of ``origin`` will be recreated there.
        Defaults to ``origin``.
    :no-default target:
    :param base_url: The base URL of the simple repository.
    :param sort: Sort the wheel files into per-project base directories.
    :param copy: Copy files from the source to the destination, rather than moving them.

    :returns: A mapping of (unnormalized) project names to a list of wheels for that project.

    .. versionchanged:: 0.2.0

        Now ignores wheels in the following directories: ``.git``, ``.hg``, ``.tox``, ``.tox4``,
        ``.nox``, ``venv``, ``.venv``.

    .. versionchanged:: 0.3.0

        * Renamed the ``move`` option to ``sort`` to better reflect its behaviour.
        * Files are moved to the destination by default, unless the ``copy`` option is :py:obj:`True`.
    """

    Path(origin)
    target_path = Path(target)
    projects: Dict[str, List[WheelFile]] = defaultdict(list)

    for wheel_file in glob.glob(f"{origin}/*.whl"):
        wheel_path = Path(wheel_file)
        target_file = target_path.joinpath(wheel_file)

        with distributions.WheelDistribution.from_path(wheel_path) as wd:
            if not wd.has_file("METADATA"):  # pragma: no cover
                _LOGGER.warning(f"METADATA file not found in {wheel_path}")
                continue
            metadata_string = wd.read_file("METADATA")
            wheel_metadata = metadata.loads(metadata_string)

        metadata_filename = target_file.with_suffix(f"{target_file.suffix}.metadata")
        metadata_filename.write_text(metadata_string)

        projects[wheel_metadata["Name"]].append(
            WheelFile(
                filename=target_file.relative_to(target).as_posix(),
                wheel_hash=get_sha256_hash(target_file),
                requires_python=wheel_metadata.get("Requires-Python"),
                metadata_hash=get_sha256_hash(metadata_filename),
            )
        )

    index_content = str(generate_index(projects.keys(), base_url=base_url))
    write_utf8_file(str(target_path.joinpath("index.html")), index_content)

    for project_name, project_files in projects.items():
        project_dir = target_path.joinpath(canonicalize_name(project_name))
        project_index = generate_project_page(
            project_name,
            natsorted(project_files, key=attrgetter("filename"), reverse=True),
            base_url,
        )

        write_utf8_file(str(project_dir.joinpath("index.html")), str(project_index))

    return projects
