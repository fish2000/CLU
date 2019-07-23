# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def environment():
    """ Environment testing fixture: yields an instance of `os.environ`,
        free of XDG variables
    """
    from clu.constants.data import XDGS
    import os
    stash = {}
    
    # Setup: remove XDG variables from environment:
    for key in XDGS:
        if key in os.environ:
            stash[key] = os.environ.get(key)
            del os.environ[key]
    
    yield os.environ
    
    # Teardown: restore environment:
    for key, value in stash.items():
        os.environ[key] = value

@pytest.fixture
def temporarydir():
    """ clu.fs.filesystem.TemporaryDirectory fixture factory: yields
        a new instance of `TemporaryDirectory`, without making any
        calls to “os.chdir()”.
    """
    from clu.fs.filesystem import TemporaryDirectory
    from clu.naming import qualified_name, dotpath_to_prefix
    
    prefix = dotpath_to_prefix(
             qualified_name(TemporaryDirectory))
    
    with TemporaryDirectory(prefix=prefix,
                            change=False) as temporarydir:
        yield temporarydir
    
    assert not temporarydir.exists

@pytest.fixture(scope="module")
def clumods():
    """ Import all CLU modules that use the “clu.exporting.Exporter”
        mechanism for listing and exporting their module contents
    """
    from clu.constants.data import MODNAMES
    import importlib
    mods = []
    
    for modname in MODNAMES:
        mods.append(importlib.import_module(modname))
    
    modules = dict(zip(MODNAMES, mods))
    
    yield modules

@pytest.fixture(scope="package")
def greektext():
    """ Greek-text fixture: yield a dictionary with several lorem-ipsum-ish
        blocks of text.
        
        Keys to the available texts are:
        
            • “lorem”   (the classic),
            • “faust”   (lots of Germanic short capitalized words),
            • “thoreau” (in actual English), and
            • “poe”     (exerpted from The Raven, because I live in Baltimore)
        
        … All these came straight from the output of the top-notch `lorem` CLT:
            https://github.com/per9000/lorem
    """
    from clu.constants.data import GREEKOUT
    yield dict(GREEKOUT)

@pytest.fixture(scope="package")
def dirname(request):
    """ Fixture for wrapping up the “request.fspath.dirname” value in a
        clu.fs.filesystem.Directory instance – this is intended to be a
        read-only value (no way to enforce that just now) so we only run
        it once per test package (which really there is one test package,
        total, so you see what we’re going for here doggie).
    """
    from clu.fs.filesystem import Directory
    from clu.predicates import resolve
    
    # Get the test-local (née “shared”) data path:
    dirname = Directory(pth=resolve(request, 'fspath.dirname'))
    
    # Ensure it exists:
    assert dirname.exists
    
    # Yield the Directory instance – N.B. do *NOT* manage this
    # objects’ context, unless you hold the specific desire of
    # changing the process working directory to what is specified
    # in the the context-managed instance… That’s what they do,
    # doggie, by default:
    yield dirname
    
    # Ensure it continues to exist:
    assert dirname.exists

@pytest.fixture
def datadir(dirname):
    """ Local version of pytest-datadir’s “datadir” fixture, reimplemented
        using clu.fs.filesystem classes – ensuring that the temporary directory
        will be deleted immediately after use – and performing the directory-copy
        operations through instance methods (vs. raw calls to “shutil.copytree(…)”).
    """
    from clu.fs.filesystem import TemporaryDirectory
    from clu.naming import determine_module, dotpath_join, dotpath_to_prefix
    
    # Get the test-local (née “shared”) data path:
    datadir = dirname.subdirectory('data')
    
    # Ensure source data directory exists:
    assert datadir.exists
    
    prefix = dotpath_to_prefix(
             dotpath_join(
             determine_module(TemporaryDirectory), 'ttd', 'datadir'))
    
    with TemporaryDirectory(prefix=prefix,
                            change=False) as temporarydir:
        # Assert that we exist:
        assert temporarydir.exists
        
        # Copy files to the 'data' temporary subdirectory:
        destination = temporarydir.subdirectory('data')
        assert datadir.copy_all(destination=destination)
        
        # Yield the 'data' temporary subdirectory,
        # prior to scope exit:
        yield destination
    
    # Assert that we no longer exist after scope exit:
    assert not temporarydir.exists
