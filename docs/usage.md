# Usage

`index-503` generates a [PEP 503](https://peps.python.org/pep-0503/) "simple"
repository index from a directory of wheel files.

## Command line

Point `index-503` at a directory that contains `.whl` files:

```bash
index-503 musllinux
```

This produces a sibling directory `musllinux-index/` containing:

- A top-level `index.html` listing every project found.
- A per-project `<name>/index.html` listing every wheel for that project.
- A `<wheel>.metadata` sidecar for every wheel (see *Generated metadata* below).
- A `cache.json` used to skip unchanged wheels on subsequent runs.

The wheels themselves are exposed via a symlink, so the original wheel
directory is never modified. A re-run swaps the index atomically and a
lock in the parent directory prevents concurrent executions.

## Installing from the index

For image builds (single index):

```bash
pip install --only-binary=:all: \
    --index-url "https://wheels.example.org/musllinux-index/" \
    -r requirements.txt
```

For runtime installs that should fall back to PyPI:

```bash
pip install --only-binary=:all: \
    --extra-index-url "https://wheels.example.org/musllinux-index/" \
    -r requirements.txt
```

`pip` 23.2 or newer is required — see
[pypa/pip#12038](https://github.com/pypa/pip/issues/12038).

## Generated metadata

`index-503` produces more than the bare PEP 503 layout — every wheel gets a
[PEP 658](https://peps.python.org/pep-0658/) /
[PEP 714](https://peps.python.org/pep-0714/) core-metadata sidecar:

- The wheel's `METADATA` file is extracted to `<wheel-filename>.metadata`.
- The anchor tag for each wheel advertises that sidecar with both
  `data-core-metadata="sha256=..."` (PEP 714, current) and
  `data-dist-info-metadata="sha256=..."` (PEP 658, legacy alias).
- The wheel's `Requires-Python` value is exposed via `data-requires-python`.

This lets resolvers like `pip` fetch dependency metadata without downloading
the full wheel, which makes resolution dramatically faster on slow links.
