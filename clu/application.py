# -*- coding: utf-8 -*-
from __future__ import print_function

# import clu.abstract
import sys

# from clu.repr import stringify
from clu.predicates import newtype, mro, attr_search
from clu.typespace import SimpleNamespace as sns
from clu.importing import (FinderBase,
                           LoaderBase,
                           ModuleBase,
                           MetaModule)

from clu.constants import consts
# from clu.extending import Extensible
from clu.importing import installed_appnames
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

DEFAULT_APPSPACE = 'app'

class AppMeta(MetaModule):
    
    @property
    def exportercls(cls):
        from clu.exporting import Registry
        if Registry.has_appname(cls.appname):
            return Registry[cls.appname]
        raise TypeError(f"exporter class not found for appname: {cls.appname}")

@export
class AppBase(ModuleBase, metaclass=AppMeta):
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        # 1) Call up:
        prefix = kwargs.pop('prefix', None)
        cls.basepath = prefix or attr_search('prefix', *mro(cls))
        super(AppBase, cls).__init_subclass__(**kwargs)
        
        # 2) Check appname:
        if not cls.appname:
            raise NameError("no appname available on AppBase subclass")
        
        # 3) install finder, loader, exporter…
        cls._exporter  = cls.initialize_exporter()
        Finder, Loader = cls.initialize_finder_and_loader()
        cls.finder     = Finder
        cls.loader     = Loader
        cls.__loader__ = Finder.loader
        
        # 4) possibly update `sys.meta_path`
        if cls.appname not in installed_appnames():
            sys.meta_path.append(cls.finder)
    
    @classmethod
    def initialize_finder_and_loader(cls):
        # name, *bases, metaclass, attributes, **keywords
        LoaderCls = newtype('Loader', LoaderBase, appname=cls.appname)
        attrspace = sns(__loader__=LoaderCls,
                          loader=LoaderCls())
        FinderCls = newtype('Finder', FinderBase, attributes=attrspace,
                                                  appname=cls.appname)
        return FinderCls, LoaderCls
    
    @classmethod
    def initialize_exporter(cls):
        from clu.exporting import ExporterBase
        try:
            return cls.exportercls
        except TypeError:
            ExporterCls = newtype('Exporter', ExporterBase, appname=cls.appname,
                                                            prefix=cls.basepath)
            return ExporterCls

@export
class Application(AppBase, appname=consts.APPNAME,
                            prefix=consts.BASEPATH,
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
        assert app._exporter is Exporter
    
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
        
        from flynn.app import Shmapplication as shmodule
        
        assert shmodule
        assert shmodule.appname == 'flynn'
        assert shmodule.appspace == 'app'
    
    @inline.diagnostic
    def show_app_class_attribs():
        pout.v(Application)
        
        stuff = dir(Application)
        pout.v({ k : getattr(Application, k) for k in stuff })
        
        print("APPNAME:", Application.appname)
        print("APPSPACE:", Application.appspace)
        
        print("consts.APPNAME:", consts.APPNAME)
        print("DEFAULT_APPSPACE:", DEFAULT_APPSPACE)
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())


