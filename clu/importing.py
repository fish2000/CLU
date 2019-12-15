# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict as DefaultDict
from dataclasses import dataclass, field, fields
from functools import lru_cache
from itertools import chain

cache = lambda function: lru_cache()(function)
iterchain = chain.from_iterable

import abc
import clu.abstract
import clu.dicts
import importlib
import importlib.abc
import importlib.machinery
import inspect
import pkgutil
import sys
import typing as tx
import weakref
import zict

try:
    import importlib.metadata
except ImportError:
    import importlib_metadata as _metadata
    importlib.metadata = _metadata

from clu.constants import consts
from clu.extending import Extensible
from clu.naming import nameof, dotpath_split, dotpath_join
from clu.predicates import anyattrs, attr, attr_search, mro
from clu.repr import stringify
from clu.typespace import Namespace, types
from clu.typology import ismodule, ismapping, isstring, subclasscheck
from clu.exporting import Registry as ExporterRegistry
from clu.exporting import ExporterBase, Exporter

NoDefault = consts.NoDefault

exporter = Exporter(path=__file__)
export = exporter.decorator()

# The module-subclass registry dictionary:
monomers = DefaultDict(weakref.WeakValueDictionary)

class MetaRegistry(Extensible):
    
    """ A metaclass for the class-based-module registry, wrapping all
        access to the actual dict-of-dicts registry structure§ with
        class methods.
        
        End-users shouldn’t have to use this in their own code, hence
        it is not exported.
        
        § Actually a “collections.defaultdict” containing instances of
         “weakref.WeakValueDictionary” – but who’s counting, really.
    """
    
    @property
    def monomers(cls):
        return monomers
    
    @staticmethod
    def has_appname(appname):
        """ Check if a given app name has been registered """
        return appname in Registry.monomers
    
    @staticmethod
    def for_appname(appname):
        """ Return the weak-value dictionary of classes for the registered appname """
        if not appname:
            raise ValueError("appname required")
        if not isstring(appname):
            raise TypeError("module registry access by string keys only")
        return Registry.monomers[appname]
    
    def __getitem__(cls, key):
        """ Allows lookup of an app name through subscripting the Registry class """
        return Registry.for_appname(key)
    
    @staticmethod
    def unregister(appname, qualified_name):
        """ Unregister a previously-registered per-appname class from the registry """
        if Registry.has_appname(appname):
            if qualified_name in Registry.monomers[appname]:
                cls = Registry.monomers[appname].pop(qualified_name)
                if qualified_name in sys.modules:
                    del sys.modules[qualified_name]
                if hasattr(cls, 'exporter'):
                    cls.exporter.unregister(qualified_name)
                importlib.invalidate_caches()
                return bool(cls)
        return False

@export
def all_registered_appnames():
    """ Return a tuple of strings, listing all registered app names """
    return tuple(sorted(Registry.monomers.keys()))

@export
def all_registered_modules():
    """ Return a tuple filled with instances of all registered class-based modules """
    return tuple(iterchain(modules.values() for modules in Registry.monomers.values()))

@export
def modules_for_appname(appname):
    """ Return a tuple filled with instances of an apps’ registered class-based modules """
    if appname not in Registry.monomers:
        return tuple()
    return tuple(Registry.monomers[appname].values())

@export
class Registry(abc.ABC, metaclass=MetaRegistry):
    
    """ The Registry mixin handles the registration of all
        class-based module subclasses.
    """
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        """ If the qualified name of this class is not yet registered,
            then register it – store a weakref to it in the per-appname
            dictionary, indexed by the qualified name.
        """
        # Call up:
        super(Registry, cls).__init_subclass__(**kwargs)
        
        # We were called with a class for which the values
        # of appname, appspace, and __name__ have been assigned:
        if cls.appname and cls.appspace and nameof(cls):
            # Register this subclass if the names are good:
            if cls.qualname not in Registry.monomers[cls.appname]:
                Registry.monomers[cls.appname][cls.qualname] = cls
            # Register the root class for this subclass,
            # also name-wellness permitting:
            # if cls.prefix not in Registry.monomers[cls.appname]:
            #     Registry.monomers[cls.appname][cls.qualname] = ???

@export
class ModuleSpec(importlib.machinery.ModuleSpec):
    
    """ A local “importlib.machinery.ModuleSpec” subclass
        that conveniently deals with setting the “origin”
        attribute, and identifies all of its instances as
        package modules.
    """
    
    def __init__(self, name, loader):
        """ Initialize a new ModuleSpec, with a qualified (dotted)
            path string, and a module loader instance (both of which
            are required).
        """
        _, packagename = dotpath_split(name)
        super(ModuleSpec, self).__init__(name,
                                         loader,
                                         origin=packagename,
                                         is_package=True)
    
    def __hash__(self):
        return hash(self.loader) \
             & hash(self.name) \
             & hash(self.origin) \
             & hash(self.parent)

@export
class Package(types.Module):
    
    """ A subclass of ‘types.Module’ which assigns all instances
        of which either an empty list or the value of the “path”
        keyword argument to its “__path__” attribute in “__init__(…)”
    """
    
    def __init__(self, name, doc=None, path=None):
        super(Package, self).__init__(name, doc)
        self.__path__ = path or []
    
    def __repr__(self):
        """ A nicer, kindler, gentler module repr-function """
        location = attr(self, '__spec__.origin',
                              '__file__',
                              '__package__')
        name = attr(self, '__name__', 'name')
        typename = subclasscheck(self, ModuleBase) \
                                  and 'class-module' \
                                   or 'module'
        out = f"<{typename} ‘{name}’"
        if location:
            out += f" from “{location}”"
        out += ">"
        return out

@export
class FinderBase(clu.abstract.AppName, importlib.abc.MetaPathFinder):
    
    """ The base class for all class-based module finders.
        
        One must subclass this class once per app, specifying
        an “appname” – the name of the app. Q.v. the function
        “initialize_types(…)” sub. to easily set these up for
        your own app.
        
        The method “FinderBase.find_spec(…)” caches returned
        instances of “ModuleSpec” using a ‘zict.LRU’ buffer.
    """
    
    specs = {}
    cache = zict.LRU(64, specs)
    
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        # N.B. this shouldn’t technically be a class method,
        # but making it so fixed a bizarre bug where importing
        # from the class-based module using the machinery of
        # “from appname.appspace.xxx import xxx” would fail
        # when the method was called unbound-method-style
        # with classes like 'str' …?!
        if fullname in cls.cache:
            return cls.cache[fullname]
        if cls.appname == fullname.split(consts.QUALIFIER).pop(0):
            out = cls.cache[fullname] = ModuleSpec(fullname, cls.loader)
            return out
        return None
    
    @classmethod
    def invalidate_caches(cls):
        cls.loader.create_module.cache_clear()
        cls.cache.clear()
        return None
    
    @classmethod
    def iter_modules(cls):
        """ This “non-standard API method”§ yields ‘pkgutil.ModuleInfo’
            instances for each registered class-module in the finder
            subclasses’ given app.
            
            § q.v. boxed notation sub., Python documentation,
              https://docs.python.org/3/library/pkgutil.html#pkgutil.iter_modules
        """
        yield from (pkgutil.ModuleInfo(cls,
                                       module.qualname,
                                       ispkg=True) \
                    for module in modules_for_appname(cls.appname))

@export
class LoaderBase(clu.abstract.AppName, importlib.abc.Loader):
    
    """ The base class for all class-based module loaders.
        
        One must subclass this class once per app, specifying
        an “appname” – the name of the app. Q.v. the function
        “initialize_types(…)” sub. to easily set these up for
        your own app.
        
        The method “LoaderBase.create_module(…)” caches returned
        instances of “types.Module” using the ‘functools.lru_cache’
        function decorator.
    """
    
    @staticmethod
    def package_module(name):
        """ Convenience method, returning an empty package module """
        return Package(name, f"Package (filler) module {name}")
    
    @cache
    def create_module(self, spec):
        """ Create a new class-based module from a spec instance """
        cls = type(self)
        if Registry.has_appname(cls.appname):
            if spec.name in Registry[cls.appname]:
                modulename, _ = dotpath_split(spec.name)
                ModuleClass = Registry[cls.appname][spec.name]
                docstr = inspect.getdoc(ModuleClass)
                module = ModuleClass(modulename, doc=docstr)
                return module
            return self.package_module(spec.name)
        return None
    
    def exec_module(self, module):
        """ Execute a newly created module.
            
            Since the code of class-based module has, by definition,
            already been executed by the Python interpreter at this point,
            we delegate this action to a user-provided “__execute__()”
            instance method of the class-based module in question.
            
            The “__execute__()” method will be called with no arguments.
            The class-based module instance will, at this point, have its
            “appname” and “appspace” class attributes set and readable,
            in addition to all of the contemporary module-instance attributes
            documented in e.g. PEP 451 and friends.
            
            An “__execute__()” method shouldn’t return anything.
        """
        if not getattr(module, '_executed', False):
            if hasattr(module, '__execute__'):
                if callable(module.__execute__):
                    try:
                        module.__execute__()
                    finally:
                        module._executed = True
                else:
                    raise TypeError("__execute__() method not callable")
            else:
                module._executed = True

@export
class ArgumentSink(object):
    
    """ ArgumentSink is a class that stores the arguments with
        which it is initialized, for either later retrieval or
        subsequent functional application.
        
        To wit:
        
            >>> sink = ArgumentSink('yo', 'dogg', iheard="you like")
            >>> assert sink.args == ('yo', 'dogg')
            >>> assert sink.kwargs == dict(iheard="you like")
            >>> sink(stringify) # prints “str(iheard=you like) @ 0x10bd”
    """
    __slots__ = ('args', 'kwargs')
    
    def __init__(self, *args, **kwargs):
        """ Initialize an ArgumentSink, with arbitrary positional
            and/or keyword arguments
        """
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, function):
        """ Apply the sinks’ arguments to a function – or, indeed,
            any callable – returning the result
        """
        return function(*self.args, **self.kwargs)

class MetaModule(MetaRegistry):
    
    """ A metaclass for class-module subclasses.
        
        This metaclass inherits from the private MetaRegistry
        metaclass, by necessity – like its ancestor, it’s a
        private resource and would be of questionable value
        to CLU users if exported.
        
        MetaModule defines “__prepare__” and “__new__” metaclass
        methods typical of many metaclasses. Specifically, the
        “__prepare__” method is used to inject a specialized
        version of the familiar “@export” decorator, which, when
        used in class-body definition namespaces, will export
        things so decorated via a custom behind-the-scenes employ
        of the “clu.exporting” machinery.
    """
    
    @property
    def name(cls):
        return nameof(cls)
    
    @property
    def prefix(cls):
        if any(attrib is None for attrib in (cls.appname, cls.appspace)):
            if cls.appname:
                return cls.appname
            if cls.appspace:
                return cls.appspace
            return None
        return dotpath_join(cls.appname,
                            cls.appspace)
    
    @property
    def qualname(cls):
        return dotpath_join(cls.prefix,
                            cls.name)
    
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        """ Prepare the class-module namespace with an injected
            “@export” decorator
        """
        # Define a deferred export function, utilizing
        # a private list of ArgumentSink instances:
        def deferred_export(thing, name=None, doc=None):
            deferred_export.sinks.append(ArgumentSink(thing,
                                                      name=name,
                                                      doc=doc))
            return thing
        
        # Set attributes:
        deferred_export.sinks = []
        deferred_export.__doc__ = inspect.getdoc(ExporterBase.export)
        
        # Call up:
        attributes = super(MetaModule, metacls).__prepare__(name,
                                                            bases,
                                                          **kwargs)
        
        # Return a new Namespace with the deferred export function
        # defined as “export”:
        return Namespace(export=deferred_export, **attributes)
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Create a new class-module subclass, expanding any
            deferred export directives embedded in the class-module
            definition’s namespace
        """
        # Remove the deferred export function:
        deferred_export = attributes.pop('export', None)
        
        # Call up, creating and initializing the module class:
        cls = super(MetaModule, metacls).__new__(metacls, name,
                                                          bases,
                                                          dict(attributes),
                                                        **kwargs)
        
        # If an appname is defined, try to install
        # an instance of the appropriate Exporter:
        if cls.appname is not None and not name.endswith('Module'):
            if ExporterRegistry.has_appname(cls.appname):
                ExporterClass = ExporterRegistry[cls.appname]
                cls.exporter = ExporterClass(dotpath=cls.qualname)
                
                # Invoke all of our argument sinks against the
                # Exporter instance’s “export(…)” function:
                for sink in getattr(deferred_export, 'sinks', []):
                    sink(cls.exporter.export)
        
        # Return the new module class:
        return cls

DO_NOT_INCLUDE = { '__abstractmethods__',
                   '__execute__',
                   '_abc_impl', '_executed', 'monomers' }

@export
class ModuleBase(Package, Registry, metaclass=MetaModule):
    
    """ The base class for all class-based modules.
        
        One must subclass this class once per app, specifying
        an “appname” – the name of the app – and an “appspace” –
        an optional prefix from which all class-based modules
        will be found and imported. Q.v. “initialize_types(…)”
        sub. to easily set these up for your own app.
        
        Within CLU, the appname is “clu” (duh) and the appspace
        is “app” – all class-based modules are therefore imported
        from “clu.app”, á la:
            
            from clu.app import class_based_module
        
        Note that class-based modules are forbidden from using
        the “__slots__” class attribute – the module class’ metaclass
        will remove any __slots__ it encounters, in fact, so don’t
        even bother with ’em.
    """
    
    # The appname and appspace default to None:
    appname = None
    appspace = None
    
    # Block access to the registry’s underlying data:
    monomers = clu.abstract.ValueDescriptor({})
    
    @classmethod
    def __init_subclass__(cls, appname=None, appspace=None, **kwargs):
        """ Properly set the “appname” and “appspace” class attributes
            on any registered class-based module subclasses.
        """
        ancestors = mro(cls)
        cls.appname  = appname  or attr_search('appname',  *ancestors)
        cls.appspace = appspace or attr_search('appspace', *ancestors)
        super(ModuleBase, cls).__init_subclass__(**kwargs)
    
    def __init__(self, name, doc=None):
        """ Initialize a new class-based module instance, using the name
            as specified and an optional docstring.
        """
        qualified_name = None
        if self.prefix:
            qualified_name = dotpath_join(self.prefix, name)
        super(ModuleBase, self).__init__(qualified_name or name, doc)
    
    def __execute__(self):
        """ The “__execute__()” class-based module instance method is called
            when the module is quote-unquote “executed.” This is analagous
            to the point at which a file-based modules’ code is actually run
            by the Python interpreter; since a class-based modules’ code has,
            by definition, already been executed once the class itself has
            been initialized, this method hook is provided to execute custom
            module code at that point in the class modules’ lifecycle.
            
            An “__execute__()” method should not accept any arguments or return
            any values. The “self” instance it receives will be fully initialized
            and include “appname”, “appspace”, ‘name’, ‘prefix’, ‘qualname’,
            as well as all of the PEP-451-related module attributes.
            
            Currently, the base class implementation is a no-op – but should
            class-based module authors write their own “__execute__()” methods,
            they are advised to include a “super(…)” call within their own
            implementations, as this is likely to change in the future.
        """
        pass
    
    @property
    def name(self):
        return nameof(self)
    
    @property
    def prefix(self):
        return type(self).prefix
    
    @property
    def qualname(self):
        return dotpath_join(self.prefix,
                            self.name)
    
    def __dir__(self):
        cls = type(self)
        if hasattr(cls, 'exporter'):
            return cls.exporter.dir_function()()
        names = chain(cls.__dict__.keys(),
                      super(ModuleBase, self).__dir__())
        return sorted(frozenset(names) - DO_NOT_INCLUDE)

class PolymerType(dict):
    
    def store(self, appname, loader, finder, **modules):
        self[appname] = PerApp(loader=loader,
                               finder=finder,
                              modules=modules,
                              appname=appname)
        return self[appname]
    
    def add_module(self, appname, appspace, module):
        if not appspace:
            raise ValueError("an appspace is required")
        if not module:
            raise ValueError("a module is required")
        if not self.get(appname, None):
            raise ValueError(f"no PerApp instance for appname: {appname}")
        self[appname].modules.update({ appspace : module })
        return self[appname]

polymers = PolymerType()

@dataclass(repr=False)
class PerApp:
    
    loader:     Extensible
    finder:     Extensible
    modules:    tx.Dict[str, MetaModule]    = field(default_factory=dict)
    appname:    str                         = field(default_factory=str)
    
    def __repr__(self):
        return stringify(self,
                    type(self).field_names,
                         try_callables=False)

PerApp.field_names = tuple(field.name for field in fields(PerApp))

def installed_appnames():
    """ Return a set of the appnames for all installed finders
        that have one defined.
    """
    # { finder.appname for finder in sys.meta_path if hasattr(finder, 'appname') }
    appnames = set()
    for finder in sys.meta_path:
        if hasattr(finder, 'appname'):
            appnames.add(finder.appname)
    return appnames

def initialize_new_types(appname, appspace):
    """ Private helper for “initialize_types(…)” """
    
    class Loader(LoaderBase, appname=appname):
        pass
    
    class Finder(FinderBase, appname=appname):
        __loader__ = Loader
        loader = Loader()
    
    class Module(ModuleBase, appname=appname,
                             appspace=appspace):
        __loader__ = Finder.loader
    
    return Module, Finder, Loader

def initialize_module(appname, appspace, loader):
    """ Private helper for “initialize_types(…)” """
    
    class Module(ModuleBase, appname=appname,
                             appspace=appspace):
        __loader__ = loader
    
    return Module

@export
def initialize_types(appname, appspace='app'):
    """ Initialize subtypes of FinderBase, LoaderBase, and ModuleBase,
        configured for a specific “appname” and “appspace” (the latter
        of which defaults to ‘app’).
        
        You use ‘initialize_types(…)’ in one of your own app’s modules
        like so:
        
            Module, Finder, Loader = initialize_types('myappname')
        
        … if you insert that line of code in a module of yours called,
        say, “myappname/modules.py” you could then either a) proceed
        to subclass Module to create your class-modules, or b) import
        the ‘Module’ class from elsewhere and subclass it subsequently.
    """
    try:
        perapp = polymers[appname]
    
    except KeyError:
        Module, Finder, Loader = initialize_new_types(appname, appspace)
        polymers.store(appname, loader=Loader,
                                finder=Finder,
                        **{ appspace : Module })
    
    else:
        Loader = perapp.loader
        Finder = perapp.finder
        Module = perapp.modules.get(appspace, None)
        
        if Module is None:
            Module = initialize_module(appname, appspace, perapp.finder.loader)
            polymers.add_module(appname=appname,
                               appspace=appspace,
                                 module=Module)
    
    if appname not in installed_appnames():
        sys.meta_path.append(Finder)
    
    return Module, Finder, Loader

Module, Finder, Loader = initialize_types(consts.PROJECT_NAME)

@export
class ChainModuleMap(clu.dicts.ChainMap):
    
    """ Custom “clu.dicts.ChainMap” subclass, tailored for module dicts """
    
    def __iter__(self):
        yield from filter(lambda item: item not in consts.BUILTINS,
                          super().__iter__())
    
    def __missing__(self, key):
        if key in self:
            return 0
        raise KeyError(key)
    
    def inner_repr(self):
        from pprint import pformat
        return pformat(dict(zip(self, (self[item] for item in self))))

# Define out-of-line target-processing function:
def add_targets(instance, *targets):
    """ Out-of-line, use-twice-and-destroy function for processing targets """
    if getattr(instance, 'target_dicts', None) is None:
        instance.target_dicts = []
    if getattr(instance, 'target_lists', None) is None:
        instance.target_lists = []
    for target in targets:
        if target is None:
            continue
        if ismodule(target):
            instance.target_dicts.append(target.__dict__)
            instance.target_lists.append(dir(target))
            continue
        if ismapping(target):
            instance.target_dicts.append(target)
            instance.target_lists.append(list(target.keys()))
            continue

@export
class ProxyModule(Module):
    
    """ A ProxyModule is a specific type of module: one that wraps one or
        more other things and surfaces their attributes, as if they are all
        one big unified module.
        
        In this case, “things” can be either modules or mappings. Internally,
        the ProxyModule uses a bespoke ChainMap subclass to keep these modules
        and/or mappings in line, and to access them idempotently, with a
        deterministic ordering, and generally in a way that doesn’t surprise
        or scare anybody.
        
        Here’s a basic example of a ProxyModule definition:
        
            overrides = dict(…)
            from yodogg.app import base_module
            from yodogg.utils import misc as second_module
            
            class myproxy(ProxyModule):
                targets = (overrides, base_module,
                                    second_module)
        
        … which after defining that, you’d use it like so – assuming your app
        is called “yodogg” with a default “app” appspace (see “ModuleBase” for
        more on these terms):
        
            from yodogg.app import myproxy
            myproxy.attrib # searches overrides, base_module and second_module
                           # in sequence, looking for the 'attrib' value
            dir(myproxy)   # returns a list of the union of available stuff,
                           # across the proxy modules’ targets
        
        … you can, in the modules’ definition, include other stuff besides the
        class-level “targets” tuple; other elements added to the proxy will
        behave like elements of any other class-based module.
    """
    
    def __new__(cls, name, *targets, doc=None):
        """ Allocate a new tabula-rasa proxy-module instance.
            
            Adds any targets passed in when the constructor was called –
            which that should be like never, except maybe under testing
            or somesuch – for the most part, ProxyModule targets’ll be
            specified as a class-level tuple attribute.
            
            See the main class docstring for the deets.
        """
        
        # Call up, creating the instance:
        instance = super(ProxyModule, cls).__new__(cls)
        
        # Fill in empty “slots”:
        instance.__proxies__ = {}
        instance.__filters__ = []
        instance.target_dicts = []
        instance.target_lists = []
        
        # Process any targets with which this instance
        # may have been constructed:
        add_targets(instance, *targets)
        
        # Return the new instance:
        return instance
    
    def __init__(self, name, *targets, doc=None):
        """ Initialize a proxy-module instance.
            
            The signature for initializing a proxy module is the same
            as that for a class-based module – the proxy module class
            derives directly from the application-specific class-based
            module definition – with the optional addition of zero-to-N
            “targets”.
            
            Each target so named can be either a mapping-ish type, or a
            module. The proxy module will then use the list of targets
            – considerate of order – to construct a “clu.dicts.ChainMap”
            instance that pulls, in turn, from the target list.
            
            Attribute lookup on the proxy module instance will follow
            along through the “ChainMap” instances’ internal stack of
            mappings.
        """
        # Super-initialize:
        super(ProxyModule, self).__init__(name, doc=doc)
        
        # Get a reference to the module class:
        cls = type(self)
        
        # Process and strip off a class-level “targets”
        # list attribute – if such a thing exists – and
        # then sequester the “targets” attribute behind an
        # underscore, if necessary:
        if anyattrs(cls, 'targets', '_targets'):
            add_targets(self, *attr(cls, 'targets', '_targets'))
            if hasattr(cls, 'targets'):
                setattr(cls, '_targets', attr(cls, 'targets', '_targets'))
                delattr(cls, 'targets')
    
    def __execute__(self):
        # Create the internal “clu.dicts.ChainMap” subclass instance:
        self.__proxies__ = ChainModuleMap(*self.target_dicts)
        self.__filters__ = tuple(iterchain(self.target_lists))
        
        # Further unclutter the module namespace:
        delattr(self, 'target_dicts')
        delattr(self, 'target_lists')
        
        # Call up:
        super().__execute__()
    
    def __dir__(self):
        cls = type(self)
        names = chain(self.__filters__,
                       cls.__dict__.keys())
        return sorted(frozenset(names) - DO_NOT_INCLUDE)
    
    def __getattr__(self, key):
        # N.B. AttributeError typenames (herein “ProxyModule”) must be
        # somehow hardcoded – using “self.name” leads to an infinite
        # recursion kertwang within “__getattr__(…)” – since “name”
        # is a property that uses “nameof(self)” which invariably will
        # attempt to get one or another nonexistant attributes from ‘self’.
        try:
            if not self.__dict__.get('_executed', False):
                raise KeyError(key)
            elif key in consts.BUILTINS:
                raise KeyError(key)
            return self.__proxies__[key]
        except KeyError:
            typename = type(self).__name__
            raise AttributeError(f"‘{typename}’ proxy module has no attribute ‘{key}’")

export(Module, name='Module')
export(Finder, name='Finder')
export(Loader, name='Loader')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, pout
    from pprint import pprint
    
    @inline
    def test_one():
        
        m = Module(consts.PROJECT_NAME)
        assert m
        assert m.appname == consts.PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.PROJECT_NAME
        print(nameof(m))
        print(m.__name__)
    
    @inline
    def test_two():
        
        class OtherModule(ModuleBase):
            pass
        
        class DerivedModule(Module):
            pass
        
        class DerivedOther(OtherModule):
            pass
        
        o = OtherModule("other")
        d = DerivedModule("derived")
        O = DerivedOther("derived-other")
        
        assert o
        assert d
        assert O
    
    @inline
    def test_three():
        assert pout
        
        pout.v(all_registered_appnames())
        pout.v(all_registered_modules())
        
        m = Module(consts.PROJECT_NAME)
        
        assert len(Registry.monomers) > 0
        try:
            assert len(m.monomers) == 0
        except AttributeError:
            pass
        else:
            pass
        
        pout.v(m.__dict__)
        
        assert m.appname == consts.PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.PROJECT_NAME
        
        pout.v(mro(m))
    
    @inline
    def three_and_a_half():
        finder = Finder()
        assert type(finder.loader) is Loader
        assert type(finder) in sys.meta_path
        
        class FindMe(Module):
            pass
        
        spec0 = finder.find_spec('clu.app.FindMe', [])
        assert spec0.name == 'clu.app.FindMe'
        
        module0 = finder.loader.create_module(spec0)
        assert type(module0) is FindMe
        
        module1 = finder.loader.create_module(spec0)
        assert type(module1) is FindMe
        
        spec1 = finder.find_spec('clu.app.FindMe', [])
        assert spec1.name == 'clu.app.FindMe'
        
        pout.v(mro(finder))
    
    @inline
    def test_four():
        
        class Derived(Module):
            
            """ I heard you like docstrings """
            
            yo = 'dogg'
            
            @export
            def yodogg(self):
                return "I heard you like"
            
            @export
            def nodogg(self):
                return None
            
            export(yo, name='yo')
        
        from clu.app import Derived as derived
        
        assert type(derived) is Derived
        assert derived.yo == 'dogg'
        
        for attname in dir(derived):
            assert hasattr(derived, attname)
        
        pout.v(dir(derived))
        pout.v(derived.exporter.exports())
        
        assert type(derived.exporter).__name__ == 'Exporter'
    
    @inline
    def test_five():
        
        overrides = dict(PROJECT_NAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        class testing_overridden_consts(ProxyModule):
            targets = (overrides, consts)
        
        from clu.app import testing_overridden_consts as overridden
        
        assert overridden.USER == consts.USER
        assert overridden.BUILTINS == consts.BUILTINS
        assert overridden.PROJECT_NAME == 'yodogg'
        assert overridden.PROJECT_PATH.endswith('yodogg')
        assert overridden.BASEPATH.endswith('yodogg')
        
        assert not hasattr(overridden, 'targets')
        assert not hasattr(overridden, 'target_dicts')
        assert hasattr(overridden, '_targets')
        
        # pout.v(overridden)
        pprint(overridden.__proxies__)
        
        # return tuple(overridden.exporter.exports())
        return dir(overridden)
    
    @inline
    def test_six():
        """ AppClasses dataclass check """
        pprint(dict(polymers), indent=4)
        
        Module0, Finder0, Loader0 = initialize_types(consts.PROJECT_NAME)
        
        assert Finder is Finder0
        assert Loader is Loader0
        assert Module is Module0
        assert Finder0.__loader__ is Loader0
        assert isinstance(Module0.__loader__, Loader0)
        assert isinstance(Finder0.loader, Loader0)
        
        Module1, Finder1, Loader1 = initialize_types(consts.PROJECT_NAME, appspace='apps')
        
        assert Finder is Finder1
        assert Loader is Loader1
        assert Module is not Module1 # DIFFERENT!!!
        assert Finder1.__loader__ is Loader1
        assert isinstance(Module1.__loader__, Loader1)
        assert isinstance(Finder1.loader, Loader1)
        
        from clu.apps import Module as apps_module # Note how this is the things’ actual name,
                                                   # “Module”, and not just what we called it,
                                                   # «Module1» …ooof.
        
        # assert type(apps_module) is Module1
        print("MODULETYPE:", type(apps_module))
        print("MONOMERS:")
        pprint(dict(monomers['clu']))
    
    print("PYTHON:", sys.executable)
    
    # Run all tests:
    inline.test()

if __name__ == '__main__':
    test()