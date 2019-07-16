# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import OrderedDict, defaultdict as DefaultDict, Counter

import array
import argparse
import contextlib
import decimal
import io
import os

from clu.constants.consts import λ
from clu.constants.polyfills import long, unicode, numpy
from clu.constants.polyfills import HashableABC, SequenceABC, Path
from clu.constants.polyfills import Mapping, MutableMapping
from clu.exporting import Exporter

from clu.predicates import (isclasstype,
                            allpyattrs, getpyattr, haspyattr,
                            pyattr, or_none,
                            isiterable,
                            tuplize, uniquify,
                            apply_to, predicate_any,
                                      predicate_all)

from clu.typespace import types

exporter = Exporter(path=__file__)
export = exporter.decorator()

# TYPELISTS: lists containing only types -- according to `clu.predicates.isclasstype(…)` –
# can be formulated and tested by these lambdas and functions

isunique = lambda thing: isiterable(thing) and (len(frozenset(thing)) == len(tuple(thing)))
istypelist = predicate_all(isclasstype)
maketypelist = apply_to(lambda thing: isclasstype(thing) and thing or type(thing),
                        lambda total: tuple(frozenset(total)))

@export
def isderivative(putative, thing):
    """ isderivative(thing) → Boolean predicate, True if putative is either a subclass
        or an instance of thing – depending on whether putative is either a classtype
        or an instance, basically.
        
        Used internally to implement `subclasscheck(…)` (née “graceful_issubclass(…)”).
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

numeric_types = uniquify(bool, int, long, float, complex, decimal.Decimal)
array_types = (array.ArrayType, bytearray, memoryview)

array_types += tuplize(or_none(numpy, 'ndarray'),
                       or_none(numpy, 'matrix'),
                       hasattr(numpy, 'ma') and or_none(
                       getattr(numpy, 'ma'),
                                      'MaskedArray') or None)

# N.B. this numpy typelist does *not* include `decimal.Decimal` –
# and it *does* include `memoryview`:
scalar_types = frozenset(getattr(numpy, 'ScalarType',
                     set(numeric_types) - { decimal.Decimal }))

try:
    from six import string_types
except (ImportError, SyntaxError):
    string_types = uniquify(str, unicode)

bytes_types = (bytes, bytearray)
path_classes = tuplize(argparse.FileType, or_none(os, 'PathLike'), Path) # Path may be “None” in disguise
path_types = string_types + bytes_types + path_classes
file_types = (io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase)

dict_types = { dict, OrderedDict, DefaultDict, Counter }
mapping_types = { Mapping, MutableMapping }
mapping_classes = dict_types | mapping_types

function_types = Λ = (types.Function,
                      types.Method,
                      types.Lambda)

callable_types = Λ + (types.BuiltinFunction,
                      types.BuiltinMethod)

# These next types are generally only present in CPython’s “types” module,
# circa version 3.7-ish… PyPy seems to omit them as of v7.1.1, under its
# Python 3.6-compatible interpreter build:

callable_types += tuplize(or_none(types, 'Coroutine'),
                          or_none(types, 'ClassMethodDescriptor'),
                          or_none(types, 'MemberDescriptor'),
                          or_none(types, 'MethodDescriptor'))

# PREDICATE FUNCTIONS: is<something>() unary-predicates, many of which make use
# of the aforementioned typelists:

ispathtype = lambda cls: issubclass(cls, path_types)
ispath = lambda thing: subclasscheck(thing, path_types) or haspyattr(thing, 'fspath')
isvalidpath = lambda thing: ispath(thing) and os.path.exists(os.path.expanduser(thing))

isabstractmethod = lambda method: getpyattr(method, 'isabstractmethod', False)
isabstract = lambda thing: bool(pyattr(thing, 'abstractmethods', 'isabstractmethod'))
isabstractcontextmanager = lambda cls: subclasscheck(cls, contextlib.AbstractContextManager)
iscontextmanager = lambda cls: allpyattrs(cls, 'enter', 'exit') or isabstractcontextmanager(cls)

isnumber = lambda thing: subclasscheck(thing, numeric_types)
isnumeric = lambda thing: subclasscheck(thing, numeric_types)
iscomplex = lambda thing: subclasscheck(thing, complex)
isarray = lambda thing: subclasscheck(thing, array_types)
isscalar = lambda thing: subclasscheck(thing, scalar_types)
isstring = lambda thing: subclasscheck(thing, string_types)
isbytes = lambda thing: subclasscheck(thing, bytes_types)
ismodule = lambda thing: subclasscheck(thing, types.Module)
isfunction = ΛΛ = lambda thing: isinstance(thing, Λ) or callable(thing)
islambda = λλ = lambda thing: pyattr(thing, 'lambda_name', 'name', 'qualname') == λ
ishashable = lambda thing: isinstance(thing, HashableABC)
issequence = lambda thing: isinstance(thing, SequenceABC)

ispathtypelist = lambda thinglist: istypelist(thinglist) and predicate_all(ispathtype, *thinglist)
ispathlist = lambda thinglist: issequence(thinglist) and predicate_all(ispath, *thinglist)
isvalidpathlist = lambda thinglist: issequence(thinglist) and predicate_all(isvalidpath, *thinglist)

isnumberlist = lambda thinglist: issequence(thinglist) and predicate_all(isnumber, *thinglist)
isnumericlist = lambda thinglist: issequence(thinglist) and predicate_all(isnumeric, *thinglist)
iscomplexlist = lambda thinglist: issequence(thinglist) and predicate_all(iscomplex, *thinglist)
isarraylist = lambda thinglist: issequence(thinglist) and predicate_all(isarray, *thinglist)
isscalarlist = lambda thinglist: issequence(thinglist) and predicate_all(isscalar, *thinglist)
isstringlist = lambda thinglist: issequence(thinglist) and predicate_all(isstring, *thinglist)
isbyteslist = lambda thinglist: issequence(thinglist) and predicate_all(isbytes, *thinglist)
ismodulelist = lambda thinglist: issequence(thinglist) and predicate_all(ismodule, *thinglist)
isfunctionlist = lambda thinglist: issequence(thinglist) and predicate_all(isfunction, *thinglist)
islambdalist = lambda thinglist: issequence(thinglist) and predicate_all(islambda, *thinglist)
ishashablelist = lambda thinglist: issequence(thinglist) and predicate_all(ishashable, *thinglist)
issequencelist = lambda thinglist: issequence(thinglist) and predicate_all(issequence, *thinglist)

# MODULE EXPORTS:
export(isunique,        name='isunique',    doc="isunique(thing) → boolean predicate, True if `thing` is an iterable with unique contents")
export(istypelist,      name='istypelist',  doc="istypelist(thing) → boolean predicate, True if `thing` is a “typelist” – a list consisting only of class types")
export(maketypelist,    name='maketypelist',
                         doc="maketypelist(iterable) → convert an iterable of unknown things into a uniquified typelist – a list consisting only of class types")


export(subclasscheck,   name='subclasscheck',
                         doc="subclasscheck(putative, *cls_or_tuple) → A wrapper for `issubclass(…)` and `isinstance(…)` that tries to work with you`")

export(graceful_issubclass,
                        name='graceful_issubclass')

# NO DOCS ALLOWED:
export(numeric_types,   name='numeric_types')
export(array_types,     name='array_types')
export(scalar_types,    name='scalar_types')
export(bytes_types,     name='bytes_types')
export(string_types,    name='string_types')
export(path_classes,    name='path_classes')
export(path_types,      name='path_types')
export(file_types,      name='file_types')
export(function_types,  name='function_types')
export(Λ,               name='Λ')
export(callable_types,  name='callable_types')

export(ispathtype,      name='ispathtype',  doc="ispathtype(thing) → boolean predicate, True if `thing` is a path type")
export(ispath,          name='ispath',      doc="ispath(thing) → boolean predicate, True if `thing` seems to be path-ish instance")
export(isvalidpath,     name='isvalidpath', doc="isvalidpath(thing) → boolean predicate, True if `thing` represents a valid path on the filesystem")

export(isabstractmethod,                    doc="isabstractmethod(thing) → boolean predicate, True if `thing` is a method declared “abstract” with `@abc.abstractmethod`")
export(isabstract,                          doc="isabstract(thing) → boolean predicate, True if `thing` is an abstract method OR an “abstract base class” (née ABC)")
export(isabstractcontextmanager,            doc="isabstractcontextmanager(thing) → boolean predicate, True if `thing` decends from `contextlib.AbstractContextManager`")
export(iscontextmanager,                    doc="iscontextmanager(thing) → boolean predicate, True if `thing` is a context manager (either abstract or concrete)")

export(isnumber,        name='isnumber',    doc="isnumber(thing) → boolean predicate, True if `thing` is a numeric type or an instance of same")
export(isnumeric,       name='isnumeric',   doc="isnumeric(thing) → boolean predicate, True if `thing` is a numeric type or an instance of same")
export(iscomplex,       name='iscomplex',   doc="iscomplex(thing) → boolean predicate, True if `thing` is a complex numeric type or an instance of same")
export(isarray,         name='isarray',     doc="isarray(thing) → boolean predicate, True if `thing` is an array type or an instance of same")
export(isscalar,        name='isscalar',    doc="isscalar(thing) → boolean predicate, True if `thing` is a numpy scalar numeric type or an instance of same")
export(isstring,        name='isstring',    doc="isstring(thing) → boolean predicate, True if `thing` is a string type or an instance of same")
export(isbytes,         name='isbytes',     doc="isbytes(thing) → boolean predicate, True if `thing` is a bytes-like type or an instance of same")
export(ismodule,        name='ismodule',    doc="ismodule(thing) → boolean predicate, True if `thing` is a module type or an instance of same")
export(isfunction,      name='isfunction',  doc="isfunction(thing) → boolean predicate, True if `thing` is of a callable function type")
export(ΛΛ,              name='ΛΛ',          doc="ΛΛ(thing) → boolean predicate, True if `thing` is of a callable function type")
export(islambda,        name='islambda',    doc="islambda(thing) → boolean predicate, True if `thing` is a function created with the «lambda» keyword")
export(λλ,              name='λλ',          doc="λλ(thing) → boolean predicate, True if `thing` is a function created with the «lambda» keyword")
export(ishashable,      name='ishashable',  doc="ishashable(thing) → boolean predicate, True if `thing` can be hashed, via the builtin `hash(…)` function")
export(issequence,      name='issequence',  doc="issequence(thing) → boolean predicate, True if `thing` is a sequence type (e.g. a `tuple` or `list` type)")

export(ispathtypelist,  name='ispathtypelist',  doc="ispathtypelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of path-related class types")
export(ispathlist,      name='ispathlist',      doc="ispathlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of path-like instances")
export(isvalidpathlist, name='isvalidpathlist', doc="isvalidpathlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of valid filesystem path instances")

export(isnumberlist,    name='isnumberlist',    doc="isnumberlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numeric types")
export(isnumericlist,   name='isnumericlist',   doc="isnumericlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numeric types")
export(iscomplexlist,   name='iscomplexlist',   doc="iscomplexlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of complex numeric types")
export(isarraylist,     name='isarraylist',     doc="isarraylist(thinglist) → boolean predicate, True if `thinglist` is a sequence of array types")
export(isscalarlist,    name='isscalarlist',    doc="isscalarlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numpy scalar numeric types")
export(isstringlist,    name='isstringlist',    doc="isstringlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of string types")
export(isbyteslist,     name='isbyteslist',     doc="isbyteslist(thinglist) → boolean predicate, True if `thinglist` is a sequence of bytes-like types")
export(ismodulelist,    name='ismodulelist',    doc="ismodulelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of module types")
export(isfunctionlist,  name='isfunctionlist',  doc="isfunctionlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of callable function types")
export(islambdalist,    name='islambdalist',    doc="islambdalist(thinglist) → boolean predicate, True if `thinglist` is a sequence of functions created with the «lambda» keyword")
export(ishashablelist,  name='ishashablelist',  doc="ishashablelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of things that can be hashed, via the builtin `hash(…)` function")
export(issequencelist,  name='issequencelist',  doc="issequencelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of sequence types")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
