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
                                  PARTIAL, φ,
                                  PROJECT_NAME, PROJECT_PATH,
                                  PY3, PYPY,
                                  PYTHON_VERSION,
                                  QUALIFIER,
                                  SEPARATOR_WIDTH,
                                  SINGLETON_TYPES,
                                  SCRIPT_PATH, TEST_PATH,
                                  TEXTMATE,
                                  TOKEN,
                                  USER,
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
                                     Path, reduce)

from clu.compilation import (Macro, Macros,
                             CDBSubBase, CDBBase, CDBJsonFile)

from clu.exporting import (itermodule, moduleids, itermoduleids,
                           search_by_id,
                           search_for_name, search_for_module,
                           search_modules,
                           determine_name,
                           path_to_dotpath,
                           Exporter, ExporterBase,
                           Registry)

from clu.extending import (Extensible,
                           pairtype, ΩΩ, pairmro, ω, pair, Ω,
                           DoubleDutchRegistry, doubledutch,
                           DoubleDutchFunction)

from clu.importing import (Module, Finder, Loader,
                           initialize_types,
                           all_registered_appnames,
                           all_registered_modules,
                           modules_for_appname,
                           ModuleBase, FinderBase, LoaderBase,
                           Package, ModuleSpec,
                           Registry as ClassModuleRegistry,
                           ArgumentSink)

from clu.sanitizer import sanitize, sanitizers, utf8_encode, utf8_decode
from clu.version import version_info

from clu.predicates import (negate, reverse,
                            ismetaclass, isclass, isclasstype,
                            metaclass, typeof,
                            noattr, haspyattr, nopyattr,
                            anyattrs, allattrs, noattrs,
                            anypyattrs, allpyattrs, nopyattrs,
                            haslength,
                            isiterable, ismergeable,
                            always, never, nuhuh,
                            no_op, or_none, stor_none, resolve,
                            getpyattr, getitem, retrieve,
                            accessor, acquirer, collator, searcher,
                            attr, stattr, pyattr, item,
                            attrs, stattrs, pyattrs, items,
                            attr_search, stattr_search, pyattr_search, item_search,
                            attr_across, stattr_across, pyattr_across, item_across,
                            finditem, finditems,
                            try_items,
                            dunder_or, mro, rmro, unwrap, origin,
                            isancestor, isorigin, newtype,
                            isenum, enumchoices,
                            predicate_nop, function_nop,
                            wrap_value, none_function, true_function,
                            uncallable, hoist,
                            pyname, pymodule,
                            isexpandable, isnormative, iscontainer,
                            lambda_repr,
                            apply_to,
                            predicate_all, predicate_any, predicate_none,
                            predicate_and, predicate_or, predicate_xor,
                            thing_has, class_has,
                            isslotted, isdictish, isslotdicty,
                            case_sort,
                            itervariadic,
                            tuplize, uniquify, listify, union,
                            ancestral, ancestral_union,
                            allof, anyof, noneof,
                            slots_for)

from clu.typespace import types, modulize
from clu.typespace.namespace import NamespaceRepr, SimpleNamespace, Namespace, isnamespace

from clu.typology import (samelength, differentlength, isunique,
                          istypelist, ismetatypelist, maketypelist, makemetatypelist,
                          isderivative, subclasscheck, metaclasscheck, graceful_issubclass,
                          numeric_types, array_types, scalar_types, string_types, bytes_types,
                          path_classes, path_types, file_types,
                          dict_types, mapping_types, mapping_classes,
                          function_types, Λ, callable_types,
                          ispathtype, ispath, isnotpath, isvalidpath,
                          isaliasdescriptor, hasmembers, hasaliases,
                          isabstractmethod, isabstract, isabstractcontextmanager, iscontextmanager,
                          isabc, isslottedtype, isextensibletype,
                          isnumber, isnumeric, iscomplex, ismapping,
                          isarray, isscalar, isstring, isbytes, ismodule,
                          isfunction, ΛΛ, islambda, λλ,
                          iscallable, iscallabletype, ishashable, issequence,
                          isxlist, isxtypelist, isxmetatypelist, isabclist,
                          ispathtypelist, ispathlist, isvalidpathlist,
                          isnumberlist, isnumericlist, iscomplexlist, ismappinglist,
                          isarraylist, isscalarlist, isstringlist, isbyteslist,
                          ismodulelist, isfunctionlist, islambdalist,
                          iscallablelist, iscallabletypelist, ishashablelist, issequencelist)

from clu.naming import (determine_module, nameof, moduleof,
                        isbuiltin, isnativemodule, isnative,
                        dotpath_join, dotpath_split, qualified_import,
                                                     qualified_name_tuple,
                                                     qualified_name,
                        dotpath_to_prefix, path_to_prefix,
                        split_abbreviations)

from clu.abstract import Cloneable, ReprWrapper

# from clu.config.base import Flat, Nested
from clu.config.abc import FlatOrderedSet, functional_and, functional_set
from clu.config.defg import (NAMESPACE_SEP, FrozenKeyMap, KeyMap, FrozenFlat, Flat,
                                                                  FrozenNested, Nested)
from clu.config.defg import nestedmaps, flatdict
from clu.config.proxy import KeyMapView, KeyMapProxy

from clu.config.env import Env
from clu.config.filebase import FileName, FileBase
from clu.config.fieldtypes import ValidationError
from clu.config.fieldtypes import FieldBase
from clu.config.fieldtypes import fields
from clu.config.settings import Schema
from clu.config.formats import JsonFile, PickleFile, TomlFile, YamlFile

from clu.csv import pad_csv
from clu.dicts import OrderedMappingView, OrderedItemsView, OrderedKeysView, OrderedValuesView
from clu.dicts import ChainMap, merge_two, merge_as, merge, asdict

# Add miscellaneous necessities:
from PIL import Image
from pprint import pprint, pformat
import sys, os, re
import argparse
import collections
import contextlib
import copy
import datetime
import decimal
import functools
import importlib
import inspect
import io
import itertools
import math
import operator
import pickle
import requests
import shutil
import six
import sysconfig
import weakref

from clu.mathematics import (σ, Σ,
                             isdtype, isnumpything,
                                      isnumpytype,
                                      isnumpythinglist,
                                      isnumpytypelist,
                             Clamper, clamp)

from clu import keyvalue
from clu.enums import (DUNDER, SUNDER,
                       alias, AliasingEnumMeta, AliasingEnum)

from clu.repl.ansi import (print_separator, evict_announcer,
                           print_ansi, print_ansi_centered,
                           paragraphize,
                           ansidoc, highlight,
                           ANSIBase, ANSI,
                           Text, Weight, Background, ANSIFormat)

from clu.repl.banners import print_banner

# Compile all Greekly definitions and their names:
GREEK_STRINGS = ('σ', 'Σ', 'λ', 'λλ', 'Λ', 'ΛΛ', 'φ', 'Ω', 'ω', 'ΩΩ')
GREEK_DEFS = (σ, Σ, λ, λλ, Λ, ΛΛ, φ, Ω, ω, ΩΩ)

GREEK_PHONETICS = ('sigma-lower',
                   'sigma-upper',
                   'lambda-lower',
                   'double-lambda-lower',
                   'lambda-upper',
                   'double-lambda-upper',
                   'phi-lower',
                   'omega-upper',
                   'omega-lower'
                   'double-omega-upper')

GREEK_STRINGDICT = dict(zip(GREEK_STRINGS, GREEK_DEFS))
GREEK_NAMEDICT = dict(zip(GREEK_PHONETICS, GREEK_DEFS))

# Practice safe star-importing:
__all__ = ('Image',
           'pprint', 'pformat',
           'sys', 'os', 're',
           'appdirectories',
           'argparse',
           'collections',
           'contextlib',
           'copy',
           'datetime',
           'decimal',
           'functools',
           'importlib',
           'inspect',
           'io',
           'itertools',
           'math',
           'operator',
           'pickle',
           'reduce',
           'requests',
           'shutil',
           'six',
           'sysconfig',
           'types',
           'weakref',
           'print_banner',
           'GREEK_STRINGS', 'GREEK_DEFS', 'GREEK_PHONETICS',
                                          'GREEK_STRINGDICT',
                                          'GREEK_NAMEDICT',
           'σ', 'Σ',
           'isdtype', 'isnumpything', 'isnumpytype', 'isnumpythinglist', 'isnumpytypelist',
           'Clamper', 'clamp',
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
           'Path',
           'sanitize', 'sanitizers', 'utf8_encode', 'utf8_decode',
           'Macro', 'Macros',
           'CDBSubBase', 'CDBBase', 'CDBJsonFile',
           'itermodule', 'moduleids', 'itermoduleids',
           'search_by_id',
           'search_for_name', 'search_for_module',
           'search_modules',
           'determine_name',
           'Exporter', 'ExporterBase', 'Registry',
           'path_to_dotpath',
           'Extensible',
           'pairtype', 'ΩΩ', 'pairmro', 'ω', 'pair', 'Ω',
           'DoubleDutchRegistry', 'doubledutch',
           'DoubleDutchFunction',
           'Module', 'Finder', 'Loader',
           'initialize_types',
           'all_registered_appnames',
           'all_registered_modules',
           'modules_for_appname',
           'ModuleBase', 'FinderBase', 'LoaderBase',
           'Package', 'ModuleSpec',
           'ClassModuleRegistry',
           'ArgumentSink',
           'negate', 'reverse',
           'ismetaclass', 'isclass', 'isclasstype',
           'metaclass', 'typeof',
           'noattr', 'haspyattr', 'nopyattr',
           'anyattrs', 'allattrs', 'noattrs',
           'anypyattrs', 'allpyattrs', 'nopyattrs',
           'haslength',
           'isiterable', 'ismergeable',
           'always', 'never', 'nuhuh',
           'no_op', 'or_none', 'stor_none', 'resolve',
           'getpyattr', 'getitem', 'retrieve',
           'accessor', 'acquirer', 'collator', 'searcher',
           'attr', 'stattr', 'pyattr', 'item',
           'attrs', 'stattrs', 'pyattrs', 'items',
           'attr_search', 'stattr_search', 'pyattr_search', 'item_search',
           'attr_across', 'stattr_across', 'pyattr_across', 'item_across',
           'finditem', 'finditems',
           'try_items',
           'dunder_or', 'mro', 'rmro', 'unwrap', 'origin',
           'isancestor', 'isorigin', 'newtype',
           'isenum', 'enumchoices',
           'predicate_nop', 'function_nop',
           'wrap_value', 'none_function', 'true_function',
           'uncallable', 'hoist',
           'pyname', 'pymodule',
           'isexpandable', 'isnormative', 'iscontainer',
           'lambda_repr',
           'apply_to',
           'predicate_all', 'predicate_any', 'predicate_none',
           'predicate_and', 'predicate_or', 'predicate_xor',
           'thing_has', 'class_has',
           'isslotted', 'isdictish', 'isslotdicty',
           'slots_for',
           'case_sort',
           'itervariadic',
           'tuplize', 'uniquify', 'listify', 'union',
           'ancestral', 'ancestral_union',
           'allof', 'anyof', 'noneof',
           'types', 'modulize',
           'NamespaceRepr', 'SimpleNamespace', 'Namespace', 'isnamespace',
           'samelength', 'differentlength', 'isunique',
           'istypelist', 'ismetatypelist', 'maketypelist', 'makemetatypelist',
           'isderivative', 'subclasscheck', 'metaclasscheck', 'graceful_issubclass',
           'numeric_types', 'array_types', 'scalar_types', 'string_types', 'bytes_types',
           'path_classes', 'path_types', 'file_types',
           'dict_types', 'mapping_types', 'mapping_classes',
           'function_types', 'Λ', 'callable_types',
           'ispathtype', 'ispath', 'isnotpath', 'isvalidpath',
           'isaliasdescriptor', 'hasmembers', 'hasaliases',
           'isabstractmethod', 'isabstract', 'isabstractcontextmanager', 'iscontextmanager',
           'isabc', 'isslottedtype', 'isextensibletype',
           'isnumber', 'isnumeric', 'iscomplex', 'ismapping',
           'isarray', 'isscalar', 'isstring', 'isbytes',
           'ismodule', 'isfunction', 'ΛΛ', 'islambda', 'λλ',
           'iscallable', 'iscallabletype', 'ishashable', 'issequence',
           'isxlist', 'isxtypelist', 'isxmetatypelist', 'isabclist',
           'ispathtypelist', 'ispathlist', 'isvalidpathlist',
           'isnumberlist', 'isnumericlist', 'iscomplexlist', 'ismappinglist',
           'isarraylist', 'isscalarlist', 'isstringlist', 'isbyteslist',
           'ismodulelist', 'isfunctionlist', 'islambdalist',
           'iscallablelist', 'iscallabletypelist', 'ishashablelist', 'issequencelist',
           'determine_module', 'nameof', 'moduleof',
           'isbuiltin', 'isnativemodule', 'isnative',
           'dotpath_join', 'dotpath_split',
           'qualified_import', 'qualified_name_tuple', 'qualified_name',
           'dotpath_to_prefix', 'path_to_prefix',
           'split_abbreviations',
           'NAMESPACE_SEP', 'Cloneable', 'ReprWrapper', 'FlatOrderedSet',
           'FrozenKeyMap', 'KeyMap',
           'FrozenFlat', 'FrozenNested',
           'KeyMapView', 'KeyMapProxy',
           'Flat', 'Nested',
           'Env', 'FileName', 'FileBase',
           'ValidationError', 'hoist',
           'functional_and', 'functional_set',
           'FieldBase', 'fields',
           'Schema', 'JsonFile', 'PickleFile', 'TomlFile', 'YamlFile',
           'pad_csv',
           'OrderedMappingView', 'OrderedItemsView', 'OrderedKeysView', 'OrderedValuesView',
           'ChainMap', 'merge_two', 'merge_as', 'merge', 'asdict',
           'DUNDER', 'SUNDER', 'alias', 'AliasingEnumMeta', 'AliasingEnum',
           'print_separator', 'evict_announcer',
           'print_ansi', 'print_ansi_centered',
           'paragraphize',
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
    import colorama
    import termcolor
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('colorama', 'termcolor')

try:
    import colorio
    import colormath
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('colorio', 'colormath')

try:
    import xerox
    import zict
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('xerox', 'zict')

try:
    from clu.testing.utils import pout, inline
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('pout', 'inline')

try:
    from clu import dispatch
    from clu.shelving.redat import RedisConf, RedRun
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('dispatch', 'RedisConf', 'RedRun')

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
    from clu.fs.filesystem import (DEFAULT_PREFIX, DEFAULT_TIMEOUT,
                                   ensure_path_is_valid,
                                   script_path, which, back_tick,
                                   rm_rf, temporary,
                                   TypeLocker,
                                   TemporaryName, Directory,
                                                  cd, wd, td, hd,
                                   TemporaryDirectory, Intermediate,
                                   NamedTemporaryFile)
    from clu.fs.misc import (gethomedir, isinvalidpath,
                             re_matcher, re_searcher,
                             re_suffix, suffix_searcher,
                             re_excluder,
                             extension, swapext,
                             differentfile,
                             filesize, samesize, differentsize)
    from clu.fs import appdirectories, pypath
    from clu.repr import (hexid, typenameof, typename_hexid,
                          strfield, strfields, stringify)
except (ImportError, SyntaxError):
    pass
else:
    # Extend `__all__`:
    __all__ += ('DEFAULT_PREFIX', 'DEFAULT_TIMEOUT',
                'ensure_path_is_valid',
                'script_path', 'which', 'back_tick',
                'rm_rf', 'temporary',
                'TypeLocker',
                'TemporaryName', 'Directory',
                                 'cd', 'wd', 'td', 'hd',
                'TemporaryDirectory', 'Intermediate',
                'NamedTemporaryFile',
                'gethomedir', 'isinvalidpath',
                're_matcher', 're_searcher',
                're_suffix', 'suffix_searcher',
                're_excluder',
                'extension', 'swapext',
                'differentfile',
                'filesize', 'samesize', 'differentsize',
                'appdirectories', 'pypath',
                'hexid', 'typenameof', 'typename_hexid',
                'strfield', 'strfields', 'stringify')
    D = Directory()

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

# Set up some “example” instances –
# I frequently create trivial lists, strings, tuples etc.,
# to be used as exemplars from which I can check methods and
# suchlike using the interactive interpreter:
b = b'yo dogg'
B = bytearray(b)
m = memoryview(b)
c = complex(0, 1)
d = { 'yo' : "dogg" }
t = ('yo', 'dogg')
l = ['yo', 'dogg']
S = { 'yo', 'dogg' }
F = frozenset(S)
f = 0.666
i = 666
o = object()
s = 'yo dogg'

sns = SimpleNamespace(yo='dogg', iheard='youlike')
ns = Namespace(yo='dogg', iheard='youlike')

flat = Flat(flatdict())
nest = Nested(nestedmaps())
fview = KeyMapView(flat)
fprox = KeyMapProxy(flat)
nview = KeyMapView(nest)
nprox = KeyMapProxy(nest)

# Remove duplicate and invalid sys.paths:
if 'pypath' in __all__:
    pypath.remove_invalid_paths()

# Print the Python banner and/or warnings, messages, and other tripe:
print_banner()

