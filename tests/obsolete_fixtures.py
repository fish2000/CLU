# -*- coding: utf-8 -*-
import os
import shutil

import pytest

@pytest.fixture
def shared_datadir(request, tmpdir):
    """ Vendored version of “shared_datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    from clu.fs.misc import win32_longpath
    
    # Get the shared data path:
    original_shared_path = os.path.join(request.fspath.dirname, 'data')
    
    # Prepare a temp_path pointing to a temporary data folder:
    temp_path = Path(str(tmpdir.join('data')))
    
    # Copy everything to the temp_path:
    shutil.copytree(win32_longpath(original_shared_path),
                    win32_longpath(str(temp_path)))
    
    # Return the temp_path:
    return temp_path

@pytest.fixture
def original_datadir(request):
    """ Vendored version of “original_datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    
    # Split the “.py” from the requesting modules’ file path,
    # and return a path instance based on that filesystem path prefix:
    return Path(os.path.splitext(request.module.__file__)[0])

@pytest.fixture
def copied_datadir(original_datadir, tmpdir):
    """ Vendored version of “datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    from clu.fs.misc import win32_longpath
    
    # Prepare a temporary path for return:
    temp_path = Path(str(tmpdir.join(original_datadir.stem)))
    
    # Copy data to the temporary path from the original datadir, if it exists;
    # If it doesn’t exist, just ensure that the new path has been created:
    if original_datadir.is_dir():
        shutil.copytree(win32_longpath(str(original_datadir)),
                        win32_longpath(str(temp_path)))
    else:
        temp_path.mkdir()
    
    # Return the temporary path:
    return temp_path
