# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache
from importlib.machinery import all_suffixes
from pathlib import Path

import abc
import clu.abstract
import collections
import collections.abc
import contextlib
import hashlib
import importlib
import inspect
import itertools
import shelve
import sys, os, re
import warnings
import weakref

abstract = abc.abstractmethod
chain = itertools.chain
iterchain = itertools.chain.from_iterable

from clu.constants.consts import (λ, φ, # type: ignore
                                  APPNAME, BASEPATH, BUILTINS, ENCODING,
                                  EXPORTER_NAME, QUALIFIER, ROOT_PATH,
                                  NoDefault, pytuple)
from clu.constants.exceptions import BadDotpathWarning, ExportError, ExportWarning

# Q.v. `search_by_id(…)` function sub.
cache = lambda function: lru_cache(maxsize=128, typed=False)(function)

# Not what you are looking for
NotYourThing = object()

def itermodule(module):
    """ Get an iterable of `(name, thing)` tuples for all things
        contained in a given module (although it’ll probably work
        for classes and instances too – anything `dir()`-able.)
    """
    # the `getattr(…)` call below uses a default of `NotYourThing`
    # to supress weird bugs that can arise when iterating through
    # the contents of third-party modules that do “clever” things
    # when their module code executes or whatever.
    keys = tuple(key for key in dir(module) \
                      if key not in BUILTINS)
    values = (getattr(module, key, NotYourThing) for key in keys)
    yield from zip(keys, values)

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
    # the `getattr(…)` call below uses a default value of the id
    # of `NotYourThing` to supress weird bugs that can arise when
    # iterating through the contents of third-party modules that
    # do “clever” things when their module code executes or whatever.
    keys = tuple(key for key in dir(module) \
                      if key not in BUILTINS)
    ids = (id(getattr(module, key, NotYourThing)) for key in keys)
    yield from zip(keys, ids)

# This goes against all logic and reason, but it fucking seems
# to fix the problem of constants, etc showing up erroneously
# as members of the `__console__` or `__main__` modules –
# a problem which, I should mention, is present in the operation
# of the `pickle.whichmodule(…)` function (!)
sysmods = lambda: reversed(tuple(frozenset(sys.modules.values())))

class Modulespace(object):
    
    """ Makes top-level python modules available as an attribute,
        importing them on first access.
        
        Q.v. pypy/rpython source supra:
            http://bit.ly/lazy-borg-modulespace
    """
    
    def __init__(self):
        self.__dict__ = sys.modules
    
    def __getattr__(self, key):
        try:
            module = importlib.import_module(key)
        except (ModuleNotFoundError, ImportError) as exc:
            raise AttributeError("could not import module: %s" % key) from exc
        return module

@cache
def search_by_id(thingID):
    """ Cached function to find the name of a thing, according
        to what it is called in the context of a module in which
        it resides – searching across all currently imported
        modules in entirely, as indicated from the inspection of
        `sys.modules.values()` (which is potentially completely
        fucking enormous).
        
        This function helps implement `search_for_name(…)` – q.v.
        the calling function code sub., and is also used in the
        implementation of `search_for_module(…)`, - also q.v.
        the calling function code sub.
        
        Caching courtesy the `functools.lru_cache(…)` decorator.
    """
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
    # N.B. we catch RuntimeErrors and recursively re-attempt the
    # call, retrying as many times as are necessary, due to suprious
    # and infuriating “dict changed size during iteration” errors
    # that certain package modules – whose names I *could* mention here,
    # ahem – are prone to induce during their initial assumptive
    # import-everything tree-walk behavior… UGH.
    try:
        return search_by_id(id(thing))[1]
    except RuntimeError: # pragma: no cover
        return search_for_name(thing)

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
    # N.B. we catch RuntimeErrors and recursively re-attempt the
    # call, retrying as many times as are necessary, due to suprious
    # and infuriating “dict changed size during iteration” errors
    # that certain package modules – whose names I *could* mention here,
    # ahem – are prone to induce during their initial assumptive
    # import-everything tree-walk behavior… UGH.
    try:
        return search_by_id(id(thing))[0]
    except RuntimeError: # pragma: no cover
        return search_for_module(thing)

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

@cache
def stringhash(string):
    """ Expediently hash a string to another string """
    digester = hashlib.sha256()
    digester.update(bytes(string, encoding=ENCODING))
    return digester.hexdigest()

def determine_name(thing, name=None, try_repr=False):
    """ Private module function to find a name for a thing. """
    # Shortcut everything if a name was explictly specified:
    if name is not None:
        return name
    # … or if called without a “thing”:
    if thing is None:
        return None
    # Check for a function wrapper:
    # N.B. when the Walrus hits Python main this’ll be
    # a good spot for one of those:
    if callable(getattr(thing, '__wrapped__', None)):
        return determine_name(thing.__wrapped__)
    # Check for telltale function-object attributes:
    code = None
    if hasattr(thing, '__code__'): # Python 3.x
        code = thing.__code__
    elif hasattr(thing, 'func_code'): # Python 2.x
        code = thing.func_code
    # Use the function’s code object, if found…
    if code is not None:
        if hasattr(code, 'co_name') and \
       not hasattr(thing, '__lambda_name__'):
            name = code.co_name
    # … Otherwise, try the standard name attributes:
    if name is None:
        if hasattr(thing, '__name__'):
            name = thing.__name__
        elif hasattr(thing, '__qualname__'):
            name = thing.__qualname__.rpartition(QUALIFIER)[-1]
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

# Regexp for matching dashes in dotpaths:
dash_re = re.compile("-")

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

def path_to_dotpath(path, relative_to=None,
                          convert_dashes=True):
    """ Convert a file path (e.g. “/yo/dogg/iheard/youlike.py”)
        to a dotpath (á la “yo.dogg.iheard.youlike”) in what I
        would call a “quick and dirty” fashion.
        
        Issues a BadDotpathWarning if the converted path contains
        dashes, and the “convert_datshes” flag is set to False
        – I don’t quite know what to do about something like that
        besides warn, so erm. There you go.
    """
    # Garbage in, garbage out:
    if path is None:
        return None
    
    # Relativize the path to either the “relative_to” arg
    # …or – if that’s not a thing – the filesystem root,
    # and replace path separators with dots:
    relpath = os.path.relpath(path, start=relative_to or ROOT_PATH)
    dotpath = relpath.replace(os.path.sep, QUALIFIER)
    
    # Trim off any remaining “.py” suffixes,
    # and extraneous dot-prefixes:
    for ending in replaceable_endings:
        if dotpath.endswith(ending):
            dotpath = dotpath[:len(dotpath)-len(ending)]
    
    while dotpath.startswith(QUALIFIER):
        dotpath = dotpath[1:]
    
    if '-' in dotpath:
        if convert_dashes:
            # Substitute underscores for any dashes found:
            dotpath = dash_re.subn('_', dotpath)[0]
        else:
            # Warn before returning, if the converted path
            # should contain dashes:
            warnings.warn(f"Dotpath contains dashes: “{dotpath}”",
                            BadDotpathWarning, stacklevel=2)
    
    return dotpath

# One-off private versions of “ismergeable” and “isstring” – NOT FOR EXPORT:
ismergeable = lambda thing: isinstance(thing, collections.abc.Mapping)
isstring = lambda thing: isinstance(thing, str)

# The actual exporter subclass registry datastructures:
classes = weakref.WeakValueDictionary()
appnames = set()

class Registry(abc.ABC, metaclass=clu.abstract.Slotted):
    
    """ A class-registry mixin ancestor type suitable for use
        in the ExporterBase inheritance chain – it uses the
        “clu.abstract.Slotted” metaclass and respects the
        class keywords already in use.
    """
    
    @abstract
    def exports(self):
        """ An abstract method, ensuring Registry types can’t be just
            instantiated willy-nilly. The clu.exporting.ExporterBase
            descendant class implements this method.
        """
        ...
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        if not appname:
            appname = determine_name(cls)
        else:
            if appname in classes:
                raise TypeError(f"appname already registered: {appname}")
            appnames.add(appname)
            classes[appname] = cls
        super().__init_subclass__(**kwargs) # type: ignore
        cls.instances = weakref.WeakValueDictionary()
        cls.appname = clu.abstract.ValueDescriptor(appname)
    
    @staticmethod
    def all_appnames():
        """ Return a generator over all currently registered appnames """
        yield from sorted(appnames)
    
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
            
                >>> from clu import exporting
                >>> assert Registry['clu'] is exporting.Exporter
        """
        return cls.for_appname(key)
    
    @staticmethod
    def unregister(appname):
        """ Unregister a previously-registered appname, returning the
            successfully unregistered ExporterBase subclass.
            
            Attempting to unregister the core CLU application’s exporter
            is not allowed and will raise a KeyError.
        """
        if appname == APPNAME:
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

class ExporterTypeRepr(clu.abstract.BasePath):
    
    """ At the time of writing, type-specific “__repr__(…)” definitions
        require the use of a metaclass – soooooooo…
    """
    
    def __repr__(cls):
        from clu.naming import qualified_name
        appname = getattr(cls, 'appname', None)
        basepath = getattr(cls, 'basepath', None)
        qualname = qualified_name(cls)
        if not appname and not basepath:
            return f"<class “{qualname}”>"
        if not appname:
            return f"<class “{qualname}”, basepath=“{basepath}”>"
        if not basepath:
            return f"<class “{qualname}”, appname=“{appname}”>"
        return f"<class “{qualname}”, appname=“{appname}”, basepath=“{basepath}”>"

class ExporterBase(collections.abc.MutableMapping,
                   clu.abstract.ReprWrapper,
                   contextlib.AbstractContextManager,
                   Registry, metaclass=ExporterTypeRepr):
    
    """ The base class for “clu.exporting.Exporter”. Override this
        class in your own project to use the CLU exporting mechanism –
        q.v. “clu.exporting.Exporter” docstring sub.
        
        This class uses the “clu.abstract.BasePath” metaclass, which
        automatically adds a “basepath” class attribute, as well as
        the “clu.exporting.Registry” mixin, which keeps a registry
        containing it and all of its derived subclasses, and furnishes
        the “instances” weak-value dictionary for instance registration.
    """
    
    __slots__ = pytuple('exports', 'weakref') + ('path', 'dotpath')
    
    def __new__(cls, *args, path=None, dotpath=None, **kwargs):
        
        putative = path_to_dotpath(path,
                   relative_to=cls.basepath) or dotpath
        
        if putative is not None:
            if putative in cls.instances:
                return cls.instances[putative]
        
        # Call super:
        instance = super().__new__(cls) # type: ignore
        
        instance.__exports__ = {}
        instance.path = path
        instance.dotpath = putative
        
        if instance.dotpath is not None:
            cls.instances[instance.dotpath] = instance
        
        return instance
    
    @classmethod
    def __class_getitem__(cls, key):
        """ Return a specific Exporter instance from the registry,
            given a dotted module path, like e.g:
            
                >>> from clu import naming
                >>> assert Exporter['clu.naming'] == naming.exporter
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
        """ Get a generator yielding from a sorted list of module names
            – keys to the Exporter instance registry – currently available
        """
        yield from sorted(cls.instances.keys())
    
    @classmethod
    def modules(cls):
        """ Get a dictionary of actual modules corresponding to the
            currently registered Exporter instances
        """
        return { modulename : importlib.import_module(modulename) \
                                                  for modulename \
                                               in cls.modulenames() }
    
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
    
    def hash(self):
        """ Return a stringified hash value corresponding to this
            particular exporter instances’ dotpath.
        """
        return self.dotpath and stringhash(self.dotpath) or None
    
    def datafile(self):
        """ Return a unique filename for this instance """
        from clu.fs.appdirectories import AppDirs
        from clu.constants.exceptions import FilesystemError
        
        # Initialize an AppDirs instance:
        appdirs = AppDirs(appname=type(self).appname)
        
        # Ensure the user config directory exists:
        if not appdirs.user_config.exists:
            appdirs.user_config.makedirs()
        
        # Construct database filename:
        selfhash = self.hash()
        if not selfhash:
            raise AttributeError("Could not hash the exporter instances’ dotpath")
        return Path(appdirs.user_config / selfhash + ".pkl")
    
    @contextlib.contextmanager
    def data(self, path=NoDefault):
        """ Context manager for opening a shelving database, corresponding
            to this particular exporter instances’ dotpath.
        """
        if path is NoDefault:
            path = self.datafile()
        
        # Yield out a proper shelving database instance:
        with contextlib.closing(shelve.open(os.fspath(path), writeback=True)) as shelving:
            yield shelving
    
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
    
    def popitem(self):
        """ Remove and return a single key-value pair, raising a KeyError
            if the exporter is empty
        """
        return self.__exports__.popitem()
    
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
            
                >>> exporter = Exporter()
                >>> export = exporter.decorator() # q.v. “decorator()” sub.
            
            Use `export` as a decorator to a function definition:
                
                >>> @export
                >>> def yo_dogg(i_heard=None):
                >>>     …
                
            … or manually, to export anything that doesn’t have a name:
                
                >>> yo_dogg = lambda i_heard=None: …
                >>> dogg_heard_index = ( ¬ ) 
                
                >>> export(yo_dogg,             name="yo_dogg")
                >>> export(dogg_heard_index,    name="dogg_heard_index")
            
        """
        # Try to determine the thing’s name – deferring to anything passed:
        named = determine_name(thing, name=name)
        
        # Double-check our determined name and item before stowing:
        if named is None:
            raise ExportError("can’t export an unnamed thing")
        if thing is self.__exports__:
            raise ExportError("can’t export the __exports__ dict directly")
        if thing is self:
            raise ExportError("can’t export an exporter instance directly")
        
        # Re-target bound-method-type things to their parent function definition:
        target = getattr(thing, '__func__', thing)
        
        # At this point, “named” is valid -- if we were passed
        # a callable, try to rename it with either our valid name,
        # or the result of an ID-based search for that callable:
        if callable(thing) and hasattr(thing, '__name__'):
            
            # Ensure “named” is something with which we can work:
            if named in (λ, φ):
                named = search_for_name(thing)
            if named is None:
                raise ExportError(type(self).messages['noname'] % id(thing))
            
            # Retrieve the things’ ostensible __name__, __qualname__, and
            # __code__ attribute values:
            dname = getattr(thing, '__name__')
            qname = getattr(target, '__qualname__')
            fcode = getattr(target, '__code__', None)
            
            # ATTEMPT TO RENAME!!!…
            # VIA FULL-FLOW MULTI-STAGED COMBUSTION:
            
            # Attempt Nº1: update the part(s) of __qualname__ matching __name__:
            try:
                if qname:
                    setattr(target, '__qualname__', qname.replace(
                    getattr(target, '__name__'), named))
            except AttributeError:
                pass
            
            # Attempt Nº2: update __code__.co_name, by replacing __code__:
            try:
                if fcode:
                    target.__code__ = fcode.replace(co_name=named)
            except AttributeError:
                pass    
            
            # Attempt Nº3: update __name__ and set __lambda_name__ if necessary
            # …to recall the lambda’s genesis:
            try:
                target.__name__ = named
                target.__lambda_name__ = getattr(target, '__lambda_name__', dname)
            except AttributeError:
                pass
            else:
                # Only pursue the Nº4 attempt if Nº3 didn’t fail –
                # …reset __module__ for phi-types:
                if dname == φ and self.dotpath is not None:
                    target.__module__ = str(self.dotpath)
        
        # If a “doc” argument was passed in, attempt to assign
        # the __doc__ attribute accordingly on the item -- note
        # that this won’t work for e.g. slotted, builtin, or C-API
        # types that lack mutable __dict__ internals (or at least
        # a settable __doc__ slot or established attribute).
        if doc is not None:
            try:
                target.__doc__ = inspect.cleandoc(doc)
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
            
                >>> export = exporter.decorator()
                
                >>> @export
                >>> def yodogg():
                >>>     ''' Yo dogg, I heard you like exporting '''
                >>>     …
            
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
            
                >>> __all__, __dir__ = exporter.all_and_dir()
            
            … This should be done near the end of a module, after
            all calls to `exporter.export(…)` (aka @export) have
            been made – q.v. the “decorator()” method supra.
        """
        return self.all_tuple(*additionals), \
               self.dir_function(*additionals)
    
    def dir_and_all(self, *additionals):
        """ Assign a modules’ __dir__ and __all__ values, e.g.:
            
                >>> __dir__, __all__ = exporter.dir_and_all()
            
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
    
    def module(self):
        """ Shortcut to get the parent module for the exporter. """
        if self.dotpath is not None:
            return importlib.import_module(self.dotpath)
        return None
    
    fields = ('dotpath', 'appname', 'basepath')
    
    def inner_repr(self):
        """ Stringify a subset of the Exporter instances’ fields. """
        from clu.repr import strfields
        length = len(self)
        if self.path:
            relpath = os.path.relpath(self.path, start=self.basepath)
            path = f"“{relpath}”"
        else:
            path = "«undefined»"
        return strfields(self, type(self).fields,
                               try_callables=False,
                               items=length,
                               path=f"{path}")
    
    def __enter__(self):
        return self.decorator()
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        return exc_type is None
    
    def __iter__(self):
        yield from self.__exports__.keys()
    
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
        from clu.dicts import merge_fast_two
        if not ismergeable(operand):
            return NotImplemented
        return type(self)(merge_fast_two(self, operand))
    
    def __radd__(self, operand):
        # On reverse-add, old values are overwritten
        from clu.dicts import merge_fast_two
        if not ismergeable(operand):
            return NotImplemented
        return type(self)(merge_fast_two(operand, self))
    
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
                                                     'has_appname',
                                                     'for_appname',
                                                     'unregister'),
                           super().__dir__()))

class Exporter(ExporterBase, basepath=BASEPATH, appname=APPNAME):
    
    """ A class representing a list of things for a module to export.
        
        This class is specifically germane to the CLU project – note
        that the “basepath” class keyword is used to assign a value from
        the CLU constants module.
        
        Users of CLU who wish to use the Exporter mechanism in their
        own projects should create a subclass of ExporterBase of their
        own. Like this one, it need only assign the “basepath” class
        keyword; it is unnecessary (but OK!) to define further methods,
        properties, class constants, and whatnot.
        
        When writing your subclass, if you •do• choose to add methods
        or other things, it is imperative that you ensure you aren’t
        accedentally clobbering anything important from ExporterBase,
        or you risk UNDEFINED BEHAVIOR!!!! Erm.
        
        Also note that all derived subclasses of ExporterBase will
        automatically be slotted classes – a “__slots__” attribute
        will be added to the class dict by the “clu.abstract.Slotted”
        metaclass, if your subclass doesn’t define one – and so if
        you desire a class with a working “__dict__” attribute for
        some reason, you’ll need to specify:
        
            >>> __slots__ = tuplize('__dict__')
        
        … in your class (or an equivalent).
    """
    
    pass

exporter = Exporter(path=__file__)

# GLOBAL INSPECTION: thismodule() will return the module in which it is called:
thismodule = lambda: inspect.currentframe().f_back.f_globals.get(EXPORTER_NAME, ExporterBase()).dotpath

with exporter as export:
    
    export(itermodule)
    export(moduleids)
    export(itermoduleids)
    export(Modulespace)
    export(search_by_id)
    export(search_for_name)
    export(search_for_module)
    export(search_modules)
    export(stringhash)
    export(determine_name)
    export(path_to_dotpath)
    export(thismodule, name='thismodule', doc="thismodule() → return the name of the module in which the `thismodule()` function was called")
    
    # NO DOCS ALLOWED:
    export(Registry)
    export(ExporterTypeRepr)
    export(ExporterBase)
    export(Exporter) # hahaaaaa

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def everything():
    from pprint import pprint
    print("» LOCALS:")
    pprint(locals())
    print()
    
    print("» GLOBALS:")
    pprint(globals())
    print()

def test():
    
    from clu.testing.utils import inline
    from clu.constants import consts
    
    @inline.precheck
    def check_everything():
        """ Print all locals and globals for the module """
        everything()
    
    @inline.runif(not consts.TEXTMATE)
    def test_thismodule():
        """ Sanity-check “thismodule()” """
        assert thismodule() == 'clu.exporting'
    
    @inline
    def test_itermodule_itermoduleids():
        """ Test “itermodule(…)” and “itermoduleids(…)” """
        from clu.typology import iterlen
        
        assert iterlen(itermodule(consts)) == len(consts.__all__)
        assert iterlen(itermoduleids(consts)) == len(consts.__all__)
        
        # pairs = tuple(zip((const, getattr(consts, const)) for const in dir(consts)))
        # assert tuple(pairs) == tuple(itermodule(consts))
        # assert len(pairs) == len(consts.__all__)
        pairs = dict(zip(dir(consts), (getattr(consts, const) for const in dir(consts))))
        assert pairs == dict(itermodule(consts))
        idpairs = dict(zip(dir(consts), (id(getattr(consts, const)) for const in dir(consts))))
        assert idpairs == dict(itermoduleids(consts))
    
    @inline
    def test_modulespace():
        """ Test the “Modulespace” shortcut class """
        modspace = Modulespace()
        import sys, os, io
        
        assert modspace.sys == sys
        assert modspace.os == os
        assert modspace.io == io
    
    @inline
    def test_search_for_name():
        """ Test “search_for_name(…)” """
        from clu.testing import utils
        inlinetester_name = search_for_name(utils.InlineTester)
        assert utils.InlineTester.__name__ == inlinetester_name
        bucket_name = search_for_name(utils.Bucket)
        assert utils.Bucket.__name__ == bucket_name
    
    @inline
    def test_search_for_module():
        """ Test “search_for_module(…)” """
        from clu.testing import utils
        inlinetester_module = search_for_module(utils.InlineTester)
        assert utils == inlinetester_module
        bucket_module = search_for_module(utils.Bucket)
        assert utils == bucket_module
        format_environment_module = search_for_module(utils.format_environment)
        assert utils == format_environment_module
    
    @inline
    def test_hash():
        """ Test the string-hashing of the exporters’ dotpath """
        expo = Exporter(path=__file__)
        assert expo.hash() == exporter.hash()
        print(expo.hash())
    
    @inline
    def test_shelving():
        """ Test the arbitrary data-shelving context manager """
        from clu.fs.filesystem import TemporaryName
        
        with TemporaryName(randomized=True, suffix='pkl') as tempfile:
            tempname = tempfile.name
            with exporter.data(path=tempfile.name) as database:
                database['yo'] = 'dogg'
                database['i_heard'] = 'you like dicts'
            with exporter.data(path=tempfile.name) as database:
                assert database['yo'] == 'dogg'
                assert database['i_heard'] == 'you like dicts'
                assert len(database) == 2
        
        assert not os.path.exists(tempname)
    
    @inline.diagnostic
    def show_search_by_id_cache_info():
        print("SEARCH-BY-ID CACHE INFO:")
        print(Exporter.cache_info())
    
    @inline.diagnostic
    def show_stringhash_cache_info():
        print("STRINGHASH CACHE INFO:")
        print(stringhash.cache_info())
    
    return inline.test(100)

if __name__ == '__main__':
    test()