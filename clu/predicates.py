# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain
from functools import partial

from clu.constants import PYPY, λ
from clu.constants import Enum, unicode
from clu.enums import alias
from clu.exporting import Exporter

exporter = Exporter()
export = exporter.decorator()

# PREDICATE LOGIC: negate(function) will “negate” a boolean predicate function –

negate = lambda function: (lambda *args, **kwargs: not function(*args, **kwargs))

# … You use `negate(function)` thusly:
# 
# >>> iscat = lambda thing: thing == 😺
# >>> isnotcat = lambda thing: negate(iscat)(thing) # <-- SEE??
# >>> iscat(😺)
# True
# >>> isnotcat(🐇)
# True
# >>> isnotcat(😺)
# False
#
# … You’ll find that `negate(function)` works great with builtin and stdlib functions:
#
# >>> uncallable = lambda thing: negate(callable)(thing) # see below!
# >>> os.path.differentfile = negate(os.path.samefile) # I’ll admit to having done this
# >>> misfnmatch = negate(shutil.fnmatch.fnmatch) # There are times when this makes sense
#

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

no_op     = lambda thing, atx, default=None: thing
or_none   = lambda thing, atx: getattr(thing, atx, None)
getpyattr = lambda thing, atx, default=None: getattr(thing, '__%s__' % atx, default)
getitem   = lambda thing, itx, default=None: getattr(thing, 'get', no_op)(itx, default)

accessor = lambda function, thing, *attrs, default=None: ([atx for atx in (function(thing, atx) \
                                                               for atx in attrs) \
                                                                if atx is not None] or [default]).pop(0)

searcher = lambda function, xatx, *things, default=None: ([atx for atx in (function(thing, xatx) \
                                                               for thing in things) \
                                                                if atx is not None] or [default]).pop(0)

attr   = lambda thing, *attrs, default=None: accessor(or_none,   thing, *attrs, default=default)
pyattr = lambda thing, *attrs, default=None: accessor(getpyattr, thing, *attrs, default=default)
item   = lambda thing, *items, default=None: accessor(getitem,   thing, *items, default=default)

attr_search   = lambda atx, *things, default=None: searcher(or_none,   atx, *things, default=default)
pyattr_search = lambda atx, *things, default=None: searcher(getpyattr, atx, *things, default=default)
item_search   = lambda itx, *things, default=None: searcher(getitem,   itx, *things, default=default)

# ENUM PREDICATES: `isenum(…)` predicate; `enumchoices(…)` to return a tuple
# of strings naming an enum’s choices (like duh)

@export
def isenum(cls):
    """ isenum(cls) → boolean predicate, True if cls descends from Enum. """
    if not isclasstype(cls):
        return False
    return Enum in cls.__mro__

@export
def enumchoices(cls):
    """ enumchoices(cls) → Return a tuple of strings naming the members of an Enum class. """
    if not isenum(cls):
        return tuple()
    return tuple(choice.name for choice in cls)

isaliasdescriptor = lambda thing: isinstance(thing, alias)
hasmembers = lambda thing: isenum(thing) and haspyattr(thing, 'members')
hasaliases = lambda thing: isenum(thing) and haspyattr(thing, 'aliases')

# PREDICATE LOGCIAL FUNCTIONS: all/any/and/or/xor shortcuts:

predicate_nop = lambda *things: None
function_nop = lambda iterable: None

uncallable = lambda thing: negate(callable)(thing)
pyname = lambda thing: pyattr(thing, 'qualname', 'name')

isexpandable = lambda thing: isinstance(thing, (tuple, list, set, frozenset,
                                                map, filter, reversed) or isenum(thing))

isnormative = lambda thing: isinstance(thing, (str, unicode, bytes, bytearray))
iscontainer = lambda thing: isiterable(thing) and \
                        not isnormative(thing) and \
                        not isclasstype(thing)

# This is the equivalent of a lambda types’ built-in __repr__ function:
lambda_repr = lambda instance, default=λ: "<function %s at 0x%0x>" % (pyattr(instance, 'qualname', 'name',
                                                                             default=default),
                                                                          id(instance))

class Partial(partial):
    
    """ A subclass of `functools.partial` designed to be renameable –
        it offers the same `repr`-style as lambda-types, and can have
        its `__doc__` value assigned as well.
    """
    
    def __init__(self, *args, **kwargs):
        """ Initialize a new Partial object """
        # N.B. The real action seems to happen in partial.__new__(…)
        # Name the Partial instance, as if it’s a lambda-type:
        self.__name__ = self.__qualname__ = λ
        if PYPY:
            super(Partial, self).__init__(*args, **kwargs)
            return
        super(Partial, self).__init__()
    
    def __repr__(self):
        # Use the lambda_repr equivalent:
        return lambda_repr(self)

@export
def apply_to(predicate, function, *things):
    """ apply_to(predicate, function, *things) → Apply a predicate to each
        of the things, and finally a function to the entirety of the things,
        returning as that function returns. Like e.g.:
        
            function(predicate(thing) for thing in things)
        
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
        # Return a Partial for this predicate and function:
        return Partial(apply_to, predicate, function)
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
            lambda thing: atx in (pyattr(thing, 'dict', 'slots', default=tuple())),
                   thing, *getpyattr(type(thing), 'mro'))

class_has = lambda cls, atx: isclasstype(cls) and thing_has(cls, atx)

# Is this a thing based on a `__dict__`, or one using `__slots__`?
isslotted = lambda thing: haspyattr(thing, 'slots') and negate(isclasstype)(thing)
isdictish = lambda thing: haspyattr(thing, 'dict') and negate(isclasstype)(thing)
isslotdicty = lambda thing: allpyattrs(thing, 'slots', 'dict') and negate(isclasstype)(thing)

@export
def slots_for(cls):
    """ slots_for(cls) → get the summation of the `__slots__` tuples for a class and its ancestors """
    # q.v. https://stackoverflow.com/a/6720815/298171
    if not isclasstype(cls):
        return tuple()
    return tuple(chain.from_iterable(
                 getpyattr(ancestor, 'slots', tuple()) \
                       for ancestor in cls.__mro__))

# For sorting with ALL_CAPS stuff first or last:
case_sort = lambda c: c.lower() if c.isupper() else c.upper()

# UTILITY FUNCTIONS: helpers for builtin container types:

@export
def tuplize(*items):
    """ tuplize(*items) → Return a new tuple containing all non-`None` arguments """
    return tuple(item for item in items if item is not None)

@export
def uniquify(*items):
    """ uniquify(*items) → Return a tuple with a unique set of all non-`None` arguments """
    return tuple(frozenset(item for item in items if item is not None))

@export
def listify(*items):
    """ listify(*items) → Return a new list containing all non-`None` arguments """
    return list(item for item in items if item is not None)

# MODULE EXPORTS:
export(negate,          name='negate',          doc="negate(function) → Negate a boolean function. Used like: `isnotxxx = lambda thing: negate(isxxx)(thing)`")

export(ismetaclass,     name='ismetaclass',     doc="ismetaclass(thing) → boolean predicate, True if thing is a class, descending from `type`")
export(isclass,         name='isclass',         doc="isclass(thing) → boolean predicate, True if thing is a class, descending from `object`")
export(isclasstype,     name='isclasstype',     doc="isclasstype(thing) → boolean predicate, True if thing is a class, descending from either `object` or `type`")

export(haspyattr,       name='haspyattr',       doc="haspyattr(thing, attribute) → boolean predicate, shortcut for hasattr(thing, '__%s__' % attribute)")
export(anyattrs,        name='anyattrs',        doc="anyattrs(thing, *attributes) → boolean predicate, shortcut for any(hasattr(thing, atx) for atx in attributes)")
export(allattrs,        name='allattrs',        doc="allattrs(thing, *attributes) → boolean predicate, shortcut for all(hasattr(thing, atx) for atx in attributes)")
export(anypyattrs,      name='anypyattrs',      doc="anypyattrs(thing, *attributes) → boolean predicate, shortcut for any(haspyattr(thing, atx) for atx in attributes)")
export(allpyattrs,      name='allpyattrs',      doc="allpyattrs(thing, *attributes) → boolean predicate, shortcut for all(haspyattr(thing, atx) for atx in attributes)")
export(haslength,       name='haslength',       doc="haslength(thing) → boolean predicate, True if thing has a “__len__” attribute")
export(isiterable,      name='isiterable',      doc="isiterable(thing) → boolean predicate, True if thing can be iterated over")
export(ismergeable,     name='ismergeable',     doc="ismergeable(thing) → boolean predicate, True if thing is a valid operand to merge(…) or merge_as(…)")

export(always,          name='always',          doc="always(thing) → boolean predicate that always returns True")
export(never,           name='never',           doc="never(thing) → boolean predicate that always returns False")
export(nuhuh,           name='nuhuh',           doc="nuhuh(thing) → boolean predicate that always returns None")
export(no_op,           name='no_op',           doc="no_op(thing, attribute[, default]) → shortcut for (attribute or default)")
export(or_none,         name='or_none',         doc="or_none(thing, attribute) → shortcut for getattr(thing, attribute, None)")
export(getpyattr,       name='getpyattr',       doc="getpyattr(thing, attribute[, default]) → shortcut for getattr(thing, '__%s__' % attribute[, default])")
export(getitem,         name='getitem',         doc="getitem(thing, item[, default]) → shortcut for thing.get(item[, default])")
export(accessor,        name='accessor',        doc="accessor(func, thing, *attributes) → return the first non-None value had by successively applying func(thing, attribute)")
export(searcher,        name='searcher',        doc="searcher(func, attribute, *things) → return the first non-None value had by successively applying func(thing, attribute)")

export(attr,            name='attr',            doc="attr(thing, *attributes) → Return the first existing attribute from a thing, given 1+ attribute names")
export(pyattr,          name='pyattr',          doc="pyattr(thing, *attributes) → Return the first existing __special__ attribute from a thing, given 1+ attribute names")
export(item,            name='item',            doc="item(thing, *itemnames) → Return the first existing item held by thing, given 1+ item names")
export(attr_search,     name='attr_search',     doc="attr_search(attribute, *things) → Return the first-found existing attribute from a thing, given 1+ things")
export(pyattr_search,   name='pyattr_search',   doc="pyattr_search(attribute, *things) → Return the first-found existing __special__ attribute from a thing, given 1+ things")
export(item_search,     name='item_search',     doc="item_search(itemname, *things) → Return the first-found existing item from a thing, given 1+ things")

export(isaliasdescriptor,
name='isaliasdescriptor',                       doc="isaliasdescriptor(thing) → boolean predicate, returns True if thing is an alias descriptor instance for an enum member")
export(hasmembers,      name='hasmembers',      doc="hasmembers(cls) → boolean predicate, True if cls descends from Enum and has 1+ items in its __members__ dict")
export(hasaliases,      name='hasaliases',      doc="hasaliases(cls) → boolean predicate, True if cls descends from Enum and has 1+ items in its __aliases__ dict")

export(predicate_nop,   name='predicate_nop',   doc="predicate_nop(thing) → boolean predicate that always returns None")
export(function_nop,    name='function_nop',    doc="function_nop(*args) → variadic function always returns None")
export(uncallable,      name='uncallable',      doc="uncallable(thing) → boolean predicate, shortcut for `not callable(thing)`")
export(pyname,          name='pyname',          doc="pyname(thing) → Return either the __qualname__ or __name__ for a given thing")

export(isexpandable,    name='isexpandable',    doc="isexpandable(thing) → boolean predicate, True if thing can be `*expanded`")
export(isnormative,     name='isnormative',     doc="isnormative(thing) → boolean predicate, True if thing is a string-like or bytes-like iterable")
export(iscontainer,     name='iscontainer',     doc="iscontainer(thing) → boolean predicate, True if thing is iterable and not “normative” (q.v. `isnormative(…)` supra.)")

export(lambda_repr,     name='lambda_repr',     doc="lambda_repr(instance) → Equivalent to the built-in __repr__ method of a lambda function")

export(predicate_all,   name='predicate_all',   doc="predicate_all(predicate, *things) → boolean predicate, shortcut for apply_to(predicate, all, *things")
export(predicate_any,   name='predicate_any',   doc="predicate_any(predicate, *things) → boolean predicate, shortcut for apply_to(predicate, any, *things")
export(predicate_and,   name='predicate_and',   doc="predicate_and(predicate, a, b) → boolean predicate, shortcut for apply_to(predicate, all, a, b")
export(predicate_or,    name='predicate_or',    doc="predicate_or(predicate, a, b) → boolean predicate, shortcut for apply_to(predicate, all, a, b")
export(predicate_xor,   name='predicate_xor',   doc="predicate_xor(predicate, a, b) → boolean predicate, shortcut for apply_to(predicate, all, a, b")

export(case_sort,       name='case_sort',       doc="case_sort(string) → Sorting predicate to sort UPPERCASE names first")

export(thing_has,       name='thing_has',       doc="thing_has(thing, attribute) → boolean predicate, True if thing has the attribute (in either __dict__ or __slots__)")
export(class_has,       name='class_has',       doc="class_has(cls, attribute) → boolean predicate, True if cls is a class type and has the attribute (in either __dict__ or __slots__)")
export(isslotted,       name='isslotted',       doc="isslotted(thing) → boolean predicate, True if thing has both an __mro__ and a __slots__ attribute")
export(isdictish,       name='isdictish',       doc="isdictish(thing) → boolean predicate, True if thing has both an __mro__ and a __dict__ attribute")
export(isslotdicty,     name='isslotdicty',     doc="isslotdicty(thing) → boolean predicate, True if thing has __mro__, __slots__, and __dict__ attributes")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
