# https://github.com/repo-helper/simple503/blob/master/simple503/__init__.py
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
import posixpath
from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path
from typing import Any, Dict, Optional, Union

from airium import Airium
from dist_meta import metadata
from typing_extensions import Literal
from yarl import URL

from .metadata import extract_metadata_from_wheel_file
from .util import canonicalize_name, get_sha256_hash

WHEEL_FILE_VERSION = 9

HASH_FORMAT = "sha256"


@dataclass
class WheelFile:
    """Represents a wheel file in the repository."""

    version: int
    """The version of the wheel file format."""

    canonical_name: str
    """The canonicalized name of the project."""

    filename: str
    """The filename of the wheel file."""

    metadata_name: str
    """The Name field from the METADATA file."""

    wheel_hash: str  # HASH_FORMAT
    """
    The hash of the wheel file.

    Repositories SHOULD choose a hash function from one of the ones guaranteed
    to be available via the hashlib module in the Python standard library
    (currently ``md5``, ``sha1``, ``sha224``, ``sha256``, ``sha384``, ``sha512``).
    The current recommendation is to use ``sha256``.
    """

    requires_python: Optional[str] = None
    """
    The ``Requires-Python`` attribute from the wheel's ``METADATA`` file.

    :py:obj:`None` if undefined.
    """

    metadata_hash: Union[str, Literal[True], None] = None
    """
    The hash of the wheel's METADATA file.

    :py:obj:`None` if the metadata file is not exposed.
    May be :py:obj:`True` if no hash is available.
    """

    def as_anchor(self, page: Airium, base_url: Union[str, URL] = "/") -> None:
        """
        Generate an anchor tag in a :class:`airium.Airium` document for this file.

        :param page:
        :param base_url: The base URL of the Python package repository.
        """

        base_url = URL(base_url)

        href = f"{base_url / self.filename}#{HASH_FORMAT}={self.wheel_hash}"
        kwargs = {"href": href}

        if self.requires_python is not None:
            kwargs["data-requires-python"] = escape(self.requires_python)
        elif self.metadata_hash is not None:
            kwargs["data-dist-info-metadata"] = f"{HASH_FORMAT}={self.metadata_hash}"

        with page.a(**kwargs):
            page(posixpath.basename(self.filename))

    def update_metadata(self, metadata_path: Path) -> None:
        """
        Update the metadata hash of this wheel file.

        :param metadata_path:
        """

        self.metadata_hash = get_sha256_hash(metadata_path)

    def as_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this wheel file."""
        return asdict(self)

    @classmethod
    def from_cache(cls, cache_data: Dict[str, Any]) -> Optional["WheelFile"]:
        """Create a :class:`~.WheelFile` from a cache entry."""
        if cache_data["version"] != WHEEL_FILE_VERSION:
            return None
        return cls(**cache_data)

    @classmethod
    def from_wheel(
        cls,
        wheel_path: Path,
        metadata_path: Path,
    ) -> Optional["WheelFile"]:
        """Create a :class:`~.WheelFile` from a wheel file and its metadata file."""
        metadata_string = extract_metadata_from_wheel_file(wheel_path)
        if not metadata_string:
            return None
        metadata_path.write_text(metadata_string)
        wheel_metadata = metadata.loads(metadata_string)
        wheel_file_name = wheel_path.name
        metadata_name = wheel_metadata["Name"]
        canonical_name = canonicalize_name(metadata_name)
        return cls(
            version=WHEEL_FILE_VERSION,
            metadata_name=metadata_name,
            canonical_name=canonical_name,
            filename=wheel_file_name,
            wheel_hash=get_sha256_hash(wheel_path),
            requires_python=wheel_metadata.get("Requires-Python"),
            metadata_hash=get_sha256_hash(metadata_path),
        )
