# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
from itertools import chain

iterchain = chain.from_iterable

import abc
import importlib
import importlib.abc
import importlib.machinery
import sys
import weakref
# import zict

from clu.constants.consts import PROJECT_NAME
from clu.predicates import getpyattr, or_none, attr_search, mro
from clu.naming import nameof, dotpath_split, dotpath_join
from clu.typespace import types
from clu.typology import isstring
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class NonSlotted(abc.ABCMeta):
    
    """ A metaclass that ensures its classes, and all subclasses,
        will •not• use the “__slots__” optimization.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived un-slotted class.
        """
        if '__slots__' in attributes:
            del attributes['__slots__']
        
        return super(NonSlotted, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

# The module-subclass registry dictionary:
# monomers = weakref.WeakValueDictionary()
monomers = defaultdict(weakref.WeakValueDictionary)

class MetaRegistry(NonSlotted):
    
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
        return tuple(Registry.monomers.keys())
    
    @staticmethod
    def all_modules():
        return tuple(iterchain(modules.values() for modules in Registry.monomers.values()))
    
    @staticmethod
    def has_appname(name):
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
        return Registry.for_appname(key)

@export
class Registry(abc.ABC, metaclass=MetaRegistry):
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        
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

class AppName(abc.ABC):
    
    __slots__ = tuple()
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        """ Translate the “appname” class-keyword into an “appname” read-only
            descriptor value
        """
        super(AppName, cls).__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname)
    
    def __init__(self, *args, **kwargs):
        """ Stub __init__(…) method, throwing a lookup error for subclasses
            upon which the “appname” value is None
        """
        if type(self).appname is None:
            name = type(self).__name__
            raise LookupError(f"Cannot instantiate base config class {name} "
                              f"(appname is None)")

@export
class ModuleSpec(importlib.machinery.ModuleSpec):
    
    def __init__(self, name, loader):
        _, packagename = dotpath_split(name)
        super(ModuleSpec, self).__init__(name,
                                         loader,
                                         origin=packagename,
                                         is_package=True)

@export
class FinderBase(AppName, importlib.abc.MetaPathFinder):
    
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        # N.B. this shouldn’t technically be a class method,
        # but making it so fixed a bizarre bug where importing
        # from the class-based module using the machinery of
        # “from appname.appspace.xxx import xxx” would fail
        # when the method was called unbound-method-style
        # with classes like 'str' …?!
        # print('CLASS [finder]:', cls)
        if Registry.has_appname(cls.appname):
            return ModuleSpec(fullname, cls.loader)
        return None

@export
class LoaderBase(AppName, importlib.abc.Loader):
    
    def package_module(self, name):
        return types.Module(name, "Package (filler) module")
    
    def create_module(self, spec):
        cls = type(self)
        # print('CLASS [loader]:', cls)
        if Registry.has_appname(cls.appname):
            modulename, packagename = dotpath_split(spec.name)
            if spec.name in Registry[cls.appname]:
                ModuleClass = Registry[cls.appname][spec.name]
                module = ModuleClass(modulename,
                                     getpyattr(ModuleClass, 'doc'))
                return module
            return self.package_module(spec.name)
    
    def exec_module(self, module):
        pass

DO_NOT_INCLUDE = { '__abstractmethods__', '_abc_impl' }

@export
class ModuleBase(types.Module, Registry, metaclass=NonSlotted):
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
        qualified_name = None
        if self.namespace:
            qualified_name = dotpath_join(self.namespace, name)
        super(ModuleBase, self).__init__(qualified_name or name, doc)
        self.__path__ = []
    
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

def initialize_types(appname, appspace='app'):
    
    class Loader(LoaderBase, appname=appname):
        pass
    
    class Finder(FinderBase, appname=appname):
        loader = Loader()
    
    class Module(ModuleBase, appname=appname,
                             appspace=appspace):
        __loader__ = Finder.loader
    
    if Loader not in sys.meta_path:
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