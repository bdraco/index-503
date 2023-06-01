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
from dataclasses import dataclass
from html import escape
from typing import Optional, Union

from airium import Airium
from typing_extensions import Literal
from yarl import URL

WHEEL_FILE_VERSION = 8


@dataclass
class WheelFile:
    """
    Represents a wheel file in the repository.
    """

    # The version of the wheel file format.
    version: int

    # The canonicalized name of the project.
    canonical_name: str

    # The filename of the wheel file.
    filename: str

    # The Name field from the METADATA file.
    metadata_name: str

    wheel_hash: str  # sha256
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

        href = f"{base_url / self.filename}#sha256={self.wheel_hash}"
        kwargs = {"href": href}

        if self.requires_python is not None:
            kwargs["data-requires-python"] = escape(self.requires_python)
        if self.metadata_hash is True:
            kwargs["data-dist-info-metadata"] = "true"
        elif self.metadata_hash is not None:
            kwargs["data-dist-info-metadata"] = f"sha256={self.metadata_hash}"

        with page.a(**kwargs):
            page(posixpath.basename(self.filename))
