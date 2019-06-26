# -*- coding: utf-8 -*-
from __future__ import print_function

from .consts import (BASEPATH,
                     BUILTINS,
                     DEBUG,
                     DELETE_FLAG,
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
                     XDG_RUNTIME_BASE, XDG_RUNTIME_DIR,
                                       XDG_RUNTIME_MODE,
                     NoDefault)

from .enums import System, CSIDL, SYSTEM

from .polyfills import (Enum, EnumMeta, unique, ispyname,
                        AutoType, auto,
                        Counter, OrderedDict,
                        unicode, long,
                        Mapping, MutableMapping, HashableABC,
                        cache_from_source,
                        lru_cache,
                        Path)

from .terminalsize import get_terminal_size

__all__ = ('BASEPATH',
           'BUILTINS',
           'DEBUG',
           'DELETE_FLAG',
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
           'NoDefault',
           'System', 'CSIDL', 'SYSTEM',
           'Enum', 'EnumMeta', 'unique', 'ispyname',
           'AutoType', 'auto',
           'Counter', 'OrderedDict',
           'unicode', 'long',
           'Mapping', 'MutableMapping', 'HashableABC',
           'cache_from_source',
           'lru_cache',
           'Path',
           'get_terminal_size')

__dir__ = lambda: list(__all__)