import glob
import json
import logging
import os
import tempfile
from collections import defaultdict
from dataclasses import asdict
from operator import attrgetter
from pathlib import Path
from shutil import copyfile, rmtree
from typing import Any, Dict, List, Tuple

from dist_meta import distributions, metadata
from natsort import natsorted
from yarl import URL

from .file import write_utf8_file
from .page_generator import canonicalize_name, generate_index, generate_project_page
from .util import get_sha256_hash, load_json_file
from .wheel_file import WheelFile

_LOGGER = logging.getLogger(__name__)


def make_index(origin_path: Path) -> Tuple[Path, Dict[str, List["WheelFile"]]]:
    """Generate a simple repository of Python wheels.

    This function will take a directory of wheels at the top level
    of a webserver and generate a simple repository of wheels.

    :param origin: The name of the directory containing the wheels.

    Example
    musllinux

    This will generate
    musllinux-index
    """
    origin_name = origin_path.name
    target_path = origin_path.parent / (origin_path.name + "-index")
    old_index = target_path.readlink() if target_path.exists() else None
    target_path_parent = target_path.parent
    projects: Dict[str, List[WheelFile]] = defaultdict(list)
    cache_file = target_path.joinpath("cache.json")
    cache: Dict[str, Dict[str, Any]] = {}
    if cache_file.exists():
        cache = load_json_file(cache_file)

    with tempfile.TemporaryDirectory(
        dir=target_path_parent, ignore_cleanup_errors=True
    ) as temp_dir:
        temp_dir_path = Path(temp_dir)
        all_wheel_files: set[str] = set()

        for wheel_file in glob.glob(str(origin_path.joinpath("*.whl"))):
            wheel_path = Path(wheel_file)
            wheel_file_name = wheel_path.name
            all_wheel_files.add
            target_file = temp_dir_path.joinpath(wheel_file_name)
            metadata_filename = target_file.with_suffix(
                f"{target_file.suffix}.metadata"
            )

            if wheel_file_name in cache:
                wheel_file_obj = WheelFile(**cache[wheel_file_name])
                projects[wheel_file_obj.name].append(wheel_file_obj)
                previous_metadata_filename = target_path.joinpath(
                    metadata_filename.name
                )
                copyfile(previous_metadata_filename, metadata_filename)
                os.symlink(f"../{origin_name}/{wheel_path.name}", target_file)
                continue

            with distributions.WheelDistribution.from_path(wheel_path) as wd:
                if not wd.has_file("METADATA"):  # pragma: no cover
                    _LOGGER.warning(f"METADATA file not found in {wheel_path}")
                    continue
                metadata_string = wd.read_file("METADATA")
                wheel_metadata = metadata.loads(metadata_string)

            metadata_filename.write_text(metadata_string)
            project_name = wheel_metadata["Name"]
            wheel_file_obj = WheelFile(
                name=project_name,
                filename=target_file.relative_to(temp_dir_path).as_posix(),
                wheel_hash=get_sha256_hash(wheel_path),
                requires_python=wheel_metadata.get("Requires-Python"),
                metadata_hash=get_sha256_hash(metadata_filename),
            )
            projects[project_name].append(wheel_file_obj)
            cache[wheel_file_obj.filename] = asdict(wheel_file_obj)
            os.symlink(f"../{origin_name}/{wheel_path.name}", target_file)

        removed_wheels = set(cache.keys()) - all_wheel_files
        for old_wheel_file in removed_wheels:
            del cache[old_wheel_file]

        index_content = str(generate_index(projects.keys()))
        write_utf8_file(temp_dir_path.joinpath("index.html"), index_content)
        project_base_url = URL("../")

        for project_name, project_files in projects.items():
            project_dir = temp_dir_path.joinpath(canonicalize_name(project_name))
            project_dir.mkdir(exist_ok=True)
            project_index = generate_project_page(
                project_name,
                natsorted(project_files, key=attrgetter("filename"), reverse=True),
                project_base_url,
            )

            write_utf8_file(project_dir.joinpath("index.html"), str(project_index))

        final_name = target_path.parent / (target_path.name + "-" + temp_dir_path.name)
        final_build_name = final_name.parent / (final_name.name + "-build")

        # Rename the new index to the final name
        os.rename(temp_dir, final_name)

        write_utf8_file(final_name.joinpath("cache.json"), json.dumps(cache))

        # Create a temporary symlink to the final name
        os.symlink(final_name, final_build_name)

        # Finally replace the live index with the new one
        os.replace(final_build_name, target_path)

        if old_index:
            rmtree(old_index)

        return target_path, projects
