# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict as DefaultDict
from itertools import chain

iterchain = chain.from_iterable

import abc
import importlib
import importlib.abc
import importlib.machinery
import sys
import weakref
import zict

from clu.constants.consts import PROJECT_NAME, QUALIFIER, NoDefault
from clu.abstract import NonSlotted, AppName
from clu.predicates import getpyattr, attr, attr_search, mro, newtype, union
from clu.naming import nameof, dotpath_split, dotpath_join
from clu.typespace import Namespace, types
from clu.typology import isstring, subclasscheck
from clu.exporting import Registry as ExporterRegistry
from clu.exporting import ValueDescriptor, ExporterBase, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# The module-subclass registry dictionary:
monomers = DefaultDict(weakref.WeakValueDictionary)

class MetaRegistry(NonSlotted):
    
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
        """ Return the module with the qualified registered module name """
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
                if hasattr(cls, 'exporter'):
                    cls.exporter.unregister(qualified_name)
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
class Registry(abc.ABC, metaclass=MetaRegistry):
    
    """ The Registry mixin handles the registration of all
        class-based module subclasses.
    """
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        """ Properly set the “appname” and “appspace” class attributes
            on registered class-based module subclasses
        """
        # We were called with a class for which the values
        # of appname, appspace, and __name__ have been assigned:
        if cls.appname and cls.appspace and nameof(cls):
            qualified_name = dotpath_join(cls.appname,
                                          cls.appspace,
                                getpyattr(cls, 'name'))
            
            # Register if the names are good:
            if qualified_name not in Registry.monomers[cls.appname]:
                Registry.monomers[cls.appname][qualified_name] = cls
        
        # Call up:
        super(Registry, cls).__init_subclass__(**kwargs)

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

@export
class Package(types.Module):
    
    """ A subclass of ‘types.Module’ which assigns all instances
        of which either an empty list or the value of the “path”
        keyword argument to its “__path__” attribute in “__init__(…)”
    """
    
    def __init__(self, name, doc=None, path=None):
        super(Package, self).__init__(name, doc)
        self.__path__ = path or []

@export
class FinderBase(AppName, importlib.abc.MetaPathFinder):
    
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
        if cls.appname == fullname.split(QUALIFIER).pop(0):
            out = cls.cache[fullname] = ModuleSpec(fullname, cls.loader)
            return out
        return None
    
    @classmethod
    def invalidate_caches(cls):
        cls.cache.clear()
        return None

@export
class LoaderBase(AppName, importlib.abc.Loader):
    
    """ The base class for all class-based module loaders.
        
        One must subclass this class once per app, specifying
        an “appname” – the name of the app. Q.v. the function
        “initialize_types(…)” sub. to easily set these up for
        your own app.
    """
    
    @staticmethod
    def package_module(name):
        """ Convenience method, returning an empty package module """
        return Package(name, f"Package (filler) module {name}")
    
    def create_module(self, spec):
        """ Create a new class-based module from a spec instance """
        cls = type(self)
        if Registry.has_appname(cls.appname):
            if spec.name in Registry[cls.appname]:
                modulename, _ = dotpath_split(spec.name)
                ModuleClass = Registry[cls.appname][spec.name]
                module = ModuleClass(modulename,
                                     getpyattr(ModuleClass, 'doc'))
                return module
            return self.package_module(spec.name)
        return None
    
    def exec_module(self, module):
        """ Execute a newly created module – this is a no-op for
            class-based modules, as they have by definition already
            been executed by the interpreter
        """
        pass
    
    def module_repr(self, module):
        """ A nicer, kindler, gentler module repr-function """
        location = attr(module, '__spec__.origin',
                                '__file__',
                                '__package__')
        name = attr(module, '__name__', 'name')
        typename = subclasscheck(module, ModuleBase) \
                                  and 'class-module' \
                                   or 'module'
        out = f"<{typename} ‘{name}’"
        if location:
            out += f" from “{location}”"
        out += ">"
        return out

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
        deferred_export.__doc__ = ExporterBase.export.__doc__
        
        # Return a new Namespace with the deferred export function
        # defined as “export”:
        return Namespace(export=deferred_export)
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Create a new class-module subclass, expanding any
            deferred export directives embedded in the class-module
            definition’s namespace
        """
        # Remove the deferred export function:
        deferred_export = attributes.pop('export', None)
        
        # Call up, creating and initializing the module class:
        cls = super(MetaRegistry, metacls).__new__(metacls, name,
                                                            bases,
                                                            dict(attributes),
                                                          **kwargs)
        
        # If an appname is defined, try to install
        # an instance of the appropriate Exporter:
        if cls.appname is not None and name != 'Module':
            if ExporterRegistry.has_appname(cls.appname):
                ExporterClass = ExporterRegistry[cls.appname]
                qualified_name = dotpath_join(cls.appname,
                                              cls.appspace,
                                    getpyattr(cls, 'name'))
                cls.exporter = ExporterClass(dotpath=qualified_name)
                
                # Invoke all of our argument sinks against the
                # Exporter instance’s “export(…)” function:
                for sink in getattr(deferred_export, 'sinks', []):
                    sink(cls.exporter.export)
        
        # Return the new module class:
        return cls

DO_NOT_INCLUDE = { '__abstractmethods__', '_abc_impl', 'monomers' }

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
    monomers = ValueDescriptor({})
    
    @classmethod
    def __init_subclass__(cls, appname=None, appspace=None, **kwargs):
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
    
    @property
    def name(self):
        return nameof(self)
    
    @property
    def prefix(self):
        cls = type(self)
        if any(field is None for field in (cls.appname, cls.appspace)):
            if cls.appname:
                return cls.appname
            if cls.appspace:
                return cls.appspace
            return None
        return dotpath_join(cls.appname,
                            cls.appspace)
    
    @property
    def qualname(self):
        return dotpath_join(self.prefix,
                            self.name)
    
    def __dir__(self):
        cls = type(self)
        if hasattr(cls, 'exporter'):
            return cls.exporter.dir_function()()
        names = union(cls.__dict__.keys(),
                      super(ModuleBase, self).__dir__())
        return sorted(list(names - DO_NOT_INCLUDE))

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
    
    class Loader(LoaderBase, appname=appname):
        pass
    
    class Finder(FinderBase, appname=appname):
        loader = Loader()
    
    class Module(ModuleBase, appname=appname,
                             appspace=appspace):
        __loader__ = Finder.loader
    
    if Finder not in sys.meta_path:
        sys.meta_path.append(Finder)
    
    return Module, Finder, Loader

Module, Finder, Loader = initialize_types(PROJECT_NAME)

@export
class SubModule(object):
    
    """ A context manager that creates a temporary
        class-module subclass on enter, and unregisters
        the temporary subclass on exit. Handy for testing.
    """
    
    __slots__ = ('ModuleClass',
                 'ModuleSubclass',
                 'name', 'appname', 'appspace')
    
    def __init__(self, name='ModuleSubclass', ModuleClass=NoDefault):
        """ Initializes a SubModule context manager with a given
            module class (defaults to “clu.importing.Module”).
        """
        if not name:
            raise TypeError("a name is required")
        if ModuleClass in (None, NoDefault):
            ModuleClass = Module
        self.ModuleClass = ModuleClass
        self.name = name
        self.appname = ModuleClass.appname
        self.appspace = ModuleClass.appspace
    
    def __enter__(self):
        """ Create and return the temporary class-module subclass """
        self.ModuleSubclass = newtype(self.name, self.ModuleClass)
        return self.ModuleSubclass
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        """ Unregister the temporary class-module subclass """
        qualified_name = dotpath_join(self.appname,
                                      self.appspace,
                               nameof(self.ModuleSubclass))
        Registry.unregister(self.appname,
                            qualified_name)
        return exc_type is None

export(Module, name='Module')
export(Finder, name='Finder')
export(Loader, name='Loader')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, pout
    
    @inline
    def test_one():
        
        m = Module(name=PROJECT_NAME)
        assert m
        assert m.appname == PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == PROJECT_NAME
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
        
        o = OtherModule(name="other")
        d = DerivedModule(name="derived")
        O = DerivedOther(name="derived-other")
        
        assert o
        assert d
        assert O
    
    @inline
    def test_three():
        assert pout
        
        # registry = dict(Registry.monomers)
        # pout.v(registry)
        # pout.v(Module.__dict__)
        
        pout.v(all_registered_appnames())
        pout.v(all_registered_modules())
        
        m = Module(name=PROJECT_NAME)
        
        assert len(Registry.monomers) > 0
        try:
            assert len(m.monomers) == 0
        except AttributeError:
            pass
        else:
            pass
        
        pout.v(m.__dict__)
        
        assert m.appname == PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == PROJECT_NAME
        
        pout.v(mro(m))
    
    @inline
    def three_and_a_half():
        finder = Finder()
        assert type(finder.loader) is Loader
        assert type(finder) in sys.meta_path
        
        class FindMe(Module):
            pass
        
        spec = finder.find_spec('clu.app.FindMe', [])
        # pout.v(spec.__dict__)
        assert spec.name == 'clu.app.FindMe'
        
        module = finder.loader.create_module(spec)
        # pout.v(module)
        assert type(module) is FindMe
        
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
        
        # print(derived.__spec__)
        # pout.v(dict(derived.__dict__))
        # pout.v(derived.__spec__)
        # pout.v(derived.__dict__.keys())
        
        for attname in dir(derived):
            # assert or_none(derived, attname) is not None
            assert hasattr(derived, attname)
        
        pout.v(dir(derived))
        pout.v(derived.exporter.exports())
        
        assert type(derived.exporter).__name__ == 'Exporter'
    
    @inline
    def test_five():
        
        before = all_registered_modules()
        
        with SubModule('derived_module') as DerivedModule:
            from clu.app import derived_module as derived
            
            assert type(derived) is DerivedModule
            assert type(derived.exporter).__name__ == 'Exporter'
            assert len(all_registered_modules()) == len(before) + 1
        
        after = all_registered_modules()
        assert before == after
    
    # Run all tests:
    test_one()
    test_two()
    test_three()
    three_and_a_half()
    test_four()
    test_five()

if __name__ == '__main__':
    test()