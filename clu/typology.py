# -*- coding: utf-8 -*-
from __future__ import print_function

import array
import argparse
import contextlib
import decimal
import io
import os

from constants import LAMBDA, PY3, PYPY
from constants import long, unicode, HashableABC, Path
from constants import numpy

from predicates import (isclasstype,
                        allpyattrs, getpyattr, haspyattr,
                        pyattr, or_none,
                        isiterable,
                        tuplize, uniquify,
                        apply_to, predicate_any,
                                  predicate_all)

from typespace import types

# TYPELISTS: lists containing only types -- according to `clu.predicates.isclasstype(…)` –
# can be formulated and tested by these lambdas and functions

isunique = lambda thing: isiterable(thing) and (len(frozenset(thing)) == len(tuple(thing)))
istypelist = predicate_all(isclasstype)
maketypelist = apply_to(lambda thing: isclasstype(thing) and thing or type(thing),
                        lambda total: tuple(frozenset(total)))

def isderivative(putative, thing):
    """ isderivative(thing) → Boolean predicate, True if putative is either a subclass
        or an instance of thing – depending on whether putative is either a classtype
        or an instance, basically.
    """
    try:
        return issubclass(putative, thing)
    except TypeError:
        return isinstance(putative, thing)

# PREDICATE FUNCTION “graceful_issubclass”: A wrapper for `issubclass(…)`
# and `isinstance(…)` that tries to work with you, instead of barfing up
# all sorts of TypeErrors willy-nilly at the slightest misconfiguration: 

subclasscheck = lambda putative, *thinglist: predicate_any(
                lambda thing: isderivative(putative, thing),
                                      *maketypelist(*thinglist))

# LEGACY CODE SUPPORT:
graceful_issubclass = subclasscheck

# TYPELISTS: manual assemblages of types, used for predicate testing
# and other similar stuff.

numeric_types = uniquify(int, long, float, complex, decimal.Decimal)
array_types = (array.ArrayType, bytearray, memoryview)

if numpy is not None:
    array_types += (numpy.ndarray,
                    numpy.matrix,
                    numpy.ma.MaskedArray)

try:
    from six import string_types
except (ImportError, SyntaxError):
    string_types = uniquify(str, unicode)

bytes_types = (bytes, bytearray)
path_classes = tuplize(argparse.FileType, or_none(os, 'PathLike'), Path) # Path may be “None” in disguise
path_types = string_types + bytes_types + path_classes
file_types = (io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase)

callable_types = (types.Function,
                  types.Method,
                  types.Lambda,
                  types.BuiltinFunction,
                  types.BuiltinMethod)

if PY3 and not PYPY:
    callable_types += (
                  types.Coroutine,
                  types.ClassMethodDescriptor,
                  types.MemberDescriptor,
                  types.MethodDescriptor)

# PREDICATE FUNCTIONS: is<something>() unary-predicates, many of which make use
# of the aforementioned typelists:

ispathtype = lambda cls: issubclass(cls, path_types)
ispath = lambda thing: graceful_issubclass(thing, path_types) or haspyattr(thing, 'fspath')
isvalidpath = lambda thing: ispath(thing) and os.path.exists(os.path.expanduser(thing))

isabstractmethod = lambda method: getpyattr(method, 'isabstractmethod', False)
isabstract = lambda thing: bool(pyattr(thing, 'abstractmethods', 'isabstractmethod'))
isabstractcontextmanager = lambda cls: graceful_issubclass(cls, contextlib.AbstractContextManager)
iscontextmanager = lambda cls: allpyattrs(cls, 'enter', 'exit') or isabstractcontextmanager(cls)

isnumber = lambda thing: graceful_issubclass(thing, numeric_types)
isnumeric = lambda thing: graceful_issubclass(thing, numeric_types)
iscomplex = lambda thing: graceful_issubclass(thing, complex)
isarray = lambda thing: graceful_issubclass(thing, array_types)
isstring = lambda thing: graceful_issubclass(thing, string_types)
isbytes = lambda thing: graceful_issubclass(thing, bytes_types)
ismodule = lambda thing: graceful_issubclass(thing, types.Module)
isfunction = lambda thing: isinstance(thing, (types.Function, types.Lambda)) or callable(thing)
islambda = lambda thing: pyattr(thing, 'lambda_name', 'name', 'qualname') == LAMBDA
ishashable = lambda thing: isinstance(thing, HashableABC)

__all__ = ('isunique', 'istypelist', 'maketypelist',
           'isderivative', 'subclasscheck', 'graceful_issubclass',
           'numeric_types', 'array_types', 'string_types', 'bytes_types',
           'path_classes', 'path_types', 'file_types', 'callable_types',
           'ispathtype', 'ispath', 'isvalidpath',
           'isabstractmethod', 'isabstract', 'isabstractcontextmanager', 'iscontextmanager',
           'isnumber', 'isnumeric', 'iscomplex', 'isarray', 'isstring', 'isbytes', 'ismodule',
           'isfunction', 'islambda', 'ishashable')

__dir__ = lambda: list(__all__)
