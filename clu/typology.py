# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import count

import abc
import argparse
import collections
import collections.abc
import contextlib
import decimal
import io
import operator
import os

from clu.constants.consts import λ, φ, SINGLETON_TYPES # type: ignore
from clu.constants.polyfills import long, unicode, numpy
from clu.constants.polyfills import Path # type: ignore
from clu.abstract import Slotted
from clu.enums import alias
from clu.extending import Extensible
from clu.exporting import Exporter

from clu.predicates import (negate,
                            ismetaclass, isclasstype, metaclass,
                            allpyattrs, haspyattr, nopyattr,
                            isiterable, haslength, typeof,
                            getpyattr, or_none, isenum,
                            pyattr, attrs,
                            tuplize, uniquify,
                            apply_to, predicate_any,
                                      predicate_all)

from clu.typespace import types

exporter = Exporter(path=__file__)
export = exporter.decorator()

# TYPELISTS: lists containing only types -- according to `clu.predicates.isclasstype(…)` –
# can be formulated and tested by these lambdas and functions

samelength = lambda a, b: haslength(a) and haslength(b) and operator.eq(len(a), len(b))
differentlength = lambda a, b: haslength(a) and haslength(b) and operator.ne(len(a), len(b))
isunique = lambda thing: isiterable(thing) and samelength(tuple(thing), frozenset(thing))

@export
def iterlen(iterable):
    """ iterlen(iterable) → Return the number of items in “iterable.”
        
        This will consume the iterable – be careful with it!
    """
    # Stolen from “more-itertools”: http://bit.ly/2LUZqCx
    counter = count()
    collections.deque(zip(iterable, counter), maxlen=0)
    return next(counter)

istypelist = predicate_all(isclasstype)
ismetatypelist = predicate_all(ismetaclass)
maketypelist = apply_to(typeof, uniquify)
makemetatypelist = apply_to(metaclass, uniquify)

@export
def isderivative(putative, thing):
    """ isderivative(putative, thing) → Boolean predicate, True if putative is either
        a subclass or an instance of thing – depending on whether putative is either
        a classtype or an instance, basically.
        
        Used internally to implement `subclasscheck(…)` (née “graceful_issubclass(…)”).
    """
    try:
        return issubclass(putative, thing)
    except (AttributeError, TypeError):
        return isinstance(putative, thing)

# PREDICATE FUNCTION “subclasscheck”: A wrapper for `issubclass(…)` and
# `isinstance(…)` that tries to work with you – instead of barfing up
# all sorts of TypeErrors willy-nilly at the slightest misconfiguration:

subclasscheck = lambda putative, *thinglist: predicate_any(
                lambda thing: isderivative(putative, thing),
                                                    *thinglist)

metaclasscheck = lambda putative, *thinglist: predicate_any(
                 lambda thing: isderivative(metaclass(putative), thing),
                                                                *thinglist)

# LEGACY CODE SUPPORT:
graceful_issubclass = subclasscheck

# TYPELISTS: manual assemblages of types, used for predicate testing
# and other similar stuff.

numeric_types = uniquify(bool, int, long, float, complex, decimal.Decimal)
array_types = (types.Array, bytearray, memoryview) # type: tuple
array_types += attrs(numpy, 'ndarray',
                            'matrix',
                            'ma.core.MaskedArray')

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
path_types = string_types + bytes_types + path_classes # type: ignore
file_types = (io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase)

dict_types      = { dict, collections.defaultdict,
                          collections.OrderedDict,
                          collections.Counter,
                          collections.ChainMap }

namespace_types = { types.SimpleNamespace,
                    types.Namespace }

mapping_types   = { collections.abc.Mapping,
                    collections.abc.MutableMapping,
                    types.MappingProxy }

mapping_classes = dict_types | namespace_types | mapping_types

function_types = Λ = (types.Function,
                      types.Method,
                      types.Lambda)

callable_types = Λ + (types.BuiltinFunction,
                      types.BuiltinMethod)

# These next types are generally only present in CPython’s “types” module,
# circa version 3.7-ish… PyPy seems to omit them as of v7.1.1, under its
# Python 3.6-compatible interpreter build:

callable_types += attrs(types, 'Coroutine',
                               'ClassMethodDescriptor',
                               'MemberDescriptor',
                               'MethodDescriptor',
                               'MethodWrapper',
                               'WrapperDescriptor')

# PREDICATE FUNCTIONS: is<something>() unary-predicates, many of which make use
# of the aforementioned typelists:

# Path types:
ispathtype  = lambda cls: issubclass(cls, path_types)
ispath      = lambda thing: subclasscheck(thing, path_types) or haspyattr(thing, 'fspath')
isnotpath   = negate(ispath)
isvalidpath = lambda thing: ispath(thing) and os.path.exists(os.path.expanduser(thing))

# Abstract items and context managers:
isabstractmethod = lambda method: getpyattr(method, 'isabstractmethod', False)
isabstract = lambda thing: bool(pyattr(thing, 'abstractmethods', 'isabstractmethod'))
isabstractcontextmanager = lambda cls: subclasscheck(cls, contextlib.AbstractContextManager)
iscontextmanager = lambda cls: allpyattrs(cls, 'enter', 'exit') or isabstractcontextmanager(cls)

# Enum and enum alias types:
isaliasdescriptor = lambda thing: isinstance(thing, alias)
hasmembers = lambda thing: isenum(thing) and haspyattr(thing, 'members')
hasaliases = lambda thing: isenum(thing) and haspyattr(thing, 'aliases')

# MappingView → KeysView, ValuesView, ItemsView types –
# These predicates work for the extension types returned by e.g. {}.keys():
isview       = lambda thing: subclasscheck(thing, collections.abc.MappingView)
iskeysview   = lambda thing: isinstance(thing,    collections.abc.KeysView)
isvaluesview = lambda thing: isinstance(thing,    collections.abc.ValuesView)
isitemsview  = lambda thing: isinstance(thing,    collections.abc.ItemsView)

isabc = lambda thing: metaclasscheck(thing, abc.ABCMeta)
isslottedtype = lambda thing: metaclasscheck(thing, Slotted)
isextensibletype = lambda thing: metaclasscheck(thing, Extensible)

# Typelist predicates:
isnumber = lambda thing: subclasscheck(thing, numeric_types)
isnumeric = lambda thing: subclasscheck(thing, numeric_types)
iscomplex = lambda thing: subclasscheck(thing, complex)
ismapping = lambda thing: subclasscheck(thing, mapping_classes)
isarray = lambda thing: subclasscheck(thing, array_types)
isscalar = lambda thing: subclasscheck(thing, scalar_types)
isstring = lambda thing: subclasscheck(thing, string_types)
isbytes = lambda thing: subclasscheck(thing, bytes_types)
ismodule = lambda thing: subclasscheck(thing, types.Module)
isfunction = ΛΛ = lambda thing: isinstance(thing, Λ) and nopyattr(thing, 'mro')
islambda = λλ = lambda thing: pyattr(thing, 'lambda_name', 'name', 'qualname') in (λ, φ)
iscallable = lambda thing: haspyattr(thing, 'call') and nopyattr(thing, 'code')
iscallabletype = lambda thing: isinstance(thing, callable_types) and nopyattr(thing, 'mro')
issequence = lambda thing: subclasscheck(thing, collections.abc.Sequence)
ishashable = lambda thing: subclasscheck(thing, collections.abc.Hashable)
issingleton = lambda thing: subclasscheck(thing, SINGLETON_TYPES)

# Helper predicates for composing sequence-based predicates:
isxlist = lambda predicate, thinglist: issequence(thinglist) and predicate_all(predicate, thinglist)
isxtypelist = lambda predicate, thinglist: istypelist(thinglist) and predicate_all(predicate, thinglist)
isxmetatypelist = lambda predicate, thinglist: ismetatypelist(thinglist) and predicate_all(predicate, thinglist)

isabclist = lambda thinglist: isxtypelist(lambda thing: metaclasscheck(thing, abc.ABCMeta), thinglist)

# Typelist list-type predicates (?!)
ispathtypelist = predicate_all(lambda thing: isclasstype(thing) and ispathtype(thing))
ispathlist = predicate_all(ispath)
isvalidpathlist = predicate_all(isvalidpath)

isnumberlist = predicate_all(isnumber)
isnumericlist = predicate_all(isnumeric)
iscomplexlist = predicate_all(iscomplex)
ismappinglist = predicate_all(ismapping)
isarraylist = predicate_all(isarray)
isscalarlist = predicate_all(isscalar)
isstringlist = predicate_all(isstring)
isbyteslist = predicate_all(isbytes)
ismodulelist = predicate_all(ismodule)
isfunctionlist = predicate_all(ΛΛ)
islambdalist = predicate_all(λλ)
iscallablelist = predicate_all(iscallable)
iscallabletypelist = predicate_all(iscallabletype)
issequencelist = predicate_all(issequence)
ishashablelist = predicate_all(ishashable)
issingletonlist = predicate_all(issingleton)

# MODULE EXPORTS:
export(samelength,      name='samelength',  doc="samelength(a, b) → boolean predicate, True if both `len(a)` and `len(b)` are defined and equal to each other")
export(differentlength, name='differentlength', doc="differentlength(a, b) → boolean predicate, True if both `len(a)` and `len(b)` are defined, but are unequal")
export(isunique,        name='isunique',    doc="isunique(thing) → boolean predicate, True if `thing` is an iterable with unique contents")
export(istypelist,      name='istypelist',  doc="istypelist(thing) → boolean predicate, True if `thing` is a “typelist” – a list consisting only of class types")
export(ismetatypelist,  name='ismetatypelist',
                         doc="ismetatypelist(thing) → boolean predicate, True if `thing` is a “metatypelist” – a list consisting only of metaclass types")
export(maketypelist,    name='maketypelist',
                         doc="maketypelist(iterable) → convert an iterable of unknown things into a uniquified typelist – a list consisting only of class types")
export(makemetatypelist, name='makemetatypelist',
                         doc="makemetatypelist(iterable) → convert an iterable of unknown things into a uniquified metatypelist – a list consisting only of metaclass types")

export(subclasscheck,   name='subclasscheck',
                         doc="subclasscheck(putative, *cls_or_tuple) → A wrapper for `issubclass(…)` and `isinstance(…)` that tries to work with you")

export(metaclasscheck,  name='metaclasscheck',
                         doc="metaclasscheck(putative, *cls_or_tuple) → A wrapper for `issubclass(…)` and `isinstance(…)` that specifically inspects the metaclass of its primary operand")

export(graceful_issubclass,
                        name='graceful_issubclass')


# NO DOCS ALLOWED:
export(numeric_types,   name='numeric_types')
export(array_types,     name='array_types')
export(scalar_types,    name='scalar_types')
export(string_types,    name='string_types')
export(bytes_types,     name='bytes_types')
export(path_classes,    name='path_classes')
export(path_types,      name='path_types')
export(file_types,      name='file_types')
export(dict_types,      name='dict_types')
export(mapping_types,   name='mapping_types')
export(mapping_classes, name='mapping_classes')
export(function_types,  name='function_types')
export(Λ,               name='Λ')
export(callable_types,  name='callable_types')

export(ispathtype,      name='ispathtype',  doc="ispathtype(thing) → boolean predicate, True if `thing` is a path type")
export(ispath,          name='ispath',      doc="ispath(thing) → boolean predicate, True if `thing` seems to be a path-ish instance")
export(isnotpath,       name='isnotpath',   doc="isnotpath(thing) → boolean predicate, True if `thing` seems not to be a path-ish instance")
export(isvalidpath,     name='isvalidpath', doc="isvalidpath(thing) → boolean predicate, True if `thing` represents a valid path on the filesystem")

export(isabstractmethod,                    doc="isabstractmethod(thing) → boolean predicate, True if `thing` is a method declared “abstract” with `@abc.abstractmethod`")
export(isabstract,                          doc="isabstract(thing) → boolean predicate, True if `thing` is an abstract method OR an “abstract base class” (née ABC)")
export(isabstractcontextmanager,            doc="isabstractcontextmanager(thing) → boolean predicate, True if `thing` decends from `contextlib.AbstractContextManager`")
export(iscontextmanager,                    doc="iscontextmanager(thing) → boolean predicate, True if `thing` is a context manager (either abstract or concrete)")

export(isaliasdescriptor,                       name='isaliasdescriptor',
                                                doc="isaliasdescriptor(thing) → boolean predicate, returns True if `thing` is an aliasing descriptor bound to an existing Enum member")
export(hasmembers,      name='hasmembers',      doc="hasmembers(cls) → boolean predicate, True if `cls` descends from Enum and has 1+ items in its `__members__` dict")
export(hasaliases,      name='hasaliases',      doc="hasaliases(cls) → boolean predicate, True if `cls` descends from Enum and has 1+ items in its `__aliases__` dict")

export(isview,          name='isview',          doc="isview(thing) → boolean predicate, True if `thing` is any sort of mapping view instance – keys, values, or items")
export(iskeysview,      name='iskeysview',      doc="iskeysview(thing) → boolean predicate, True if `thing` is a mapping-keys view instance")
export(isvaluesview,    name='isvaluesview',    doc="isvaluesview(thing) → boolean predicate, True if `thing` is a mapping-values view instance")
export(isitemsview,     name='isitemsview',     doc="isitemsview(thing) → boolean predicate, True if `thing` is a mapping-items view instance")

export(isabc,           name='isabc',           doc="isabc(thing) → boolean predicate, True if `thing` is an abstract base class (née ‘ABC’) or a descendant or instance of same")
export(isslottedtype,   name='isslottedtype',   doc="isslottedtype(thing) → boolean predicate, True if `thing` has “clu.exporting.Slotted” as its metaclass")
export(isextensibletype,    name='isextensibletype',
                             doc="isextensibletype(thing) → boolean predicate, True if `thing` is an “extensible” type (q.v. “clu.extending” source supra.)")

export(isnumber,        name='isnumber',    doc="isnumber(thing) → boolean predicate, True if `thing` is a numeric type or an instance of same")
export(isnumeric,       name='isnumeric',   doc="isnumeric(thing) → boolean predicate, True if `thing` is a numeric type or an instance of same")
export(iscomplex,       name='iscomplex',   doc="iscomplex(thing) → boolean predicate, True if `thing` is a complex numeric type or an instance of same")
export(ismapping,       name='ismapping',   doc="ismapping(thing) → boolean predicate, True if `thing` is a mapping (dict-ish) type or an instance of same")
export(isarray,         name='isarray',     doc="isarray(thing) → boolean predicate, True if `thing` is an array type or an instance of same")
export(isscalar,        name='isscalar',    doc="isscalar(thing) → boolean predicate, True if `thing` is a numpy scalar numeric type or an instance of same")
export(isstring,        name='isstring',    doc="isstring(thing) → boolean predicate, True if `thing` is a string type or an instance of same")
export(isbytes,         name='isbytes',     doc="isbytes(thing) → boolean predicate, True if `thing` is a bytes-like type or an instance of same")
export(ismodule,        name='ismodule',    doc="ismodule(thing) → boolean predicate, True if `thing` is a module type or an instance of same")
export(isfunction,      name='isfunction',  doc="isfunction(thing) → boolean predicate, True if `thing` is of a callable function type")
export(ΛΛ,              name='ΛΛ',          doc="ΛΛ(thing) → boolean predicate, True if `thing` is of a callable function type")
export(islambda,        name='islambda',    doc="islambda(thing) → boolean predicate, True if `thing` is a function created with the «lambda» keyword")
export(λλ,              name='λλ',          doc="λλ(thing) → boolean predicate, True if `thing` is a function created with the «lambda» keyword")
export(iscallable,      name='iscallable',  doc="iscallable(thing) → boolean predicate, True if `thing` is a callable type (a class with a “__call__” method) or an instance of same\n\n"
                                                "N.B. this predicate is *NOT* the same as the built-in “callable(…)” predicate")
export(iscallabletype,  name='iscallabletype',  doc="iscallabletype(thing) → boolean predicate, True if `thing` is one of the predefined callable types (q.v. “clu.typology.callable_types” supra.)")
export(issequence,      name='issequence',  doc="issequence(thing) → boolean predicate, True if `thing` is a sequence type (e.g. a `tuple` or `list` type)")
export(ishashable,      name='ishashable',  doc="ishashable(thing) → boolean predicate, True if `thing` can be hashed, via the builtin `hash(…)` function")
export(issingleton,     name='issingleton', doc="issingleton(thing) → boolean predicate, True if `thing` is one of the “singleton” types: True, False, None, Ellipsis (aka “...”) or NotImplemented")

export(isxlist,         name='isxlist',     doc="isxlist(predicate, thinglist) → boolean predicate, True if `thinglist` is a sequence of items, all of which match the predicate function")
export(isxtypelist,     name='isxtypelist', doc="isxtypelist(predicate, thinglist) → boolean predicate, True if `thinglist` is a typelist, all types in which match the predicate function")
export(isxmetatypelist, name='isxmetatypelist',
                         doc="isxmetatypelist(predicate, thinglist) → boolean predicate, True if `thinglist` is a metatypelist, all types in which match the predicate function")
export(isabclist,       name='isabclist' ,      doc="isabclist(thinglist) → boolean predicate, True if `thinglist` is a sequence of abstract base classes (née ABCs)")

export(ispathtypelist,  name='ispathtypelist',  doc="ispathtypelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of path-related class types")
export(ispathlist,      name='ispathlist',      doc="ispathlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of path-like instances")
export(isvalidpathlist, name='isvalidpathlist', doc="isvalidpathlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of valid filesystem path instances")

export(isnumberlist,    name='isnumberlist',    doc="isnumberlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numeric types")
export(isnumericlist,   name='isnumericlist',   doc="isnumericlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numeric types")
export(iscomplexlist,   name='iscomplexlist',   doc="iscomplexlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of complex numeric types")
export(ismappinglist,   name='ismappinglist',   doc="ismappinglist(thinglist) → boolean predicate, True if `thinglist` is a sequence of mapping (dict-ish) types")
export(isarraylist,     name='isarraylist',     doc="isarraylist(thinglist) → boolean predicate, True if `thinglist` is a sequence of array types")
export(isscalarlist,    name='isscalarlist',    doc="isscalarlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of numpy scalar numeric types")
export(isstringlist,    name='isstringlist',    doc="isstringlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of string types")
export(isbyteslist,     name='isbyteslist',     doc="isbyteslist(thinglist) → boolean predicate, True if `thinglist` is a sequence of bytes-like types")
export(ismodulelist,    name='ismodulelist',    doc="ismodulelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of module types")
export(isfunctionlist,  name='isfunctionlist',  doc="isfunctionlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of callable function types")
export(islambdalist,    name='islambdalist',    doc="islambdalist(thinglist) → boolean predicate, True if `thinglist` is a sequence of functions created with the «lambda» keyword")
export(iscallablelist,  name='iscallablelist',  doc="iscallablelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of callable types (class types with “__call__” methods or instances of same)")
export(iscallabletypelist,  name='iscallabletypelist',  doc="iscallabletypelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of predefined callable types (q.v. “clu.typology.callable_types” supra.)")
export(issequencelist,  name='issequencelist',  doc="issequencelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of sequence types")
export(ishashablelist,  name='ishashablelist',  doc="ishashablelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of things that can be hashed, via the builtin `hash(…)` function")
export(issingletonlist, name='issingletonlist', doc="issingletonlist(thinglist) → boolean predicate, True if `thinglist` is a sequence of things that are amongst the “singleton” types: True, False, None, Ellipsis (aka “...”) or NotImplemented")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
