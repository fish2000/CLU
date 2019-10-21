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

from clu.constants.consts import PROJECT_NAME, QUALIFIER
from clu.abstract import NonSlotted, AppName
from clu.predicates import attr, getpyattr, attr_search, mro
from clu.naming import nameof, dotpath_split, dotpath_join
from clu.typespace import types
from clu.typology import isstring, subclasscheck
from clu.exporting import Exporter

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
    
    @monomers.setter
    def monomers(cls, value):
        global monomers
        monomers = value
    
    @monomers.deleter
    def monomers(cls):
        raise TypeError("Can’t delete the module registry dictionary")
    
    @staticmethod
    def all_appnames():
        """ Return a tuple of strings, listing all registered app names """
        return tuple(Registry.monomers.keys())
    
    @staticmethod
    def all_modules():
        """ Return a tuple filled with instances of all registered class-based modules """
        return tuple(iterchain(modules.values() for modules in Registry.monomers.values()))
    
    @staticmethod
    def has_appname(name):
        """ Check if a given app name has been registered """
        return name in Registry.monomers
    
    @staticmethod
    def for_appname(name):
        """ Return the module with the qualified registered module name """
        if not name:
            raise ValueError("name required")
        if not isstring(name):
            raise TypeError("module registry access by string keys only")
        return Registry.monomers[name]
    
    def __getitem__(cls, key):
        """ Allows lookup of an app name through subscripting the Registry class """
        return Registry.for_appname(key)

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
            
            # Raise if an existing module has that name:
            if qualified_name in Registry.monomers[cls.appname]:
                raise TypeError(f"module class already exists: {qualified_name}")
            
            # Register if the names are good
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
        keyword argument to “__init__(…)”
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
    """
    
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        # N.B. this shouldn’t technically be a class method,
        # but making it so fixed a bizarre bug where importing
        # from the class-based module using the machinery of
        # “from appname.appspace.xxx import xxx” would fail
        # when the method was called unbound-method-style
        # with classes like 'str' …?!
        if cls.appname == fullname.split(QUALIFIER).pop(0):
            return ModuleSpec(fullname, cls.loader)
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
            modulename, packagename = dotpath_split(spec.name)
            if spec.name in Registry[cls.appname]:
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

DO_NOT_INCLUDE = { '__abstractmethods__', '_abc_impl' }

@export
class ModuleBase(Package, Registry, metaclass=NonSlotted):
    
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
    """
    
    appname = None
    appspace = None
    
    @classmethod
    def __init_subclass__(cls, appname=None, appspace=None, **kwargs):
        if any(field is None for field in (appname, appspace)):
            pass
        ancestors = mro(cls)
        cls.appname  = appname  or attr_search('appname', *ancestors)
        cls.appspace = appspace or attr_search('appspace', *ancestors)
        super(ModuleBase, cls).__init_subclass__(**kwargs)
    
    def __init__(self, name, doc=None):
        """ Initialize a new class-based module instance, using the name
            as specified and an optional docstring.
        """
        qualified_name = None
        if self.namespace:
            qualified_name = dotpath_join(self.namespace, name)
        super(ModuleBase, self).__init__(qualified_name or name, doc)
    
    @property
    def name(self):
        return nameof(self)
    
    @property
    def namespace(self):
        cls = type(self)
        if any(field is None for field in (cls.appname, cls.appspace)):
            if cls.appname:
                return cls.appname
            if cls.appspace:
                return cls.appspace
            return None
        return dotpath_join(cls.appname,
                            cls.appspace)
    
    def __dir__(self):
        names = set().union(chain(type(self).__dict__.keys(),
                                  super(ModuleBase, self).__dir__()))
        return list(names - DO_NOT_INCLUDE)

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

export(Module, name='Module')
export(Finder, name='Finder')
export(Loader, name='Loader')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import pout
    
    def test_one():
        
        m = Module(name=PROJECT_NAME)
        assert m
        assert m.appname == PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == PROJECT_NAME
        print(nameof(m))
        print(m.__name__)
        
        print("test_one(): PASSED")
    
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
        
        print("test_two(): PASSED")
    
    def test_three():
        assert pout
        
        # registry = dict(Registry.monomers)
        # pout.v(registry)
        # pout.v(Module.__dict__)
        
        # pout.v(Registry.all_appnames())
        # pout.v(Registry.all_modules())
        
        m = Module(name=PROJECT_NAME)
        
        assert len(Registry.monomers) > 0
        try:
            assert len(m.monomers) == 0
        except AttributeError:
            pass
        else:
            raise
        
        pout.v(m.__dict__)
        
        assert m.appname == PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == PROJECT_NAME
        
        pout.v(mro(m))
        
        print("test_three(): PASSED")
    
    def three_and_a_half():
        finder = Finder()
        assert type(finder.loader) is Loader
        assert finder in sys.meta_path
        
        class FindMe(Module):
            pass
        
        spec = finder.find_spec('clu.app.FindMe', [])
        # pout.v(spec.__dict__)
        assert spec.name == 'clu.app.FindMe'
        
        module = finder.loader.create_module(spec)
        # pout.v(module)
        assert type(module) is FindMe
        
        pout.v(mro(finder))
        
        print("three_and_a_half(): PASSED")
    
    def test_four():
        
        class Derived(Module):
            
            """ I heard you like docstrings """
            
            yo = 'dogg'
        
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
        
        print("test_four(): PASSED")
    
    # Run all tests:
    test_one()
    test_two()
    test_three()
    three_and_a_half()
    test_four()

if __name__ == '__main__':
    test()