# -*- encoding: utf-8 -*-
from __future__ import print_function

# from replutilities import test, thingname_search_by_id
# from replutilities import *
# from replenv import *
# import keyvalue

from clu.constants import (BASEPATH,
                           BUILTINS,
                           DEBUG,
                           DELETE_FLAG,
                           DYNAMIC_MODULE_PREFIX,
                           ENCODING,
                           FILE_ARGUMENT_NAMES,
                           HOSTNAME,
                           LAMBDA, λ,
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
                           NoDefault,
                           System, CSIDL, SYSTEM,
                           BadDotpathWarning,
                           CDBError,
                           ConfigurationError,
                           ExecutionError, FilesystemError,
                           ExportError, ExportWarning,
                           KeyValueError,
                           Enum, EnumMeta, unique,
                           ispyname, pytuple,
                           AutoType, auto,
                           Counter, OrderedDict,
                           unicode, long,
                           Mapping, MutableMapping,
                           HashableABC, SequenceABC, SizedABC,
                           cache_from_source,
                           lru_cache,
                           Path, scandir, walk,
                           get_terminal_size)

from clu.compilation import (Macro, Macros,
                             CDBSubBase, CDBBase, CDBJsonFile)

from clu.exporting import (doctrim,
                           thingname_search, determine_name, sysmods,
                           Exporter, exporter, export,
                           predicates_for_types)

from clu.sanitizer import sanitize, sanitizers, utf8_encode, utf8_decode
from clu.version import version_info

from clu.predicates import (negate,
                            ismetaclass, isclass, isclasstype,
                            noattr, haspyattr, nopyattr,
                            anyattrs, allattrs, noattrs,
                            anypyattrs, allpyattrs, nopyattrs,
                            haslength,
                            isiterable, ismergeable,
                            always, never, nuhuh,
                            no_op, or_none,
                            getpyattr, getitem,
                            accessor, searcher,
                            attr, pyattr, item,
                            attr_search, pyattr_search, item_search,
                            isenum, enumchoices,
                            isaliasdescriptor, hasmembers, hasaliases,
                            predicate_nop, function_nop, uncallable,
                            pyname,
                            isexpandable, isnormative, iscontainer,
                            lambda_repr,
                            apply_to,
                            predicate_all, predicate_any,
                            predicate_and, predicate_or, predicate_xor,
                            thing_has, class_has,
                            isslotted, isdictish, isslotdicty, slots_for,
                            case_sort,
                            tuplize, uniquify, listify,
                            allof, anyof, noneof)

from clu.typespace import SimpleNamespace, Namespace, types, modulize

from clu.typology import (isunique, istypelist, maketypelist,
                          isderivative, subclasscheck, graceful_issubclass,
                          numeric_types, array_types, string_types, bytes_types,
                          path_classes, path_types, file_types, callable_types,
                          ispathtype, ispath, isvalidpath,
                          isabstractmethod, isabstract, isabstractcontextmanager, iscontextmanager,
                          isnumber, isnumeric, iscomplex, isarray, isstring, isbytes, ismodule,
                          isfunction, islambda, ishashable, issequence,
                          isnumberlist, isnumericlist, iscomplexlist,
                          isarraylist, isstringlist, isbyteslist,
                          ismodulelist, isfunctionlist, islambdalist,
                          ishashablelist, issequencelist)

from clu.naming import (thingname, itermodule, moduleids, nameof,
                        determine_module,
                        path_to_dotpath,
                        dotpath_join, dotpath_split, qualified_import,
                                                     qualified_name_tuple,
                                                     qualified_name, split_abbreviations)

from clu.dicts import merge_two, merge_as, merge, asdict

# Add miscellaneous necessities:
from PIL import Image
from pprint import pprint, pformat
import sys, os, re
import argparse
import collections
import colorama
import contextlib
import copy
import datetime
import decimal
import functools
import inspect
import itertools
import math
import requests
import shutil
import six
import sysconfig
import termcolor
import xerox

from clu.mathematics import isdtype, Clamper, clamp
from clu import keyvalue

from clu.enums import (DUNDER, SUNDER,
                       alias, AliasingEnumMeta, AliasingEnum)

from clu.repl.ansi import (print_separator,
                           Text, Weight, Background, ANSIFormat,
                           print_ansi, print_ansi_centered, highlight)

from clu.repl.banners import print_banner

# Practice safe star-importing:
__all__ = ('Image',
           'pprint', 'pformat',
           'sys', 'os', 're',
           'appdirectories',
           'argparse',
           'collections',
           'colorama',
           'contextlib',
           'copy',
           'datetime',
           'decimal',
           'functools',
           'inspect',
           'itertools',
           'math',
           'reduce',
           'requests',
           'shutil',
           'six',
           'sysconfig',
           'termcolor',
           'types',
           'xerox',
           'print_banner',
           'isdtype', 'Clamper', 'clamp',
           'predicates_for_types',
           'version_info',
           'BASEPATH',
           'BUILTINS',
           'DEBUG',
           'DELETE_FLAG',
           'DYNAMIC_MODULE_PREFIX',
           'ENCODING',
           'FILE_ARGUMENT_NAMES',
           'HOSTNAME',
           'LAMBDA', 'λ',
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
           'BadDotpathWarning',
           'CDBError',
           'ConfigurationError',
           'ExecutionError', 'FilesystemError',
           'ExportError', 'ExportWarning',
           'KeyValueError',
           'Enum', 'EnumMeta', 'unique',
           'ispyname', 'pytuple',
           'AutoType', 'auto',
           'Counter', 'OrderedDict',
           'unicode', 'long',
           'Mapping', 'MutableMapping', 
           'HashableABC', 'SequenceABC', 'SizedABC',
           'cache_from_source',
           'lru_cache',
           'Path', 'scandir', 'walk',
           'get_terminal_size',
           'sanitize', 'sanitizers', 'utf8_encode', 'utf8_decode',
           'Macro', 'Macros',
           'CDBSubBase', 'CDBBase', 'CDBJsonFile',
           'doctrim', 'sysmods', 'thingname_search', 'determine_name',
           'Exporter', 'exporter', 'export',
           'predicates_for_types',
           'negate',
           'ismetaclass', 'isclass', 'isclasstype',
           'noattr', 'haspyattr', 'nopyattr',
           'anyattrs', 'allattrs', 'noattrs',
           'anypyattrs', 'allpyattrs', 'nopyattrs',
           'haslength',
           'isiterable', 'ismergeable',
           'always', 'never', 'nuhuh',
           'no_op', 'or_none',
           'getpyattr', 'getitem',
           'accessor', 'searcher',
           'attr', 'pyattr', 'item',
           'attr_search', 'pyattr_search', 'item_search',
           'isenum', 'enumchoices',
           'isaliasdescriptor', 'hasmembers', 'hasaliases',
           'predicate_nop', 'function_nop', 'uncallable',
           'pyname',
           'isexpandable', 'isnormative', 'iscontainer',
           'lambda_repr',
           'apply_to',
           'predicate_all', 'predicate_any',
           'predicate_and', 'predicate_or', 'predicate_xor',
           'thing_has', 'class_has',
           'isslotted', 'isdictish', 'isslotdicty', 'slots_for',
           'case_sort',
           'tuplize', 'uniquify', 'listify',
           'allof', 'anyof', 'noneof',
           'SimpleNamespace', 'Namespace', 'types', 'modulize',
           'isunique', 'istypelist', 'maketypelist',
           'isderivative', 'subclasscheck', 'graceful_issubclass',
           'numeric_types', 'array_types', 'string_types', 'bytes_types',
           'path_classes', 'path_types', 'file_types', 'callable_types',
           'ispathtype', 'ispath', 'isvalidpath',
           'isabstractmethod', 'isabstract', 'isabstractcontextmanager', 'iscontextmanager',
           'isnumber', 'isnumeric', 'iscomplex',
           'isarray', 'isstring', 'isbytes',
           'ismodule', 'isfunction', 'islambda',
           'ishashable', 'issequence',
           'isnumberlist', 'isnumericlist', 'iscomplexlist',
           'isarraylist', 'isstringlist', 'isbyteslist',
           'ismodulelist', 'isfunctionlist', 'islambdalist',
           'ishashablelist', 'issequencelist',
           'thingname', 'itermodule', 'moduleids', 'slots_for', 'nameof',
           'determine_module',
           'path_to_dotpath', 'dotpath_join', 'dotpath_split',
           'qualified_import', 'qualified_name_tuple', 'qualified_name', 'split_abbreviations',
           'merge_two', 'merge_as', 'merge', 'asdict',
           'DUNDER', 'SUNDER', 'alias', 'AliasingEnumMeta', 'AliasingEnum',
           'print_separator', 'Text', 'Weight', 'Background', 'ANSIFormat',
           'print_ansi', 'print_ansi_centered', 'highlight',
           'keyvalue')

try:
    from functools import reduce
except (ImportError, SyntaxError):
    pass

try:
    if PY3:
        from replpy3 import Σ
except (AttributeError, SyntaxError):
    pass
else:
    if PY3:
        __all__ += (u'Σ',)

try:
    import numpy
    import scipy
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('numpy', 'scipy')

try:
    import colorio
    import colormath
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('colorio', 'colormath')

try:
    import dateutil
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('dateutil',)

try:
    import abc
    import collections.abc as collectionsabc
    import asciiplotlib
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('abc', 'collectionsabc', 'asciiplotlib')

try:
    from clu.fs import appdirectories
    from clu.fs.pypath import append_paths, remove_paths
    from clu.fs.filesystem import (DEFAULT_PREFIX, DEFAULT_TIMEOUT,
                                   ensure_path_is_valid,
                                   script_path, which, back_tick,
                                   rm_rf, temporary,
                                   TemporaryName, Directory, cd, wd,
                                   TemporaryDirectory, Intermediate,
                                   NamedTemporaryFile)
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('appdirectories', 'append_paths', 'remove_paths',
                'DEFAULT_PREFIX', 'DEFAULT_TIMEOUT',
                'ensure_path_is_valid',
                'script_path', 'which', 'back_tick',
                'rm_rf', 'temporary',
                'TemporaryName', 'Directory', 'cd', 'wd',
                'TemporaryDirectory', 'Intermediate',
                'NamedTemporaryFile')

try:
    from instakit.utils.static import asset
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('asset', 'image_paths', 'catimage')
    # Prepare a list of readily open-able image file paths:
    image_paths = list(map(
        lambda image_file: asset.path('img', image_file),
            asset.listfiles('img')))
    # I do this practically every time, so I might as well do it here:
    catimage = Image.open(image_paths[0])

# `__dir__` listifies `__all__`:
__dir__ = lambda: list(__all__)
modules = tuple(__dir__())

# Remove duplicate sys.paths:
import site
site.removeduppaths()

# Print the Python banner and/or warnings, messages, and other tripe:
print_banner()

