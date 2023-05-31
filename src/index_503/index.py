import re
from typing import Iterable, Union

from airium import Airium
from natsort import natsorted
from yarl import URL


# modified from https://github.com/repo-helper/simple503/blob/master/simple503/__init__.py
def generate_index(projects: Iterable[str], base_url: Union[str, URL] = "/") -> Airium:
    """
    Generate the simple repository index page, containing a list of all projects.

    :param projects: The list of projects to generate links for.
    :param base_url: The base URL of the Python package repository.
        For example, with PyPI's URL, a URL of /foo/ would be https://pypi.org/simple/foo/.
    """

    base_url = URL(base_url)
    index = Airium()

    index("<!DOCTYPE html>")
    with index.html(lang="en"):
        with index.head():
            get_meta_tags(index)

            with index.title():
                index("Simple Package Repository")

        with index.body():
            for project_name in natsorted(projects, key=str.lower):
                normalized_name = canonicalize_name(project_name)

                with index.a(href=f"{base_url / normalized_name}/"):
                    index(project_name)
                index.br()

    return index


_canonicalize_regex = re.compile(r"[-_.]+")
# PEP 427: The build number must start with a digit.


def canonicalize_name(name: str) -> str:
    # This is taken from PEP 503.
    return _canonicalize_regex.sub("-", name).lower()


def get_meta_tags(page: Airium) -> None:
    from . import __version__

    # Not part of the spec, but allowed
    page.meta(name="generator", content=f"index503 version {__version__}")
    page.meta(name="pypi:repository-version", content="1.0")
    page.meta(charset="UTF-8")
