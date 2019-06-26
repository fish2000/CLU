# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import partial

from constants import Enum, unicode

# PREDICATE FUNCTIONS: boolean predicates for class types

ismetaclass = lambda thing: hasattr(thing, '__mro__') and \
                                len(thing.__mro__) > 1 and \
                                    thing.__mro__[-2] is type

isclass = lambda thing: (thing is object) or (hasattr(thing, '__mro__') and \
                         thing.__mro__[-1] is object and \
                         thing.__mro__[-2] is not type)

isclasstype = lambda thing: hasattr(thing, '__mro__') and \
                                    thing.__mro__[-1] is object

# PREDICATE FUNCTIONS: hasattr(…) shortcuts:

haspyattr = lambda thing, atx: hasattr(thing, '__%s__' % atx)
anyattrs = lambda thing, *attrs: any(hasattr(thing, atx) for atx in attrs)
allattrs = lambda thing, *attrs: all(hasattr(thing, atx) for atx in attrs)
anypyattrs = lambda thing, *attrs: any(haspyattr(thing, atx) for atx in attrs)
allpyattrs = lambda thing, *attrs: all(haspyattr(thing, atx) for atx in attrs)

# Things with a __len__(…) method “have length”:
haslength = lambda thing: haspyattr(thing, 'len')

# Things with either __iter__(…) OR __getitem__(…) are iterable:
isiterable = lambda thing: anypyattrs(thing, 'iter', 'getitem')

# q.v. `merge_two(…)` implementation sub.
ismergeable = lambda thing: bool(hasattr(thing, 'get') and isiterable(thing))

# ACCESSORS: getattr(…) shortcuts:

always = lambda thing: True
never = lambda thing: False
nuhuh = lambda thing: None

no_op = lambda thing, atx, default=None: thing
or_none = lambda thing, atx: getattr(thing, atx, None)
getpyattr = lambda thing, atx, default=None: getattr(thing, '__%s__' % atx, default)
getitem = lambda thing, itx, default=None: getattr(thing, 'get', no_op)(itx, default)

accessor = lambda function, thing, *attrs: ([atx for atx in (function(thing, atx) \
                                                 for atx in attrs) \
                                                 if atx is not None] or [None]).pop(0)

searcher = lambda function, xatx, *things: ([atx for atx in (function(thing, xatx) \
                                                 for thing in things) \
                                                 if atx is not None] or [None]).pop(0)

attr = lambda thing, *attrs: accessor(or_none, thing, *attrs)
pyattr = lambda thing, *attrs: accessor(getpyattr, thing, *attrs)
item = lambda thing, *items: accessor(getitem, thing, *items)

attr_search = lambda atx, *things: searcher(or_none, atx, *things)
pyattr_search = lambda atx, *things: searcher(getpyattr, atx, *things)
item_search = lambda itx, *things: searcher(getitem, itx, *things)

# ENUM PREDICATES: `isenum(…)` predicate; `enumchoices(…)` to return a tuple
# of strings naming an enum’s choices (like duh)

def isenum(cls):
    """ isenum(cls) → boolean predicate, True if cls descends from Enum. """
    if not isclasstype(cls):
        return False
    return Enum in cls.__mro__

def enumchoices(cls):
    """ isenum(cls) → Return a tuple of strings naming the members of an Enum class. """
    if not isenum(cls):
        return tuple()
    return tuple(choice.name for choice in cls)

# PREDICATE LOGCIAL FUNCTIONS: all/any/and/or/xor shortcuts:

predicate_nop = lambda *things: None
function_nop = lambda iterable: None

uncallable = lambda thing: not callable(thing)
pyname = lambda thing: pyattr(thing, 'qualname', 'name')

isexpandable = lambda thing: isinstance(thing, (tuple, list, set, frozenset,
                                                map, filter, reversed) or isenum(thing))

isnormative = lambda thing: isinstance(thing, (str, unicode, bytes, bytearray))
iscontainer = lambda thing: isiterable(thing) and \
                        not isnormative(thing) and \
                        not isclasstype(thing)

def apply_to(predicate, function, *things):
    """ apply_to(predicate, function, *things) → Apply a predicate to each
        of the things, and finally a function to the entirety of the things,
        returning as that function returns.
        
        apply_to(predicate, function) → Return a partial† function ƒ(*things)
        that will behave as `apply_to(predicate, function, *things)` when it
        is called as above.
        
        † q.v. `functools.partial(…)` standard-library module function supra.
    """
    # Ensure both the predicate and function are callable:
    if any(uncallable(f) for f in (predicate, function)):
        names = tuple(pyname(f) for f in (predicate, function))
        raise ValueError("Noncallable passed to apply_to(%s, %s, …)" % names)
    if len(things) < 1:
        # Return a partial for this predicate and function:
        return partial(apply_to, predicate, function)
    elif len(things) == 1:
        # Recursive call, expanding the one argument:
        if isexpandable(things[0]):
            return apply_to(predicate, function, *things[0])
        if iscontainer(things[0]):
            return apply_to(predicate, function, *tuple(things[0]))
    # Actually do the thing:
    return function(predicate(thing) for thing in things)

# Variadics:
predicate_all = lambda predicate, *things: apply_to(predicate, all, *things)
predicate_any = lambda predicate, *things: apply_to(predicate, any, *things)

# Booleans:
predicate_and = lambda predicate, a, b: apply_to(predicate, all, a, b)
predicate_or  = lambda predicate, a, b: apply_to(predicate, any, a, b)
predicate_xor = lambda predicate, a, b: apply_to(predicate, any, a, b) and \
                                    not apply_to(predicate, all, a, b)

# Does a thing or a class contain an attribute --
# whether it uses `__dict__` or `__slots__` (or both)?
thing_has = lambda thing, atx: predicate_any(
            lambda thing: atx in (pyattr(thing, 'dict', 'slots')),
                   thing, *getpyattr(type(thing), 'mro'))

class_has = lambda cls, atx: isclasstype(cls) and thing_has(cls, atx)

# Is this a thing based on a `__dict__`, or one using `__slots__`?
isslotted = lambda thing: haspyattr(thing, 'slots') and not isclasstype(thing)
isdictish = lambda thing: haspyattr(thing, 'dict') and not isclasstype(thing)
isslotdicty = lambda thing: allpyattrs(thing, 'slots', 'dict') and not isclasstype(thing)

# For sorting with ALL_CAPS stuff first or last:
case_sort = lambda c: c.lower() if c.isupper() else c.upper()

# UTILITY FUNCTIONS: helpers for builtin container types:

def tuplize(*items):
    """ Return a new tuple containing all non-`None` arguments """
    return tuple(item for item in items if item is not None)

def uniquify(*items):
    """ Return a tuple with a unique set of all non-`None` arguments """
    return tuple(frozenset(item for item in items if item is not None))

def listify(*items):
    """ Return a new list containing all non-`None` arguments """
    return list(item for item in items if item is not None)

__all__ = ('ismetaclass', 'isclass', 'isclasstype',
           'haspyattr', 'anyattrs', 'allattrs', 'anypyattrs', 'allpyattrs',
           'haslength',
           'isiterable', 'ismergeable',
           'always', 'never', 'nuhuh',
           'no_op', 'or_none',
           'getpyattr', 'getitem',
           'accessor', 'searcher',
           'attr', 'pyattr', 'item',
           'attr_search', 'pyattr_search', 'item_search',
           'isenum', 'enumchoices',
           'predicate_nop', 'function_nop', 'uncallable',
           'isexpandable', 'isnormative', 'iscontainer',
           'apply_to',
           'predicate_all', 'predicate_any',
           'predicate_and', 'predicate_or', 'predicate_xor',
           'thing_has', 'class_has',
           'isslotted', 'isdictish', 'isslotdicty',
           'case_sort',
           'tuplize', 'uniquify', 'listify')

__dir__ = lambda: list(__all__)