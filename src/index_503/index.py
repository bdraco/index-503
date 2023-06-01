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
from typing import Any, Dict, List, Set

from natsort import natsorted
from yarl import URL

from .file import write_utf8_file
from .metadata import repair_metadata_file
from .page_generator import generate_index, generate_project_page
from .util import canonicalize_name, get_sha256_hash, load_json_file
from .wheel_file import WHEEL_FILE_VERSION, WheelFile

_LOGGER = logging.getLogger(__name__)

CACHE_FILE = "cache.json"


def make_index(origin_path: Path) -> Path:
    """Generate a simple repository of Python wheels.

    This function will take a directory of wheels at the top level
    of a webserver and generate a simple repository of wheels.

    :param origin: The name of the directory containing the wheels.

    Example
    musllinux

    This will generate
    musllinux-index
    """
    return IndexMaker(origin_path).make_index()


class IndexCache:
    def __init__(self, target_path: Path) -> None:
        """Cache of WheelFiles between runs."""
        cache_file = target_path.joinpath(CACHE_FILE)
        self.cache_file = cache_file
        self.cache: Dict[str, Dict[str, Any]] = {}
        if cache_file.exists():
            self.cache = load_json_file(cache_file)

    def write_to_new(self, target: Path) -> None:
        """Write the cache to a new file."""
        cache_file = target.joinpath(CACHE_FILE)
        write_utf8_file(cache_file, json.dumps(self.cache))

    def remove_stale_keys(self, all_wheel_files: Set[str]) -> None:
        """Remove any wheel file names that no longer exist."""
        removed_wheels = set(self.cache.keys()) - all_wheel_files
        for old_wheel_file in removed_wheels:
            del self.cache[old_wheel_file]


class IndexMaker:
    """Generate a simple repository of Python wheels."""

    def __init__(self, origin_path: Path) -> None:
        """Generate a simple repository of Python wheels."""
        self.origin_path = origin_path
        self.origin_name = origin_path.name
        target_path = origin_path.parent / (origin_path.name + "-index")
        self.target_path = target_path
        self.cache = IndexCache(target_path)

    def make_index(self) -> Path:
        """Generate a simple repository of Python wheels."""
        with tempfile.TemporaryDirectory(
            dir=str(self.target_path.parent), ignore_cleanup_errors=True
        ) as temp_dir:
            temp_dir_path = Path(temp_dir)

            self._make_index_at_temp_dir(temp_dir_path)
            self._atomic_replace_old_index(temp_dir_path)

            old_index = (
                self.target_path.readlink() if self.target_path.exists() else None
            )
            if old_index:
                rmtree(old_index)

            return self.target_path

    def _atomic_replace_old_index(self, temp_dir_path: Path) -> None:
        """Atomically replace the old index with the new one."""
        final_name = self.target_path.parent / (
            self.target_path.name + "-" + temp_dir_path.name
        )
        final_build_name = final_name.parent / (final_name.name + "-build")

        # Rename the new index to the final name
        os.rename(temp_dir_path, final_name)

        # Create a temporary symlink to the final name
        os.symlink(final_name, final_build_name)

        # Finally replace the live index with the new one
        os.replace(final_build_name, self.target_path)

    def _make_index_at_temp_dir(self, temp_dir_path: Path) -> None:
        """Generate a simple repository of Python wheels in a temp dir."""
        new_wheel_file_objects: List[WheelFile] = []
        projects: Dict[str, List[WheelFile]] = defaultdict(list)
        wheel_file_name_to_metadata_path: Dict[str, Path] = {}
        all_wheel_files: Set[str] = set()
        canonical_name_to_metadata_name: Dict[str, str] = {}

        for wheel_file in glob.glob(str(self.origin_path.joinpath("*.whl"))):
            wheel_path = Path(wheel_file)
            wheel_file_name = wheel_path.name
            all_wheel_files.add(wheel_file_name)
            target_file = temp_dir_path.joinpath(wheel_file_name)
            metadata_path = target_file.with_suffix(f"{target_file.suffix}.metadata")
            wheel_file_symlink_target = f"../{self.origin_name}/{wheel_file_name}"
            wheel_cache = self.cache.cache.get(wheel_file_name)

            if wheel_cache and wheel_cache["version"] == WHEEL_FILE_VERSION:
                wheel_file_obj = WheelFile(**wheel_cache)
                copyfile(self.target_path.joinpath(metadata_path.name), metadata_path)
            else:
                maybe_wheel_file_obj = WheelFile.from_wheel(wheel_path, metadata_path)
                if not maybe_wheel_file_obj:
                    continue
                wheel_file_obj = maybe_wheel_file_obj
                wheel_file_name_to_metadata_path[wheel_file_name] = metadata_path
                new_wheel_file_objects.append(wheel_file_obj)
                self.cache.cache[wheel_file_name] = asdict(wheel_file_obj)

            canonical_name = wheel_file_obj.canonical_name
            metadata_name = wheel_file_obj.metadata_name
            projects[metadata_name].append(wheel_file_obj)
            canonical_name_to_metadata_name[canonical_name] = metadata_name
            os.symlink(wheel_file_symlink_target, target_file)

        self.cache.remove_stale_keys(all_wheel_files)
        self.repair_metadata_files(
            new_wheel_file_objects,
            wheel_file_name_to_metadata_path,
            canonical_name_to_metadata_name,
        )
        self.generate_index_pages(temp_dir_path, projects)
        self.cache.write_to_new(temp_dir_path)

    def repair_metadata_files(
        self,
        new_wheel_file_objects: List[WheelFile],
        wheel_file_name_to_metadata_path: Dict[str, Path],
        canonical_name_to_metadata_name: Dict[str, str],
    ) -> None:
        """Repair the metadata files."""
        # Now fix all the metadata files and update the sha256 hash + cache
        for wheel_file_obj in new_wheel_file_objects:
            wheel_file_name = wheel_file_obj.filename
            metadata_path = wheel_file_name_to_metadata_path[wheel_file_name]

            if repair_metadata_file(metadata_path, canonical_name_to_metadata_name):
                wheel_file_obj.metadata_hash = get_sha256_hash(metadata_path)
                self.cache.cache[wheel_file_name] = asdict(wheel_file_obj)

    def generate_index_pages(
        self, temp_dir_path: Path, projects: Dict[str, List[WheelFile]]
    ) -> None:
        """Generate the index pages."""
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

        _LOGGER.debug("Generated index pages for %s projects.", len(projects))
