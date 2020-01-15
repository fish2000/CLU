# -*- coding: utf-8 -*-

# Load the CLU plugin for `pytest`:
pytest_plugins = "clu.testing.pytest"

# Directories to exclude (using “norecursedirs”):
excludes = ('.git', '.svn', '.hg', '.tox', 'CVS',
            '*.egg', '*.egg-info',
            '*.',
            'build', 'bdist', 'dist', 'sdist',
            'venv', 'develop')

import pytest

# The same as passing “--delete-temporary”:
@pytest.hookimpl(tryfirst=True)
def pytest_delete_temporary_default():
    """ Delete all “$TMPDIR/pytest-of-$USER” files by default """
    return True

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ Add the configuration options for CLU’s test suite """
    config.addinivalue_line('testpaths',        "tests")
    config.addinivalue_line('norecursedirs',    " ".join(excludes))
