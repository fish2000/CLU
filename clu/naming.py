# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

import os
import site
import sys
import warnings

from constants import BUILTINS, DEBUG, MAXINT, QUALIFIER
from constants import lru_cache
from predicates import haspyattr, getpyattr, pyattr, uniquify

pytuple = lambda *attrs: tuple('__%s__' % str(atx) for atx in attrs)

def doctrim(docstring):
    """ This function is straight outta PEP257 -- q.v. `trim(…)`,
       “Handling Docstring Indentation” subsection sub.:
            https://www.python.org/dev/peps/pep-0257/#id18
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = MAXINT
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < MAXINT:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

# Q.v. `thingname_search_by_id(…)` function sub.
cache = lru_cache(maxsize=128, typed=False)

# This goes against all logic and reason, but it fucking seems
# to fix the problem of constants, etc showing up erroneously
# as members of the `__console__` or `__main__` modules –
# a problem which, I should mention, is present in the operation
# of the `pickle.whichmodule(…)` function (!)
sysmods = lambda: reversed(uniquify(*sys.modules.values()))

@cache
def thingname_search_by_id(thingID):
    """ Cached function to find the name of a thing, according
        to what it is called in the context of a module in which
        it resides – searching across all currently imported
        modules in entirely, as indicated from the inspection of
        `sys.modules.values()` (which is potentially completely
        fucking enormous).
        
        This function implements `thingname_search(…)` – q.v.
        the calling function code sub., and is also used in the
        implementdation of `determine_module(…)`, - also q.v.
        the calling function code sub.
        
        Caching courtesy the `functools.lru_cache(…)` decorator.
    """
    # Would you believe that the uniquify(…) call is absolutely
    # fucking necessary to use on `sys.modules`?! I checked and
    # on my system, like on all my REPLs, uniquifying the modules
    # winnowed the module list (and therefore, this functions’
    # search space) by around 100 fucking modules (!) every time!!
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for module in sysmods():
            for key, valueID in itermoduleids(module):
                if valueID == thingID:
                    return module, key
    return None, None

def thingname_search(thing):
    """ Attempt to find the name for thing, using the logic from
        the `thingname(…)` function, applied to all currently
        imported modules, as indicated from the inspection of
        `sys.modules.values()` (which that, as a search space,
        is potentially fucking enormous).
        
        This function may be called by `determine_name(…)`. Its
        subordinate internal function, `thingname_search_by_id(…)`,
        uses the LRU cache from `functools`.
    """
    return thingname_search_by_id(id(thing))[1]

def determine_name(thing, name=None, try_repr=False):
    """ Private module function to find a name for a thing. """
    # Shortcut everything if a name was explictly specified:
    if name is not None:
        return name
    # Check for telltale function-object attributes:
    code = None
    if hasattr(thing, '__code__'): # Python 3.x
        code = thing.__code__
    elif hasattr(thing, 'func_code'): # Python 2.x
        code = thing.func_code
    # Use the function’s code object, if found…
    if code is not None:
        if hasattr(code, 'co_name'):
            name = code.co_name
    # … Otherwise, try the standard name attributes:
    else:
        if hasattr(thing, '__qualname__'):
            name = thing.__qualname__
        elif hasattr(thing, '__name__'):
            name = thing.__name__
    # We likely have something by now:
    if name is not None:
        return name
    # If asked to try the thing’s repr, return that:
    if try_repr:
        return repr(thing)
    # LAST RESORT: Search the entire id-space
    # of objects within imported modules -- it is
    # possible (however unlikely) that this’ll ending
    # up returning None:
    return thingname_search(thing)

# MODULE SEARCH FUNCTIONS: iterate and search modules, yielding
# names, thing values, and/or id(thing) values, matching by given
# by thing names or id(thing) values

def itermodule(module):
    """ Get an iterable of `(name, thing)` tuples for all things
        contained in a given module (although it’ll probably work
        for classes and instances too – anything `dir()`-able.)
    """
    keys = tuple(key for key in sorted(dir(module)) \
                      if key not in BUILTINS)
    values = (getattr(module, key) for key in keys)
    return zip(keys, values)

def moduleids(module):
    """ Get a dictionary of `(name, thing)` tuples from a module,
        indexed by the `id()` value of `thing`
    """
    out = {}
    for key, thing in itermodule(module):
        out[id(thing)] = (key, thing)
    return out

def thingname(original, *modules):
    """ Find the name of a thing, according to what it is called
        in the context of a module in which it resides
    """
    inquestion = id(original)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for module in frozenset(modules):
            for key, thing in itermodule(module):
                if id(thing) == inquestion:
                    return key
    return None

def itermoduleids(module):
    """ Internal function to get an iterable of `(name, id(thing))`
        tuples for all things comntained in a given module – q.v.
        `itermodule(…)` implementation supra.
    """
    keys = tuple(key for key in dir(module) \
                      if key not in BUILTINS)
    ids = (id(getattr(module, key)) for key in keys)
    return zip(keys, ids)

def slots_for(cls):
    """ Get the summation of the `__slots__` tuples for a class and its ancestors """
    # q.v. https://stackoverflow.com/a/6720815/298171
    if not haspyattr(cls, 'mro'):
        return tuple()
    return tuple(chain.from_iterable(
                 getpyattr(ancestor, 'slots', tuple()) \
                       for ancestor in cls.__mro__))

def nameof(thing, fallback=''):
    """ Get the name of a thing, according to either:
        >>> thing.__qualname__
        … or:
        >>> thing.__name__
        … optionally specifying a fallback string.
    """
    return determine_name(thing) or fallback

def determine_module(thing):
    """ Determine in which module a given thing is ensconced,
        and return that modules’ name as a string.
    """
    return pyattr(thing, 'module', 'package') or \
           determine_name(
           thingname_search_by_id(id(thing))[0])

# QUALIFIED-NAME FUNCTIONS: import by qualified name (like e.g. “yo.dogg.DoggListener”),
# assess a thing’s qualified name, etc etc.

def path_to_dotpath(path):
    """ Convert a file path (e.g. “/yo/dogg/iheard/youlike.py”)
        to a dotpath (á la “yo.dogg.iheard.youlike”) in what I
        would call a “quick and dirty” fashion.
    """ 
    relpath = os.path.relpath(path,
        start=os.path.dirname('/usr/local/lib/python3.7/site-packages'))
    dotpath = relpath.replace(os.path.sep, QUALIFIER)
    
    if dotpath.endswith('.py'):
        dotpath = dotpath[:len(dotpath)-3]
    while dotpath.startswith(QUALIFIER):
        dotpath = dotpath[1:]
    
    return dotpath

def dotpath_join(base, *addenda):
    """ Join dotpath elements together as one, á la os.path.join(…) """
    if base is None or base == '':
        return dotpath_join(*addenda)
    for addendum in addenda:
        if not base.endswith(QUALIFIER):
            base += QUALIFIER
        if addendum.startswith(QUALIFIER):
            if len(addendum) == 1:
                raise ValueError('operand too short: %s' % addendum)
            addendum = addendum[1:]
        base += addendum
    # N.B. this might be overthinking it -- 
    # maybe we *want* to allow dotpaths
    # that happen to start and/or end with dots?
    if base.endswith(QUALIFIER):
        return base[:-1]
    return base

def dotpath_split(dotpath):
    """ For a dotted path e.g. `yo.dogg.DoggListener`,
        return a tuple `('DoggListener', 'yo.dogg')`.
        When called with a string containing no dots,
        `dotpath_split(…)` returns `(string, None)`.
    """
    head = dotpath.split(QUALIFIER)[-1]
    tail = dotpath.replace("%s%s" % (QUALIFIER, head), '')
    return head, tail != head and tail or None

def qualified_import(qualified):
    """ Import a qualified thing-name.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    import importlib
    if QUALIFIER not in qualified:
        raise ValueError("qualified name required (got %s)" % qualified)
    head, tail = dotpath_split(qualified)
    module = importlib.import_module(tail)
    imported = getattr(module, head)
    if DEBUG:
        print("Qualified Import: %s" % qualified)
    return imported

def qualified_name_tuple(thing):
    """ Get the module/package and thing-name for a class or module.
        e.g. ('instakit.processors.halftone', 'FloydSteinberg')
    """
    return determine_module(thing), \
           dotpath_split(
           determine_name(thing))[0]

def qualified_name(thing):
    """ Get a qualified thing-name for a thing.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    mod_name, cls_name = qualified_name_tuple(thing)
    qualname = dotpath_join(mod_name, cls_name)
    if DEBUG:
        print("Qualified Name: %s" % qualname)
    return qualname

def split_abbreviations(s):
    """ Split a string into a tuple of its unique constituents,
        based on its internal capitalization -- to wit:
        
        >>> split_abbreviations('RGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('CMYK')
        ('C', 'M', 'Y', 'K')
        >>> split_abbreviations('YCbCr')
        ('Y', 'Cb', 'Cr')
        >>> split_abbreviations('sRGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('XYZZ')
        ('X', 'Y', 'Z')
        >>> split_abbreviations('I;16B')
        ('I',)
        
        If you still find this function inscrutable,
        have a look here: https://gist.github.com/4027079
    """
    abbreviations = []
    current_token = ''
    for char in s.split(';')[0]:
        if current_token == '':
            current_token += char
        elif char.islower():
            current_token += char
        else:
            if not current_token.islower():
                if current_token not in abbreviations:
                    abbreviations.append(current_token)
            current_token = ''
            current_token += char
    if current_token != '':
        if current_token not in abbreviations:
            abbreviations.append(current_token)
    return tuple(abbreviations)

__all__ = ('pytuple', 'doctrim',
           'sysmods', 'thingname', 'thingname_search', 'determine_name',
           'itermodule', 'moduleids',
           'slots_for',
           'nameof',
           'determine_module',
           'dotpath_join', 'dotpath_split',
           'qualified_import',
           'qualified_name_tuple',
           'qualified_name',
           'split_abbreviations')

__dir__ = lambda: list(__all__)