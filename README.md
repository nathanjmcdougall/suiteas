# SuiteAs

An opinionated testing suite organizer for pytest.

SuiteAs will automatically generate a skeletonized unit test suite based on the
structure of your project. Then, going forward, it will enforce matching names and folder structure between your testing suite and your project.

> _Sweet As_
>
> INFORMAL • NEW ZEALAND
>
> _very satisfactory; excellent._

The recommended way to use SuiteAs is using the [`pre-commit`](https://pre-commit.com/) framework. Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/nathanjmcdougall/suiteas
    rev: v0.2.0
    hooks:
      - id: suiteas
```

You can also install and run SuiteAs as a standalone package:

```bash
pip install suiteas
python -m suiteas .
```

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
