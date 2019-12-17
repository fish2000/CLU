# -*- coding: utf-8 -*-
from __future__ import print_function
from inspect import getattr_static
from itertools import chain
from functools import partial, wraps

iterchain = chain.from_iterable

from clu.constants.consts import λ, φ, pytuple, NoDefault, QUALIFIER # type: ignore
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# PREDICATE LOGIC: negate(function) will “negate” a boolean predicate function –

assigned = pytuple('doc', 'annotations')
wrap = lambda function: wraps(function, assigned=assigned)

negate = lambda function: wrap(function)(lambda *args, **kwargs: not function(*args, **kwargs))
reverse = lambda function: wrap(function)(lambda *args, **kwargs: reversed(function(*args, **kwargs)))

negate_doc = """
### … You use `negate(function)` thusly:

>>> iscat = lambda thing: thing == 😺
>>> isnotcat = lambda thing: negate(iscat)(thing) # <-- SEE??
>>> iscat(😺)
True
>>> isnotcat(🐇)
True
>>> isnotcat(😺)
False

### … You’ll find that `negate(function)` works great with builtin and stdlib functions:

>>> uncallable = lambda thing: negate(callable)(thing) # see below!
>>> os.path.differentfile = negate(os.path.samefile) # I’ll admit to having done this
>>> misfnmatch = negate(shutil.fnmatch.fnmatch) # There are times when this makes sense
"""

# PREDICATE FUNCTIONS: boolean predicates for class types

ismetaclass = lambda thing: hasattr(thing, '__mro__') and \
                                len(thing.__mro__) > 1 and \
                                    thing.__mro__[-2] is type

isclass     = lambda thing: (thing is object) or (hasattr(thing, '__mro__') and \
                             thing.__mro__[-1] is object and \
                             thing.__mro__[-2] is not type)

isclasstype = lambda thing: hasattr(thing, '__mro__') and \
                                    thing.__mro__[-1] is object

metaclass   = lambda thing: ismetaclass(thing) and thing \
                            or (isclass(thing) and type(thing) \
                            or (type(type(thing))))

# PREDICATE FUNCTIONS: hasattr(…) shortcuts:

hasitem     = lambda thing, itx: itx in thing
noattr      = negate(hasattr) # type: ignore
noitem      = negate(hasitem)

haspyattr   = lambda thing, atx: hasattr(thing, f'__{atx}__')
nopyattr    = negate(haspyattr)

anyitems    = lambda thing, *items: any(hasitem(thing, itx) for itx in items)
allitems    = lambda thing, *items: all(hasitem(thing, itx) for itx in items)
noitems     = negate(anyitems)

anyattrs    = lambda thing, *attrs: any(hasattr(thing, atx) for atx in attrs)
allattrs    = lambda thing, *attrs: all(hasattr(thing, atx) for atx in attrs)
noattrs     = negate(anyattrs)

anypyattrs  = lambda thing, *attrs: any(haspyattr(thing, atx) for atx in attrs)
allpyattrs  = lambda thing, *attrs: all(haspyattr(thing, atx) for atx in attrs)
nopyattrs   = negate(anypyattrs)

# Calling “typeof(…)” on a thing returns either its type, or – if it is
# a classtype – the thing itself:
typeof      = lambda thing: nopyattr(thing, 'mro') and type(thing) or thing

# Things with a __len__(…) method “have length”:
haslength   = lambda thing: haspyattr(thing, 'len')

# Things with either __iter__(…) OR __getitem__(…) are iterable:
isiterable  = lambda thing: anypyattrs(thing, 'iter', 'getitem')

# q.v. `merge_two(…)` implementation sub. –
# this predicate could also be called “isgetitemable()” in terms of
# the implementation of “getitem(…)” as below:
ismergeable = lambda thing: isiterable(thing) and \
                            allpyattrs(thing, 'getitem', 'contains')

# ACCESSORS: getattr(…) shortcuts

always = lambda thing: True
never = lambda thing: False
nuhuh = lambda thing: None

no_op     = lambda thing, atx=None, default=None: thing
or_none   = lambda thing, atx: getattr(thing, atx, None)
stor_none = lambda thing, atx: getattr_static(thing, atx, None)
getpyattr = lambda thing, atx, default=None: getattr(thing, f'__{atx}__', default)
getitem   = lambda thing, itx, default=None: itx in thing and thing[itx] or default
retrieve  = lambda thing, itx, default=None: itx in thing and thing or default

@export
def resolve(thing, atx):
    """ resolve(thing, atx) → retrieve and resolve an attribute, following
        each dotted segment, back from its host thing.
        
        Q.v. the standard library “operator” module notes supra.:
            https://docs.python.org/3/library/operator.html#operator.attrgetter
    """
    for atn in atx.split(QUALIFIER):
        thing = or_none(thing, atn)
    return thing

@export
def stresolve(thing, atx):
    """ stresolve(thing, atx) → statically retrieve and resolve an attribute,
        following each dotted segment, back from its host thing.
        
        Q.v. the standard library “operator” module notes supra.:
            https://docs.python.org/3/library/operator.html#operator.attrgetter
    """
    for atn in atx.split(QUALIFIER):
        thing = stor_none(thing, atn)
    return thing

accessor = lambda function, thing, *attrs, default=None: ([atx for atx in (function(thing, atx) \
                                                               for atx in attrs) \
                                                                if atx is not None] or [default]).pop(0)

acquirer = lambda function, thing, *attrs, default=tuple(): tuple(atx for atx in (function(thing, atx) \
                                                                      for atx in attrs) \
                                                                       if atx is not None) or default

searcher = lambda function, xatx, *things, default=None: ([atx for atx in (function(thing, xatx) \
                                                               for thing in things) \
                                                                if atx is not None] or [default]).pop(0)

collator = lambda function, xatx, *things, default=tuple(): tuple(atx for atx in (function(thing, xatx) \
                                                                      for thing in things) \
                                                                       if atx is not None) or default

attr     = lambda thing, *attrs, default=None: accessor(resolve,   thing, *attrs, default=default)
stattr   = lambda thing, *attrs, default=None: accessor(stresolve, thing, *attrs, default=default)
pyattr   = lambda thing, *attrs, default=None: accessor(getpyattr, thing, *attrs, default=default)
item     = lambda thing, *items, default=None: accessor(getitem,   thing, *items, default=default)

attrs    = lambda thing, *attrs, default=tuple(): acquirer(resolve,   thing, *attrs, default=default)
stattrs  = lambda thing, *attrs, default=tuple(): acquirer(stresolve, thing, *attrs, default=default)
pyattrs  = lambda thing, *attrs, default=tuple(): acquirer(getpyattr, thing, *attrs, default=default)
items    = lambda thing, *items, default=tuple(): acquirer(getitem,   thing, *items, default=default)

attr_search   = lambda atx, *things, default=None: searcher(resolve,   atx, *things, default=default)
stattr_search = lambda atx, *things, default=None: searcher(stresolve, atx, *things, default=default)
pyattr_search = lambda atx, *things, default=None: searcher(getpyattr, atx, *things, default=default)
item_search   = lambda itx, *things, default=None: searcher(getitem,   itx, *things, default=default)

attr_across   = lambda atx, *things, default=tuple(): collator(resolve,   atx, *things, default=default)
stattr_across = lambda atx, *things, default=tuple(): collator(stresolve, atx, *things, default=default)
pyattr_across = lambda atx, *things, default=tuple(): collator(getpyattr, atx, *things, default=default)
item_across   = lambda itx, *things, default=tuple(): collator(getitem,   itx, *things, default=default)

finditem      = lambda itx, *things, default=None:    searcher(retrieve,  itx, *things, default=default)
finditems     = lambda itx, *things, default=tuple(): collator(retrieve,  itx, *things, default=default)

@export
def try_items(itx, *things, default=NoDefault):
    """ try_items(itx, *things[, default]) → attempt to retrieve an item
        from each of the things, in sequence – falling back to a default,
        or raising a KeyError if no default is specified.
        
        This works like “item_search(itx, *things[, default])” – with the
        notable exception that, if any of the things are instances of
        “collections.defaultdict”, “try_items(…)” will correctly trigger
        any “defaultdict” instances’ default factories.
    """
    for thing in things:
        try:
            return thing[itx]
        except KeyError:
            pass
    if default is not NoDefault:
        return default
    raise KeyError(f"{itx} not found in any of things: {things!r}")

# SOME COMMON SHORTCUTS:

dunder_or   = lambda thing, atx: getpyattr(thing, atx, thing)

mro         = lambda thing: getpyattr(typeof(thing), 'mro')
unwrap      = lambda thing: dunder_or(thing, 'wrapped')
origin      = lambda thing: typeof(dunder_or(thing, 'origin'))
rmro        = reverse(mro)

isancestor  = lambda cls, ancestor=object: isclasstype(cls) and (ancestor in mro(cls))
isorigin    = lambda cls, original=object: isclasstype(cls) and isancestor(origin(cls), typeof(original))

newtype     = lambda name, *bases, **attributes: type(name, tuple(bases) or (object,), dict(attributes))

# ENUM PREDICATES: `isenum(…)` predicate; `enumchoices(…)` to return a tuple
# of strings naming an enum’s choices (like duh)

@export
def isenum(cls):
    """ isenum(cls) → boolean predicate, True if cls descends from `Enum`. """
    from clu.constants.polyfills import Enum # type: ignore
    if nopyattr(cls, 'mro'):
        return False
    return Enum in cls.__mro__

@export
def enumchoices(cls):
    """ enumchoices(cls) → Return a tuple of strings naming the members of an `Enum` class. """
    if not isenum(cls):
        return tuple()
    return tuple(choice.name for choice in cls)

# PREDICATE LOGCIAL FUNCTIONS: all/any/and/or/xor shortcuts:

@export
def wrap_value(value):
    """ Get a “lazified” copy of a value, wrapped in a lamba """
    wrapper = lambda *args, **kwargs: value
    wrapper.__wrapped__ = value
    return wrapper

none_function   = predicate_nop = function_nop = wrap_value(None)
true_function   = wrap_value(True)
false_function  = wrap_value(False)

uncallable      = negate(callable) # type: ignore
hoist           = lambda thing: uncallable(thing) and wrap_value(thing) or thing

pyname          = lambda thing: pyattr(thing, 'name', 'qualname')
pymodule        = lambda thing: pyattr(thing, 'module', 'package')

the_expandables = (tuple, list, set, frozenset,
                   map, filter, reversed)

the_normies     = (str, bytes, bytearray)

isexpandable    = lambda thing: isinstance(thing, the_expandables) or isenum(thing) # type: ignore

isnormative     = lambda thing: isinstance(thing, the_normies) or haspyattr(thing, 'fspath')
iscontainer     = lambda thing: isiterable(thing) and \
                            not isnormative(thing) and \
                            not isclasstype(thing)

# HACKITTY HACK HACK HAAAAAAAACK:
isnamespace     = lambda thing: typeof(thing).__name__.endswith('Namespace')

# This is the equivalent of a lambda types’ built-in __repr__ function:
lambda_repr     = lambda instance, default=λ: "<function %s at 0x%0x>" % (pyname(instance) or default,
                                                                              id(instance))

class Partial(partial):
    
    """ A subclass of `functools.partial` designed to be renameable –
        it offers the same `__repr__(…)`-style as lambda-types, and to whose
        `__doc__` value may be mutably written as well.
    """
    
    def __init__(self, *args, **kwargs):
        """ Initialize a new Partial object, with a predicate and a function """
        # N.B. The real action seems to happen in partial.__new__(…)
        # Name the Partial instance, as if it’s a phi-type:
        self.__name__ = self.__qualname__ = φ
        try:
            super(Partial, self).__init__(*args, **kwargs)
        except:
            super(Partial, self).__init__() # type: ignore
    
    @property
    def predicate(self):
        """ Return the “predicate” argument with which this Partial was initialized """
        return (len(self.args) > 0) and self.args[0] or None
    
    @property
    def function(self):
        """ Return the “function” argument with which this Partial was initialized """
        return (len(self.args) > 1) and self.args[1] or None
    
    def __repr__(self):
        # Use the lambda_repr equivalent, with a phi-type default name:
        return lambda_repr(self, default=φ)

@export
def apply_to(predicate, function, *things):
    """ apply_to(predicate, function, *things) → Apply a predicate to each
        of the things, and finally a function to the entirety of the things,
        returning as that function returns. Like e.g.:
        
            function(predicate(thing) for thing in things)
        
        apply_to(predicate, function) → Return a Partial† function ƒ(*things)
        that will behave as `apply_to(predicate, function, *things)` when it
        is called as above.
        
        † q.v. `functools.partial(…)` standard-library module function supra.
    """
    # Ensure both the predicate and function are callable:
    if any(uncallable(f) for f in (predicate, function)):
        names = tuple(pyname(f) for f in (predicate, function))
        raise ValueError("Noncallable passed to apply_to(%s, %s, …)" % names) # type: ignore
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
predicate_all  = lambda predicate, *things: apply_to(predicate, all,         *things)
predicate_any  = lambda predicate, *things: apply_to(predicate, any,         *things)
predicate_none = lambda predicate, *things: apply_to(predicate, negate(any), *things)

# Booleans:
predicate_and  = lambda predicate, a, b: apply_to(predicate, all, a, b)
predicate_or   = lambda predicate, a, b: apply_to(predicate, any, a, b)
predicate_xor  = lambda predicate, a, b: apply_to(predicate, any, a, b) and \
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

# For sorting with ALL_CAPS stuff first or last:
case_sort = lambda c: c.lower() if c.isupper() else c.upper()

# UTILITY FUNCTIONS: helpers for builtin container types:

isnotnone = lambda thing: thing is not None

@export
def itervariadic(function):
    """ Wrap a variadic function – one with the signature “function(•args)” –
        in logic that allows it to be called with a single-argument iterable
        (“function(iterable)”) with the same effect.
        
        Screens out strings, bytes-y, and file-path-ish operands without
        iterating or expanding them.
    """
    @wraps(function)
    def wrapper(*args, expand=True):
        if len(args) == 1 and expand:
            if isexpandable(args[0]):
                return function(*args[0])
            if iscontainer(args[0]):
                return function(*tuple(args[0]))
        return function(*args)
    return wrapper

@export
@itervariadic
def tuplize(*items):
    """ tuplize(*items) → Return a new tuple containing all non-`None` arguments """
    return tuple(item for item in items if item is not None)

@export
@itervariadic
def uniquify(*items):
    """ uniquify(*items) → Return a tuple with a unique set of all non-`None` arguments """
    seen = set() # type: set
    stuff = []
    for item in filter(isnotnone, items):
        if item not in seen:
            seen.add(item)
            stuff.append(item)
    return tuple(stuff)

@export
@itervariadic
def listify(*items):
    """ listify(*items) → Return a new list containing all non-`None` arguments """
    return [item for item in items if item is not None]

@export
@itervariadic
def union(*items):
    """ union(*items) → Return the set-union of the contents of all non-`None` arguments """
    return set().union(item for item in items if item is not None)

# UTILITY ANCESTOR PREDICATES: search through attributes across the MRO of a given type –
# q.v. “resolve” meta-predicate supra.:

ancestral       = lambda atx, cls, default=tuple(): collator(resolve,            atx, *rmro(cls), default=default)
ancestral_union = lambda atx, cls, default=tuple(): uniquify(iterchain(ancestral(atx,       cls,  default=default)))

# UTILITY FUNCTIONS: helpers for builtin predicate functions over iterables:

@export
@itervariadic
def allof(*items):
    """ allof(*items) → Return the result of “all(…)” on all non-`None` arguments """
    return all(item for item in items if item is not None)

@export
@itervariadic
def anyof(*items):
    """ anyof(*items) → Return the result of “any(…)” on all non-`None` arguments """
    return any(item for item in items if item is not None)

@export
@itervariadic
def noneof(*items):
    """ noneof(*items) → Return the result of “not any(…)” on all non-`None` arguments """
    return negate(any)(item for item in items if item is not None)

@export
def slots_for(cls):
    """ slots_for(cls) → get the summation of the `__slots__` tuples for a class and its ancestors """
    # q.v. https://stackoverflow.com/a/6720815/298171
    if nopyattrs(cls, 'mro', 'bases'):
        return slots_for(type(cls))
    mro = pyattr(cls, 'mro', 'bases', default=tuplize(object))
    return tuple(iterchain(
                 getpyattr(ancestor, 'slots', tuple()) \
                       for ancestor in reversed(mro)))

# MODULE EXPORTS:
export(negate,          name='negate',          doc="negate(function) → Negate a boolean function, returning the callable inverse. \n" + negate_doc)
export(reverse,         name='reverse',         doc="reverse(function) → Reverse an iterating function, returning the reverse of the iterable returned.")

export(ismetaclass,     name='ismetaclass',     doc="ismetaclass(thing) → boolean predicate, True if thing is a metaclass, descending directly from `type`")
export(isclass,         name='isclass',         doc="isclass(thing) → boolean predicate, True if thing is a class, descending from `object` but not `type`")
export(isclasstype,     name='isclasstype',     doc="isclasstype(thing) → boolean predicate, True if thing is a class type, descending from either `object` or `type`")
export(metaclass,       name='metaclass',       doc="metaclass(thing) → Returns: a) thing, if thing is a metaclass; b) type(thing), if thing is a class; or c) type(type(thing)), for all other instances")
export(typeof,          name='typeof',          doc="typeof(thing) → Returns thing, if thing is a class type; or type(thing), if it is not")

export(hasitem,         name='hasitem',         doc="hasitem(thing, item) → boolean predicate, shortcut for `item in thing`")
export(noattr,          name='noattr',          doc="noattr(thing, attribute) → boolean predicate, shortcut for `(not hasattr(thing, attribute))`")
export(noitem,          name='noitem',          doc="noitem(thing, item) → boolean predicate, shortcut for `(not hasitem(thing, item))`")

export(haspyattr,       name='haspyattr',       doc="haspyattr(thing, attribute) → boolean predicate, shortcut for `hasattr(thing, '__%s__' % attribute)`")
export(nopyattr,        name='nopyattr',        doc="nopyattr(thing, attribute) → boolean predicate, shortcut for `(not hasattr(thing, '__%s__' % attribute))`")

export(anyitems,        name='anyitems',        doc="anyitems(thing, *items) → boolean predicate, shortcut for `any(hasitem(thing, itx) for itx in items)`")
export(allitems,        name='allitems',        doc="allitems(thing, *items) → boolean predicate, shortcut for `all(hasitem(thing, itx) for itx in items)`")
export(noitems,         name='noitems',         doc="noitems(thing, *items) → boolean predicate, shortcut for `(not anyitems(*attributes)`")

export(anyattrs,        name='anyattrs',        doc="anyattrs(thing, *attributes) → boolean predicate, shortcut for `any(hasattr(thing, atx) for atx in attributes)`")
export(allattrs,        name='allattrs',        doc="allattrs(thing, *attributes) → boolean predicate, shortcut for `all(hasattr(thing, atx) for atx in attributes)`")
export(noattrs,         name='noattrs',         doc="noattrs(thing, *attributes) → boolean predicate, shortcut for `(not anypyattrs(*attributes)`")

export(anypyattrs,      name='anypyattrs',      doc="anypyattrs(thing, *attributes) → boolean predicate, shortcut for `any(haspyattr(thing, atx) for atx in attributes)`")
export(allpyattrs,      name='allpyattrs',      doc="allpyattrs(thing, *attributes) → boolean predicate, shortcut for `all(haspyattr(thing, atx) for atx in attributes)`")
export(nopyattrs,       name='nopyattrs',       doc="nopyattrs(thing, *attributes) → boolean predicate, shortcut for `(not any(haspyattr(thing, atx) for atx in attributes))`")

export(haslength,       name='haslength',       doc="haslength(thing) → boolean predicate, True if `thing` has a “__len__” attribute")
export(isiterable,      name='isiterable',      doc="isiterable(thing) → boolean predicate, True if `thing` can be iterated over")
export(ismergeable,     name='ismergeable',     doc="ismergeable(thing) → boolean predicate, True if `thing` is a valid operand to `merge(…)` or `merge_as(…)`")

export(always,          name='always',          doc="always(thing) → boolean predicate that always returns `True`")
export(never,           name='never',           doc="never(thing) → boolean predicate that always returns `False`")
export(nuhuh,           name='nuhuh',           doc="nuhuh(thing) → boolean predicate that always returns `None`")
export(no_op,           name='no_op',           doc="no_op(thing, attribute[, default]) → shortcut for `(attribute or default)`")
export(or_none,         name='or_none',         doc="or_none(thing, attribute) → shortcut for `getattr(thing, attribute, None)`")
export(stor_none,       name='stor_none',       doc="stor_none(thing, attribute) → shortcut for `inspect.getattr_static(thing, attribute, None)`")
export(getpyattr,       name='getpyattr',       doc="getpyattr(thing, attribute[, default]) → shortcut for `getattr(thing, '__%s__' % attribute[, default])`")
export(getitem,         name='getitem',         doc="getitem(thing, item[, default]) → shortcut for `thing.get(item[, default])`")
export(retrieve,        name='retrieve',        doc="retrieve(thing, item[, default]) → shortcut for `hasitem(thing, itx) and thing or default`")

export(accessor,        name='accessor',        doc="accessor(func, thing, *attributes) → return the first non-None value had by successively applying func(thing, attribute) to all attributes")
export(acquirer,        name='acquirer',        doc="acquirer(func, thing, *attributes) → return all of the non-None values had by successively applying func(thing, attribute) to all attributes")
export(searcher,        name='searcher',        doc="searcher(func, attribute, *things) → return the first non-None value had by successively applying func(thing, attribute) sequentially to all things")
export(collator,        name='collator',        doc="collator(func, attribute, *things) → return all of the non-None values had by successively applying func(thing, attribute) across all things")

export(attr,            name='attr',            doc="attr(thing, *attributes) → Return the first existing attribute from `thing`, given 1+ attribute names")
export(stattr,          name='stattr',          doc="stattr(thing, *attributes) → Statically return the first existing attribute from `thing`, given 1+ attribute names (q.v. “inspect.getattr_static(¬)” supra.)")
export(pyattr,          name='pyattr',          doc="pyattr(thing, *attributes) → Return the first existing __special__ attribute from `thing`, given 1+ attribute names")
export(item,            name='item',            doc="item(thing, *itemnames) → Return the first existing item held by `thing`, given 1+ item names")

export(attrs,           name='attrs',           doc="attrs(thing, *attributes) → Return all of the existing named attributes from `thing`, given 1+ attribute names")
export(stattrs,         name='stattrs',         doc="stattrs(thing, *attributes) → Statically return all of the existing named attributes from `thing`, given 1+ attribute names (q.v. “inspect.getattr_static(¬)” supra.)")
export(pyattrs,         name='pyattrs',         doc="pyattrs(thing, *attributes) → Return all of the existing named __special__ attributes from `thing`, given 1+ attribute names")
export(items,           name='items',           doc="items(thing, *itemnames) → Return all of the existing named items held by `thing`, given 1+ item names")

export(attr_search,     name='attr_search',     doc="attr_search(attribute, *things) → Return the first-found existing attribute from a thing, given 1+ things")
export(stattr_search,   name='stattr_search',   doc="stattr_search(attribute, *things) → Statically return the first-found existing attribute from a thing, given 1+ things (q.v. “inspect.getattr_static(¬)” supra.)")
export(pyattr_search,   name='pyattr_search',   doc="pyattr_search(attribute, *things) → Return the first-found existing __special__ attribute from a thing, given 1+ things")
export(item_search,     name='item_search',     doc="item_search(itemname, *things) → Return the first-found existing item from a thing, given 1+ things")

export(attr_across,     name='attr_across',     doc="attr_across(attribute, *things) → Return all of the existing named attributes across all things (given 1+ things)")
export(stattr_across,   name='stattr_across',   doc="stattr_across(attribute, *things) → Statically return all of the existing named attributes across all things (given 1+ things) (q.v. “inspect.getattr_static(¬)” supra.)")
export(pyattr_across,   name='pyattr_across',   doc="pyattr_across(attribute, *things) → Return all of the existing named __special__ attributes across all things (given 1+ things)")
export(item_across,     name='item_across',     doc="item_across(attribute, *things) → Return all of the existing named items held across all things (given 1+ things)")

export(finditem,        name='finditem',        doc="finditem(itx, *mappings, default=None) → Return the first mapping that contains “itx”, or “default” if “itx” isn’t found in any of them")
export(finditems,       name='finditems',       doc="finditems(itx, *mappings, default=tuple()) → Return a tuple of all mappings that contain “itx”, or “default” if “itx” isn’t found in any of them")

export(dunder_or,       name='dunder_or',       doc="dunder_or(thing, atx) → Like “getpyattr(…)” only with a default return value of `thing` itself")
export(mro,             name='mro',             doc="mro(thing) → Return the method resolution order (née “MRO”) tuple for thing (using “type(thing)” for non-classtype operands)")
export(rmro,            name='rmro',            doc="rmro(thing) → Return the reverse of the method resolution order (née “MRO”) tuple for thing (using “type(thing)” for non-classtype operands)")
export(unwrap,          name='unwrap',          doc="unwrap(thing) → Return either `thing.__wrapped__` or `thing` for a given `thing`")
export(origin,          name='origin',          doc="origin(thing) → Return either `typeof(thing).__origin__` or `typeof(thing)` for a given `thing`")
export(isancestor,      name='isancestor',      doc="isancestor(thing, ancestor=object) → boolean predicate, True if `ancestor` is found in “mro(thing)”")
export(isorigin,        name='isorigin',        doc="isorigin(thing, original=object) → boolean predicate, True if `original` is an ancestor of “origin(thing)”")
export(newtype,         name='newtype',         doc="newtype(name, *bases, **attributes) → Shortcut for “type(name, tuple(bases) or (object,), dict(attributes))”")

export(predicate_nop,   name='predicate_nop',   doc="predicate_nop(thing) → boolean predicate that always returns `None`")
export(function_nop,    name='function_nop',    doc="function_nop(*args) → variadic function always returns `None`")
export(none_function,   name='none_function',   doc="none_function() → A function that always returns None")
export(true_function,   name='true_function',   doc="true_function() → A function that always returns True")
export(false_function,  name='false_function',  doc="false_function() → A function that always returns False")
export(uncallable,      name='uncallable',      doc="uncallable(thing) → boolean predicate, shortcut for `not callable(thing)`")
export(hoist,           name='hoist',           doc="hoist(thing) → if “thing” isn’t already callable, turn it into a lambda that returns it as a value (using “wrap_value(…)”).")
export(pyname,          name='pyname',          doc="pyname(thing) → Return either `__qualname__` or `__name__` from a given `thing`")
export(pymodule,        name='pymodule',        doc="pymodule(thing) → Return either `__module__` or `__package__` from a given `thing`")

export(isexpandable,    name='isexpandable',    doc="isexpandable(thing) → boolean predicate, True if `thing` can be `*expanded`")
export(isnormative,     name='isnormative',     doc="isnormative(thing) → boolean predicate, True if `thing` is a string-like or bytes-like iterable")
export(iscontainer,     name='iscontainer',     doc="iscontainer(thing) → boolean predicate, True if `thing` is iterable and not “normative” (q.v. `isnormative(…)` supra.)")
export(isnamespace,     name='isnamespace',     doc="isnamespace(thing) → boolean predicate, True if the name of the type of “thing” ends with the string “Namespace” (hacky, I know – but functional!)")

export(lambda_repr,     name='lambda_repr',     doc="lambda_repr(instance) → Equivalent to the built-in `__repr__(…)` method of a lambda function")

export(predicate_all,   name='predicate_all',   doc="predicate_all(predicate, *things) → boolean predicate, shortcut for `apply_to(predicate, all, *things)`")
export(predicate_any,   name='predicate_any',   doc="predicate_any(predicate, *things) → boolean predicate, shortcut for `apply_to(predicate, any, *things)`")
export(predicate_none,  name='predicate_none',  doc="predicate_none(predicate, *things) → boolean predicate, shortcut for `apply_to(predicate, negate(any), *things)`")
export(predicate_and,   name='predicate_and',   doc="predicate_and(predicate, a, b) → boolean predicate, shortcut for `apply_to(predicate, all, a, b)`")
export(predicate_or,    name='predicate_or',    doc="predicate_or(predicate, a, b) → boolean predicate, shortcut for `apply_to(predicate, any, a, b)`")
export(predicate_xor,   name='predicate_xor',   doc="predicate_xor(predicate, a, b) → boolean predicate, shortcut for `apply_to(predicate, any, a, b) and not apply_to(predicate, all, a, b)`")

export(case_sort,       name='case_sort',       doc="case_sort(string) → Sorting predicate to sort UPPERCASE names first")
export(isnotnone,       name='isnotnone',       doc="isnotnone(thing) → boolean predicate, return True if “thing” is not None")

export(ancestral,       name='ancestral',       doc="ancestral(atx, cls[, default]) → shortcut for “attr_across(atx, *rmro(cls)[, default])”")
export(ancestral_union, name='ancestral_union', doc="ancestral_union(atx, cls[, default]) → shortcut for “uniquify(iterchain(attr_across(atx, *mro(cls)[, default])))”")

export(thing_has,       name='thing_has',       doc="thing_has(thing, attribute) → boolean predicate, True if `thing` has “attribute” (in either `__dict__` or `__slots__`)")
export(class_has,       name='class_has',       doc="class_has(cls, attribute) → boolean predicate, True if `cls` is a class type and has “attribute” (in either `__dict__` or `__slots__`)")
export(isslotted,       name='isslotted',       doc="isslotted(thing) → boolean predicate, True if `thing` has both an `__mro__` and a `__slots__` attribute")
export(isdictish,       name='isdictish',       doc="isdictish(thing) → boolean predicate, True if `thing` has both an `__mro__` and a `__dict__` attribute")
export(isslotdicty,     name='isslotdicty',     doc="isslotdicty(thing) → boolean predicate, True if `thing` has `__mro__`, `__slots__`, and `__dict__` attributes")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
