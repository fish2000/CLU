# -*- coding: utf-8 -*-
from __future__ import print_function

import getpass
import platform
import sysconfig
import sys, os, re

# Choose a “path” interim operator for path-type consts –
# trying “pathlib.Path”, “pathlib2.Path”, and falling
# back to string-interning with “sys.intern”:
try:
    from clu.constants.polyfills import Path as path
except (ImportError, SyntaxError): # pragma: no cover
    path = sys.intern
else:
    if not callable(path):  # pragma: no cover
        path = sys.intern

# Get VersionInfo from clu.version:
from clu.version import VersionInfo

# Define the “pytuple” shortcut lambda:
pytuple = lambda *attrs: tuple(f'__{atx}__' for atx in attrs)

# Appname (née PROJECT_NAME):
APPNAME = sys.intern('clu')

# Project base path:
BASEPATH = path(
           os.path.dirname(
           os.path.dirname(
           os.path.dirname(__file__))))

# Possible names for builtin modules:
builtins = ('builtins', 'builtin', 'main')
BUILTINS = pytuple(*builtins) + builtins

# q.v. STRINGPAIR sub.:
BYTEPAIR = b"{!s} : {!s}"

# Determine if we’re running in bpython:
BPYTHON = any('bpython' in key for key in sys.modules) # https://stackoverflow.com/a/42818291/298171

# Determine if we’re on CPython:
CPYTHON = platform.python_implementation().casefold() == 'cpython'

# Are we debuggin out?
DEBUG = bool(int(os.environ.get('DEBUG', '0') or '0', base=10))

# Flag for deleting temporary files:
DELETE_FLAG = getattr(os, 'O_TEMPORARY', 0)

# Default “appspace”, for class-based module imports:
DEFAULT_APPSPACE = sys.intern('app')

# Default terminal width:
default_terminal_width = '100'
DEFAULT_TERMINAL_WIDTH = int(os.environ.get('COLUMNS',
                             default_terminal_width) \
                          or default_terminal_width, base=10)

# Dollar-sign string (for use in regexing):
DOLLA = sys.intern('$')

# On non-macOS platforms this may be awry:
ENCODING = sys.intern(sys.getfilesystemencoding().upper()) # 'UTF-8'

# The environment-variable name partition separator:
ENVIRONS_SEP = sys.intern('_')

# The default exporter instance name:
EXPORTER_NAME = sys.intern('exporter')

# Possible names for file arguments (used for introspection):
FILE_ARGUMENT_NAMES = ('path', 'pth', 'file')

# The hostname for this computer:
nodename = platform.node().casefold()
HOSTNAME = sys.intern(os.extsep in nodename \
                               and nodename \
                             or f"{nodename}.local")

# Determine if we’re running in IPython:
try:
    __IPYTHON__
except NameError:
    IPYTHON = False
else: # pragma: no cover
    IPYTHON = True

# Determine if we’re on Jython (hint, not likely):
JYTHON = sys.platform.casefold().startswith('java')

# The __name__ of a lambda function:
lam = lambda: None # pragma: no cover
λ = LAMBDA = sys.intern(getattr(lam, '__qualname__',
                        getattr(lam, '__name__',
                                     "<lambda>")))

# N.B. this may or may not be a PY2/PY3 thing:
MAXINT = getattr(sys, 'maxint',
         getattr(sys, 'maxsize', (2 ** 64) / 2))

# The namespace separator for namespaced KeyMaps:
NAMESPACE_SEP = sys.intern(os.pathsep)

# A boolean value for “numpy” availability – False if it’s not present:
try:
    from clu.constants.polyfills import numpy
except (ImportError, SyntaxError): # pragma: no cover
    NUMPY = False
else:
    NUMPY = bool(numpy)

# The PATH environment variable, with a sensible default:
PYTHON_BIN = path(os.path.join(sysconfig.get_path('data'), 'bin'))
DEFAULT_PATH = os.pathsep.join(filter(os.path.exists, (os.fspath(PYTHON_BIN),
                                                       "/usr/local/bin",
                                                       "/bin",  "/usr/bin",
                                                       "/sbin", "/usr/sbin"))) # type: ignore
PATH = os.getenv("PATH", DEFAULT_PATH)

φ = PARTIAL = sys.intern("<Partial>")

# The name of this project
PROJECT_NAME = APPNAME

# Path to the projects’ root package directory:
PROJECT_PATH = path(os.path.join(BASEPATH, APPNAME))

# Determine if our Python is three’d up:
PY3 = sys.version_info.major > 2

# Determine if we’re on PyPy:
PYPY = hasattr(sys, 'pypy_version_info')

# The current Python major/minor version:
PYTHON_VERSION = VersionInfo("%s%s%s" % (sys.version_info.major, os.extsep,
                                         sys.version_info.minor))

# Qualifier for qualified-name operations:
QUALIFIER = sys.intern(os.extsep)

# Delimiter for repr-strings indicating instance IDs:
REPR_DELIMITER = sys.intern('@')

try:
    # Determine the root path for the current filesystem:
    ROOT_PATH = sys.intern(path(BASEPATH).absolute().root)
except (AttributeError, SyntaxError): # pragma: no cover
    # Fall back to the Unix default
    ROOT_PATH = sys.intern('/')

# List of Python’s built-in singleton types:
NoneType = type(None)
EllipsisType = type(Ellipsis)
NotImplementedType = type(NotImplemented)

SINGLETON_TYPES = (bool, NoneType, EllipsisType, NotImplementedType)

# String used in custom repr implementations:
STRINGPAIR = sys.intern("{!s} : {!s}")

# Path to the script directory:
SCRIPT_PATH = path(os.path.join(BASEPATH, APPNAME, 'scripts'))

# Path to the project tests:
TEST_PATH = path(os.path.join(BASEPATH, 'tests'))

# Determine if we’re in TextMate:
TEXTMATE = 'TM_PYTHON' in os.environ

# For terminal pretty-printing:
if TEXTMATE: # pragma: no cover
    SEPARATOR_WIDTH = DEFAULT_TERMINAL_WIDTH

else:
    def terminal_width(fallback=DEFAULT_TERMINAL_WIDTH):
        """ Wrapper for “os.get_terminal_size(…)” """
        # q.v. http://bit.ly/py-term-size sub.
        for idx in range(0, 3): # stdin, stdout, stderr
            try:
                columns = os.get_terminal_size(idx)[0]
            except OSError:
                continue
            break
        else:
            columns = fallback
        return columns
    
    try:
        SEPARATOR_WIDTH = terminal_width()
    
    except IOError: # pragma: no cover
        SEPARATOR_WIDTH = DEFAULT_TERMINAL_WIDTH

# WTF HAX:
TOKEN = sys.intern(' -')

# Username:
USER = sys.intern(getpass.getuser())

# Stuff we want to keep out of namespaces:
VERBOTEN = pytuple('all', 'cached', 'loader', 'file', 'spec')
VERBOTEN += BUILTINS
VERBOTEN += ('Namespace', 'SimpleNamespace')

# Regex for picking up whitespace:
WHITESPACE = re.compile(r'\s+')

class MetaNoDefault(type):
    """ A metaclasss to make a type Falsey. """
    def __bool__(cls):
        return False
    
    def __repr__(cls):
        return 'NoDefault'

class NoDefault(metaclass=MetaNoDefault):
    """ A singleton object to signify a lack of an argument. """
    __slots__ = tuple() # type: tuple
    
    def __new__(cls, *args, **kwargs): # pragma: no cover
        return cls
    
    def __bool__(self):
        return False
    
    def __repr__(self):
        return 'NoDefault'

# Manually rename `pytuple(…)` per mechanism of “clu.exporting.Exporter”:
pytuple.__lambda_name__ = λ # type: ignore
pytuple.__qualname__ = pytuple.__name__ = 'pytuple'
pytuple.__doc__ = "pytuple(*attrs) → turns ('do', 're', 'mi') into ('__do__', '__re__', '__mi__')"

__all__ = ('APPNAME',
           'BASEPATH',
           'BUILTINS',
           'BYTEPAIR',
           'BPYTHON',
           'CPYTHON',
           'DEBUG',
           'DELETE_FLAG',
           'DEFAULT_APPSPACE',
           'DEFAULT_PATH',
           'DEFAULT_TERMINAL_WIDTH',
           'DOLLA',
           'ENCODING',
           'ENVIRONS_SEP',
           'EXPORTER_NAME',
           'FILE_ARGUMENT_NAMES',
           'HOSTNAME',
           'IPYTHON',
           'JYTHON',
           'LAMBDA',
           'MAXINT',
           'NUMPY',
           'NAMESPACE_SEP',
           'PATH',
           'PARTIAL',
           'PROJECT_NAME', 'PROJECT_PATH',
           'PY3', 'PYPY',
           'PYTHON_BIN',
           'PYTHON_VERSION',
           'QUALIFIER',
           'REPR_DELIMITER',
           'ROOT_PATH',
           'SEPARATOR_WIDTH',
           'SINGLETON_TYPES',
           'STRINGPAIR',
           'SCRIPT_PATH', 'TEST_PATH',
           'TEXTMATE',
           'TOKEN',
           'USER',
           'VERBOTEN',
           'WHITESPACE',
           'φ', 'λ',
           'NoDefault',
           'pytuple')

__dir__ = lambda: list(__all__)

def print_all():
    """ Print out all of the constant variables defined in consts.py """
    # It’s not pretty – but actually it’s almost pretty, sort-of.
    WIDTH = TEXTMATE and max(SEPARATOR_WIDTH, 100) or SEPARATOR_WIDTH
    
    print('*' * WIDTH)
    print(f"≠≠≠ CONSTS: (total {len(__all__)} defined)")
    print('*' * WIDTH)
    
    G = globals()
    SEP = ",\n" + (" " * 30)
    
    printout = lambda name, value: print("» %25s : %s" % (name, value))
    lowers   = lambda string: sum(1 for c in string if c.islower())
    
    for const_name in sorted(__all__, key=lowers):
        if const_name.endswith('PATH') and os.pathsep in str(G[const_name]):
            printout(const_name, str(G[const_name]).replace(os.pathsep, SEP))
        elif type(G[const_name]) is tuple:
            printout(const_name, SEP.join(f"“{g!s}”" for g in G[const_name]))
        elif type(G[const_name]) is str:
            printout(const_name, f"“{G[const_name]}”")
        elif type(G[const_name]) is bytes:
            value = str(G[const_name], encoding=ENCODING)
            printout(const_name, f"b“{value}”")
        else:
            printout(const_name, G[const_name])
    
    print('*' * WIDTH)

if __name__ == '__main__':
    print_all()