# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import socket
import sys
import sysconfig

# Possible names for builtin modules:
BUILTINS = ('__builtins__', '__builtin__', 'builtins', 'builtin')

# Are we debuggin out?
DEBUG = bool(int(os.environ.get('DEBUG', '0'), base=10))

# A prefix to use when creating new modules programmatically:
DYNAMIC_MODULE_PREFIX = sys.intern('__dynamic_modules__')

# On non-macOS platforms this may be awry:
ENCODING = sys.intern(sys.getfilesystemencoding().upper()) # 'UTF-8'

# Possible names for file arguments (used for introspection):
FILE_ARGUMENT_NAMES = ('path', 'pth', 'file')

# The hostname for this computer:
HOSTNAME = socket.gethostname()

# The __name__ of a lambda function:
lam = lambda: None
LAMBDA = sys.intern(getattr(lam, '__qualname__',
                    getattr(lam, '__name__', None)))

# N.B. this may or may not be a PY2/PY3 thing:
MAXINT = getattr(sys, 'maxint',
         getattr(sys, 'maxsize', (2 ** 64) / 2))

# The PATH environment variable, with a sensible default:
PYTHON_BIN = os.path.join(sysconfig.get_path('data'), 'bin')
DEFAULT_PATH = ":".join(filter(os.path.exists, (PYTHON_BIN,
                                               "/usr/local/bin",
                                               "/bin",  "/usr/bin",
                                               "/sbin", "/usr/sbin")))
PATH = os.getenv("PATH", DEFAULT_PATH)

# The name of this project
PROJECT_NAME = sys.intern('clu')

# Determine if our Python is three’d up:
PY3 = sys.version_info.major > 2

# Determine if we’re on PyPy:
PYPY = hasattr(sys, 'pypy_version_info')

# Qualifier for qualified-name operations:
QUALIFIER = '.'

# List of Python’s built-in singleton types:
NoneType = type(None)
EllipsisType = type(Ellipsis)
NotImplementedType = type(NotImplemented)

SINGLETON_TYPES = (bool, NoneType, EllipsisType, NotImplementedType)

# Determine if we’re in TextMate:
TEXTMATE = 'TM_PYTHON' in os.environ

# For terminal-printing:
if TEXTMATE:
    SEPARATOR_WIDTH = 100
else:
    from .terminalsize import get_terminal_size
    SEPARATOR_WIDTH = get_terminal_size(default=(100, 25))[0]

# WTF HAX:
TOKEN = sys.intern(' -')

# Stuff we want to keep out of namespaces:
pytuple = lambda *attrs: tuple('__%s__' % str(atx) for atx in attrs)
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
    __slots__ = tuple()
    def __new__(cls, *a, **k):
        return cls


__all__ = ('BUILTINS',
           'DEBUG',
           'DYNAMIC_MODULE_PREFIX',
           'ENCODING',
           'FILE_ARGUMENT_NAMES',
           'HOSTNAME',
           'LAMBDA',
           'MAXINT',
           'PATH',
           'PROJECT_NAME',
           'PY3', 'PYPY',
           'QUALIFIER',
           'SEPARATOR_WIDTH',
           'SINGLETON_TYPES',
           'TEXTMATE',
           'TOKEN',
           'VERBOTEN',
           'XDG_RUNTIME_BASE', 'XDG_RUNTIME_DIR',
                               'XDG_RUNTIME_MODE',
           'NoDefault')

__dir__ = lambda: list(__all__)