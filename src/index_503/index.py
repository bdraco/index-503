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
from .wheel_file import WHEEL_FILE_VERSION, WheelFile

_LOGGER = logging.getLogger(__name__)

CACHE_FILE = "cache.json"


def repair_metadata_file(
    metadata_file: Path, canonical_name_to_metadata_name: Dict[str, str]
) -> None:
    """Repair the metadata file."""
    metadata_file_content = metadata_file.read_text().splitlines()
    # We have to parse the metadata file manually because the dist_meta library
    # doesn't support every version of the METADATA file.
    modified = False
    for index, line in enumerate(metadata_file_content):
        if line.startswith("Requires-Dist: "):
            items = line.split(" ")
            canonical_name = items[1]
            metadata_name = canonical_name_to_metadata_name.get(canonical_name)
            if metadata_name and metadata_name != canonical_name:
                _LOGGER.warning(
                    f"Repairing {metadata_file} Requires-Dist {canonical_name} -> {metadata_name}"
                )
                items[1] = metadata_name
                metadata_file_content[index] = " ".join(items)
                modified = True
        if line == "":
            break
    if modified:
        metadata_file.write_text("\n".join(metadata_file_content))


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
    cache_file = target_path.joinpath(CACHE_FILE)
    cache: Dict[str, Dict[str, Any]] = {}
    if cache_file.exists():
        cache = load_json_file(cache_file)

    with tempfile.TemporaryDirectory(
        dir=str(target_path_parent), ignore_cleanup_errors=True
    ) as temp_dir:
        temp_dir_path = Path(temp_dir)
        all_wheel_files: set[str] = set()
        canonical_name_to_metadata_name: Dict[str, str] = {}
        metadata_files_to_repair: List[Path] = []

        for wheel_file in glob.glob(str(origin_path.joinpath("*.whl"))):
            wheel_path = Path(wheel_file)
            wheel_file_name = wheel_path.name
            all_wheel_files.add(wheel_file_name)
            target_file = temp_dir_path.joinpath(wheel_file_name)
            metadata_filename = target_file.with_suffix(
                f"{target_file.suffix}.metadata"
            )
            wheel_file_symlink_target = f"../{origin_name}/{wheel_path.name}"
            wheel_cache = cache.get(wheel_file_name)

            if wheel_cache and wheel_cache["version"] == WHEEL_FILE_VERSION:
                wheel_file_obj = WheelFile(**wheel_cache)
                projects[wheel_file_obj.metadata_name].append(wheel_file_obj)
                previous_metadata_filename = target_path.joinpath(
                    metadata_filename.name
                )
                copyfile(previous_metadata_filename, metadata_filename)
                os.symlink(wheel_file_symlink_target, target_file)
                continue

            with distributions.WheelDistribution.from_path(wheel_path) as wd:
                if not wd.has_file("METADATA"):  # pragma: no cover
                    _LOGGER.warning(f"METADATA file not found in {wheel_path}")
                    continue
                metadata_string = wd.read_file("METADATA")
                wheel_metadata = metadata.loads(metadata_string)

            metadata_filename.write_text(metadata_string)
            metadata_files_to_repair.append(metadata_filename)
            metadata_name = wheel_metadata["Name"]
            canonical_name = canonicalize_name(metadata_name)
            wheel_file_obj = WheelFile(
                version=WHEEL_FILE_VERSION,
                metadata_name=metadata_name,
                canonical_name=canonical_name,
                filename=target_file.relative_to(temp_dir_path).as_posix(),
                wheel_hash=get_sha256_hash(wheel_path),
                requires_python=wheel_metadata.get("Requires-Python"),
                metadata_hash=get_sha256_hash(metadata_filename),
            )
            canonical_name_to_metadata_name[canonical_name] = metadata_name
            projects[metadata_name].append(wheel_file_obj)
            cache[wheel_file_name] = asdict(wheel_file_obj)
            os.symlink(wheel_file_symlink_target, target_file)

        for metadata_filename in metadata_files_to_repair:
            repair_metadata_file(metadata_filename, canonical_name_to_metadata_name)

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

        write_utf8_file(temp_dir_path.joinpath(CACHE_FILE), json.dumps(cache))

        final_name = target_path.parent / (target_path.name + "-" + temp_dir_path.name)
        final_build_name = final_name.parent / (final_name.name + "-build")

        # Rename the new index to the final name
        os.rename(temp_dir_path, final_name)

        # Create a temporary symlink to the final name
        os.symlink(final_name, final_build_name)

        # Finally replace the live index with the new one
        os.replace(final_build_name, target_path)

        if old_index:
            rmtree(old_index)

        return target_path, projects
