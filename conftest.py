# -*- coding: utf-8 -*-

# Load the CLU plugin for `pytest`:
pytest_plugins = "clu.testing.pytest"

# The same as passing “--delete-temporary”:
def pytest_delete_temporary_default():
    """ Delete all “$TMPDIR/pytest-of-$USER” files by default """
    return True