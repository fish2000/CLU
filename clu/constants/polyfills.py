# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import Counter, OrderedDict
from enum import Enum, EnumMeta, unique, _is_dunder as ispyname
from functools import wraps

from clu.constants.consts import PY3, pytuple

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

class FakeNumpy(object):
    
    FAKE = True
    
    def get_include(self):
        return '.'

# Try to get `auto` from `enum`, falling back to the polyfill:
try:
    from enum import auto
except (ImportError, SyntaxError):
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
except (ImportError, SyntaxError):
    from collections import (Mapping, MutableMapping,
                             Hashable as HashableABC,
                             Sequence as SequenceABC,
                             Sized as SizedABC)

try:
    from importlib.util import cache_from_source
except (ImportError, SyntaxError):
    # As far as I can tell, this is what Python 2.x does:
    cache_from_source = lambda pth: f'{pth}c'

try:
    from functools import lru_cache
except (ImportError, SyntaxError):
    def lru_cache(**keywrds):
        """ No-op dummy decorator for lesser Pythons """
        def inside(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return inside

try:
    from pathlib import Path
except (ImportError, SyntaxError):
    try:
        from pathlib2 import Path
    except (ImportError, SyntaxError):
        Path = None

try:
    from scandir import scandir, walk
except ImportError:
    from os import scandir, walk

try:
    import numpy
except (ImportError, SyntaxError):
    numpy = None

try:
    from functools import reduce
except (ImportError, SyntaxError):
    pass

__all__ = ('Counter', 'OrderedDict',
           'Enum', 'EnumMeta', 'unique',
           'ispyname', 'pytuple',
           'AutoType', 'auto',
           'unicode', 'long',
           'Mapping', 'MutableMapping',
           'HashableABC', 'SequenceABC', 'SizedABC',
           'cache_from_source',
           'lru_cache',
           'Path', 'scandir', 'walk',
           'numpy',
           'reduce')

__dir__ = lambda: list(__all__)