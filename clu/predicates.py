# -*- coding: utf-8 -*-
from __future__ import print_function

from constants import Enum

# UTILITY FUNCTIONS: boolean predicates for class types

ismetaclass = lambda thing: hasattr(thing, '__mro__') and \
                                len(thing.__mro__) > 1 and \
                                    thing.__mro__[-2] is type

isclass = lambda thing: (thing is object) or (hasattr(thing, '__mro__') and \
                         thing.__mro__[-1] is object and \
                         thing.__mro__[-2] is not type)

isclasstype = lambda thing: hasattr(thing, '__mro__') and \
                                    thing.__mro__[-1] is object

# UTILITY FUNCTIONS: hasattr(…) shortcuts:

haspyattr = lambda thing, atx: hasattr(thing, '__%s__' % atx)
anyattrs = lambda thing, *attrs: any(hasattr(thing, atx) for atx in attrs)
allattrs = lambda thing, *attrs: all(hasattr(thing, atx) for atx in attrs)
anypyattrs = lambda thing, *attrs: any(haspyattr(thing, atx) for atx in attrs)
allpyattrs = lambda thing, *attrs: all(haspyattr(thing, atx) for atx in attrs)

# Things with either __iter__(…) OR __getitem__(…) are iterable:
isiterable = lambda thing: anypyattrs(thing, 'iter', 'getitem')

# q.v. `merge_two(…)` implementation sub.
ismergeable = lambda thing: bool(hasattr(thing, 'get') and isiterable(thing))

# UTILITY FUNCTIONS: getattr(…) shortcuts:

always = lambda thing: True
never = lambda thing: False
nuhuh = lambda thing: None

no_op = lambda thing, atx, default=None: atx or default
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

# Does a class contain an attribute -- whether it uses `__dict__` or `__slots__`?
thing_has = lambda thing, atx: atx in (pyattr(thing, 'dict', 'slots') or tuple())
class_has = lambda cls, atx: isclasstype(cls) and thing_has(cls, atx)

# Is this a class based on a `__dict__`, or one using `__slots__`?
isslotted = lambda thing: allpyattrs('mro', 'slots')
isdictish = lambda thing: allpyattrs('mro', 'dict')
isslotdicty = lambda thing: allpyattrs('mro', 'slots', 'dict')

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

# ENUM UTILITIES: `isenum(…)` predicate; `enumchoices(…)` to return a tuple
# of strings naming an enum’s choices (like duh)

def isenum(cls):
    """ isenum(cls) → boolean predicate, True if cls descends from Enum. """
    if not hasattr(cls, '__mro__'):
        return False
    return Enum in cls.__mro__

def enumchoices(cls):
    """ isenum(cls) → Return a tuple of strings naming the members of an Enum class. """
    if not isenum(cls):
        return tuple()
    return tuple(choice.name for choice in cls)

__all__ = ('ismetaclass', 'isclass', 'isclasstype',
           'haspyattr', 'anyattrs', 'allattrs', 'anypyattrs', 'allpyattrs',
           'isiterable', 'ismergeable',
           'always', 'never', 'nuhuh',
           'no_op', 'or_none',
           'getpyattr', 'getitem',
           'accessor', 'searcher',
           'attr', 'pyattr', 'item',
           'attr_search', 'pyattr_search', 'item_search',
           'thing_has', 'class_has',
           'isslotted', 'isdictish', 'isslotdicty',
           'case_sort',
           'tuplize', 'uniquify', 'listify',
           'isenum', 'enumchoices')

__dir__ = lambda: list(__all__)