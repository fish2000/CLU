# -*- encoding: utf-8 -*-
from __future__ import print_function

from clu.constants.consts import (BASEPATH,
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
                                  PROJECT_NAME, PROJECT_PATH,
                                  PY3, PYPY,
                                  QUALIFIER,
                                  SEPARATOR_WIDTH,
                                  SINGLETON_TYPES,
                                  SCRIPT_PATH, TEST_PATH,
                                  TEXTMATE,
                                  TOKEN,
                                  VERBOTEN,
                                  XDG_RUNTIME_BASE, XDG_RUNTIME_DIR,
                                                    XDG_RUNTIME_MODE,
                                  NoDefault, pytuple)

from clu.constants.data import GREEKOUT
from clu.constants.enums import (System, CSIDL, SYSTEM)

from clu.constants.exceptions import (BadDotpathWarning,
                                      CDBError,
                                      ConfigurationError,
                                      ExecutionError, FilesystemError,
                                      ExportError, ExportWarning,
                                      KeyValueError)

from clu.constants.polyfills import (Enum, EnumMeta, unique,
                                     ispyname,
                                     AutoType, auto,
                                     Counter, OrderedDict,
                                     unicode, long,
                                     Mapping, MutableMapping,
                                     HashableABC, SequenceABC, SizedABC,
                                     cache_from_source,
                                     lru_cache,
                                     Path, scandir, walk,
                                     reduce)

from clu.constants.terminalsize import get_terminal_size
from clu.compilation import (Macro, Macros,
                             CDBSubBase, CDBBase, CDBJsonFile)

from clu.exporting import (doctrim,
                           thingname_search, determine_name, sysmods,
                           Exporter, path_to_dotpath,
                                     predicates_for_types)

from clu.sanitizer import sanitize, sanitizers, utf8_encode, utf8_decode
from clu.version import version_info

from clu.predicates import (negate,
                            ismetaclass, isclass, isclasstype, metaclass,
                            noattr, haspyattr, nopyattr,
                            anyattrs, allattrs, noattrs,
                            anypyattrs, allpyattrs, nopyattrs,
                            haslength,
                            isiterable, ismergeable,
                            always, never, nuhuh,
                            no_op, or_none, resolve,
                            getpyattr, getitem,
                            accessor, collator, searcher,
                            attr, pyattr, item,
                            attrs, pyattrs, items,
                            attr_search, pyattr_search, item_search,
                            isenum, enumchoices,
                            isaliasdescriptor, hasmembers, hasaliases,
                            predicate_nop, function_nop, uncallable,
                            pyname,
                            isexpandable, isnormative, iscontainer,
                            lambda_repr,
                            apply_to,
                            predicate_all, predicate_any, predicate_none,
                            predicate_and, predicate_or, predicate_xor,
                            thing_has, class_has,
                            isslotted, isdictish, isslotdicty, slots_for,
                            case_sort,
                            tuplize, uniquify, listify,
                            allof, anyof, noneof)

from clu.typespace import SimpleNamespace, Namespace, types, modulize

from clu.typology import (samelength, differentlength, isunique, istypelist, maketypelist,
                          isderivative, subclasscheck, graceful_issubclass,
                          numeric_types, array_types, scalar_types, string_types, bytes_types,
                          path_classes, path_types, file_types,
                          dict_types, mapping_types, mapping_classes,
                          function_types, Λ, callable_types,
                          ispathtype, ispath, isvalidpath,
                          isabstractmethod, isabstract, isabstractcontextmanager, iscontextmanager,
                          isnumber, isnumeric, iscomplex, isarray, isscalar, isstring, isbytes, ismodule,
                          isfunction, ΛΛ, islambda, λλ,
                          iscallable, ishashable, issequence,
                          ispathtypelist, ispathlist, isvalidpathlist,
                          isnumberlist, isnumericlist, iscomplexlist,
                          isarraylist, isscalarlist, isstringlist, isbyteslist,
                          ismodulelist, isfunctionlist, islambdalist,
                          iscallablelist, ishashablelist, issequencelist)

from clu.naming import (thingname, itermodule, moduleids, nameof,
                        determine_module,
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
import operator
import requests
import shutil
import six
import sysconfig
import termcolor
import xerox

from clu.mathematics import (σ, Σ,
                             isdtype, isnumpything, isnumpytype,
                             Clamper, clamp)

from clu import keyvalue
from clu.enums import (DUNDER, SUNDER,
                       alias, AliasingEnumMeta, AliasingEnum)

from clu.repl.ansi import (print_separator, print_ansi, print_ansi_centered,
                           ansidoc, highlight,
                           ANSIBase, ANSI,
                           Text, Weight, Background, ANSIFormat)

from clu.repl.banners import print_banner

# Compile all Greekly definitions and their names:
GREEK_STRINGS = ('σ', 'Σ', 'λ', 'λλ', 'Λ', 'ΛΛ')
GREEK_DEFS = (σ, Σ, λ, λλ, Λ, ΛΛ)

GREEK_PHONETICS = ('sigma-lower',
                   'sigma-upper',
                   'lambda-lower',
                   'double-lambda-lower',
                   'lambda-upper',
                   'double-lambda-upper')

GREEK_STRINGDICT = dict(zip(GREEK_STRINGS, GREEK_DEFS))
GREEK_NAMEDICT = dict(zip(GREEK_PHONETICS, GREEK_DEFS))

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
           'operator',
           'reduce',
           'requests',
           'shutil',
           'six',
           'sysconfig',
           'termcolor',
           'types',
           'xerox',
           'print_banner',
           'GREEK_STRINGS', 'GREEK_DEFS', 'GREEK_PHONETICS',
                                          'GREEK_STRINGDICT',
                                          'GREEK_NAMEDICT',
           'σ', 'Σ',
           'isdtype', 'isnumpything', 'isnumpytype',
           'Clamper', 'clamp',
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
           'PROJECT_NAME', 'PROJECT_PATH',
           'PY3', 'PYPY',
           'QUALIFIER',
           'SEPARATOR_WIDTH',
           'SINGLETON_TYPES',
           'SCRIPT_PATH', 'TEST_PATH',
           'TEXTMATE',
           'TOKEN',
           'VERBOTEN',
           'XDG_RUNTIME_BASE', 'XDG_RUNTIME_DIR',
                               'XDG_RUNTIME_MODE',
           'NoDefault',
           'GREEKOUT',
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
           'Exporter',
           'predicates_for_types',
           'path_to_dotpath',
           'negate',
           'ismetaclass', 'isclass', 'isclasstype', 'metaclass',
           'noattr', 'haspyattr', 'nopyattr',
           'anyattrs', 'allattrs', 'noattrs',
           'anypyattrs', 'allpyattrs', 'nopyattrs',
           'haslength',
           'isiterable', 'ismergeable',
           'always', 'never', 'nuhuh',
           'no_op', 'or_none', 'resolve',
           'getpyattr', 'getitem',
           'accessor', 'collator', 'searcher',
           'attr', 'pyattr', 'item',
           'attrs', 'pyattrs', 'items',
           'attr_search', 'pyattr_search', 'item_search',
           'isenum', 'enumchoices',
           'isaliasdescriptor', 'hasmembers', 'hasaliases',
           'predicate_nop', 'function_nop', 'uncallable',
           'pyname',
           'isexpandable', 'isnormative', 'iscontainer',
           'lambda_repr',
           'apply_to',
           'predicate_all', 'predicate_any', 'predicate_none',
           'predicate_and', 'predicate_or', 'predicate_xor',
           'thing_has', 'class_has',
           'isslotted', 'isdictish', 'isslotdicty', 'slots_for',
           'case_sort',
           'tuplize', 'uniquify', 'listify',
           'allof', 'anyof', 'noneof',
           'SimpleNamespace', 'Namespace', 'types', 'modulize',
           'samelength', 'differentlength', 'isunique', 'istypelist', 'maketypelist',
           'isderivative', 'subclasscheck', 'graceful_issubclass',
           'numeric_types', 'array_types', 'scalar_types', 'string_types', 'bytes_types',
           'path_classes', 'path_types', 'file_types',
           'dict_types', 'mapping_types', 'mapping_classes',
           'function_types', 'Λ', 'callable_types',
           'ispathtype', 'ispath', 'isvalidpath',
           'isabstractmethod', 'isabstract', 'isabstractcontextmanager', 'iscontextmanager',
           'isnumber', 'isnumeric', 'iscomplex',
           'isarray', 'isscalar', 'isstring', 'isbytes',
           'ismodule', 'isfunction', 'ΛΛ', 'islambda', 'λλ',
           'iscallable', 'ishashable', 'issequence',
           'ispathtypelist', 'ispathlist', 'isvalidpathlist',
           'isnumberlist', 'isnumericlist', 'iscomplexlist',
           'isarraylist', 'isscalarlist', 'isstringlist', 'isbyteslist',
           'ismodulelist', 'isfunctionlist', 'islambdalist',
           'iscallablelist', 'ishashablelist', 'issequencelist',
           'thingname', 'itermodule', 'moduleids', 'slots_for', 'nameof',
           'determine_module',
           'dotpath_join', 'dotpath_split',
           'qualified_import', 'qualified_name_tuple', 'qualified_name', 'split_abbreviations',
           'merge_two', 'merge_as', 'merge', 'asdict',
           'DUNDER', 'SUNDER', 'alias', 'AliasingEnumMeta', 'AliasingEnum',
           'print_separator', 'print_ansi', 'print_ansi_centered',
           'ansidoc', 'highlight',
           'ANSIBase', 'ANSI',
           'Text', 'Weight', 'Background', 'ANSIFormat',
           'keyvalue')

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
    import pytz
    import dateutil
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('pytz', 'dateutil')

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

