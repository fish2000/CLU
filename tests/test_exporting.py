# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestExporting(object):
    
    """ Run the tests for the clu.exporting module. """
    
    def test_combine_real_world_exporters(self):
        from clu.predicates import exporter as exporter0
        from clu.typology import exporter as exporter1
        
        exporter_sum = exporter0 + exporter1
        assert len(exporter_sum) == len(exporter0) + len(exporter1)
    
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
    
    def _test_exporter_export_lambdas_no_name_provided(self):
        # N.B. “thingname_search()” should inspect locals (?!)
        # in order to make this work at non-module-level:
        from clu.exporting import Exporter
        from clu.naming import nameof
        
        exporter = Exporter()
        export = exporter.decorator()
        
        yo_dogg = lambda: print("Yo dogg.")
        i_heard = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        export(yo_dogg,     doc='yo_dogg() → Prints “Yo dogg.”')
        export(i_heard,     doc='i_heard() → Prints “I heard you like …” with argument reprs')
        
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
