# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract
import copy
import os

import pytest

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
        
        # Ensure “sys.path” contains the “yodogg” package:
        prefix = dirname.subdirectory('yodogg')
        assert prefix.exists
        pypath.enhance(prefix)
        
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
        
        class YoDogg(clu.abstract.Cloneable, metaclass=clu.abstract.Slotted):
            
            __slots__ = ('yo', 'dogg', 'yo_dogg')
            
            def __init__(self, **kwargs):
                self.yo         = kwargs.pop('yo',      'YO')
                self.dogg       = kwargs.pop('dogg',    'DOGG')
                self.yo_dogg    = kwargs.pop('yo_dogg', 'YO_DOGG')
            
            def __eq__(self, other):
                return self.yo == other.yo and \
                       self.dogg == other.dogg and \
                       self.yo_dogg == other.yo_dogg
            
            def clone(self, deep=False, memo=None):
                kwargs = dict(zip(self.__slots__,
                         (getattr(self, slot, None) for slot in self.__slots__)))
                return type(self)(**kwargs)
        
        i0 = YoDogg()
        i1 = i0.clone()
        i2 = copy.copy(i0)
        i3 = copy.deepcopy(i0)
        
        assert i0 == i1
        assert i0 == i2
        assert i0 == i3
        assert i0 == YoDogg(yo='YO', dogg='DOGG', yo_dogg='YO_DOGG')
    
    def test_abc_ReprWrapper(self):
        from clu.repr import compare_instance_reprs
        
        class YoDogg(clu.abstract.ReprWrapper, metaclass=clu.abstract.Slotted):
            
            __slots__ = ('yo', 'dogg', 'yo_dogg')
            
            def __init__(self, **kwargs):
                self.yo         = kwargs.pop('yo',      'YO')
                self.dogg       = kwargs.pop('dogg',    'DOGG')
                self.yo_dogg    = kwargs.pop('yo_dogg', 'YO_DOGG')
            
            def __eq__(self, other):
                return self.yo == other.yo and \
                       self.dogg == other.dogg and \
                       self.yo_dogg == other.yo_dogg
            
            def inner_repr(self):
                return f"yo=“{self.yo}”, dogg=“{self.dogg}”, yo_dogg=“{self.yo_dogg}”"
        
        i0 = YoDogg()
        i1 = YoDogg(yo='YO', dogg='DOGG', yo_dogg='YO_DOGG')
        i2 = YoDogg(yo='Yo', dogg='Dogg', yo_dogg='Yo Dogg')
        
        assert i0 == i1
        assert i0 != i2
        assert compare_instance_reprs(i0, i1)
        assert not compare_instance_reprs(i0, i2)
        assert not compare_instance_reprs(i0, i1, i2)
    
    def test_abc_AppName(self):
        
        class AppConfigBase(clu.abstract.AppName):
            pass
        
        class AppConfig(AppConfigBase, appname='YoDogg'):
            pass
        
        appconfig = AppConfig()
        assert appconfig.appname == 'YoDogg'
        assert appconfig.appname == AppConfig.appname
        
        with pytest.raises(LookupError) as exc:
            _ = AppConfigBase()
        assert "Cannot instantiate a base config" in str(exc.value)
    
    def test_abc_ManagedContext(self):
        import contextlib
        from clu.typology import (subclasscheck,
                                  iscontextmanager,
                                  isabstractcontextmanager)
        
        class Managed(clu.abstract.ManagedContext):
            
            def setup(self):
                return self
            
            def teardown(self):
                pass
        
        assert iscontextmanager(Managed)
        assert isabstractcontextmanager(Managed)
        assert subclasscheck(Managed, contextlib.AbstractContextManager)
        assert issubclass(Managed, contextlib.AbstractContextManager)
        
        with Managed() as m:
            assert iscontextmanager(m)
            assert isabstractcontextmanager(m)
            assert subclasscheck(m, Managed)
            assert isinstance(m, Managed)

class TestAbstractReprClasses(object):
    
    """ Run the tests for the clu.abstract module’s repr classes. """
    
    def test_repr_SlottedRepr(self):
        from clu.repr import compare_instance_reprs
        
        class YoDogg(clu.abstract.SlottedRepr):
            
            __slots__ = ('yo', 'dogg', 'yo_dogg')
            
            def __init__(self, **kwargs):
                self.yo         = kwargs.pop('yo',      'YO')
                self.dogg       = kwargs.pop('dogg',    'DOGG')
                self.yo_dogg    = kwargs.pop('yo_dogg', 'YO_DOGG')
            
            def __eq__(self, other):
                return self.yo == other.yo and \
                       self.dogg == other.dogg and \
                       self.yo_dogg == other.yo_dogg
        
        i0 = YoDogg()
        i1 = YoDogg(yo='YO', dogg='DOGG', yo_dogg='YO_DOGG')
        i2 = YoDogg(yo='Yo', dogg='Dogg', yo_dogg='Yo Dogg')
        
        assert i0 == i1
        assert i0 != i2
        assert compare_instance_reprs(i0, i1)
        assert not compare_instance_reprs(i0, i2)
        assert not compare_instance_reprs(i0, i1, i2)
    
    @pytest.mark.TODO
    def test_repr_MappingViewRepr(self, dirname):
        # TODO: this test makes no sense – rewrite it
        from clu.repr import compare_instance_reprs
        data = dirname.subdirectory('data')
        
        keys = repr(data.keys())
        values = repr(data.values())
        items = repr(data.items())
        
        assert compare_instance_reprs(keys.replace('KeysView', 'ItemsView'), items)
        assert compare_instance_reprs(values.replace('ValuesView', 'ItemsView'), items)
        assert not compare_instance_reprs(keys, items)
        assert not compare_instance_reprs(values, items)

class TestAbstractDescriptors(object):
    
    """ Run the tests for the clu.abstract module’s descriptor classes. """
    
    def test_descriptor_Descriptor(self):
        pass
    
    def test_descriptor_ValueDescriptor(self, environment, consts):
        from clu.fs.misc import gethomedir
        from clu.predicates import isclasstype, pyattr
        from clu.predicates import attr, attrs, stattr, stattrs
        
        # Data descriptor wrapping a R/O value:
        from clu.abstract import ValueDescriptor
        
        # We have to use these irritating default environment values everywhere,
        # in case the testing environment is kertwanged:
        home = environment.get('HOME', gethomedir())
        user = environment.get('USER', consts.USER)
        
        # Non-data descriptor wrapping R/O access to a named environment variable,
        # a default value for that variable, and the variables’ name:
        class EnvironmentName(object):
            
            __slots__ = ('name', 'default')
            
            def __init__(self, name=None, default=None):
                self.default = default
                if name is not None:
                    self.name = name
            
            def __set_name__(self, cls, name):
                if name is not None:
                    self.name = name
            
            def __get__(self, instance=None, cls=None):
                if instance is not None:
                    return environment.get(self.name,
                                           self.default)
                if isclasstype(cls):
                    return self.name
            
            def __repr__(self):
                clsname = pyattr(type(self), 'name', 'qualname')
                selfname =  attr(     self,  'name', 'default')
                return f"{clsname}<[{selfname}]>"
        
        # Slotted type with non-data descriptors,
        # wrapping values and environment variables:
        class Slotted(object):
            __slots__ = ('yo', 'dogg', 'wtf')
            
            hax = ValueDescriptor('HAXXX')
            HOME = EnvironmentName(default=gethomedir())
            USER = EnvironmentName(default=consts.USER)
            
            def __init__(self):
                self.yo: str = "YO"
                self.dogg: str = "DOGG"
                self.wtf: str = "WTFFF"
        
        # Non-slotted (“dictish”) type with data descriptors,
        # wrapping both values and environment variables:
        class Dictish(object):
            yo: str = "YO"
            dogg: str = "DOGG"
            
            wtf = ValueDescriptor('WTFFF')
            HOME = EnvironmentName(default=gethomedir())
            USER = EnvironmentName(default=consts.USER)
            
            def __init__(self):
                self.hax: str = "HAXXX"
        
        # The basics – Slotted type and instance attributes:
        assert attr(Slotted,    'hax', 'HOME', 'USER') ==  'HAXXX'
        assert attr(Slotted(),  'hax', 'HOME', 'USER') ==  'HAXXX'
        assert attrs(Slotted,   'hax', 'HOME', 'USER') == ('HAXXX', 'HOME', 'USER')
        assert attrs(Slotted(), 'hax', 'HOME', 'USER') == ('HAXXX',  home,   user)
        
        # More basics – Dictish type and instance attributes:
        assert attr(Dictish,    'wtf', 'HOME', 'USER') ==  'WTFFF'
        assert attr(Dictish(),  'wtf', 'HOME', 'USER') ==  'WTFFF'
        assert attrs(Dictish,   'wtf', 'HOME', 'USER') == ('WTFFF', 'HOME', 'USER')
        assert attrs(Dictish(), 'wtf', 'HOME', 'USER') == ('WTFFF',  home,   user)
        
        # Check statically obtained ValueDescriptor instances,
        # from Slotted types and instances:
        assert repr(stattr(Slotted,    'hax', 'HOME', 'USER')) ==                       'HAXXX'
        assert repr(stattr(Slotted(),  'hax', 'HOME', 'USER')) ==                       'HAXXX'
        assert repr(stattr(Slotted,    'hax', 'HOME', 'USER')) ==  repr(ValueDescriptor('HAXXX'))
        assert repr(stattr(Slotted(),  'hax', 'HOME', 'USER')) ==  repr(ValueDescriptor('HAXXX'))
        assert type(stattr(Slotted,    'hax', 'HOME', 'USER')) is       ValueDescriptor
        assert type(stattr(Slotted(),  'hax', 'HOME', 'USER')) is       ValueDescriptor
        
        # Check statically obtained ValueDescriptor instances,
        # from Dictish types and instances:
        assert repr(stattr(Dictish,    'wtf', 'HOME', 'USER')) ==                       'WTFFF'
        assert repr(stattr(Dictish(),  'wtf', 'HOME', 'USER')) ==                       'WTFFF'
        assert repr(stattr(Dictish,    'wtf', 'HOME', 'USER')) ==  repr(ValueDescriptor('WTFFF'))
        assert repr(stattr(Dictish(),  'wtf', 'HOME', 'USER')) ==  repr(ValueDescriptor('WTFFF'))
        assert type(stattr(Dictish,    'wtf', 'HOME', 'USER')) is       ValueDescriptor
        assert type(stattr(Dictish(),  'wtf', 'HOME', 'USER')) is       ValueDescriptor
        
        # Check statically obtained EnvironmentName instances,
        # from both Slotted and Dictish types and instances:
        assert repr(stattr(Slotted,   'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Slotted(), 'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Slotted,   'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Slotted(), 'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Slotted,   'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Slotted(), 'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Slotted,   'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Slotted(), 'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Dictish,   'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Dictish(), 'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Dictish,   'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Dictish(), 'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Dictish,   'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Dictish(), 'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Dictish,   'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Dictish(), 'USER')) ==     "EnvironmentName<[USER]>"
        
        # Slotted attributes are named descriptors that can compare with __eq__():
        assert stattr(Slotted, 'yo')   == stattr(Slotted(), 'yo')   == attr(Slotted, 'yo')
        assert stattr(Slotted, 'dogg') == stattr(Slotted(), 'dogg') == attr(Slotted, 'dogg')
        assert stattr(Slotted, 'wtf')  == stattr(Slotted(), 'wtf')  == attr(Slotted, 'wtf')
        
        # Dictish attributes are just attributes -- statically obtained attributes come from
        # the class __dict__, while “normally” obtained attributes are probably coming out of
        # the instance __dict__:
        atts = ('yo', 'dogg', 'wtf')
        assert stattrs(Dictish, *atts) == stattrs(Dictish(), *atts) != attrs(Dictish(), *atts)
        
        # N.B. Dictish.hax is a ValueDescriptor instance:
        atts = ('yo', 'dogg', 'hax')
        assert stattrs(Dictish, *atts) != stattrs(Dictish(), *atts) == attrs(Dictish(), *atts)
