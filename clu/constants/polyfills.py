# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import Counter, OrderedDict
from enum import Enum, EnumMeta, unique, _is_dunder as ispyname

from .consts import PY3, pytuple

class AutoType(object):
    
    """ Simple polyfill for `enum.auto` (which apparently
        does not exist in PyPy 2 for some reason)
    """
    
    def __init__(self):
        self.count = 0
    
    def __call__(self, increment=1):
        out = int(self.count)
        self.count += increment
        return out

# Try to get `auto` from `enum`, falling back to the polyfill:
try:
    from enum import auto
except ImportError:
    auto = AutoType()

# Deal with some “missing” Python 3 things:
if PY3:
    unicode = str
    long = int

try:
    from collections.abc import (Mapping, MutableMapping,
                                 Hashable as HashableABC,
                                 Sequence as SequenceABC,
                                 Sized as SizedABC)
except ImportError:
    from collections import (Mapping, MutableMapping,
                             Hashable as HashableABC,
                             Sequence as SequenceABC,
                             Sized as SizedABC)

try:
    from importlib.util import cache_from_source
except ImportError:
    # As far as I can tell, this is what Python 2.x does:
    cache_from_source = lambda pth: pth + 'c'

try:
    from functools import lru_cache
except ImportError:
    def lru_cache(**keywrds):
        """ No-op dummy decorator for lesser Pythons """
        def inside(function):
            return function
        return inside

try:
    from pathlib import Path
except ImportError:
    try:
        from pathlib2 import Path
    except ImportError:
        Path = None
try:
    import numpy
except (ImportError, SyntaxError):
    numpy = None

__all__ = ('Counter', 'OrderedDict',
           'Enum', 'EnumMeta', 'unique',
           'ispyname', 'pytuple',
           'AutoType', 'auto',
           'unicode', 'long',
           'Mapping', 'MutableMapping',
           'HashableABC', 'SequenceABC', 'SizedABC',
           'cache_from_source',
           'lru_cache',
           'Path', 'numpy')

__dir__ = lambda: list(__all__)