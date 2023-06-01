from typing import Iterable, Union

from airium import Airium
from natsort import natsorted
from yarl import URL

from .util import canonicalize_name
from .wheel_file import WheelFile


# modified from https://github.com/repo-helper/simple503/blob/master/simple503/__init__.py
def generate_index(projects: Iterable[str]) -> Airium:
    """
    Generate the simple repository index page, containing a list of all projects.

    :param projects: The list of projects to generate links for.
    """

    base_url = URL("./")
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


def generate_project_page(
    name: str, files: Iterable[WheelFile], base_url: Union[str, URL] = "/"
) -> Airium:
    """
    Generate the repository page for a project.

    :param name: The project name, e.g. ``domdf-python-tools``.
    :param files: An iterable of files for the project, which will be linked to from the index page.
    :param base_url: The base URL of the Python package repository.
        For example, with PyPI's URL, a URL of /foo/ would be https://pypi.org/simple/foo/.
    """

    name = canonicalize_name(name)
    page = Airium()

    page("<!DOCTYPE html>")
    with page.html(lang="en"):
        with page.head():
            get_meta_tags(page)
            with page.title():
                page(f"Links for {name}")

        with page.body():
            with page.h1():
                # Not part of the spec, but allowed
                page(f"Links for {name}")

            for wheel_file in files:
                wheel_file.as_anchor(page, base_url)
                page.br()

    return page


def get_meta_tags(page: Airium) -> None:
    from . import __version__

    # Not part of the spec, but allowed
    page.meta(name="generator", content=f"index503 version {__version__}")
    page.meta(name="pypi:repository-version", content="1.0")
    page.meta(charset="UTF-8")
