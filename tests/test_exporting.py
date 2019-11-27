# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

# Currently these need to be defined at the module level,
# in order for “search_for_name(…)” to find them properly –
# q.v. “test_exporter_export_lambdas_no_name_provided(…)”
# definition sub.:
yo_dogg_lambda = lambda: print("Yo dogg.")
i_heard_lambda = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))

class TestExporting(object):
    
    """ Run the tests for the clu.exporting module. """
    
    def test_exporterbase_subclass_package(self, dirname):
        from clu.exporting import Registry
        from clu.fs import pypath
        import os
        
        # Ensure “sys.path” contains the “yodogg” package:
        prefix = dirname.subdirectory('yodogg')
        assert prefix.exists
        pypath.enhance(prefix)
        
        # Bring in the package-specific ExporterBase subclass,
        # as well as the module-local instance of that subclass,
        # and an exemplary function that instance exports:
        from yodogg.exporting import Exporter
        from yodogg.iheard import exporter, youlike
        
        assert os.path.exists(exporter.path)
        assert exporter.dotpath == 'yodogg.iheard'
        assert 'clu' in Registry.all_appnames()
        assert 'yodogg' in Registry.all_appnames()
        assert len(exporter) == 1
        assert exporter['youlike'] is youlike
        assert Exporter['yodogg.iheard'] is exporter
        assert Registry['yodogg'] is Exporter
        
        # __class_getitem__ method abuse 4 LYFE:
        assert Registry['yodogg']['yodogg.iheard']['youlike']() == "registries"
    
    def test_exporterbase_subclass(self, dirname):
        from clu.exporting import ExporterBase, Registry
        import os
        
        prefix = dirname.subdirectory('yodogg')
        yodogg = prefix.subdirectory('yodogg')
        assert prefix.exists
        assert yodogg.exists
        
        # Subclass ExporterBase locally -
        # This will register the subclass:
        class Exporter(ExporterBase, prefix=prefix, appname="yolocal"):
            pass
        
        # Instantiate the ExporterBase subclass –
        # This will register the instance:
        exporter = Exporter(path=yodogg.subpath('iheard.py'))
        export = exporter.decorator()
        
        # Export an exemplary function:
        @export
        def youlike():
            return "registries"
        
        assert os.path.exists(exporter.path)
        assert exporter.dotpath == 'yodogg.iheard'
        assert 'clu' in Registry.all_appnames()
        assert 'yolocal' in Registry.all_appnames()
        assert len(Exporter.modulenames()) == 1
        assert len(exporter) == 1
        assert exporter['youlike'] is youlike
        assert Exporter['yodogg.iheard'] is exporter
        assert Registry['yolocal'] is Exporter
        
        # __class_getitem__ method abuse 4 LYFE:
        assert Registry['yolocal']['yodogg.iheard']['youlike']() == "registries"
        
        # UNREGISTRATION » instance:
        assert Exporter.unregister('yodogg.iheard') is exporter
        assert len(Exporter.modulenames()) == 0
        assert 'yodogg.iheard' not in Exporter.modulenames()
        assert 'yodogg.iheard' not in Exporter.instances
        
        # UNREGISTRATION » subclass:
        assert Registry.unregister('yolocal') is Exporter
        assert 'yolocal' not in Registry.all_appnames()
    
    def test_exporter_instance_registry(self, clumods, consts):
        from clu.exporting import path_to_dotpath, Exporter
        from clu.fs.filesystem import Directory
        from clu.importing import modules_for_appname, Module
        from clu.predicates import haspyattr
        
        # Walk the importables:
        submodules = Directory(consts.BASEPATH).importables(consts.PROJECT_NAME)
        clsmodules = tuple(clsmodule.qualname for clsmodule in modules_for_appname(consts.PROJECT_NAME))
        
        # Sanity-check the number of modules:
        assert len(clumods) <= len(submodules) + len(clsmodules)
        
        # Check the Exporter instance against the module instance:
        for modname, module in clumods.items():
            assert (modname in submodules) or (modname in clsmodules)
            # assert Exporter[modname] # empty Exporter instances are Falsey
            if haspyattr(module, 'file'):
                # It’s a file-based module:
                assert Exporter[modname].path == module.__file__
                assert Exporter[modname].dotpath == path_to_dotpath(module.__file__,
                                                                    relative_to=consts.BASEPATH)
            elif isinstance(module, Module):
                # It’s a class-based module:
                assert Exporter[modname].path is None
                assert Exporter[modname].dotpath == module.qualname
            assert set(Exporter[modname].all_tuple()).issubset(module.__dir__())
    
    def test_combine_real_world_exporters_2(self):
        from clu.predicates import exporter as exporter0
        from clu.typology import exporter as exporter1
        from clu.fs.filesystem import exporter as exporter2
        from clu.exporting import Exporter
        
        # Sum the exporters:
        exporter_sum = Exporter()
        exporter_sum += exporter0
        exporter_sum += exporter1
        exporter_sum += exporter2
        
        # Check length:
        assert len(exporter_sum) == len(exporter0) + len(exporter1) + len(exporter2)
        
        # Check key membership:
        for key in exporter_sum.keys():
            assert (key in exporter0) or \
                   (key in exporter1) or \
                   (key in exporter2)
        
        # Check key set heirarchy:
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter0.all_tuple()))
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter1.all_tuple()))
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter2.all_tuple()))
    
    def test_combine_real_world_exporters_1(self):
        from clu.predicates import exporter as exporter0
        from clu.typology import exporter as exporter1
        from clu.exporting import Exporter
        
        # Sum the exporters:
        exporter_sum = Exporter()
        exporter_sum += exporter0
        exporter_sum += exporter1
        
        # Check length:
        assert len(exporter_sum) == len(exporter0) + len(exporter1)
        
        # Check key membership:
        for key in exporter_sum.keys():
            assert (key in exporter0) or \
                   (key in exporter1)
        
        # Check key set heirarchy:
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter0.all_tuple()))
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter1.all_tuple()))
    
    def test_combine_real_world_exporters_0(self):
        from clu.predicates import exporter as exporter0
        from clu.typology import exporter as exporter1
        
        # Sum the exporters:
        exporter_sum = exporter0 + exporter1
        
        # Check length:
        assert len(exporter_sum) == len(exporter0) + len(exporter1)
        
        # Check key membership:
        for key in exporter_sum.keys():
            assert (key in exporter0) or \
                   (key in exporter1)
        
        # Check key set heirarchy:
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter0.all_tuple()))
        assert frozenset(exporter_sum.all_tuple()).issuperset(frozenset(exporter1.all_tuple()))
    
    @pytest.mark.TODO
    def test_exporter_export_constants(self):
        # N.B. the warning checks will *FAIL* for some reason
        # if ExportWarning is imported from clu.constants,
        # instead of the same place where it is issued – in
        # this casse, “clu.exporting.Exporter.export(…)” (?!)
        from clu.exporting import Exporter, ExportWarning
        # from clu.naming import nameof
        
        exporter = Exporter()
        export = exporter.decorator()
        
        YO_DOGG = ('yo', 'dogg')
        I_HEARD = ["I", "heard", "you", "like", "constants"]
        
        # Trying to set the docs on constants issues a warning:
        with pytest.warns(ExportWarning):
            export(YO_DOGG,     name='YO_DOGG_W',     doc="“yo dogg” tuple.")
        
        with pytest.warns(ExportWarning):
            export(I_HEARD,     name='I_HEARD_W',     doc="“I heard…” list.")
        
        # NO DOCS ALLOWED:
        export(YO_DOGG,     name='YO_DOGG')
        export(I_HEARD,     name='I_HEARD')
        
        assert 'YO_DOGG' in exporter
        assert 'I_HEARD' in exporter
        assert 'YO_DOGG_W' in exporter
        assert 'I_HEARD_W' in exporter
        
        # These don’t work right at non-module-level:
        # assert nameof(YO_DOGG) == 'yo_dogg'
        # assert nameof(I_HEARD) == 'i_heard'
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 4
        assert len(test_dir()) == 4
        assert 'YO_DOGG' in test_all
        assert 'I_HEARD' in test_all
        assert 'YO_DOGG' in test_dir()
        assert 'I_HEARD' in test_dir()
        assert 'YO_DOGG_W' in test_all
        assert 'I_HEARD_W' in test_all
        assert 'YO_DOGG_W' in test_dir()
        assert 'I_HEARD_W' in test_dir()
    
    @pytest.mark.TODO
    def test_exporter_export_lambdas_no_name_provided(self):
        # N.B. “search_for_name()” should inspect locals (?!)
        # in order to make this work at non-module-level:
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        export = exporter.decorator()
        
        export(yo_dogg_lambda,     doc='yo_dogg_lambda() → Prints “Yo dogg.”')
        export(i_heard_lambda,     doc='i_heard_lambda() → Prints “I heard you like …” with argument reprs')
        
        assert 'yo_dogg_lambda' in exporter
        assert 'i_heard_lambda' in exporter
        assert yo_dogg_lambda.__name__ == 'yo_dogg_lambda'
        assert i_heard_lambda.__name__ == 'i_heard_lambda'
        assert yo_dogg_lambda.__qualname__ == 'yo_dogg_lambda'
        assert i_heard_lambda.__qualname__ == 'i_heard_lambda'
        assert nameof(yo_dogg_lambda) == 'yo_dogg_lambda'
        assert nameof(i_heard_lambda) == 'i_heard_lambda'
        
        assert 'yo_dogg_lambda() → Prints “Yo dogg.”' in yo_dogg_lambda.__doc__
        assert 'i_heard_lambda() → Prints “I heard you like …” with argument reprs' in i_heard_lambda.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg_lambda' in test_all
        assert 'i_heard_lambda' in test_all
        assert 'yo_dogg_lambda' in test_dir()
        assert 'i_heard_lambda' in test_dir()
    
    def test_exporter_context_manager_export_lambdas(self):
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        
        yo_dogg = lambda: print("Yo dogg.")
        i_heard = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        with exporter as export:
            export(yo_dogg,     name='yo_dogg',         doc='yo_dogg() → Prints “Yo dogg.”')
            export(i_heard,     name='i_heard',         doc='i_heard() → Prints “I heard you like …” with argument reprs')
        
        assert 'yo_dogg' in exporter
        assert 'i_heard' in exporter
        assert yo_dogg.__name__ == 'yo_dogg'
        assert i_heard.__name__ == 'i_heard'
        assert yo_dogg.__qualname__ == 'yo_dogg'
        assert i_heard.__qualname__ == 'i_heard'
        assert nameof(yo_dogg) == 'yo_dogg'
        assert nameof(i_heard) == 'i_heard'
        
        assert 'yo_dogg() → Prints “Yo dogg.”' in yo_dogg.__doc__
        assert 'i_heard() → Prints “I heard you like …” with argument reprs' in i_heard.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg' in test_all
        assert 'i_heard' in test_all
        assert 'yo_dogg' in test_dir()
        assert 'i_heard' in test_dir()
    
    def test_exporter_export_lambdas(self):
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        export = exporter.decorator()
        
        yo_dogg = lambda: print("Yo dogg.")
        i_heard = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        export(yo_dogg,     name='yo_dogg',         doc='yo_dogg() → Prints “Yo dogg.”')
        export(i_heard,     name='i_heard',         doc='i_heard() → Prints “I heard you like …” with argument reprs')
        
        assert 'yo_dogg' in exporter
        assert 'i_heard' in exporter
        assert yo_dogg.__name__ == 'yo_dogg'
        assert i_heard.__name__ == 'i_heard'
        assert yo_dogg.__qualname__ == 'yo_dogg'
        assert i_heard.__qualname__ == 'i_heard'
        assert nameof(yo_dogg) == 'yo_dogg'
        assert nameof(i_heard) == 'i_heard'
        
        assert 'yo_dogg() → Prints “Yo dogg.”' in yo_dogg.__doc__
        assert 'i_heard() → Prints “I heard you like …” with argument reprs' in i_heard.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg' in test_all
        assert 'i_heard' in test_all
        assert 'yo_dogg' in test_dir()
        assert 'i_heard' in test_dir()
    
    def test_exporter_context_manager_export_functions(self):
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        with exporter as export:
            
            @export
            def yo_dogg():
                """ yo_dogg() → Prints “Yo dogg.” """
                print("Yo dogg.")
            
            @export
            def i_heard(*wat):
                """ i_heard() → Prints “I heard you like …” with argument reprs """
                print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        assert 'yo_dogg' in exporter
        assert 'i_heard' in exporter
        assert nameof(yo_dogg) == 'yo_dogg'
        assert nameof(i_heard) == 'i_heard'
        
        assert 'yo_dogg() → Prints “Yo dogg.”' in yo_dogg.__doc__
        assert 'i_heard() → Prints “I heard you like …” with argument reprs' in i_heard.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg' in test_all
        assert 'i_heard' in test_all
        assert 'yo_dogg' in test_dir()
        assert 'i_heard' in test_dir()
    
    def test_exporter_export_functions(self):
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        export = exporter.decorator()
        
        @export
        def yo_dogg():
            """ yo_dogg() → Prints “Yo dogg.” """
            print("Yo dogg.")
        
        @export
        def i_heard(*wat):
            """ i_heard() → Prints “I heard you like …” with argument reprs """
            print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        assert 'yo_dogg' in exporter
        assert 'i_heard' in exporter
        assert nameof(yo_dogg) == 'yo_dogg'
        assert nameof(i_heard) == 'i_heard'
        
        assert 'yo_dogg() → Prints “Yo dogg.”' in yo_dogg.__doc__
        assert 'i_heard() → Prints “I heard you like …” with argument reprs' in i_heard.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg' in test_all
        assert 'i_heard' in test_all
        assert 'yo_dogg' in test_dir()
        assert 'i_heard' in test_dir()
    
    def test_exporter_export_wrapped_functions(self):
        from clu.exporting import Exporter
        from clu.naming import nameof
        from functools import lru_cache
        
        exporter = Exporter()
        export = exporter.decorator()
        
        @export
        @lru_cache(maxsize=32)
        def yo_dogg():
            """ yo_dogg() → Prints “Yo dogg.” """
            print("Yo dogg.")
        
        @export
        @lru_cache(maxsize=32)
        def i_heard(*wat):
            """ i_heard() → Prints “I heard you like …” with argument reprs """
            print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        assert 'yo_dogg' in exporter
        assert 'i_heard' in exporter
        assert nameof(yo_dogg) == 'yo_dogg'
        assert nameof(i_heard) == 'i_heard'
        
        assert 'yo_dogg() → Prints “Yo dogg.”' in yo_dogg.__doc__
        assert 'i_heard() → Prints “I heard you like …” with argument reprs' in i_heard.__doc__
        
        test_all, test_dir = exporter.all_and_dir()
        
        assert len(test_all) == 2
        assert len(test_dir()) == 2
        assert 'yo_dogg' in test_all
        assert 'i_heard' in test_all
        assert 'yo_dogg' in test_dir()
        assert 'i_heard' in test_dir()
