# -*- coding: utf-8 -*-

# Load the CLU plugin for `pytest`:
pytest_plugins = "clu.testing.pytest"

# Directories to exclude (using “norecursedirs”):
excludes = ('.git', '.svn', '.hg', '.nox', '.tox', 'CVS',
            '*.egg', '*.egg-info',
            '__pycache__',
            '.pytest_cache',
            'build', 'bdist', 'dist', 'sdist',
            'venv', 'develop')

import pytest

'''
@pytest.hookimpl(tryfirst=True)
def pytest_delete_temps_default():
    """ Delete all “$TMPDIR/pytest-of-$USER” files by default """
    # Defining this function is the same as always passing the
    # option “--delete-temps” when running pytest:
    return True
'''

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ Add the configuration options for CLU’s test suite """
    config.addinivalue_line('testpaths',        "tests")
    config.addinivalue_line('norecursedirs',    " ".join(excludes))