# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract
import copy
import os

import pytest

abstract = abc.abstractmethod

@pytest.fixture(scope='module')
def strings():
    yield ('yo', 'dogg', 'iheard', 'youlike')

@pytest.fixture(scope='module')
def capstrings():
    yield ('YoDogg',
           'iHeardYouLike',
           'VariouslyCapitalizedStrings')

class TestAbstractMetas(object):
    
    """ Run the tests for the clu.abstract module’s metaclasses. """
    
    def test_metaclass_Slotted(self, strings):
        from clu.predicates import slots_for
        
        class Base(abc.ABC, metaclass=clu.abstract.Slotted):
            pass
        
        class DerivedOne(Base):
            __slots__ = ('yo', 'dogg')
        
        class DerivedTwo(DerivedOne):
            pass
        
        class DerivedThree(DerivedTwo):
            __slots__ = ('iheard', 'youlike')
        
        assert slots_for(DerivedThree) == strings
        
        assert Base.__slots__ == tuple()
        assert DerivedOne.__slots__ == ('yo', 'dogg')
        assert DerivedTwo.__slots__ == tuple()
        assert DerivedThree.__slots__ == ('iheard', 'youlike')
    
    def test_metaclass_SlotMatch(self):
        from clu.predicates import haspyattr
        
        class Base(abc.ABC, metaclass=clu.abstract.SlotMatch):
            pass
        
        class Derived(Base):
            __slots__ = ('yo', 'dogg')
            def __init__(self, yo, dogg):
                self.yo = str(yo)
                self.dogg = str(dogg)
        
        class Yowza(Base):
            pass
        
        assert Base.__slots__ == tuple()
        assert Base.__match_args__ == tuple()
        assert Derived.__slots__ == ('yo', 'dogg')
        assert Derived.__match_args__ == ('yo', 'dogg')
        assert Yowza.__slots__ == tuple()
        assert Yowza.__match_args__ == tuple()
        
        def dogg_matcher(thing):
            match thing:
                case Derived(yo="", dogg=""):
                    assert thing.yo == ""
                    assert thing.dogg == ""
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
                case Derived(yo="", dogg=dogg):
                    assert thing.yo == ""
                    assert type(thing.dogg) is str
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
                case Derived(yo=yo, dogg=""):
                    assert type(thing.yo) is str
                    assert thing.dogg == ""
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
                case Derived(yo=yo, dogg=dogg):
                    assert type(thing.yo) is str
                    assert type(thing.dogg) is str
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
                case Base():
                    assert not hasattr(thing, 'yo')
                    assert not hasattr(thing, 'dogg')
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
                case _:
                    assert haspyattr(thing, 'slots')
                    assert haspyattr(thing, 'match_args')
        
        dogg_matcher(Base())
        dogg_matcher(Derived("", ""))
        dogg_matcher(Derived("i", ""))
        dogg_matcher(Derived("", "heard"))
        dogg_matcher(Derived("i", "heard"))
        dogg_matcher(Yowza())
        
        dogg_matcher(Base)
        dogg_matcher(Derived)
        dogg_matcher(Yowza)
        
        # This will fail (a plain object lacks the attributes asserted
        # in the default case of the matcher):
        #dogg_matcher(object())
    
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
    
    def test_metaclass_BasePath(self, dirname):
        from clu.fs import pypath
        
        # Ensure “sys.path” contains the “yodogg” package:
        basepath = dirname.subdirectory('yodogg')
        assert basepath.exists
        pypath.enhance(basepath)
        
        class AppConfigBase(abc.ABC, metaclass=clu.abstract.BasePath):
            pass
        
        class AppConfig(AppConfigBase, basepath=basepath):
            pass
        
        appconfig = AppConfig()
        assert appconfig.basepath == AppConfig.basepath
        assert appconfig.basepath == os.fspath(basepath)
        assert os.path.exists(appconfig.basepath)

class TestAbstractABCs(object):
    
    """ Run the tests for the clu.abstract module’s abstract base classes. """
    
    @pytest.mark.TODO
    def test_abc_Unhashable(self):
        import collections.abc
        
        class Ancestor(abc.ABC, metaclass=clu.abstract.Slotted):
            
            @abstract
            def __hash__(self):
                ...
        
        class HashMe(Ancestor):
            
            def __hash__(self):
                return hash(type(self))
        
        class DontHashMe(HashMe, clu.abstract.Unhashable):
            
            def __hash__(self):
                return hash(type(self))
        
        class Rando(clu.abstract.Unhashable):
            pass
        
        # class Unrelated(abc.ABC):
        #     pass
        
        assert hash(HashMe())
        assert isinstance(HashMe(), collections.abc.Hashable)
        assert not isinstance(HashMe(), clu.abstract.Unhashable)
        
        with pytest.raises(TypeError) as exc:
            hash(DontHashMe())
        assert "unhashable type" in str(exc)
        assert "DontHashMe" in str(exc)
        assert not isinstance(DontHashMe(), collections.abc.Hashable)
        assert isinstance(DontHashMe(), clu.abstract.Unhashable)
        
        assert not isinstance(Rando(), collections.abc.Hashable)
        assert isinstance(Rando(), clu.abstract.Unhashable)
        
        # TODO: make it work for random, unrelated ABC classes:
        # assert not isinstance(Unrelated(), collections.abc.Hashable)
        # assert isinstance(Unrelated(), clu.abstract.Unhashable)
    
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
    
    def test_abc_Format(self, capstrings):
        
        class UpperCaser(clu.abstract.Format):
            def render(self, string):
                return str(string).upper()
        
        class CaseFolder(clu.abstract.Format):
            def render(self, string):
                return str(string).casefold()
        
        uppercaser = UpperCaser()
        casefolder = CaseFolder()
        do_nothing = clu.abstract.NonFormat()
        
        for string in capstrings:
            assert uppercaser.render(string) == string.upper()
            assert uppercaser.render(string).isupper()
            assert casefolder.render(string) == string.casefold()
            assert casefolder.render(string).islower()
            assert do_nothing.render(string) == str(string)
            assert do_nothing.render(string).isprintable() # why not
    
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

class TestAbstractFormats(object):
    
    """ Run the tests for the clu.abstract module’s format types. """
    
    def test_format_SlottedFormat(self, capstrings):
        
        class HTMLTagger(clu.abstract.SlottedFormat):
            
            def __init__(self, tag_name):
                self.opstring = "<"  + tag_name.casefold() \
                              + ">"  + "{0}"               \
                              + "</" + tag_name.casefold() \
                              + ">"
            
            def render(self, string):
                return self.opstring.format(string)
        
        boldizer        = HTMLTagger('b')
        italizer        = HTMLTagger('i')
        strengthener    = HTMLTagger('strong')
        emphasizer      = HTMLTagger('em')
        
        for string in capstrings:
            assert boldizer.render(string) == f"<b>{string}</b>"
            assert italizer.render(string) == f"<i>{string}</i>"
            assert strengthener.render(string) == f"<strong>{string}</strong>"
            assert emphasizer.render(string) == f"<em>{string}</em>"

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
