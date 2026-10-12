"""Not a package in any meaningful sense. The file exists so that mypy resolves
`extras/testbed/runner.py` as `extras.testbed.runner` instead of as `runner`:
without it the ignore_errors override for `extras.testbed.*` in pyproject.toml
never matches, and pre-commit, which hands mypy the staged file names, reports
the testbed scripts as if they were library code. `tests/` works for the same
reason."""
