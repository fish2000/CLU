# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps
from importlib.machinery import all_suffixes

import abc
import collections
import collections.abc
import inspect
import itertools
import sys, os
import warnings
import weakref

chain = itertools.chain
iterchain = itertools.chain.from_iterable

from clu.constants.consts import λ, φ, BASEPATH, PROJECT_NAME, NoDefault, pytuple # type: ignore
from clu.constants.exceptions import ExportError, ExportWarning
from clu.constants.polyfills import lru_cache # type: ignore

def doctrim(docstring):
    """ This function is straight outta PEP257 -- q.v. `trim(…)`,
       “Handling Docstring Indentation” subsection sub.:
            https://www.python.org/dev/peps/pep-0257/#id18
    """
    from clu.constants.consts import MAXINT
    
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

def itermodule(module):
    """ Get an iterable of `(name, thing)` tuples for all things
        contained in a given module (although it’ll probably work
        for classes and instances too – anything `dir()`-able.)
    """
    from clu.constants.consts import BUILTINS
    
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

def itermoduleids(module):
    """ Internal function to get an iterable of `(name, id(thing))`
        tuples for all things comntained in a given module – q.v.
        `itermodule(…)` implementation supra.
    """
    from clu.constants.consts import BUILTINS
    
    keys = tuple(key for key in dir(module) \
                      if key not in BUILTINS)
    ids = (id(getattr(module, key)) for key in keys)
    return zip(keys, ids)

# Q.v. `search_by_id(…)` function sub.
cache = lru_cache(maxsize=128, typed=False)

# This goes against all logic and reason, but it fucking seems
# to fix the problem of constants, etc showing up erroneously
# as members of the `__console__` or `__main__` modules –
# a problem which, I should mention, is present in the operation
# of the `pickle.whichmodule(…)` function (!)
sysmods = lambda: reversed(tuple(frozenset(sys.modules.values())))

@cache
def search_by_id(thingID):
    """ Cached function to find the name of a thing, according
        to what it is called in the context of a module in which
        it resides – searching across all currently imported
        modules in entirely, as indicated from the inspection of
        `sys.modules.values()` (which is potentially completely
        fucking enormous).
        
        This function implements `search_for_name(…)` – q.v.
        the calling function code sub., and is also used in the
        implementation of `determine_module(…)`, - also q.v.
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

def search_for_name(thing):
    """ Attempt to find the name for “thing”, using the logic from
        the `search_modules(…)` function, applied to all currently
        imported modules, as indicated from the inspection of
        `sys.modules.values()` (which that, as a search space,
        is potentially fucking enormous).
        
        This function may be called by `determine_name(…)`. Its
        subordinate internal function, `search_by_id(…)`,
        uses the LRU cache from `functools`.
    """
    return search_by_id(id(thing))[1]

def search_for_module(thing):
    """ Attempt to find the module containing “thing”, using the
        logic from the `search_modules(…)` function, applied to
        all currently imported modules, as indicated from the
        inspection of `sys.modules.values()` (which that, as a
        search space, is potentially fucking enormous).
        
        This function may be called by `determine_name(…)`. Its
        subordinate internal function, `search_by_id(…)`,
        uses the LRU cache from `functools`.
    """
    return search_by_id(id(thing))[0]

def search_modules(thing, *modules):
    """ Find the name of a thing, according to what it is called
        in the context of a module in which it resides
    """
    inquestion = id(thing)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for module in frozenset(modules):
            for key, value in itermodule(module):
                if id(value) == inquestion:
                    return module, key
    return None, None

def determine_name(thing, name=None, try_repr=False):
    """ Private module function to find a name for a thing. """
    # Shortcut everything if a name was explictly specified:
    if name is not None:
        return name
    # … or if called without a “thing”:
    if thing is None:
        return None
    # Check for telltale function-object attributes:
    code = None
    if hasattr(thing, '__code__'): # Python 3.x
        code = thing.__code__
    elif hasattr(thing, 'func_code'): # Python 2.x
        code = thing.func_code
    # Use the function’s code object, if found…
    if code is not None:
        # Check for a function wrapper:
        if hasattr(thing, '__wrapped__'):
            return determine_name(thing.__wrapped__)
        if hasattr(code, 'co_name') and \
       not hasattr(thing, '__lambda_name__'):
            name = code.co_name
    # … Otherwise, try the standard name attributes:
    if name is None:
        if hasattr(thing, '__name__'):
            name = thing.__name__
        elif hasattr(thing, '__qualname__'):
            name = thing.__qualname__
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
    return search_for_name(thing)

class rename(object):
    
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
    
    def __call__(self, f):
        function = self.assign_name(f)
        if not inspect.isfunction(function):
            return function
        @wraps(function)
        def renamed(*args, **kwargs):
            return function(*args, **kwargs)
        return function

# N.B. Items in the “replaceable_endings” tuple that
# possibly contain other such items should appear
# *before* the items that they contain, e.g.:
ending_suffixes = tuple(all_suffixes())
ending_prefixes = tuple(f"{os.extsep}{name}" \
                                  for name \
                                   in pytuple('init', 'main'))

replaceable_endings  = tuple(f"{pre}{suf}" \
                            for pre, suf \
                             in itertools.product(ending_prefixes,
                                                  ending_suffixes))
replaceable_endings += ending_suffixes

def path_to_dotpath(path, relative_to=None):
    """ Convert a file path (e.g. “/yo/dogg/iheard/youlike.py”)
        to a dotpath (á la “yo.dogg.iheard.youlike”) in what I
        would call a “quick and dirty” fashion.
        
        Issues a BadDotpathWarning if the converted path contains
        dashes – I don’t quite know what to do about something
        like that besides warn, so erm. There you go.
    """
    from clu.constants.consts import QUALIFIER
    from clu.constants.exceptions import BadDotpathWarning
    
    # Garbage in, garbage out:
    if path is None:
        return None
    
    # Relativize the path to either the “relative_to” arg
    # …or – if that’s not a thing – the filesystem root,
    # and replace slashes with dots:
    relpath = os.path.relpath(path, start=relative_to or "/")
    dotpath = relpath.replace(os.path.sep, QUALIFIER)
    
    # Trim off any remaining “.py” suffixes,
    # and extraneous dot-prefixes:
    for ending in replaceable_endings:
        if dotpath.endswith(ending):
            dotpath = dotpath[:len(dotpath)-len(ending)]
    
    while dotpath.startswith(QUALIFIER):
        dotpath = dotpath[1:]
    
    # Warn before returning, if the converted path
    # should contain dashes:
    if '-' in dotpath:
        warnings.warn(f"Dotpath contains dashes: “{dotpath}”",
                        BadDotpathWarning, stacklevel=2)
    
    return dotpath

class Slotted(abc.ABCMeta):
    
    """ A metaclass that ensures its classes, and all subclasses,
        will be slotted types.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived slotted class.
        """
        if '__slots__' not in attributes:
            attributes['__slots__'] = tuple()
        
        return super(Slotted, metacls).__new__(metacls, name, # type: ignore
                                                        bases,
                                                        attributes,
                                                      **kwargs)

class ValueDescriptor(object):
    
    __slots__ = ('value',)
    
    def __init__(self, value):
        self.value = value
    
    def __get__(self, *args):
        return self.value
    
    def __set__(self, instance, value):
        pass
    
    def __repr__(self):
        from clu.constants.consts import ENCODING
        return isinstance(self.value, str)   and self.value or \
               isinstance(self.value, bytes) and self.value.decode(ENCODING) or \
                                            repr(self.value)

class Prefix(Slotted):
    
    """ A metaclass to assign a “prefix” class property,
        extracted from a “prefix” class keyword, to a new
        slotted type. 
    """
    
    @classmethod
    def __prepare__(metacls, name, bases, prefix="/", **kwargs):
        """ Remove the “prefix” class keyword before calling up """
        return super(Prefix, metacls).__prepare__(name, bases, **kwargs)
    
    def __new__(metacls, name, bases, attributes, prefix="/", **kwargs):
        """ Override for `Slotted.__new__(…)` setting up a
            derived slotted class that pulls from a “prefix”
            with the requisite methods defined for access.
        """
        if 'prefix' not in attributes:
            attributes['prefix'] = ValueDescriptor(prefix)
        
        return super(Prefix, metacls).__new__(metacls, name,
                                                       bases,
                                                       attributes,
                                                     **kwargs)

# One-off private versions of “ismergeable” and “isstring” – NOT FOR EXPORT:
ismergeable = lambda thing: isinstance(thing, collections.abc.Mapping)
isstring = lambda thing: isinstance(thing, str)

classes = {}
appnames = set()

class Registry(abc.ABC, metaclass=Slotted):
    
    """ A class-registry mixin ancestor type suitable for use
        in the ExporterBase inheritance chain – it uses the
        “clu.exporting.Slotted” metaclass and respects the
        class keywords already in use.
    """
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        if appname:
            appnames.add(appname)
        else:
            appname = determine_name(cls)
        if appname in classes:
            raise TypeError(f"appname already registered: {appname}")
        classes[appname] = cls
        super(Registry, cls).__init_subclass__(**kwargs) # type: ignore
        cls.instances = weakref.WeakValueDictionary()
        cls.appname = ValueDescriptor(appname)
    
    @staticmethod
    def all_appnames():
        """ Return a tuple of all registered appnames """
        return sorted(appnames)
    
    @staticmethod
    def for_appname(appname):
        """ Return a subclass for a registered appname """
        if not appname:
            raise ValueError("appname required")
        if not isstring(appname):
            raise TypeError("class registry access by string keys only")
        return classes[appname]
    
    @staticmethod
    def has_appname(appname):
        """ Check to see if a given appname has a registered subclass """
        return (appname in appnames) and (appname in classes)
    
    @classmethod
    def __class_getitem__(cls, key):
        """ Return a specific registered class from the registry,
            given an “appname”, like e.g:
            
                from clu import exporting
                assert Registry['clu'] is exporting.Exporter
        """
        return cls.for_appname(key)
    
    @staticmethod
    def unregister(appname):
        """ Unregister a previously-registered appname, returning the
            successfully unregistered ExporterBase subclass.
            
            Attempting to unregister the core CLU application’s exporter
            is not allowed and will raise a KeyError.
        """
        if appname == PROJECT_NAME:
            raise KeyError("Can’t unregister the core application exporter")
        cls = classes.pop(appname, None)
        if cls:
            if appname in appnames:
                appnames.remove(appname)
        return cls
    
    @classmethod
    def all_modules(cls):
        return iterchain(modules().values() \
                     for modules in (classes[appname].modules \
                     for appname in cls.all_appnames()))
    
    @classmethod
    def nameof(cls, thing):
        """ Find and return the name of a thing, if that thing
            should be found to reside in one of the exported modules
        """
        return search_modules(thing, *cls.all_modules())[1]
    
    @classmethod
    def moduleof(cls, thing):
        """ Find and return the module for a thing, if that thing
            should be found to reside in one of the exported modules
        """
        return search_modules(thing, *cls.all_modules())[0]

class ExporterBase(collections.abc.MutableMapping, Registry, metaclass=Prefix):
    
    """ The base class for “clu.exporting.Exporter”. Override this
        class in your own project to use the CLU exporting mechanism –
        q.v. “clu.exporting.Exporter” docstring sub.
        
        This class uses the “clu.exporting.Prefix” metaclass, which
        automatically adds a “prefix” class attribute, as well as
        the “clu.exporting.Registry” mixin, which keeps a registry
        containing it and all of its derived subclasses, and furnishes
        the “instances” weak-value dictionary for instance registration.
    """
    
    __slots__ = pytuple('exports', 'weakref') + ('path', 'dotpath')
    
    def __new__(cls, *args, path=None, dotpath=None, **kwargs):
        try:
            instance = super(ExporterBase, cls).__new__(cls, *args, **kwargs) # type: ignore
        except TypeError:
            instance = super(ExporterBase, cls).__new__(cls)
        
        instance.__exports__ = {}
        instance.path = path
        instance.dotpath = path_to_dotpath(path,
             relative_to=cls.prefix) or dotpath
        
        if instance.dotpath is not None:
            cls.instances[instance.dotpath] = instance
        
        return instance
    
    @classmethod
    def __class_getitem__(cls, key):
        """ Return a specific Exporter instance from the registry,
            given a dotted module path, like e.g:
            
                from clu import naming
                assert Exporter['clu.naming'] == naming.exporter
        """
        # N.B. you are theoretically “not supposed” to use the
        # “__class_getitem__” method for anything whatsoever, and
        # just leave it alone unless you are fucking around with
        # “typing” module internals. I say fuck that – a) I have
        # already spent more than enough time fucking around with
        # “typing” shit and I am not interested at this time, and
        # b) it’s too useful a method to give it all up. So deal.
        if not key:
            raise ValueError("instance key required")
        if not isstring(key):
            raise TypeError("instance registry access by string keys only")
        return cls.instances[key]
    
    @classmethod
    def unregister(cls, dotpath):
        """ Unregister a previously-registered ExporterBase instance,
            specified by the dotted path (née “dotpath”) of the module
            in which it is ensconced.
            
            Returns the successfully unregistered instance in question.
        """
        return cls.instances.pop(dotpath, None)
    
    @classmethod
    def modulenames(cls):
        """ Get a sorted list of module names – the keys to the Exporter
            instance registry – that are currently available
        """
        return sorted(cls.instances.keys())
    
    @classmethod
    def modules(cls):
        """ Get a dict of actual modules corresponding to the
            currently registered Exporter instances
        """
        import importlib
        modulenames = cls.modulenames()
        mods = []
        
        for modulename in modulenames:
            mods.append(importlib.import_module(modulename))
        
        return dict(zip(modulenames, mods))
    
    @classmethod
    def nameof(cls, thing):
        """ Find and return the name of a thing, if that thing
            should be found to reside in one of the exported modules
        """
        return search_modules(thing, *cls.modules().values())[1]
    
    @classmethod
    def moduleof(cls, thing):
        """ Find and return the module for a thing, if that thing
            should be found to reside in one of the exported modules
        """
        return search_modules(thing, *cls.modules().values())[0]
    
    def __init__(self, *args, path=None, dotpath=None, **kwargs):
        for arg in args:
            if hasattr(arg, '__exports__'):
                self.__exports__.update(arg.__exports__)
            elif hasattr(arg, '_asdict'):
                self.__exports__.update(arg._asdict())
            elif hasattr(arg, 'to_dict'):
                self.__exports__.update(arg.to_dict())
            else:
                try:
                    d = dict(arg)
                except (TypeError, ValueError):
                    pass
                else:
                    self.__exports__.update(d)
    
    def exports(self):
        """ Get a new dictionary instance filled with the exports. """
        out = {} # type: dict
        out.update(self.__exports__)
        return out
    
    def keys(self):
        """ Get a key view on the exported items dictionary. """
        return self.__exports__.keys()
    
    def values(self):
        """ Get a value view on the exported items dictionary. """
        return self.__exports__.values()
    
    def items(self):
        """ Get a item view on the exported items dictionary. """
        return self.__exports__.items()
    
    def get(self, key, default=NoDefault):
        """ Get and return a value for a key, with an optional default """
        if default is NoDefault:
            return self.__exports__.get(key)
        return self.__exports__.get(key, default)
    
    def pop(self, key, default=NoDefault):
        """ Remove and return a value for a key, with an optional default """
        if default is NoDefault:
            return self.__exports__.pop(key)
        return self.__exports__.pop(key, default)
    
    def update(self, dictish=NoDefault, **updates):
        """ Update the exporter with key/value pairs and/or an iterator;
            q.v. `dict.update(…)` docstring supra.
        """
        if dictish is NoDefault:
            return self.__exports__.update(**updates)
        return self.__exports__.update(dictish, **updates)
    
    messages = {
        'docstr'    : "Can’t set the docstring for thing “%s” of type %s:",
        'noname'    : "Can’t determine a name for lambda: 0x%0x"
    }
    
    def export(self, thing, name=None, doc=None):
        """ Add a function -- or any object, really -- to the export list.
            Exported items will end up wih their names in the modules’
           `__all__` tuple, and will also be named in the list returned
            by the modules’ `__dir__()` function.
            
            It looks better if this method is decoupled from its parent
            instance, to wit:
            
                exporter = Exporter()
                export = exporter.decorator() # q.v. “decorator()” sub.
            
            Use `export` as a decorator to a function definition:
                
                @export
                def yo_dogg(i_heard=None):
                    …
                
            … or manually, to export anything that doesn’t have a name:
                
                yo_dogg = lambda i_heard=None: …
                dogg_heard_index = ( ¬ ) 
                
                export(yo_dogg,             name="yo_dogg")
                export(dogg_heard_index,    name="dogg_heard_index")
            
        """
        # No explict name was passed -- try to determine one:
        named = determine_name(thing, name=name)
        
        # Double-check our determined name and item before stowing:
        if named is None:
            raise ExportError("can’t export an unnamed thing")
        if named in self.__exports__:
            raise ExportError(f"can’t re-export name “{named}”")
        if thing is self.__exports__:
            raise ExportError("can’t export the __exports__ dict directly")
        if thing is self:
            raise ExportError("can’t export an exporter instance directly")
        
        # At this point, “named” is valid -- if we were passed
        # a lambda, try to rename it with either our valid name,
        # or the result of an ID-based search for that lambda:
        if callable(thing) and hasattr(thing, '__name__'):
            dname = getattr(thing, '__name__')
            if dname in (λ, φ):
                if named in (λ, φ):
                    named = search_for_name(thing)
                if named is None:
                    raise ExportError(type(self).messages['noname'] % id(thing))
                thing.__name__ = thing.__qualname__ = named
                thing.__lambda_name__ = dname # To recall the lambda’s genesis
                if dname == φ and self.dotpath is not None:
                    thing.__module__ = str(self.dotpath) # Reset __module__ for phi-types
        
        # If a “doc” argument was passed in, attempt to assign
        # the __doc__ attribute accordingly on the item -- note
        # that this won’t work for e.g. slotted, builtin, or C-API
        # types that lack mutable __dict__ internals (or at least
        # a settable __doc__ slot or established attribute).
        if doc is not None:
            try:
                thing.__doc__ = doctrim(doc)
            except (AttributeError, TypeError):
                typename = determine_name(type(thing))
                warnings.warn(type(self).messages['docstr'] % (named, typename),
                              ExportWarning, stacklevel=2)
        
        # Stow the item in the global __exports__ dict:
        self.__exports__[named] = thing
        
        # Return the thing, unchanged (that’s how we decorate).
        return thing
    
    def decorator(self):
        """ Return a reference to this Exporter instances’ “export”
            method, suitable for use as a decorator, e.g.:
            
                export = exporter.decorator()
                
                @export
                def yodogg():
                    ''' Yo dogg, I heard you like exporting '''
                    …
            
            … This should be done near the beginning of a module,
            to facilitate marking functions and other objects to be
            exported – q.v. the “all_and_dir()” method sub.
        """
        return self.export
    
    def all_tuple(self, *additionals):
        """ For use in module `__all__` tuple definitions """
        return tuple(chain(self.keys(), additionals))
    
    def dir_function(self, *additionals):
        """ Return a list containing the exported module names. """
        return lambda: list(chain(self.keys(), additionals))
    
    def all_and_dir(self, *additionals):
        """ Assign a modules’ __all__ and __dir__ values, e.g.:
            
                __all__, __dir__ = exporter.all_and_dir()
            
            … This should be done near the end of a module, after
            all calls to `exporter.export(…)` (aka @export) have
            been made – q.v. the “decorator()” method supra.
        """
        return self.all_tuple(*additionals), \
               self.dir_function(*additionals)
    
    def dir_and_all(self, *additionals):
        """ Assign a modules’ __dir__ and __all__ values, e.g.:
            
                __dir__, __all__ = exporter.dir_and_all()
            
            … This should be done near the end of a module, after
            all calls to `exporter.export(…)` (aka @export) have
            been made – q.v. the “decorator()” method supra.
        """
        return self.dir_function(*additionals), \
               self.all_tuple(*additionals) # OPPOSITE!
    
    @staticmethod
    def cache_info():
        """ Shortcut to get the CacheInfo namedtuple from the
            cached internal `search_by_id(…)` function,
            which is used in last-resort name lookups made by
            `determine_name(…)` during `export(…)` calls.
        """
        return search_by_id.cache_info()
    
    def __iter__(self):
        yield from iter(self.__exports__.keys())
    
    def __len__(self):
        return len(self.__exports__)
    
    def __contains__(self, key):
        return key in self.__exports__
    
    def __getitem__(self, key):
        return self.__exports__[key]
    
    def __setitem__(self, key, value):
        self.__exports__[key] = value
    
    def __delitem__(self, key):
        del self.__exports__[key]
    
    def __add__(self, operand):
        # On add, old values are not overwritten
        from clu.dicts import merge_two
        if not ismergeable(operand):
            return NotImplemented
        return merge_two(self, operand, cls=type(self))
    
    def __radd__(self, operand):
        # On reverse-add, old values are overwritten
        from clu.dicts import merge_two
        if not ismergeable(operand):
            return NotImplemented
        return merge_two(operand, self, cls=type(self))
    
    def __iadd__(self, operand):
        # On in-place add, old values are updated and replaced
        if not ismergeable(operand):
            return NotImplemented
        self.update(**getattr(operand, '__exports__', operand))
        return self
    
    def __or__(self, operand):
        return self.__add__(operand)
    
    def __ror__(self, operand):
        return self.__radd__(operand)
    
    def __ior__(self, operand):
        return self.__iadd__(operand)
    
    def __bool__(self):
        return len(self.__exports__) > 0
    
    def __dir__(self):
        return list(filter(lambda name: name not in ('all_appnames',
                                                     'all_modules',
                                                     'for_appname',
                                                     'unregister'),
                           super(ExporterBase, self).__dir__()))

class Exporter(ExporterBase, prefix=BASEPATH, appname=PROJECT_NAME):
    
    """ A class representing a list of things for a module to export.
        
        This class is specifically germane to the CLU project – note
        that the “prefix” class keyword is used to assign a value from
        the CLU constants module.
        
        Users of CLU who wish to use the Exporter mechanism in their
        own projects should create a subclass of ExporterBase of their
        own. Like this one, it need only assign the “prefix” class
        keyword; it is unnecessary (but OK!) to define further methods,
        properties, class constants, and whatnot.
        
        When writing your subclass, if you •do• choose to add methods
        or other things, it is imperative that you ensure you aren’t
        accedentally clobbering anything important from ExporterBase,
        or you risk UNDEFINED BEHAVIOR!!!! Erm.
        
        Also note that all derived subclasses of ExporterBase will
        automatically be slotted classes – a “__slots__” attribute
        will be added to the class dict by the “clu.exporting.Slotted”
        metaclass, if your subclass doesn’t define one – and so if
        you desire a class with a working “__dict__” attribute for
        some reason, you’ll need to specify:
        
            __slots__ = tuplize('__dict__')
        
        … in your class (or an equivalent).
    """
    
    pass

exporter = Exporter(path=__file__)
export = exporter.decorator()

export(doctrim)
export(itermodule)
export(moduleids)
export(itermoduleids)
export(search_by_id)
export(search_for_name)
export(search_for_module)
export(search_modules)
export(determine_name)
export(rename)
export(path_to_dotpath)
export(sysmods,         name='sysmods',         doc="sysmods() → shortcut for reversed(tuple(frozenset(sys.modules.values()))) …OK? I know. It’s not my finest work, but it works.")

# NO DOCS ALLOWED:
export(Slotted)
export(ValueDescriptor)
export(Registry)
export(ExporterBase)
export(Exporter)        # hahaaaaa

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    print("» LOCALS:")
    pprint(locals())
    print()
    
    print("» GLOBALS:")
    pprint(globals())
    print()

if __name__ == '__main__':
    test()