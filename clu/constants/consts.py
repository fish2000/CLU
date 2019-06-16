# -*- coding: utf-8 -*-
from __future__ import print_function

import sys, os

# Possible names for builtin modules:
BUILTINS = ('__builtins__', '__builtin__', 'builtins', 'builtin')

# Are we debuggin out?
DEBUG = bool(int(os.environ.get('DEBUG', '0'), base=10))

# On non-macOS platforms this may be awry:
ENCODING = sys.getfilesystemencoding().upper() # 'UTF-8'

# The __name__ of a lambda function:
lam = lambda: None
LAMBDA = getattr(lam, '__qualname__',
         getattr(lam, '__name__', None))

# N.B. this may or may not be a PY2/PY3 thing:
MAXINT = getattr(sys, 'maxint',
         getattr(sys, 'maxsize', (2 ** 64) / 2))

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
    from terminalsize import get_terminal_size
    SEPARATOR_WIDTH = get_terminal_size(default=(100, 25))[0]

# Stuff we want to keep out of namespaces:
pytuple = lambda *attrs: tuple('__%s__' % str(atx) for atx in attrs)
VERBOTEN = pytuple('all', 'cached', 'loader', 'file', 'spec')
VERBOTEN += BUILTINS
VERBOTEN += ('Namespace', 'SimpleNamespace')


class NoDefault(object):
    """ A singleton object to signify a lack of an argument. """
    __slots__ = tuple()
    def __new__(cls, *a, **k):
        return cls


__all__ = ('BUILTINS',
           'DEBUG',
           'ENCODING',
           'LAMBDA',
           'MAXINT',
           'PY3', 'PYPY',
           'QUALIFIER',
           'SEPARATOR_WIDTH',
           'SINGLETON_TYPES',
           'TEXTMATE',
           'VERBOTEN',
           'NoDefault')

__dir__ = lambda: list(__all__)