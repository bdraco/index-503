# CHANGELOG


## v2.6.0 (2025-04-01)

### Chores

- Create dependabot.yml
  ([`af2e517`](https://github.com/bdraco/index-503/commit/af2e517749e4f1abcdc3d886e083530a1b920dac))

- Update dependabot.yml to include GHA
  ([`c28c481`](https://github.com/bdraco/index-503/commit/c28c4812983bbc24de734fa78ef252c768a9e974))

- Update for Python 3.13 ([#77](https://github.com/bdraco/index-503/pull/77),
  [`e76decc`](https://github.com/bdraco/index-503/commit/e76decc035bbb112c14f864b1112a9b0d262fddf))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **deps**: Bump consolekit from 1.4.1 to 1.7.2 ([#75](https://github.com/bdraco/index-503/pull/75),
  [`39074bb`](https://github.com/bdraco/index-503/commit/39074bb0b566c7a4aa3986be4b96e45d762869cd))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump dist-meta from 0.8.1 to 0.9.0 ([#88](https://github.com/bdraco/index-503/pull/88),
  [`c56c7ca`](https://github.com/bdraco/index-503/commit/c56c7ca4788d1341bff9b77863519e2581ac88a9))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump natsort from 8.3.1 to 8.4.0 ([#73](https://github.com/bdraco/index-503/pull/73),
  [`e5f3118`](https://github.com/bdraco/index-503/commit/e5f311854042a6a4c10be7824a923f25cf11930b))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump yarl from 1.9.2 to 1.18.3 ([#74](https://github.com/bdraco/index-503/pull/74),
  [`62669ee`](https://github.com/bdraco/index-503/commit/62669eec7bf8a300a1daa47dc7275b5842b94f96))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-ci**: Bump the github-actions group with 8 updates
  ([#93](https://github.com/bdraco/index-503/pull/93),
  [`98f065c`](https://github.com/bdraco/index-503/commit/98f065c4b1e97f5277bbb6c3ad45e805c191bd62))

* chore(deps-ci): bump the github-actions group with 8 updates

Bumps the github-actions group with 8 updates:

| Package | From | To | | --- | --- | --- | |
  [actions/checkout](https://github.com/actions/checkout) | `3` | `4` | |
  [actions/setup-python](https://github.com/actions/setup-python) | `4` | `5` | |
  [pre-commit/action](https://github.com/pre-commit/action) | `3.0.0` | `3.0.1` | |
  [wagoid/commitlint-github-action](https://github.com/wagoid/commitlint-github-action) | `5.4.1` |
  `6.2.1` | | [snok/install-poetry](https://github.com/snok/install-poetry) | `1.3.4` | `1.4.1` | |
  [codecov/codecov-action](https://github.com/codecov/codecov-action) | `3` | `5` | |
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  | `7.34.6` | `9.21.0` | | [tiangolo/issue-manager](https://github.com/tiangolo/issue-manager) |
  `0.4.0` | `0.5.1` |

Updates `actions/checkout` from 3 to 4 - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v3...v4)

Updates `actions/setup-python` from 4 to 5 - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v4...v5)

Updates `pre-commit/action` from 3.0.0 to 3.0.1 - [Release
  notes](https://github.com/pre-commit/action/releases) -
  [Commits](https://github.com/pre-commit/action/compare/v3.0.0...v3.0.1)

Updates `wagoid/commitlint-github-action` from 5.4.1 to 6.2.1 -
  [Changelog](https://github.com/wagoid/commitlint-github-action/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/wagoid/commitlint-github-action/compare/v5.4.1...v6.2.1)

Updates `snok/install-poetry` from 1.3.4 to 1.4.1 - [Release
  notes](https://github.com/snok/install-poetry/releases) -
  [Commits](https://github.com/snok/install-poetry/compare/v1.3.4...v1.4.1)

Updates `codecov/codecov-action` from 3 to 5 - [Release
  notes](https://github.com/codecov/codecov-action/releases) -
  [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/codecov/codecov-action/compare/v3...v5)

Updates `python-semantic-release/python-semantic-release` from 7.34.6 to 9.21.0 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v7.34.6...v9.21.0)

Updates `tiangolo/issue-manager` from 0.4.0 to 0.5.1 - [Release
  notes](https://github.com/tiangolo/issue-manager/releases) -
  [Commits](https://github.com/tiangolo/issue-manager/compare/0.4.0...0.5.1)

--- updated-dependencies: - dependency-name: actions/checkout dependency-type: direct:production

update-type: version-update:semver-major

dependency-group: github-actions

- dependency-name: actions/setup-python dependency-type: direct:production

- dependency-name: pre-commit/action dependency-type: direct:production

update-type: version-update:semver-patch

- dependency-name: wagoid/commitlint-github-action dependency-type: direct:production

- dependency-name: snok/install-poetry dependency-type: direct:production

update-type: version-update:semver-minor

- dependency-name: codecov/codecov-action dependency-type: direct:production

- dependency-name: python-semantic-release/python-semantic-release dependency-type:
  direct:production

- dependency-name: tiangolo/issue-manager dependency-type: direct:production

dependency-group: github-actions ...

Signed-off-by: dependabot[bot] <support@github.com>

* chore: fixes

* chore: fix lock confilict

---------

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: J. Nick Koston <nick@koston.org>

- **deps-dev**: Bump jinja2 from 3.1.5 to 3.1.6 ([#92](https://github.com/bdraco/index-503/pull/92),
  [`4463dab`](https://github.com/bdraco/index-503/commit/4463dab94a0d6d6980f95885995ac77331638247))

Bumps [jinja2](https://github.com/pallets/jinja) from 3.1.5 to 3.1.6. - [Release
  notes](https://github.com/pallets/jinja/releases) -
  [Changelog](https://github.com/pallets/jinja/blob/main/CHANGES.rst) -
  [Commits](https://github.com/pallets/jinja/compare/3.1.5...3.1.6)

--- updated-dependencies: - dependency-name: jinja2 dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 7.4.4 to 8.3.4 ([#84](https://github.com/bdraco/index-503/pull/84),
  [`5b369b9`](https://github.com/bdraco/index-503/commit/5b369b977aa9323fd765df506d9bd450ac414b5d))

- **deps-dev**: Bump pytest from 8.3.4 to 8.3.5 ([#91](https://github.com/bdraco/index-503/pull/91),
  [`08d2bdf`](https://github.com/bdraco/index-503/commit/08d2bdfb1d00843d5250388ef37e010159a28227))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.4 to 8.3.5. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.4...8.3.5)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-cov from 3.0.0 to 6.0.0
  ([#76](https://github.com/bdraco/index-503/pull/76),
  [`5e2ca05`](https://github.com/bdraco/index-503/commit/5e2ca051ef45bd5851c498b6248b32e1f2bb64e1))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#60](https://github.com/bdraco/index-503/pull/60),
  [`ab586f3`](https://github.com/bdraco/index-503/commit/ab586f31b2d26d61dcf50b3d25ba0e9ed11ea57f))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#61](https://github.com/bdraco/index-503/pull/61),
  [`f513d9d`](https://github.com/bdraco/index-503/commit/f513d9d44c9fb141316c7b701a36a75922cd5ef8))

updates: - [github.com/pre-commit/mirrors-mypy: v1.10.0 →
  v1.10.1](https://github.com/pre-commit/mirrors-mypy/compare/v1.10.0...v1.10.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#62](https://github.com/bdraco/index-503/pull/62),
  [`2a05126`](https://github.com/bdraco/index-503/commit/2a05126b3bfe5683f335e7db1529c2592e445ac5))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#63](https://github.com/bdraco/index-503/pull/63),
  [`88a0ab9`](https://github.com/bdraco/index-503/commit/88a0ab9fe467d2bcd20200c99d4741bf572aa097))

updates: - [github.com/asottile/pyupgrade: v3.16.0 →
  v3.17.0](https://github.com/asottile/pyupgrade/compare/v3.16.0...v3.17.0)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#64](https://github.com/bdraco/index-503/pull/64),
  [`2f9eeaa`](https://github.com/bdraco/index-503/commit/2f9eeaa01cf72aa9d363b4f4fd05a578a04f6a34))

updates: - [github.com/psf/black: 24.4.2 →
  24.8.0](https://github.com/psf/black/compare/24.4.2...24.8.0) - [github.com/PyCQA/flake8: 7.1.0 →
  7.1.1](https://github.com/PyCQA/flake8/compare/7.1.0...7.1.1) -
  [github.com/pre-commit/mirrors-mypy: v1.11.0 →
  v1.11.1](https://github.com/pre-commit/mirrors-mypy/compare/v1.11.0...v1.11.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#65](https://github.com/bdraco/index-503/pull/65),
  [`c509722`](https://github.com/bdraco/index-503/commit/c509722f42174720abfb2de526139b33a0c53c96))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#66](https://github.com/bdraco/index-503/pull/66),
  [`fb1ae31`](https://github.com/bdraco/index-503/commit/fb1ae312f11813e00cb2ad98605ebee0bbd80919))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#67](https://github.com/bdraco/index-503/pull/67),
  [`1daadaa`](https://github.com/bdraco/index-503/commit/1daadaa5539534380eb6ca0772ec005aa7631ac8))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#68](https://github.com/bdraco/index-503/pull/68),
  [`655cb4f`](https://github.com/bdraco/index-503/commit/655cb4fb8f014e743218afc05f9078954356fec0))

updates: - [github.com/commitizen-tools/commitizen: v3.29.1 →
  v3.30.1](https://github.com/commitizen-tools/commitizen/compare/v3.29.1...v3.30.1) -
  [github.com/pre-commit/pre-commit-hooks: v4.6.0 →
  v5.0.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.6.0...v5.0.0) -
  [github.com/asottile/pyupgrade: v3.17.0 →
  v3.19.0](https://github.com/asottile/pyupgrade/compare/v3.17.0...v3.19.0) - [github.com/psf/black:
  24.8.0 → 24.10.0](https://github.com/psf/black/compare/24.8.0...24.10.0) -
  [github.com/pre-commit/mirrors-mypy: v1.11.2 →
  v1.13.0](https://github.com/pre-commit/mirrors-mypy/compare/v1.11.2...v1.13.0)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#69](https://github.com/bdraco/index-503/pull/69),
  [`1d49dc5`](https://github.com/bdraco/index-503/commit/1d49dc559f8cf325df0d962a321e30002429b406))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#70](https://github.com/bdraco/index-503/pull/70),
  [`aaf1184`](https://github.com/bdraco/index-503/commit/aaf1184233c617203e925ce0eb7a91f8934d2b63))

- **pre-commit.ci**: Pre-commit autoupdate ([#71](https://github.com/bdraco/index-503/pull/71),
  [`4426e13`](https://github.com/bdraco/index-503/commit/4426e139ade6e076963ca6eaa4cf1e36f66bbb8d))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#85](https://github.com/bdraco/index-503/pull/85),
  [`9ac5af1`](https://github.com/bdraco/index-503/commit/9ac5af155ed8ef0694d549b4a797ef2f2cc0007a))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#86](https://github.com/bdraco/index-503/pull/86),
  [`9f21ec4`](https://github.com/bdraco/index-503/commit/9f21ec4e9db54a50a6e82329aba2b73e8a1ae5ff))

- **pre-commit.ci**: Pre-commit autoupdate ([#87](https://github.com/bdraco/index-503/pull/87),
  [`c66bba9`](https://github.com/bdraco/index-503/commit/c66bba938168a3cc20508b959f9d56c0eb95bffe))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#89](https://github.com/bdraco/index-503/pull/89),
  [`ca4f936`](https://github.com/bdraco/index-503/commit/ca4f936cdbf517df3a917a03edfa11350d71da64))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate ([#90](https://github.com/bdraco/index-503/pull/90),
  [`f711f6f`](https://github.com/bdraco/index-503/commit/f711f6fe3eb57bf7a9ebdd07381fe07c8bdb5878))

updates: - [github.com/commitizen-tools/commitizen: v4.2.1 →
  v4.4.1](https://github.com/commitizen-tools/commitizen/compare/v4.2.1...v4.4.1) -
  [github.com/python-poetry/poetry: 2.1.1 →
  2.1.2](https://github.com/python-poetry/poetry/compare/2.1.1...2.1.2) - [github.com/PyCQA/isort:
  6.0.0 → 6.0.1](https://github.com/PyCQA/isort/compare/6.0.0...6.0.1) - [github.com/PyCQA/flake8:
  7.1.2 → 7.2.0](https://github.com/PyCQA/flake8/compare/7.1.2...7.2.0)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Switch to trusted publishing ([#94](https://github.com/bdraco/index-503/pull/94),
  [`a1a19ce`](https://github.com/bdraco/index-503/commit/a1a19cea7850b1f49c79d22ac0cc88a69fdca3d1))


## v2.5.1 (2023-09-29)

### Bug Fixes

- Canonicalize paths in the index ([#59](https://github.com/bdraco/index-503/pull/59),
  [`331d42a`](https://github.com/bdraco/index-503/commit/331d42af912e300815ff211aff387d8869c6faa5))


## v2.5.0 (2023-09-29)

### Features

- Handle wheel files changing ([#58](https://github.com/bdraco/index-503/pull/58),
  [`183e27c`](https://github.com/bdraco/index-503/commit/183e27c82b29ef5d43ae8ddbf7b608a265f82cd3))


## v2.4.1 (2023-09-21)

### Bug Fixes

- Ensure index is always built with readable permissions
  ([#56](https://github.com/bdraco/index-503/pull/56),
  [`7884985`](https://github.com/bdraco/index-503/commit/78849859545d1278d877577abffd432a631a0ab0))

### Chores

- Add py3.12 pre-release to CI ([#54](https://github.com/bdraco/index-503/pull/54),
  [`d0013f7`](https://github.com/bdraco/index-503/commit/d0013f7506a220877073491515b7da69fd1f51de))

- Delete labels workflow ([#55](https://github.com/bdraco/index-503/pull/55),
  [`03087cd`](https://github.com/bdraco/index-503/commit/03087cd282eb720d4a38f5e468ebab6e8131933d))


## v2.4.0 (2023-07-15)

### Chores

- Bump python-semantic-release ([#52](https://github.com/bdraco/index-503/pull/52),
  [`631914b`](https://github.com/bdraco/index-503/commit/631914b5172b8a08f68aa7dea455033ac1a333db))

### Features

- Remove pip workarounds ([#51](https://github.com/bdraco/index-503/pull/51),
  [`13853b1`](https://github.com/bdraco/index-503/commit/13853b1e4b335cddfd3ef1ef5336ce5ebfb5bd49))


## v2.3.1 (2023-06-02)

### Bug Fixes

- Document pip name compare problems ([#49](https://github.com/bdraco/index-503/pull/49),
  [`ea9e7d6`](https://github.com/bdraco/index-503/commit/ea9e7d638b70ab1dee1cea2eb61eac95cebbb890))


## v2.3.0 (2023-06-02)

### Features

- Add example pip usage to the docs ([#48](https://github.com/bdraco/index-503/pull/48),
  [`0910704`](https://github.com/bdraco/index-503/commit/0910704a46f4b7eaeec530469f021b3e8dcf955e))


## v2.2.0 (2023-06-02)

### Features

- Speed up metadata creation when there is a cache
  ([#47](https://github.com/bdraco/index-503/pull/47),
  [`a33c45f`](https://github.com/bdraco/index-503/commit/a33c45f8d8dce9a0ba1d6e62194530f2b8a31de1))


## v2.1.1 (2023-06-02)

### Bug Fixes

- Remove unused code ([#46](https://github.com/bdraco/index-503/pull/46),
  [`a023b79`](https://github.com/bdraco/index-503/commit/a023b7964f6c8653614caf688c52fb978994d7dd))


## v2.1.0 (2023-06-01)

### Bug Fixes

- Add missing cover for file ([#43](https://github.com/bdraco/index-503/pull/43),
  [`761fe3e`](https://github.com/bdraco/index-503/commit/761fe3e1c31b7a012c137c43dbe6fc30b4ab88d1))

- Util test did not sleep long enough for slow runner
  ([#44](https://github.com/bdraco/index-503/pull/44),
  [`5e97bda`](https://github.com/bdraco/index-503/commit/5e97bda7f59505399d38cddbd1f6980aef1a5bb5))

- Util test did not sleep long enough for slow runner
  ([#45](https://github.com/bdraco/index-503/pull/45),
  [`e82ed20`](https://github.com/bdraco/index-503/commit/e82ed20906a0494af723a8636e89c50eda8eada5))

### Chores

- Add tests to ensure failure cleans up ([#41](https://github.com/bdraco/index-503/pull/41),
  [`f63d733`](https://github.com/bdraco/index-503/commit/f63d7333b63c4cd2041df31ba236a0cb291af1af))

- Add tests to make sure metadata is repaired ([#40](https://github.com/bdraco/index-503/pull/40),
  [`5d08b0c`](https://github.com/bdraco/index-503/commit/5d08b0c15b8adf871cf287b1d9f87d3c4e399a0e))

### Features

- Add tests for exclusive_lock ([#42](https://github.com/bdraco/index-503/pull/42),
  [`7d8395c`](https://github.com/bdraco/index-503/commit/7d8395cec229325b4eaca91e3a952dba505b3b0a))


## v2.0.0 (2023-06-01)

### Bug Fixes

- Drop python 3.8 support ([#39](https://github.com/bdraco/index-503/pull/39),
  [`8ada082`](https://github.com/bdraco/index-503/commit/8ada0828d42c732282ce771ead90baaf8c7dc6d1))

BREAKING CHANGE: python 3.8 support is removed

- Temp dir handling on older python ([#37](https://github.com/bdraco/index-503/pull/37),
  [`eea3ea3`](https://github.com/bdraco/index-503/commit/eea3ea37da8967e70cd32cf5ba2aa87f6a4379fd))

- Tests need to work on case sensitive fs ([#38](https://github.com/bdraco/index-503/pull/38),
  [`9377df0`](https://github.com/bdraco/index-503/commit/9377df008ebce3683e7e59ec932ad4a95b4a4cf6))

### Chores

- Add coverage ([#36](https://github.com/bdraco/index-503/pull/36),
  [`33a8875`](https://github.com/bdraco/index-503/commit/33a88755e73bd81316d4b96e3ef02bc234374ab6))

- Add end to end test ([#35](https://github.com/bdraco/index-503/pull/35),
  [`4fcca9a`](https://github.com/bdraco/index-503/commit/4fcca9ae4439f2c1fb9f26c9dcca18e3ad62834f))

- Add more coverage ([#33](https://github.com/bdraco/index-503/pull/33),
  [`ea16bc4`](https://github.com/bdraco/index-503/commit/ea16bc42dc1893d62044bf92a405af01f8cca729))

- Add more test coverage ([#32](https://github.com/bdraco/index-503/pull/32),
  [`ecc59a5`](https://github.com/bdraco/index-503/commit/ecc59a5b06020ddc5a494a0db960c7e93f7dc94c))

- Add wheel file tests ([#34](https://github.com/bdraco/index-503/pull/34),
  [`812b083`](https://github.com/bdraco/index-503/commit/812b08332f41cc6c33c895c85418601f52d3f9af))

### Breaking Changes

- Python 3.8 support is removed


## v1.0.0 (2023-06-01)

### Bug Fixes

- Legacy typing for py3.8 ([#29](https://github.com/bdraco/index-503/pull/29),
  [`acf87a7`](https://github.com/bdraco/index-503/commit/acf87a7204e9969115358d63a190640eaa9ce940))

- More py3.8 typing fixes ([#31](https://github.com/bdraco/index-503/pull/31),
  [`8839d55`](https://github.com/bdraco/index-503/commit/8839d559b578626c0d0b6db03f8fd739cd69ac7b))

### Chores

- Add coverage for cache ([#25](https://github.com/bdraco/index-503/pull/25),
  [`7836c6c`](https://github.com/bdraco/index-503/commit/7836c6ce8a52db0f42a9a740020d1a4ec4437ee6))

- Add tests for file ([#26](https://github.com/bdraco/index-503/pull/26),
  [`bc9c2fd`](https://github.com/bdraco/index-503/commit/bc9c2fdd4e04bd1cf46af6e73875a36bb1fd8a5e))

- Add tests for repairing metadata ([#30](https://github.com/bdraco/index-503/pull/30),
  [`6e8d43f`](https://github.com/bdraco/index-503/commit/6e8d43f70c76eace60464acd1870ebea7c25d8dd))

- More refactoring ([#28](https://github.com/bdraco/index-503/pull/28),
  [`99b08e8`](https://github.com/bdraco/index-503/commit/99b08e8cc937c49ac0ffef16b7e40d5b88b88110))

- Remove double const ([#24](https://github.com/bdraco/index-503/pull/24),
  [`9daa163`](https://github.com/bdraco/index-503/commit/9daa163927c9e287684747837c5f61c6d7eca5bf))

### Features

- Refactor to make more testable ([#27](https://github.com/bdraco/index-503/pull/27),
  [`9c0560a`](https://github.com/bdraco/index-503/commit/9c0560aeb471f6740f145b6a2bb0b8342755dcf1))

BREAKING CHANGE: Drop python 3.7 support

### Breaking Changes

- Drop python 3.7 support


## v0.2.2 (2023-06-01)

### Bug Fixes

- Split cache into its own module ([#23](https://github.com/bdraco/index-503/pull/23),
  [`c5356af`](https://github.com/bdraco/index-503/commit/c5356af842bcf556157553ff86c0451922ea2cc7))


## v0.2.1 (2023-06-01)

### Bug Fixes

- Cleanup cache side effects ([#22](https://github.com/bdraco/index-503/pull/22),
  [`9f1e7d1`](https://github.com/bdraco/index-503/commit/9f1e7d1af5c5d52884080e5e565d7d605e6bd7fb))


## v0.2.0 (2023-06-01)

### Features

- Hold an exclusive lock to prevent multiple instances
  ([#21](https://github.com/bdraco/index-503/pull/21),
  [`25f661a`](https://github.com/bdraco/index-503/commit/25f661a5603224f91e3604b3b80b5c6357d1028a))


## v0.1.8 (2023-06-01)

### Bug Fixes

- Small cleanups ([#20](https://github.com/bdraco/index-503/pull/20),
  [`62933c1`](https://github.com/bdraco/index-503/commit/62933c14f7ead15fcb2332fce4ee8e3269cca8f0))


## v0.1.7 (2023-06-01)

### Bug Fixes

- Ensure new wheels can be found ([#19](https://github.com/bdraco/index-503/pull/19),
  [`441da84`](https://github.com/bdraco/index-503/commit/441da8446f7492bc81c8a26b5f04bf1567e21f94))

### Chores

- Cleanups ([#11](https://github.com/bdraco/index-503/pull/11),
  [`b1cb964`](https://github.com/bdraco/index-503/commit/b1cb9640ed9997551532e8a20a9a51b9fdaa6afd))

- Ensure cache is cleaned up between runs ([#18](https://github.com/bdraco/index-503/pull/18),
  [`fb066a3`](https://github.com/bdraco/index-503/commit/fb066a3319fb3e455b830fda684a86ec3dc81af0))

- More splits ([#12](https://github.com/bdraco/index-503/pull/12),
  [`a83e2d9`](https://github.com/bdraco/index-503/commit/a83e2d90fa9882a7cc148f849c488abcd026db36))

- Move metadata to its own module ([#8](https://github.com/bdraco/index-503/pull/8),
  [`02e12cd`](https://github.com/bdraco/index-503/commit/02e12cd07de56b1569bc1177bd3676b2e9e18ae3))

- Reduce code from refactor ([#17](https://github.com/bdraco/index-503/pull/17),
  [`5aea496`](https://github.com/bdraco/index-503/commit/5aea4965b06d29149d7c8071586966088b15d6ee))

- Remove duplicate code ([#14](https://github.com/bdraco/index-503/pull/14),
  [`ded13d1`](https://github.com/bdraco/index-503/commit/ded13d1941c013e00e5e0f9c0d4213429acfd9c4))

- Split up code some more ([#15](https://github.com/bdraco/index-503/pull/15),
  [`1e54084`](https://github.com/bdraco/index-503/commit/1e5408404e64ffde5301ebe224f33b7ec104e8a3))

- Split up code some more ([#16](https://github.com/bdraco/index-503/pull/16),
  [`c64bf5c`](https://github.com/bdraco/index-503/commit/c64bf5c45cb2c6c0c2452c3de523673ef7716402))

- Split up index maker code ([#10](https://github.com/bdraco/index-503/pull/10),
  [`5fbdd45`](https://github.com/bdraco/index-503/commit/5fbdd45ec7dfb4680e85e71fc9f4908b81e85437))

- Split up index maker code ([#9](https://github.com/bdraco/index-503/pull/9),
  [`b72f6ed`](https://github.com/bdraco/index-503/commit/b72f6ed0648a9dc639dc1fad7a3586c2cd6514ab))

- Split up more code ([#13](https://github.com/bdraco/index-503/pull/13),
  [`6f5b537`](https://github.com/bdraco/index-503/commit/6f5b5370dd3ae658781c866443dbd58194d54737))


## v0.1.6 (2023-06-01)

### Bug Fixes

- Repair should always update the original_name to the metadata_name
  ([#7](https://github.com/bdraco/index-503/pull/7),
  [`a491882`](https://github.com/bdraco/index-503/commit/a491882da721232efdb2b8d1a66dec44ba03433c))


## v0.1.5 (2023-06-01)

### Bug Fixes

- Canonicalize_name in repairs ([#6](https://github.com/bdraco/index-503/pull/6),
  [`12be36a`](https://github.com/bdraco/index-503/commit/12be36a6bcb7d64867e717e8aca0fd875562eab6))


## v0.1.4 (2023-06-01)

### Bug Fixes

- Caching ([#4](https://github.com/bdraco/index-503/pull/4),
  [`a303767`](https://github.com/bdraco/index-503/commit/a3037676d79fb59b0694745161b00a8f74251a39))

- Legacy typing ([#5](https://github.com/bdraco/index-503/pull/5),
  [`3847fc3`](https://github.com/bdraco/index-503/commit/3847fc342235c81cb9b94c90c366b63215ab7c0f))


## v0.1.3 (2023-06-01)

### Bug Fixes

- Rebuild hash if metadata is updated ([#3](https://github.com/bdraco/index-503/pull/3),
  [`915d65b`](https://github.com/bdraco/index-503/commit/915d65bc821de15b055f7aad2326c781cbd633b4))


## v0.1.2 (2023-06-01)

### Bug Fixes

- Load names from cache ([#2](https://github.com/bdraco/index-503/pull/2),
  [`ee2ccf7`](https://github.com/bdraco/index-503/commit/ee2ccf7c5eed26266ab33a5a81c8a9df6347ff2b))


## v0.1.1 (2023-06-01)

### Bug Fixes

- Normalize names in metadata ([#1](https://github.com/bdraco/index-503/pull/1),
  [`fcb1bd7`](https://github.com/bdraco/index-503/commit/fcb1bd74416137779749b2b5d0bfdd057dde7590))


## v0.1.0 (2023-05-31)

### Bug Fixes

- Adjust
  ([`ce8f63e`](https://github.com/bdraco/index-503/commit/ce8f63e3ddc2573a09fde23099fecf108df13c86))

- Ci
  ([`4584c36`](https://github.com/bdraco/index-503/commit/4584c368b8380d4f6eed7756642c03adda83db83))

- Ci
  ([`00f8812`](https://github.com/bdraco/index-503/commit/00f8812786bf8f43b8395a5209d5811b27fd752e))

- Ci
  ([`3fab19e`](https://github.com/bdraco/index-503/commit/3fab19eefccc157bc5686ae1686a78d9dc17e1f9))

- Fix
  ([`1dc7b79`](https://github.com/bdraco/index-503/commit/1dc7b791d2a2d028ec84f0fc06a5169d8afdde80))

- Fix
  ([`4cd7a83`](https://github.com/bdraco/index-503/commit/4cd7a8313e62d24cad563a5ec239712a93bc5cc4))

- Fix
  ([`c7e4cf7`](https://github.com/bdraco/index-503/commit/c7e4cf70e1986c5a99bcf07d75176ad7fb3e2fc5))

- Fix
  ([`a808dbc`](https://github.com/bdraco/index-503/commit/a808dbce2b77ce2363dc4592bfc33dace23efdbc))

- Fix
  ([`8b52162`](https://github.com/bdraco/index-503/commit/8b52162acf05ecc342e0a3ed865f5bbc0c63b002))

- Fix
  ([`0756c93`](https://github.com/bdraco/index-503/commit/0756c9393664492b320b74d1920f6e0eedbe2c07))

- Fix
  ([`e6bc8cc`](https://github.com/bdraco/index-503/commit/e6bc8ccb3214b4506d99d0886bc5dee36fe29cc7))

- Fix
  ([`cd30b99`](https://github.com/bdraco/index-503/commit/cd30b9929852552f42da5e3d0be8189dcb96ac29))

- Fix
  ([`42efaca`](https://github.com/bdraco/index-503/commit/42efacaae763c05304bba482f07745d68cdc888a))

- Fix
  ([`6cfcbf7`](https://github.com/bdraco/index-503/commit/6cfcbf7c18aa114596b77a1b200978f141c8d51e))

- Fix
  ([`f0faa81`](https://github.com/bdraco/index-503/commit/f0faa81355055ae927d472b1899dfda922dd73e1))

- Fixes
  ([`7d13b4a`](https://github.com/bdraco/index-503/commit/7d13b4a724333ca50aba24d9bf7770366f1a1149))

- Fixes
  ([`635e813`](https://github.com/bdraco/index-503/commit/635e813bbecc97998f3cb0de36d8d15895168860))

- Fixes
  ([`57fef5e`](https://github.com/bdraco/index-503/commit/57fef5e8352ed63edcd2980ac6e107adb6e7f002))

- Fixes
  ([`46a40be`](https://github.com/bdraco/index-503/commit/46a40bea8a1433fe62bf4d9c775830b0ca9a863c))

- Fixup names
  ([`9d6eff7`](https://github.com/bdraco/index-503/commit/9d6eff7034ebfcbd2c18d94006897f4335ca5b86))

- Fixup names
  ([`1b5f55f`](https://github.com/bdraco/index-503/commit/1b5f55fba255ada17b42dc72a6d00eeb40591698))

- Fixup names
  ([`53c4ed6`](https://github.com/bdraco/index-503/commit/53c4ed62de2d1363fc1bd6d684a7cde7e8ef3f31))

- Fixup names
  ([`b8d26f9`](https://github.com/bdraco/index-503/commit/b8d26f9f5d4968af05485eceb04bd31f625d5c0f))

- Fixup names
  ([`c2d0137`](https://github.com/bdraco/index-503/commit/c2d0137793a14980fea264c7d3cb9d641af52c1c))

- Index
  ([`13ccf7b`](https://github.com/bdraco/index-503/commit/13ccf7b9a84b154ad35708dd0d468323a6e31391))

- Readme
  ([`4c1f324`](https://github.com/bdraco/index-503/commit/4c1f324ceaec25b21b3273d0473fd488f2de1f84))

- Readme
  ([`7385204`](https://github.com/bdraco/index-503/commit/738520423add3f6ac4d6a0629f19f0ade3a0ab83))

- Split
  ([`cff4d3b`](https://github.com/bdraco/index-503/commit/cff4d3b9fddc111d2be0b6d292916197153d647e))

- Split
  ([`b76c109`](https://github.com/bdraco/index-503/commit/b76c109cf8ba18064fd836330a5854e695905736))

- Typing
  ([`3bc1549`](https://github.com/bdraco/index-503/commit/3bc154989cebecc5864ddeab52aefd2e5161cb95))

- Wip
  ([`7b3bca1`](https://github.com/bdraco/index-503/commit/7b3bca1e0652b21efaedaaa581ca03dbd4214e69))

- Wip
  ([`4235151`](https://github.com/bdraco/index-503/commit/4235151df36d737843d2761414249d2730709d85))

### Chores

- Initial commit
  ([`9ef105d`](https://github.com/bdraco/index-503/commit/9ef105d1e17287a22a0a7fd5d783bf1d66de45bb))

### Features

- Init
  ([`72de6e5`](https://github.com/bdraco/index-503/commit/72de6e5f34d292ec190374273e10283b83d0bfda))
