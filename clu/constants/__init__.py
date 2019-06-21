# -*- coding: utf-8 -*-
from __future__ import print_function

from .consts import (BUILTINS,
                     DEBUG,
                     DYNAMIC_MODULE_PREFIX,
                     ENCODING,
                     FILE_ARGUMENT_NAMES,
                     HOSTNAME,
                     LAMBDA,
                     MAXINT,
                     PATH,
                     PROJECT_NAME,
                     PY3, PYPY,
                     QUALIFIER,
                     SEPARATOR_WIDTH,
                     SINGLETON_TYPES,
                     TEXTMATE,
                     TOKEN,
                     VERBOTEN,
                     NoDefault)

from .polyfills import (Counter, OrderedDict,
                       Enum, EnumMeta, unique, ispyname,
                       AutoType, auto,
                       unicode, long,
                       Mapping, MutableMapping, HashableABC,
                       cache_from_source,
                       lru_cache,
                       Path)

from .terminalsize import get_terminal_size

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
           'NoDefault',
           'Counter', 'OrderedDict',
           'Enum', 'EnumMeta', 'unique', 'ispyname',
           'AutoType', 'auto',
           'unicode', 'long',
           'Mapping', 'MutableMapping', 'HashableABC',
           'cache_from_source',
           'lru_cache',
           'Path',
           'get_terminal_size')

__dir__ = lambda: list(__all__)