# -*- coding: utf-8 -*-
from __future__ import print_function

# import clu.abstract
import sys

# from clu.repr import stringify
from clu.predicates import newtype
from clu.typespace import SimpleNamespace
from clu.importing import (FinderBase,
                           LoaderBase,
                           ModuleBase)

from clu.constants import consts
# from clu.importing import MetaModule
# from clu.extending import Extensible
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

DEFAULT_APPSPACE = 'app'

class AppBase(ModuleBase):
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        # 1) Call up:
        super(AppBase, cls).__init_subclass__(**kwargs)
        
        # 2) Check appname:
        if not cls.appname:
            raise NameError("no appname available on AppBase subclass")
        
        # 3) install finder and loader
        Finder, Loader = cls.initialize_finder_and_loader()
        cls.finder = Finder
        cls.loader = Loader
    
    @classmethod
    def initialize_finder_and_loader(cls):
        # name, *bases, metaclass, attributes, **keywords
        LoaderCls = newtype('Loader', LoaderBase, appname=cls.appname)
        attrspace = SimpleNamespace(__loader__=LoaderCls,
                                      loader=LoaderCls())
        FinderCls = newtype('Finder', FinderBase, attributes=attrspace,
                                                  appname=cls.appname)
        return FinderCls, LoaderCls

class Application(AppBase, appname=consts.APPNAME,
                          appspace=DEFAULT_APPSPACE):
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, pout
    
    @inline
    def test_one():
        """ Instance the base Application class """
        app = Application('test_app', doc="Test Application Instance")
        assert app
    
    @inline
    def test_two():
        """ Subclass and instance a second AppBase subclass """
        
        class Shmapplication(AppBase, appname='flynn',
                                     appspace=DEFAULT_APPSPACE):
            pass
        
        shmapp = Shmapplication('test_subclass', doc="Test Secondary Subclass")
        
        assert shmapp
        assert shmapp.appname == 'flynn'
        assert shmapp.appspace == 'app'
        
        # from flynn.app import Shmapplication as shmodule
        #
        # assert shmodule
        # assert shmodule.appname == 'flynn'
        # assert shmodule.appspace == 'app'
    
    @inline.diagnostic
    def show_application_class_attributes():
        pout.v(Application)
        pout.v(dir(Application))
        
        print("APPNAME:", Application.appname)
        print("APPSPACE:", Application.appspace)
        
        print("consts.APPNAME:", consts.APPNAME)
        print("DEFAULT_APPSPACE:", DEFAULT_APPSPACE)
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())


