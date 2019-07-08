# -*- coding: utf-8 -*-
# pytest_plugins = ['pytest_osxnotify']

import pytest

XDGS = ('XDG_CONFIG_DIRS', 'XDG_DATA_HOME',
        'XDG_CONFIG_HOME', 'XDG_DATA_DIRS',
                          'XDG_CACHE_HOME',
                          'XDG_STATE_HOME',
                         'XDG_RUNTIME_DIR')

@pytest.fixture
def environment(keys=XDGS):
    """ Environment testing fixture: yields an instance of `os.environ`,
        free of XDG variables
    """
    import os
    stash = {}
    
    # Setup: remove XDG variables from environment:
    for key in keys:
        if key in os.environ:
            stash[key] = os.environ.get(key)
            del os.environ[key]
    
    yield os.environ
    
    # Teardown: restore environment:
    for key, value in stash.items():
        os.environ[key] = value

