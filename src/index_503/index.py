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

from natsort import natsorted
from yarl import URL

from .file import write_utf8_file
from .metadata import repair_metadata_file
from .page_generator import generate_index, generate_project_page
from .util import canonicalize_name, get_sha256_hash, load_json_file
from .wheel_file import WHEEL_FILE_VERSION, WheelFile

_LOGGER = logging.getLogger(__name__)

CACHE_FILE = "cache.json"


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


class IndexMaker:
    """Generate a simple repository of Python wheels."""

    def __init__(self, origin_path: Path) -> None:
        """Generate a simple repository of Python wheels."""
        self.origin_path = origin_path
        self.origin_name = origin_path.name
        target_path = origin_path.parent / (origin_path.name + "-index")
        self.target_path = target_path
        self.old_index = target_path.readlink() if target_path.exists() else None
        self.target_path_parent = target_path.parent
        self.projects: Dict[str, List[WheelFile]] = defaultdict(list)
        self.cache = IndexCache(target_path)
        self.all_wheel_files: set[str] = set()
        self.canonical_name_to_metadata_name: Dict[str, str] = {}
        self.new_wheel_file_objects: List[WheelFile] = []
        self.wheel_file_name_to_metadata_path: Dict[str, Path] = {}

    def make_index(self) -> Tuple[Path, Dict[str, List["WheelFile"]]]:
        """Generate a simple repository of Python wheels."""
        with tempfile.TemporaryDirectory(
            dir=str(self.target_path_parent), ignore_cleanup_errors=True
        ) as temp_dir:
            temp_dir_path = Path(temp_dir)

            self._make_index_at_temp_dir(temp_dir_path)
            self._atomic_replace_old_index(temp_dir_path)

            if self.old_index:
                rmtree(self.old_index)

            return self.target_path, self.projects

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
        for wheel_file in glob.glob(str(self.origin_path.joinpath("*.whl"))):
            wheel_path = Path(wheel_file)
            wheel_file_name = wheel_path.name
            target_file = temp_dir_path.joinpath(wheel_file_name)
            metadata_path = target_file.with_suffix(f"{target_file.suffix}.metadata")
            wheel_file_symlink_target = f"../{self.origin_name}/{wheel_file_name}"
            wheel_cache = self.cache.cache.get(wheel_file_name)
            self.all_wheel_files.add(wheel_file_name)

            if wheel_cache and wheel_cache["version"] == WHEEL_FILE_VERSION:
                wheel_file_obj = WheelFile(**wheel_cache)
                copyfile(self.target_path.joinpath(metadata_path.name), metadata_path)
            else:
                maybe_wheel_file_obj = WheelFile.from_wheel(wheel_path, metadata_path)
                if not maybe_wheel_file_obj:
                    continue
                wheel_file_obj = maybe_wheel_file_obj
                self.wheel_file_name_to_metadata_path[wheel_file_name] = metadata_path
                self.new_wheel_file_objects.append(wheel_file_obj)
                self.cache.cache[wheel_file_name] = asdict(wheel_file_obj)

            canonical_name = wheel_file_obj.canonical_name
            metadata_name = wheel_file_obj.metadata_name
            self.projects[metadata_name].append(wheel_file_obj)
            self.canonical_name_to_metadata_name[canonical_name] = metadata_name
            os.symlink(wheel_file_symlink_target, target_file)

        self.repair_metadata_files()
        self.generate_index_pages(temp_dir_path)
        self.cache.write_to_new(temp_dir_path)

    def remove_old_wheel_files(self) -> None:
        # Remove any old wheel files from the cache
        removed_wheels = set(self.cache.cache.keys()) - self.all_wheel_files
        for old_wheel_file in removed_wheels:
            del self.cache.cache[old_wheel_file]

    def repair_metadata_files(self) -> None:
        """Repair the metadata files."""
        # Now fix all the metadata files and update the sha256 hash + cache
        for wheel_file_obj in self.new_wheel_file_objects:
            wheel_file_name = wheel_file_obj.filename
            metadata_path = self.wheel_file_name_to_metadata_path[wheel_file_name]

            if repair_metadata_file(
                metadata_path, self.canonical_name_to_metadata_name
            ):
                wheel_file_obj.metadata_hash = get_sha256_hash(metadata_path)
                self.cache.cache[wheel_file_name] = asdict(wheel_file_obj)

    def generate_index_pages(self, temp_dir_path: Path) -> None:
        """Generate the index pages."""
        index_content = str(generate_index(self.projects.keys()))
        write_utf8_file(temp_dir_path.joinpath("index.html"), index_content)
        project_base_url = URL("../")

        for project_name, project_files in self.projects.items():
            project_dir = temp_dir_path.joinpath(canonicalize_name(project_name))
            project_dir.mkdir(exist_ok=True)
            project_index = generate_project_page(
                project_name,
                natsorted(project_files, key=attrgetter("filename"), reverse=True),
                project_base_url,
            )

            write_utf8_file(project_dir.joinpath("index.html"), str(project_index))
