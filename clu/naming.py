# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import collections.abc
import importlib
import importlib.machinery
import inspect
import pickle

from clu.constants.consts import λ, φ
from clu.constants.consts import BASEPATH, QUALIFIER, NoDefault

from clu.exporting import (path_to_dotpath, determine_name,
                                            search_for_name,
                                            search_for_module)

from clu.exporting import Exporter, Registry

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def determine_module(thing, name=None):
    """ Private module function to find the module of a thing,
        using “pickle.whichmodule(…)”
    """
    if name is not None:
        return name
    if thing is None:
        return None
    
    return pickle.whichmodule(thing, None) or name # type: ignore

"""
NAME AND MODULE SEARCH FUNCTIONS: the “nameof(…)” and “moduleof(…)”
functions each search through, in order:
  
  1) the object itself for relevant attributes (e.g “__name__”
     or “__module__”) – this is nearly instantaneous;
  
  2) The “clu.exporting” registry of Exporter classes and their
     registered instances – this is very fast, equivalent to an
     iteration over the values in a sequence of dicts;
  
  3) The entirety of all currently loaded module namespaces,
     as per “sys.modules” – this is potentially a large search
     space (the virtualenv I am using now to develop this code
     currently has 1235 unique modules loaded up); we use the
     standard-library “@functools.lru_cache” decorator to
     cache the ID values of the objects for which we search
     to return near-instantaneous results for repeat queries
     without much overhead.

… The “nameof(…)” and “moduleof(…)” functions in “clu.naming”
are intended as a top-level, users-of-CLU-facing API. They each
call functions that are also available to users (like e.g. the
“pyname(…)” and “pymodule(…)” functions from “clu.predicates”
and the eponymous class methods of “clu.exporting.Registry”).

One caveat is that a number of lower-level functions returning
a module for an object will return the actual module instance
itself, rather than a string name or qualified name value.

The functions “determine_name(…)” and “determine_module(…)”,
while exported publicly, are intended as private utilities for
which no guarantees are made about how they work, their arity,
their time complexity, or their very existence.

In general, these functions will work as fast as possible –
near attribute-access speed – for 99.9 percent of use-cases;
the few remainig 0.99 percent will be nearly as fast, and for
that pathological 0.001-percent case… well, that may be an
indication that you need to change something, dogg.
"""

@export
def nameof(thing, default=NoDefault):
    """ Get the name of a thing, according to its attributes,
        how it appears as a registered item in any Exporter
        subclasses, or (failing any of those) as it appears
        in the module in which it appears to be ensconced –
        … optionally specifying a “default” fallback.
    """
    from clu.predicates import pyname
    
    result = pyname(thing) or \
             Registry.nameof(thing) or \
             search_for_name(thing)
    
    if default is NoDefault:
        return dotpath_split(result)[0]
    return dotpath_split(result)[0] or default

@export
def moduleof(thing, default=NoDefault):
    """ Determine in which module a given thing is ensconced,
        and return that modules’ name as a string
        … optionally specifying a “default” fallback.
    """
    from clu.predicates import pymodule
    
    result = pymodule(thing) or \
             determine_name(
                 Registry.moduleof(thing) or \
                 search_for_module(thing)) or \
             determine_module(thing)
    
    if default is NoDefault:
        return result
    return result or default

# MODULE INSPECTOR PREDICATES: determine what undergirds a module object

EXTENSION_SUFFIXES = tuple(suffix.lstrip(QUALIFIER) \
                       for suffix \
                        in importlib.machinery.EXTENSION_SUFFIXES)

isbuiltin = lambda thing: moduleof(thing) == 'builtins'

suffix = lambda filename: QUALIFIER in filename \
            and filename.rpartition(QUALIFIER)[-1] \
             or ''

@export
def isnativemodule(module):
    """ isnativemodule(thing) → boolean predicate, True if `module`
        is a native-compiled (“extension”) module.
        
        Q.v. this fine StackOverflow answer on this subject:
            https://stackoverflow.com/a/39304199/298171
    """
    from clu.predicates import getpyattr
    from clu.typology import ismodule
    
    # Step one: modules only beyond this point:
    if not ismodule(module):
        return False
    
    # Step two: return truly when “__loader__” is set:
    if isinstance(getpyattr(module, 'loader'),
                  importlib.machinery.ExtensionFileLoader):
        return True
    
    # Step three: in leu of either of those indicators,
    # check the module path’s file suffix:
    ext = suffix(inspect.getfile(module))
    return ext in EXTENSION_SUFFIXES

@export
def isnative(thing):
    """ isnative(thing) → boolean predicate, True if `thing`
        comes from a native-compiled (“extension”) module.
    """
    module = moduleof(thing)
    if module == 'builtins':
        return False
    return isnativemodule(
           importlib.import_module(
                            module))

# QUALIFIED-NAME FUNCTIONS: import by qualified name (like e.g. “yo.dogg.DoggListener”),
# assess a thing’s qualified name, etc etc.

@export
def dotpath_join(base, *addenda):
    """ Join dotpath elements together as one, á la os.path.join(…) """
    if base is None or base == '':
        return dotpath_join(*addenda)
    for addendum in addenda:
        if addendum is not None:
            if not base.endswith(QUALIFIER):
                base += QUALIFIER
            if addendum.startswith(QUALIFIER):
                if len(addendum) == 1:
                    raise ValueError(f'operand too short: {addendum}')
                addendum = addendum[1:]
            base += addendum
    # N.B. this might be overthinking it -- 
    # maybe we *want* to allow dotpaths
    # that happen to start and/or end with dots?
    while base.startswith(QUALIFIER):
        base = base[1:]
    while base.endswith(QUALIFIER):
        base = base[:-1]
    return base

@export
def dotpath_split(dotpath):
    """ For a dotted path e.g. `yo.dogg.DoggListener`,
        return a tuple `('DoggListener', 'yo.dogg')`.
        When called with a string containing no dots,
        `dotpath_split(…)` returns `(string, None)`.
    """
    if dotpath is None:
        return None, None
    tail, _, head = str(dotpath).rpartition(QUALIFIER)
    return head, tail or None

@export
def qualified_import(qualified):
    """ Import a qualified thing-name.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    if QUALIFIER not in qualified:
        raise ValueError(f"qualified name required (got {qualified})")
    try:
        imported = importlib.import_module(qualified)
    except ModuleNotFoundError:
        head, tail = dotpath_split(qualified)
        module = importlib.import_module(tail)
        imported = getattr(module, head)
    return imported

@export
def qualified_name_tuple(thing):
    """ Get the thing-name and module/package name for a class or module.
        e.g. ('FloydSteinberg', 'instakit.processors.halftone')
    """
    return nameof(thing), moduleof(thing)

@export
def qualified_name(thing):
    """ Get a qualified thing-name for a thing.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    thing_name, module_name = qualified_name_tuple(thing)
    qualname = dotpath_join(module_name, thing_name)
    return qualname

@export
def dotpath_to_prefix(dotpath, sep='-', end='-'):
    """ Convert a dotted path into a “prefix” string, suitable for
        use with e.g. clu.fs.filesystem.TemporaryDirectory –
        e.g. 'clu.typespace.namespace.SimpleNamespace' becomes:
             'clu-typespace-namespace-simplenamespace-'
    """
    if any(c is None for c in (sep, end)):
        raise ValueError(f"“sep” and “end” must be non-None (sep={sep}, end={end})")
    if not dotpath:
        raise ValueError(f"“dotpath” cannot be None or zero-length (dotpath={dotpath})")
    return dotpath.casefold().replace(QUALIFIER, sep) + end

@export
def path_to_prefix(path, sep='-', end='-', relative_to=BASEPATH):
    """ Shortcut for dotpath_to_prefix(path_to_dotpath(…)) """
    return dotpath_to_prefix(path_to_dotpath(path,
                                             relative_to=relative_to),
                             sep=sep,
                             end=end)

@export
class rename(collections.abc.Callable):
    
    """ Function-rename decorator. Use like so:
        
            @rename(named='yodogg')
            def YoDogg(*args):
                ...
        
        … or:
            
            yodogg = lambda *args: ...
            yodogg = rename()(yodogg) # awkward syntax, I know
        
    """
    
    def __init__(self, named=None,
                        path=None,
                     dotpath=None):
        """ Initialize a @rename object decorator. All parameters are optional. """
        self.named = named
        self.dotpath = dotpath or path_to_dotpath(path,
                                                  relative_to=BASEPATH)
    
    def assign_name(self, function, name=None):
        """ Assign the function’s new name. Returns the mutated function. """
        named = determine_name(function, name=name or self.named)
        dname = getattr(function, '__name__')
        if dname in (λ, φ):
            if named in (λ, φ):
                named = search_for_name(function)
            if named is None:
                raise NameError(str(id(function)))
            function.__name__ = function.__qualname__ = named
            function.__lambda_name__ = dname # To recall the lambda’s genesis
            if dname == φ and self.dotpath is not None:
                function.__module__ = str(self.dotpath) # Reset __module__ for phi-types
        return function
    
    def __call__(self, thing):
        putative = self.assign_name(thing)
        if not inspect.isfunction(putative):
            return putative
        @wraps(putative)
        def renamed(*args, **kwargs):
            return putative(*args, **kwargs)
        return renamed

@export
def duplicate(target, name, gs=None, **attributes):
    """ Make a renamed copy of a target function.
        
        Q.v. pypy/rpython source supra:
            http://bit.ly/func-with-new-name
    """
    from clu.predicates import allpyattrs, pyattr, pyattrs, unwrap
    from clu.typespace import types
    from clu.typology import ΛΛ
    
    # Sanity-check arguments:
    if not ΛΛ(target):
        raise TypeError("“duplicate(…)” requires a function target")
    if not name:
        raise NameError("“duplicate(…)” requires a new function name")
    if not name.isidentifier():
        raise NameError(f"bad name “{name}” passed to “duplicate(…)”")
    
    # For bound methods, delegate the duplication
    # to the underlying function:
    if allpyattrs(target, 'func', 'self'):
        if ΛΛ(pyattr(target, 'func')):
            return duplicate(target.__func__, name, gs=gs, **attributes)
    
    # Create a new function object:
    function = types.Function(target.__code__,
                              gs or target.__globals__,
                              name, target.__defaults__,
                                    target.__closure__)
    
    # Update function dictionary:
    function.__dict__ = { **function.__dict__,
                          **target.__dict__,
                          **attributes }
    
    # Add keyword defaults and/or annotations:
    if target.__annotations__:
        function.__annotations__ = target.__annotations__.copy()
    
    if target.__kwdefaults__:
        function.__kwdefaults__  = target.__kwdefaults__.copy()
    
    # Replace the docstring:
    if target.__doc__:
        function.__doc__         = inspect.getdoc(target)
    
    # Replace only the relevant part of the qualname:
    if allpyattrs(target, 'qualname', 'name'):
        qnm, nm = pyattrs(target, 'qualname', 'name')
        function.__qualname__    = qnm.replace(nm, name)
    
    # Copy the “lambda_name”, if present:
    if pyattr(target, 'lambda_name'):
        function.__lambda_name__ = target.__lambda_name__
    elif target.__name__ in (λ, φ):
        function.__lambda_name__ = target.__name__
    
    # Duplicate the wrapped function, if present:
    if ΛΛ(pyattr(target, 'wrapped')):
        function.__wrapped__ = duplicate(unwrap(target),
                                       f"{name}_target", gs=gs,
                                       **attributes)
    # Return anew:
    return function

@export
def renamer(name, gs=None, **attributes):
    """ A decorator which renames the target function. Usage:
        
            @renamer('yo_dogg')
            def no_dogg():
                # …
        
        Q.v. pypy/rpython source supra:
            http://bit.ly/func-with-new-name
    """
    def decoration(target):
        return duplicate(target, name, gs=gs, **attributes)
    return decoration

@export
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
    abbreviations = [] # type: list
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

export(isbuiltin,      name='isbuiltin',  doc="isbuiltin(thing) → boolean predicate, True if `thing` is a builtin function/method/class")
export(suffix,         name='suffix',     doc="suffix(path) → return the suffix ≠ the file extension ≠ for a file pathname")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
