# -*- coding: utf-8 -*-
from __future__ import print_function

import array
import argparse
import contextlib
import decimal
import io
import os

from constants import unicode, HashableABC, Path, LAMBDA, PY3, PYPY

from predicates import (isclasstype,
                        allpyattrs, getpyattr, haspyattr,
                        pyattr, or_none,
                        isiterable,
                        tuplize, uniquify,
                        apply_to)

from typespace import types

def graceful_issubclass(thing, *cls_or_tuple):
    """ A wrapper for `issubclass()` that tries to work with you. """
    length = 0
    try:
        length = len(cls_or_tuple)
    except TypeError:
        pass
    else:
        if length == 1:
            cls_or_tuple = cls_or_tuple[0]
        else:
            cls_or_tuple = tuple(item for item in cls_or_tuple if item is not None)
        if (not isinstance(cls_or_tuple, (type, tuple))) \
            and isiterable(cls_or_tuple):
            cls_or_tuple = tuple(cls_or_tuple)
    try:
        return issubclass(thing, cls_or_tuple)
    except TypeError:
        pass
    try:
        return issubclass(type(thing), cls_or_tuple)
    except TypeError:
        pass
    return None


numeric_types = (int, float, decimal.Decimal)

try:
    import numpy

except (ImportError, SyntaxError):
    numpy = None
    array_types = (array.ArrayType,
                   bytearray, memoryview)

else:
    array_types = (numpy.ndarray,
                   numpy.matrix,
                   numpy.ma.MaskedArray, array.ArrayType,
                                         bytearray, memoryview)

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


ispathtype = lambda cls: issubclass(cls, path_types)
ispath = lambda thing: graceful_issubclass(thing, path_types) or haspyattr(thing, 'fspath')
isvalidpath = lambda thing: ispath(thing) and os.path.exists(os.path.expanduser(thing))

# UTILITY FUNCTIONS: is<something>() unary-predicates, and utility
# type-tuples with which said predicates use to make their decisions:

predicatenop = lambda *things: None

isabstractmethod = lambda method: getpyattr(method, 'isabstractmethod', False)
isabstract = lambda thing: bool(pyattr(thing, 'abstractmethods', 'isabstractmethod'))
isabstractcontextmanager = lambda cls: graceful_issubclass(cls, contextlib.AbstractContextManager)
iscontextmanager = lambda cls: allpyattrs(cls, 'enter', 'exit') or isabstractcontextmanager(cls)

isnumber = lambda thing: graceful_issubclass(thing, numeric_types)
isnumeric = lambda thing: graceful_issubclass(thing, numeric_types)
isarray = lambda thing: graceful_issubclass(thing, array_types)
isstring = lambda thing: graceful_issubclass(thing, string_types)
isbytes = lambda thing: graceful_issubclass(thing, bytes_types)
ismodule = lambda thing: graceful_issubclass(thing, types.Module)
isfunction = lambda thing: isinstance(thing, (types.Function, types.Lambda)) or callable(thing)
islambda = lambda thing: pyattr(thing, 'lambda_name', 'name', 'qualname') == LAMBDA
ishashable = lambda thing: isinstance(thing, HashableABC)

# TYPELISTS: lists containing only types -- according to `clu.predicates.isclasstype(…)`

isunique = lambda thing: isiterable(thing) and (len(frozenset(thing)) == len(tuple(thing)))
istypelist = apply_to(isclasstype, all)
maketypelist = apply_to(lambda thing: isclasstype(thing) and thing or type(thing),
                        lambda total: tuple(frozenset(total)))

__all__ = ('graceful_issubclass',
           'numeric_types', 'array_types', 'string_types', 'bytes_types',
           'path_classes', 'path_types', 'file_types', 'callable_types',
           'ispathtype', 'ispath', 'isvalidpath',
           'predicatenop',
           'isabstractmethod', 'isabstract', 'isabstractcontextmanager', 'iscontextmanager',
           'isnumber', 'isnumeric', 'isarray', 'isstring', 'isbytes', 'ismodule',
           'isfunction', 'islambda', 'ishashable',
           'isunique',
           'istypelist', 'maketypelist')

__dir__ = lambda: list(__all__)
