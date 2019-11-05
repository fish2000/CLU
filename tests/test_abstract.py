# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract

class TestAbstractMetas(object):
    
    """ Run the tests for the clu.abstract module’s metaclasses. """
    
    def test_metaclass_Slotted(self):
        from clu.predicates import slots_for
        
        class Base(abc.ABC, metaclass=clu.abstract.Slotted):
            pass
        
        class DerivedOne(Base):
            __slots__ = ('yo', 'dogg')
        
        class DerivedTwo(DerivedOne):
            pass
        
        class DerivedThree(DerivedTwo):
            __slots__ = ('iheard', 'youlike')
        
        assert slots_for(DerivedThree) == ('yo', 'dogg', 'iheard', 'youlike')
        
        assert Base.__slots__ == tuple()
        assert DerivedOne.__slots__ == ('yo', 'dogg')
        assert DerivedTwo.__slots__ == tuple()
        assert DerivedThree.__slots__ == ('iheard', 'youlike')
    
    def test_metaclass_NonSlotted(self):
        from clu.predicates import getpyattr, slots_for
        
        class Base(abc.ABC, metaclass=clu.abstract.NonSlotted):
            pass
        
        class DerivedOne(Base):
            __slots__ = ('yo', 'dogg')
        
        class DerivedTwo(DerivedOne):
            pass
        
        class DerivedThree(DerivedTwo):
            __slots__ = ('iheard', 'youlike')
        
        assert slots_for(DerivedThree) == tuple()
        
        # assert nopyattr(Base(), 'slots')
        # assert nopyattr(DerivedOne(), 'slots')
        # assert nopyattr(DerivedTwo(), 'slots')
        # assert nopyattr(DerivedThree(), 'slots')
        
        assert '__slots__' not in Base().__dict__
        assert '__slots__' not in DerivedOne().__dict__
        assert '__slots__' not in DerivedTwo().__dict__
        assert '__slots__' not in DerivedThree().__dict__
        assert '__slots__' not in Base.__dict__
        assert '__slots__' not in DerivedOne.__dict__
        assert '__slots__' not in DerivedTwo.__dict__
        assert '__slots__' not in DerivedThree.__dict__
        
        assert getpyattr(Base, 'slots') == tuple()
        assert getpyattr(DerivedOne, 'slots') == tuple()
        assert getpyattr(DerivedTwo, 'slots') == tuple()
        assert getpyattr(DerivedThree, 'slots') == tuple()
    
    def test_metaclass_Prefix(self, dirname):
        from clu.fs import pypath
        import os
        
        # Ensure “sys.path” contains the “yodogg” package:
        prefix = dirname.subdirectory('yodogg')
        assert prefix.exists
        pypath.remove_invalid_paths()  # cleans “sys.path”
        pypath.append_paths(prefix)    # extends “sys.path”
        
        class AppConfigBase(abc.ABC, metaclass=clu.abstract.Prefix):
            pass
        
        class AppConfig(AppConfigBase, prefix=prefix):
            pass
        
        appconfig = AppConfig()
        assert appconfig.prefix == AppConfig.prefix
        assert appconfig.prefix == os.fspath(prefix)
        assert os.path.exists(appconfig.prefix)

class TestAbstractABCs(object):
    
    """ Run the tests for the clu.abstract module’s abstract base classes. """
    
    def test_abc_Cloneable(self):
        pass
    
    def test_abc_ReprWrapper(self):
        pass
    
    def test_abc_AppName(self):
        pass

class TestAbstractReprClasses(object):
    
    """ Run the tests for the clu.abstract module’s repr classes. """
    
    def test_repr_SlottedRepr(self):
        pass
    
    def test_repr_MappingViewRepr(self):
        pass

class TestAbstractDescriptors(object):
    
    """ Run the tests for the clu.abstract module’s descriptor classes. """
    
    def test_descriptor_Descriptor(self):
        pass
    
    def test_descriptor_ValueDescriptor(self):
        pass
