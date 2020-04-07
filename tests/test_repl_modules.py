# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

mods = ('clu.all',
        'clu.abstract',
        'clu.constants.consts',
        'clu.constants.polyfills',
        'clu.config.base',
        'clu.config.settings',
        'clu.config.ns',
        'clu.csv',
        'clu.fs.appdirectories',
        'clu.fs.pypath',
        'clu.keyvalue',
        'clu.dispatch',
        'clu.scripts.ansicolors',
        'clu.scripts.boilerplate',
        'clu.sanitizer')

class TestReplModules(object):
    
    """ Run the tests for the “clu.repl.modules” module. """
    
    def test_compare_module_lookups_for_all_things_no_args(self):
        from clu.repl.modules import compare_module_lookups_for_all_things
        from clu.repl.modules import Results, Mismatches
        from clu.repl.modules import Result, Mismatch
        
        results, mismatches = compare_module_lookups_for_all_things()
        
        assert type(results) is Results
        assert type(mismatches) is Mismatches
        
        assert results.total > 500
        assert results.total == sum(len(record.thingnames) for record in results.result_records)
        assert len(mismatches.mismatch_records) == mismatches.total
        assert len(mismatches.mismatch_records) < 50    # should be around 15 or 16
        assert mismatches.failure_rate < 10.0           # last I checked this was ~2.841
        assert mismatches.failure_rate == 100 * (float(mismatches.total) / float(results.total))
        
        assert all(type(record) is Result for record in results.result_records)
        assert all(type(record) is Mismatch for record in mismatches.mismatch_records)
    
    def test_compare_module_lookups_for_all_things_variadic_args(self):
        from clu.repl.modules import compare_module_lookups_for_all_things
        from clu.repl.modules import Results, Mismatches
        from clu.repl.modules import Result, Mismatch
        
        modules = ('predicates', 'typology', 'mathematics', 'naming')
        prefixd = tuple(f"clu.{nm}" for nm in modules)
        results, mismatches = compare_module_lookups_for_all_things(*prefixd)
        
        assert type(results) is Results
        assert type(mismatches) is Mismatches
        
        assert results.total > 100
        assert results.total == sum(len(record.thingnames) for record in results.result_records)
        assert len(mismatches.mismatch_records) == mismatches.total
        assert len(mismatches.mismatch_records) < 50    # should be around 5 or 6
        assert mismatches.failure_rate < 10.0           # last I checked this was ~2.841
        assert mismatches.failure_rate == 100 * (float(mismatches.total) / float(results.total))
        
        assert all(type(record) is Result for record in results.result_records)
        assert all(type(record) is Mismatch for record in mismatches.mismatch_records)
    
    @pytest.mark.parametrize('modulename', mods)
    def test_modulemap(self, modulename):
        from clu.naming import nameof, qualified_import
        from clu.repl.modules import ModuleMap
        from copy import copy, deepcopy
        
        module = qualified_import(modulename)
        
        try:
            modmap = ModuleMap(module)
        
        except ValueError as exc:
            assert "one or more things" in str(exc)
        
        else:
            assert len(modmap) == len(module.__all__)
            
            for thingname in dir(module):
                assert modmap[thingname] == getattr(module, thingname)
            for thingname in reversed(modmap):
                assert modmap[thingname] == getattr(module, thingname)
            
            # calculate “most”:
            most = max(len(thingname) for thingname in dir(module))
            assert most == modmap.most()
            
            # set membership check for modmap.keys():
            frozenthings = frozenset(module.__all__)
            
            assert frozenthings.issuperset(modmap.keys())
            assert frozenthings.issubset(modmap.keys())
            
            # set membership check for modmap.items():
            frozenpairs = frozenset(zip(modmap.keys(), modmap.values()))
            
            assert frozenpairs.issuperset(modmap.items())
            assert frozenpairs.issubset(modmap.items())
            
            # repr checks:
            assert repr(dict(modmap)) in repr(modmap)
            assert repr(modmap).startswith(nameof(ModuleMap))
            
            # copy/clone checks:
            assert copy(modmap) == modmap
            assert deepcopy(modmap) == modmap
            assert modmap.clone() == modmap
    
    def test_modulemap_error_conditions(self, consts):
        from clu.repl.modules import ModuleMap
        
        with pytest.raises(TypeError) as exc:
            ModuleMap(None)
        assert "valid module required" in str(exc.value)
        
        with pytest.raises(TypeError) as exc:
            ModuleMap(True)
        assert "module instance required" in str(exc.value)
        
        constmap = ModuleMap(consts)
        
        # dunder attribute that exists in consts:
        with pytest.raises(KeyError) as exc:
            constmap['__dir__']
        assert "__dir__" in str(exc.value)
        
        # non-dunder attribute that does not exist in consts:
        with pytest.raises(KeyError) as exc:
            constmap['YO_DOGG']
        assert "YO_DOGG" in str(exc.value)
