# -*- coding: utf-8 -*-

# Load the “pytester” built-in pytest plugin:
pytest_plugins = 'pytester'

# Import the main pytest API entry point:
import pytest

# enum.IntEnum of pytest’s exit status codes:
from _pytest.main import ExitCode

# when not to bind the exit handler:
no_delete_codes = (ExitCode.INTERNAL_ERROR,
                   ExitCode.USAGE_ERROR,
                   ExitCode.NO_TESTS_COLLECTED)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """ Hook function to bind an exit handle – using “clu.dispatch”
        via the ‘@exithandle’ decorator – that removes any remaining
        temporary-file artifacts that may be hanging out in the
        putative directory “$TMPDIR/pytest-of-$USER”.
        
        The exit handle function executes when the Python interpreter
        either enters shutdown (via the “atexit” module) or receives
        a terminating signal (via the “signal” module).
    """
    from clu.constants import consts
    from clu.dispatch import exithandle
    from clu.fs.filesystem import td, rm_rf
    
    # putative temporary directory:
    putative = td().subdirectory(f"pytest-of-{consts.USER}")
    
    # check the exit status:
    if exitstatus not in no_delete_codes:
        # bind a remover function if the exit status is “natural” –
        # i.e. no internal errors and tests ran normally (this can
        # include occasions when tests fail):
        @exithandle
        def remover(signum, frame=None):
            """ Exit handler for removing ‘pytest’ artifacts """
            if putative.exists:
                print()
                print(f"REMOVING: {putative.name}")
                rm_rf(putative.name)

@pytest.fixture(scope='session')
def consts():
    """ Fixture providing access to the CLU constants module, which
        you may know as “clu.constants.consts”
    """
    from clu.constants import consts as consts_module
    yield consts_module

@pytest.fixture(scope='session')
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

@pytest.fixture(scope='package')
def clumods(consts):
    """ Import all CLU modules that use the “clu.exporting.Exporter”
        mechanism for listing and exporting their module contents
    """
    from clu.all import import_all_modules
    modules = import_all_modules(basepath=consts.BASEPATH,
                                  appname=consts.PROJECT_NAME)
    yield modules

@pytest.fixture(scope='package')
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
    dirname = Directory(resolve(request, 'fspath.dirname'))
    
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
        using clu.fs.filesystem classes – ensuring that the temporary
        directory will be deleted immediately after use – and performing
        its copy operations through instance methods (vs. the raw calls
        to “shutil.copytree(…)” made by “datadir”).
    """
    from clu.fs.filesystem import TemporaryDirectory
    from clu.naming import moduleof, dotpath_join, dotpath_to_prefix
    
    # Get the test-local (née “shared”) data path:
    datadir = dirname.subdirectory('data')
    
    # Ensure source data directory exists:
    assert datadir.exists
    
    prefix = dotpath_to_prefix(
             dotpath_join(
             moduleof(TemporaryDirectory), 'ttd', 'datadir'))
    
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
        # Assert that we exist:
        assert temporarydir.exists
        
        # Yield the temporary directory:
        yield temporarydir
    
    # Assert that we no longer exist after scope exit:
    assert not temporarydir.exists

@pytest.fixture(scope='module')
def temporaryname():
    """ clu.fs.filesystem.TemporaryName fixture-factory function: yields
        a function returning new instances of `TemporaryName`, which
        can be called multiple times – each time producing a new
        `TemporaryName` instance under automatic context-management
        (via a behind-the-scenes “contextlib.ExitStack” instance).
        
        The parent fixture is module-scoped; when the module in which
        this fixture-factory function was first invoked enters cleanup,
        the ExitStack is unwound and all `TemporaryName` instances are
        __exit__(…)-ed at that time.
    """
    from clu.fs.filesystem import TemporaryName
    from clu.naming import qualified_name, dotpath_to_prefix
    from contextlib import ExitStack
    
    prefix = dotpath_to_prefix(
             qualified_name(TemporaryName))
    
    # Enter a master-context stack:
    with ExitStack() as names:
        
        # Declare the fixture-factory function:
        def temporaryname_factory(suffix, prefix=prefix,
                                          parent=None):
            """ The TemporaryName clu.testing fixture-factory function """
            # Enter the new TemporaryName instances’ context,
            # and return that instance:
            return names.enter_context(TemporaryName(prefix=prefix,
                                                     suffix=suffix,
                                                     parent=parent,
                                                 randomized=True))
        
        # Yield the TemporaryName fixture-factory function:
        yield temporaryname_factory

@pytest.fixture
def environment():
    """ Environment testing fixture: yields an instance of `os.environ`,
        free of XDG variables
        
        Q.v. implementation https://git.io/JeYmf supra.
    """
    from clu.constants.data import XDGS
    import os
    
    # Setup: stash environment mapping:
    stash = os.environ.copy()
    
    # Setup: remove XDG variables from environment:
    for key in XDGS:
        if key in os.environ:
            del os.environ[key]
    
    # Yield the mapping:
    yield os.environ
    
    # Teardown: restore environment mapping wholesale:
    os.environ = stash
