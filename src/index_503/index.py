import glob
import logging
import os
from collections import defaultdict
from operator import attrgetter
from pathlib import Path
from shutil import copyfile, rmtree
from tempfile import mkdtemp
from typing import Dict, List, Set

from natsort import natsorted
from yarl import URL

from .cache import IndexCache
from .file import write_utf8_file
from .metadata import repair_metadata_file
from .page_generator import generate_index, generate_project_page
from .util import canonicalize_name, exclusive_lock
from .wheel_file import WheelFile

_LOGGER = logging.getLogger(__name__)


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
    with exclusive_lock(origin_path):
        return IndexMaker(origin_path).make_index()


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
        target_path = self.target_path
        old_index = target_path.readlink() if target_path.exists() else None
        temp_dir = mkdtemp(None, None, str(self.target_path.parent))
        try:
            self.cache.load()
            temp_dir_path = Path(temp_dir)

            self._make_index_at_temp_dir(temp_dir_path)
            self._atomic_replace_old_index(temp_dir_path, target_path)

            if old_index:
                _LOGGER.debug("Removing old index %s", old_index)
                rmtree(old_index)

            return self.target_path
        except Exception:
            _LOGGER.exception("Error generating index")
            rmtree(temp_dir)
            raise

    def _atomic_replace_old_index(self, temp_dir_path: Path, target_path: Path) -> None:
        """Atomically replace the old index with the new one."""
        final_name = target_path.parent / (target_path.name + "-" + temp_dir_path.name)
        final_build_name = final_name.parent / (final_name.name + "-build")

        _LOGGER.debug("Renaming %s with %s", temp_dir_path, final_name)
        # Rename the new index to the final name
        os.rename(temp_dir_path, final_name)

        _LOGGER.debug("Symlinking %s with %s", final_name, final_build_name)
        # Create a temporary symlink to the final name
        os.symlink(final_name, final_build_name)

        _LOGGER.debug("Replacing %s with %s", final_build_name, target_path)
        # Finally replace the live index with the new one
        os.replace(final_build_name, target_path)

    def _make_index_at_temp_dir(self, temp_dir_path: Path) -> None:
        """Generate a simple repository of Python wheels in a temp dir."""
        new_wheel_file_objects: List[WheelFile] = []
        projects: Dict[str, List[WheelFile]] = defaultdict(list)
        wheel_file_name_to_metadata_path: Dict[str, Path] = {}
        all_wheel_files: Set[str] = set()
        canonical_name_to_metadata_name: Dict[str, str] = {}
        raw_cache = self.cache.cache

        for wheel_file in glob.glob(str(self.origin_path.joinpath("*.whl"))):
            wheel_path = Path(wheel_file)
            wheel_file_name = wheel_path.name
            all_wheel_files.add(wheel_file_name)
            target_file = temp_dir_path.joinpath(wheel_file_name)
            metadata_path = target_file.with_suffix(f"{target_file.suffix}.metadata")
            wheel_file_symlink_target = f"../{self.origin_name}/{wheel_file_name}"

            if (wheel_cache := raw_cache.get(wheel_file_name)) and (
                wheel_file_obj := WheelFile.from_cache(wheel_cache)
            ):
                copyfile(self.target_path.joinpath(metadata_path.name), metadata_path)
            elif wheel_file_obj := WheelFile.from_wheel(wheel_path, metadata_path):
                wheel_file_name_to_metadata_path[wheel_file_name] = metadata_path
                new_wheel_file_objects.append(wheel_file_obj)
                raw_cache[wheel_file_name] = wheel_file_obj.as_dict()
            else:
                continue

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
        raw_cache = self.cache.cache
        for wheel_file_obj in new_wheel_file_objects:
            wheel_file_name = wheel_file_obj.filename
            metadata_path = wheel_file_name_to_metadata_path[wheel_file_name]

            if repair_metadata_file(metadata_path, canonical_name_to_metadata_name):
                wheel_file_obj.update_metadata(metadata_path)
                raw_cache[wheel_file_name] = wheel_file_obj.as_dict()

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
