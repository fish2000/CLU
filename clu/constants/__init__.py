# -*- coding: utf-8 -*-
from __future__ import print_function

from .consts import (BUILTINS,
                    DEBUG,
                    ENCODING,
                    LAMBDA,
                    MAXINT,
                    PY3, PYPY,
                    QUALIFIER,
                    SEPARATOR_WIDTH,
                    SINGLETON_TYPES,
                    TEXTMATE,
                    VERBOTEN,
                    NoDefault)

from .polyfills import (Counter, OrderedDict,
                       Enum, unique, ispyname,
                       AutoType, auto,
                       unicode, long,
                       Mapping, MutableMapping, HashableABC,
                       cache_from_source,
                       lru_cache,
                       Path)

from .terminalsize import get_terminal_size

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
           'NoDefault',
           'Counter', 'OrderedDict',
           'Enum', 'unique', 'ispyname',
           'AutoType', 'auto',
           'unicode', 'long',
           'Mapping', 'MutableMapping', 'HashableABC',
           'cache_from_source',
           'lru_cache',
           'Path',
           'get_terminal_size')

__dir__ = lambda: list(__all__)