# -*- coding: utf-8 -*-
from __future__ import print_function

import getpass
import os
import socket
import sysconfig
import sys

# pytuple shortcut lambda:
pytuple = lambda *attrs: tuple(f'__{atx}__' for atx in attrs)

# Project base path:
BASEPATH = sys.intern(
           os.path.dirname(
           os.path.dirname(
           os.path.dirname(__file__))))

# Possible names for builtin modules:
builtins = ('builtins', 'builtin')
BUILTINS = pytuple(*builtins) + builtins

# Are we debuggin out?
DEBUG = bool(int(os.environ.get('DEBUG', '0'), base=10))

# Flag for deleting temporary files:
DELETE_FLAG = getattr(os, 'O_TEMPORARY', 0)

# Default terminal width:
DEFAULT_TERMINAL_WIDTH = int(os.environ.get('COLUMNS', '100'), base=10)

# A prefix to use when creating new modules programmatically:
DYNAMIC_MODULE_PREFIX = sys.intern('__dynamic_modules__')

# On non-macOS platforms this may be awry:
ENCODING = sys.intern(sys.getfilesystemencoding().upper()) # 'UTF-8'

# Possible names for file arguments (used for introspection):
FILE_ARGUMENT_NAMES = ('path', 'pth', 'file')

# The hostname for this computer:
HOSTNAME = sys.intern(socket.gethostname())

# The __name__ of a lambda function:
lam = lambda: None
λ = LAMBDA = sys.intern(getattr(lam, '__qualname__',
                        getattr(lam, '__name__',
                                     "<lambda>")))

# N.B. this may or may not be a PY2/PY3 thing:
MAXINT = getattr(sys, 'maxint',
         getattr(sys, 'maxsize', (2 ** 64) / 2))

# The PATH environment variable, with a sensible default:
PYTHON_BIN = os.path.join(sysconfig.get_path('data'), 'bin')
DEFAULT_PATH = os.pathsep.join(filter(os.path.exists, (PYTHON_BIN,
                                                       "/usr/local/bin",
                                                       "/bin",  "/usr/bin",
                                                       "/sbin", "/usr/sbin"))) # type: ignore
PATH = os.getenv("PATH", DEFAULT_PATH)

φ = PARTIAL = sys.intern("<Partial>")

# The name of this project
PROJECT_NAME = sys.intern('clu')

# Path to the projects’ root package directory:
PROJECT_PATH = sys.intern(os.path.join(BASEPATH, PROJECT_NAME))

# Determine if our Python is three’d up:
PY3 = sys.version_info.major > 2

# Determine if we’re on PyPy:
PYPY = hasattr(sys, 'pypy_version_info')

# A float representation of the Python version:
PYTHON_VERSION = float("%s%s%s" % (sys.version_info.major, os.extsep,
                                   sys.version_info.minor))

# Qualifier for qualified-name operations:
QUALIFIER = sys.intern(os.extsep)

# List of Python’s built-in singleton types:
NoneType = type(None)
EllipsisType = type(Ellipsis)
NotImplementedType = type(NotImplemented)

SINGLETON_TYPES = (bool, NoneType, EllipsisType, NotImplementedType)

# Path to the script directory:
SCRIPT_PATH = sys.intern(os.path.join(BASEPATH, 'clu', 'scripts'))

# Path to the project tests:
TEST_PATH = sys.intern(os.path.join(BASEPATH, 'tests'))

# Determine if we’re in TextMate:
TEXTMATE = 'TM_PYTHON' in os.environ

# For terminal-printing:
if TEXTMATE:
    SEPARATOR_WIDTH = DEFAULT_TERMINAL_WIDTH
else:
    try:
        SEPARATOR_WIDTH = os.get_terminal_size()[0]
    except (IOError, OSError):
        SEPARATOR_WIDTH = DEFAULT_TERMINAL_WIDTH

# WTF HAX:
TOKEN = sys.intern(' -')

# Username:
USER = sys.intern(getpass.getuser())

# Stuff we want to keep out of namespaces:
VERBOTEN = pytuple('all', 'cached', 'loader', 'file', 'spec')
VERBOTEN += BUILTINS
VERBOTEN += ('Namespace', 'SimpleNamespace')

# XDG_RUNTIME_DIR support:
basedir = "/usr/local/var/run/xdg"
symlink = os.path.join(basedir, 'CURRENT')

XDG_RUNTIME_BASE = basedir
XDG_RUNTIME_DIR = symlink
XDG_RUNTIME_MODE = 0o700

class NoDefault(object):
    """ A singleton object to signify a lack of an argument. """
    __slots__ = tuple() # type: tuple
    def __new__(cls, *a, **k):
        return cls

# Manually rename `pytuple(…)` per mechanism of “clu.exporting.Exporter”:
pytuple.__lambda_name__ = λ # type: ignore
pytuple.__qualname__ = pytuple.__name__ = 'pytuple'
pytuple.__doc__ = "pytuple(*attrs) → turns ('do', 're', 'mi') into ('__do__', '__re__', '__mi__')"

__all__ = ('BASEPATH',
           'BUILTINS',
           'DEBUG',
           'DELETE_FLAG',
           'DEFAULT_TERMINAL_WIDTH',
           'DYNAMIC_MODULE_PREFIX',
           'ENCODING',
           'FILE_ARGUMENT_NAMES',
           'HOSTNAME',
           'LAMBDA', 'λ',
           'MAXINT',
           'PATH',
           'PARTIAL', 'φ',
           'PROJECT_NAME', 'PROJECT_PATH',
           'PY3', 'PYPY',
           'PYTHON_VERSION',
           'QUALIFIER',
           'SEPARATOR_WIDTH',
           'SINGLETON_TYPES',
           'SCRIPT_PATH', 'TEST_PATH',
           'TEXTMATE',
           'TOKEN',
           'USER',
           'VERBOTEN',
           'XDG_RUNTIME_BASE', 'XDG_RUNTIME_DIR',
                               'XDG_RUNTIME_MODE',
           'pytuple', 'NoDefault')

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
    
    for const_name in __all__:
        if const_name.endswith('PATH') and os.pathsep in G[const_name]:
            printout(const_name, G[const_name].replace(os.pathsep, SEP))
        elif type(G[const_name]) is tuple:
            printout(const_name, SEP.join(f"“{g!s}”" for g in G[const_name]))
        elif type(G[const_name]) is str:
            printout(const_name, f"“{G[const_name]}”")
        else:
            printout(const_name, G[const_name])
    
    print('*' * WIDTH)

if __name__ == '__main__':
    print_all()