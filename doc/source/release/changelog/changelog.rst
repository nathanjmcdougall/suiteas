0.3.3 (2024-04-25)
==================

Bug fixes
---------

- A bug has been fixed where UTF8 characters in Python files would give fatal errors.


0.3.2 (2024-04-25)
==================

Features
--------

- Better error messages are now provided for the situation where ``src_rel_path`` is set
  incorrectly and where as a result, SuiteAs is looking for unit tests for something which
  is not a package. (https://github.com/nathanjmcdougall/suiteas/issues/98)


0.3.1 (2024-03-03)
==================

Features
--------

- Added support for Python 3.10


0.3.0 (2024-01-18)
==================

Features
--------

- Global `ignore` configuration is now supported, allowing you to disable a linting rule
  completely across all files. (https://github.com/nathanjmcdougall/suiteas/issues/60)


Bug fixes
---------

- Provided full support for Python 3.12 syntax, namely for PEP 695 Type Aliasing. (https://github.com/nathanjmcdougall/suiteas/issues/40)


0.2.0 (2024-01-04)
==================

Features
--------

- Basic checking functionality has been implemented, comprising three rules. (https://github.com/nathanjmcdougall/suiteas/issues/30)


0.1.0 (2023-11-05)
==================

Features
--------

- The project has been initialized as a skeleton using `rye`. (https://github.com/nathanjmcdougall/suiteas/issues/3)
- Changelogs with `towncrier`` have been configured for this project. (https://github.com/nathanjmcdougall/suiteas/issues/4)
- The PyPI release process has been configured. (https://github.com/nathanjmcdougall/suiteas/issues/5)
- `pre-commit` has been configured for this project with basic hooks. (https://github.com/nathanjmcdougall/suiteas/issues/6)
