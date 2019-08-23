# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import pytest

class TestConfig(object):
    
    def test_nested_and_flat(self):
        from clu.config.base import Nested
        
        tree = {
            'yo'        : "dogg",
            'i_heard'   : "you like",
            'nested'    : "dicts",
            'so'        : "we put dicts in your dicts",
            
            'wat'       : { 'yo'        : "dogggggg",
                            'yoyo'      : "dogggggggggg" },
            
            'nodogg'    : { 'yo'        : "dogggggg",
                            'yoyo'      : "dogggggggggg" }
        }
        
        dictionary = {
            'i_heard'       : 'you like',
            'nested'        : 'dicts',
            'nodogg:yo'     : 'dogggggg',
            'nodogg:yoyo'   : 'dogggggggggg',
            'so'            : 'we put dicts in your dicts',
            'wat:yo'        : 'dogggggg',
            'wat:yoyo'      : 'dogggggggggg',
            'yo'            : 'dogg'
        }
        
        nested = Nested(tree=tree)
        
        assert tuple(nested.keys()) == ('yo', 'i_heard', 'nested', 'so',
                                        'wat:yo', 'wat:yoyo', 'nodogg:yo', 'nodogg:yoyo')
        assert tuple(nested.values()) == ('dogg', 'you like', 'dicts', 'we put dicts in your dicts',
                                          'dogggggg', 'dogggggggggg', 'dogggggg', 'dogggggggggg')
        assert tuple(nested.namespaces()) == ('nodogg', 'wat')
        
        flat = nested.flatten()
        
        assert tuple(flat.keys()) == ('yo', 'i_heard', 'nested', 'so',
                                      'wat:yo', 'wat:yoyo', 'nodogg:yo', 'nodogg:yoyo')
        assert tuple(flat.values()) == ('dogg', 'you like', 'dicts', 'we put dicts in your dicts',
                                        'dogggggg', 'dogggggggggg', 'dogggggg', 'dogggggggggg')
        assert tuple(flat.namespaces()) == ('nodogg', 'wat')
        
        assert flat.dictionary == dictionary
        
        renestified = flat.nestify()
        
        assert renestified.tree == tree
        assert renestified == flat
        assert flat == nested
        assert renestified == nested
    
    def test_FlatOrderedSet(self):
        from clu.config.fieldtypes import FlatOrderedSet
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff.things == summary.things
        assert stuff == summary
        assert not stuff.isdisjoint(summary)
    
    def test_NamespacedFieldManager_module_getattr_instancing(self):
        from clu.config.fieldtypes import fields as fields0
        from clu.config.fieldtypes import fields as fields1
        
        # Ensure each import of “fields” is instanced anew:
        assert id(fields0) != id(fields1)
        
        # Ensure the module __getattr__ raises for other keys:
        with pytest.raises(ImportError) as exc:
            from clu.config.fieldtypes import yodogg
            del yodogg
        assert "cannot import name" in str(exc.value)
    
    def test_dict_merge(self):
        pass
    
    def test_env_get(self, environment):
        from clu.config.env import Env
        env = Env()
        
        try:
            environment['CLU_ENVTEST1_YODOGG']  = "Yo, Dogg –"
            environment['CLU_ENVTEST1_IHEARD']  = "… I Heard"
            environment['CLU_ENVTEST1_YOULIKE'] = "You Like Environment Variables."
            
            assert env['envtest1:yodogg']  == "Yo, Dogg –"
            assert env['envtest1:iheard']  == "… I Heard"
            assert env['envtest1:youlike'] == "You Like Environment Variables."
            
            assert 'envtest1' in env.namespaces()
        
        finally:
            del environment['CLU_ENVTEST1_YODOGG']
            del environment['CLU_ENVTEST1_IHEARD']
            del environment['CLU_ENVTEST1_YOULIKE']
        
        assert 'envtest1:yodogg'  not in env
        assert 'envtest1:iheard'  not in env
        assert 'envtest1:youlike' not in env
        
        assert 'envtest1' not in env.namespaces()
    
    def test_env_set(self, environment):
        from clu.config.env import Env
        env = Env()
        
        try:
            env['envtest0:yodogg']  = "Yo Dogg"
            env['envtest0:iheard']  = "I Heard"
            env['envtest0:youlike'] = "You Like Environment Variables"
            
            assert environment['CLU_ENVTEST0_YODOGG']  == "Yo Dogg"
            assert environment['CLU_ENVTEST0_IHEARD']  == "I Heard"
            assert environment['CLU_ENVTEST0_YOULIKE'] == "You Like Environment Variables"
            
            assert 'envtest0' in env.namespaces()
        
        finally:
            del env['envtest0:yodogg']
            del env['envtest0:iheard']
            del env['envtest0:youlike']
        
        assert 'CLU_ENVTEST0_YODOGG'  not in environment
        assert 'CLU_ENVTEST0_IHEARD'  not in environment
        assert 'CLU_ENVTEST0_YOULIKE' not in environment
        
        assert 'envtest0' not in env.namespaces()
    
    def test_toml_and_file_search(self, dirname, environment):
        from clu.config.formats import TomlFile
        from clu.predicates import tuplize
        
        cfgs = dirname.subdirectory('data').subdirectory('config')
        
        assert cfgs.exists
        assert TomlFile.appname in TomlFile.filename
        assert TomlFile.filename in cfgs
        
        toml_file = TomlFile(extra_user_dirs=tuplize(cfgs))
        
        assert os.path.exists(toml_file.filepath)
        assert toml_file.filesuffix == 'toml'
        assert toml_file.filepath.endswith(toml_file.filesuffix)
        
        assert toml_file.namespaces() == ('debugging', 'userinfo')
        assert toml_file['project'] == 'clu'
        assert toml_file['description'] is not None
        assert toml_file['description_content_type'] == 'text/markdown'
        assert toml_file['debugging:debug'] == True
        assert toml_file['debugging:logging'] == True
        assert toml_file['debugging:logdir'] == '/usr/local/var/run/clu'
        assert toml_file['userinfo:user'] == 'fish'
        assert toml_file['userinfo:email'] == 'fish2000@gmail.com'
        assert toml_file['userinfo:fullname'] == 'Alexander Böhn'
        assert toml_file['userinfo:organization'] == 'Objects In Space And Time, LLC'
        
        flat = toml_file.flatten()
        
        assert flat.namespaces() == ('debugging', 'userinfo')
        assert flat['project'] == 'clu'
        assert flat['description'] is not None
        assert flat['description_content_type'] == 'text/markdown'
        assert flat['debugging:debug'] == True
        assert flat['debugging:logging'] == True
        assert flat['debugging:logdir'] == '/usr/local/var/run/clu'
        assert flat['userinfo:user'] == 'fish'
        assert flat['userinfo:email'] == 'fish2000@gmail.com'
        assert flat['userinfo:fullname'] == 'Alexander Böhn'
        assert flat['userinfo:organization'] == 'Objects In Space And Time, LLC'
        
        assert toml_file == flat
        
        default_toml = TomlFile.find_file(extra_user_dirs=tuplize(cfgs))
        different_toml = TomlFile.find_file(filename='yodogg.toml', extra_user_dirs=tuplize(cfgs))
        
        assert default_toml.endswith('tests/data/config/clu-config.toml')
        assert different_toml.endswith('tests/data/config/yodogg.toml')
        
        with pytest.raises(FileNotFoundError) as exc:
            TomlFile.find_file(filename='NO-DOGG.toml', extra_user_dirs=tuplize(cfgs))
        assert "config file NO-DOGG.toml" in str(exc.value)
