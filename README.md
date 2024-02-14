# SuiteAs

<!-- badges: start -->
[![License](https://img.shields.io/github/license/nathanjmcdougall/suiteas)](https://github.com/nathanjmcdougall/suiteas/blob/main/LICENSE.txt)
[![PyPI version](https://badge.fury.io/py/suiteas.svg)](https://badge.fury.io/py/suiteas)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linting: Ruff](https://img.shields.io/badge/linting-ruff-yellowgreen)](https://github.com/charliermarsh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nathanjmcdougall/suiteas/main.svg)](https://results.pre-commit.ci/latest/github/nathanjmcdougall/suiteas/main)
[![codecov](https://codecov.io/gh/nathanjmcdougall/suiteas/branch/develop/graph/badge.svg?token=OUHWT2NL8O)](https://codecov.io/gh/nathanjmcdougall/suiteas)
[![Downloads](https://static.pepy.tech/badge/suiteas)](https://pepy.tech/project/suiteas)
<!-- badges: end -->

An opinionated testing suite organizer and linter for pytest.

SuiteAs will automatically generate a skeletonized unit test suite based on the
structure of your project. Then, going forward, it will enforce matching names and folder structure between your testing suite and your project using linter rules.

For now, only linting is supported; automatic test suite generation will be added later.

> _Sweet As_
>
> INFORMAL • NEW ZEALAND
>
> _very satisfactory; excellent._

The recommended way to use SuiteAs is using the [`pre-commit`](https://pre-commit.com/) framework. Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/nathanjmcdougall/suiteas
    rev: v0.3.0
    hooks:
      - id: suiteas
```

You can also install and run SuiteAs as a standalone package:

```bash
pip install suiteas
python -m suiteas .
```

SuiteAs will try to automatically determine your project directory structure and
configuration, but you can manually configure SuiteAs in a `pyproject.toml` file.

For example, if your project looks like this:

<!-- created with tree.nathanfriend.io -->
```text
.
└── myrepo/
    ├── src/
    │   ├── mypkg/
    │   └── otherpkg/
    ├── tests/
    │   ├── unit/
    │   │   ├── mypkg/
    │   │   └── otherpkg/
    │   └── endtoend/
    └── pyproject.toml
```

Then you would add this section to `pyproject.toml`:

```TOML
[tool.suiteas]
pkg_names = ["mypkg", "otherpkg"]
src_rel_path = "src"
tests_rel_path = "tests"
unittest_dir_name = "unit"
ignore = ["SUI002"]
```

The final line will globally disable the linting of the SUI002 rule.

## Rules

SuiteAs will enforce the following rules:

| Rule | Description |
| ---- | ----------- |
| SUI001 | Function or class is missing a corresponding test function |
| SUI002 | Pytest test class is empty |
| SUI003 | Pytest file does not import the function being tested |

## Developer Information

### Package Management

This project uses [`rye`](https://rye-up.com/) to manage dependencies, virtual environments, and the python installation. Run `rye sync` from the project root to install the development environment.

### Hooks with `pre-commit`

This project uses [`pre-commit`](https://pre-commit.com/) to manage hooks. After installing the development environment, run `pre-commit install`.

### Signed Commits

This project requires signed commits. Please see [this guide from the VS Code project](https://github.com/microsoft/vscode/wiki/Commit-Signing) for instructions on how to configure this.

### Diagramming

This project uses [`D2Lang`](https://d2lang.com/) to develop and maintain design diagrams.

### Changelog

This project uses [`towncrier`](https://github.com/twisted/towncrier) to manage the changelog. Each PR should have at least one associated GitHub issue. Before the PR is merged, a changelog entry  should be created for any issues which are resolved by the PR. The changelog entry files are created in the `doc/changelog_entries` directory, with the filename following the convention `<github id>.<type>.rst` where `<github id>` is the GitHub issue ID number, and `<type>` is one of the types documented in the `pyproject.toml` file in the `[tool.towncrier.type]` sections.
