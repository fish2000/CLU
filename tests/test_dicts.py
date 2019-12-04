# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestDicts(object):
    
    """ Run the tests for merging dicts (the clu.dicts module), and
        namespaces (the clu.typespace and clu.typespace.namespace modules).
    """
    
    def test_chainmap(self, dirname, environment):
        from clu.dicts import ChainMap
        # from clu.predicates import getitem, try_items
        
        # READ-ONLY:
        data = dirname.subdirectory('data')
        
        # Arbitrary:
        dict_one = {
            'yo'    : "dogg",
            'i'     : "heard",
            'you'   : "liked",
            'dict'  : "chains" }
        
        # Create a ChainMap from a dict, a Directory instance,
        # and an environment mapping:
        hey = ChainMap(dict_one, data, environment)
        
        # Check length and boolean value:
        assert len(hey) == len(dict_one) + len(data) + len(environment)
        assert bool(hey)
        
        # Check keys from respective sub-maps:
        for key in ('yo', 'i', 'you', 'dict'):
            assert key in hey
            assert hey.mapcontaining(key) == dict_one
            assert hey.get(key) == dict_one.get(key)
        
        for key in ('config', 'yodata', 'yodogg',
                    '8ba.png', '3472236406_1fbf1a567d_o.jpg', 'shutterstock_90194617.jpg',
                    'IMG_20180505_205153567.jpg', '3471426989_aa8e83cac5_o.jpg'):
            assert key in hey
            assert hey.mapcontaining(key) == data
            assert hey.get(key) == data.get(key)
        
        for key in ('SHELL', 'LESS', 'HOME', 'LANG'):
            assert key in hey
            assert hey.mapcontaining(key) == environment
            assert hey.get(key) == environment.get(key)
        
        # Check for KeyErrors on bad item access:
        with pytest.raises(KeyError) as exc:
            hey['WTF-HAX']
        assert "WTF-HAX" in str(exc.value)
        
        with pytest.raises(KeyError) as exc:
            hey.get('WTF-HAX')
        assert "WTF-HAX" in str(exc.value)
        
        # Check for default return on bad item access with default:
        assert hey.get('WTF-HAX', default='nodogg') == 'nodogg'
        
        # SHIFT » like collections.ChainMap.parents:
        beentrying = hey.shift()
        
        assert len(beentrying.maps) < len(hey.maps)
        assert len(beentrying.keys()) < len(hey.keys())
        assert len(beentrying.values()) < len(hey.values())
        
        assert frozenset(hey).issuperset(beentrying)
        assert frozenset(hey.keys()).issuperset(beentrying.keys())
        
        for map in beentrying.maps:
            assert map in hey.maps
        
        # UNSHIFT » like collections.ChainMap.new_child(…):
        tomeetyou = hey.unshift()
        
        assert len(tomeetyou.maps) > len(hey.maps)
        assert len(tomeetyou.keys()) == len(hey.keys())
        assert len(tomeetyou.values()) == len(hey.values())
        assert len(tomeetyou.keys()) > len(beentrying.keys())
        assert len(tomeetyou.values()) > len(beentrying.values())
        
        assert frozenset(tomeetyou).issuperset(hey)
        assert frozenset(tomeetyou.keys()).issuperset(hey.keys())
        
        for map in hey.maps:
            assert map in tomeetyou.maps
        
        tomeetyou['mustbe'] = "a devil"
        tomeetyou['betweenus'] = "or whores in my head"
        tomeetyou['whoredoor'] = "whores in my bed"
        
        for key in ('mustbe', 'betweenus', 'whoredoor'):
            assert key in tomeetyou
            assert key not in hey
            assert key not in beentrying
            assert len(tomeetyou.mapcontaining(key)) == 3
            assert type(tomeetyou.get(key)) is str
        
        # CLONE » not via “clu.config.abc.Cloneable” …yet:
        
        buthey = hey.clone()
        where = beentrying.clone(deep=True)
        haveyou = tomeetyou.clone(deep=True)
        
        assert len(hey) == len(buthey)
        assert len(beentrying) == len(where)
        assert len(tomeetyou) == len(haveyou)
        
        '''
        for orig, clone in ((hey, buthey), (beentrying, where), (tomeetyou, haveyou)):
            for key in orig.keys():
                assert key in clone
                assert key in clone.flatten()
                # assert orig.get(key) == clone.get(key)
                assert key in orig
                assert key in orig.flatten()
                assert try_items(key, *orig.maps, default=None) is not None
                assert try_items(key, *clone.maps, default=None) is not None
                assert try_items(key, *orig.maps, default=None) == try_items(key, *clone.maps, default=None)
                # FAILS:
                # assert try_items(key, *orig.maps, default=None) == orig[key]
                # assert try_items(key, *clone.maps, default=None) == clone[key]
        '''
        
        # ONE LAST CHECK. And we’ll call it a day.
        been = ChainMap(dict_one, data, environment)
        assert frozenset(buthey).issuperset(where)
        assert not frozenset(hey).issuperset(haveyou)
        assert frozenset(buthey).issuperset(been)
    
    def test_ordered_mapping_views(self, dirname):
        """ The ordered mapping views are returned from “clu.fs.filesystem.Directory”
            mapping-view methods: “directory.items()”, “directory.keys()”, and
            “directory.values()”.
        """
        from clu.dicts import OrderedItemsView, OrderedKeysView, OrderedValuesView
        from clu.fs.filesystem import Directory
        from clu.typology import ismapping, issequence
        
        # READ-ONLY:
        data = dirname.subdirectory('data')
        
        # Ensure type:
        assert type(dirname) is Directory
        assert type(data) is Directory
        assert type(data.items()) is OrderedItemsView
        assert type(data.keys()) is OrderedKeysView
        assert type(data.values()) is OrderedValuesView
        
        # Ensure it’s a mapping:
        assert ismapping(dirname)
        assert ismapping(data)
        
        # Ensure it’s a sequence:
        assert issequence(data.items())
        assert issequence(data.keys())
        assert issequence(data.values())
        
        # Ensure repr:
        assert repr(dirname).startswith('Directory')
        assert repr(data).startswith('Directory')
        assert repr(data.items()).startswith('OrderedItemsView')
        assert repr(data.keys()).startswith('OrderedKeysView')
        assert repr(data.values()).startswith('OrderedValuesView')
        
        # Redundant, but correct:
        assert len(data.items()) == len(data.keys()) == len(data.values())
        assert len(list(data.items())) == len(list(data.keys())) == len(list(data.values()))
        assert len(data.items()) == len(list(data.items()))
        assert len(data.keys()) == len(list(data.keys()))
        assert len(data.values()) == len(list(data.values()))
        
        # Nonexistent subdirectory:
        assert len(data.subdirectory('wat').items()) == 0
        assert len(data.subdirectory('wat').keys()) == 0
        assert len(data.subdirectory('wat').values()) == 0
        
        # Real subdirectory with at least one item:
        assert len(data.subdirectory('yodogg').items()) > 0
        assert len(data.subdirectory('yodogg').keys()) > 0
        assert len(data.subdirectory('yodogg').values()) > 0
        
        # Set properties:
        k1 = data.subdirectory('yodogg').keys()
        k2 = data.subdirectory('yodata').keys()
        kU = k1 | k2
        assert type(kU) is set
        assert len(kU) == len(k1) + len(k2)
        assert kU.issuperset(k1)
        assert kU.issuperset(k2)
        
        # Sequence properties:
        keys = data.keys()
        for idx in range(len(keys)):
            assert keys[idx] == list(keys)[idx]
            assert keys[idx] in data
    
    def test_dict_and_namespace_merge(self):
        from clu.dicts import merge
        from clu.typespace import Namespace
        
        dict_one = { 'compress_level' : 9,
                           'optimize' : True,
                             'format' : 'png' }
        
        dict_two = { 'yo' : 'dogg' }
        
        dict_three = { 'compress_level' : 10,
                             'optimize' : True,
                               'format' : 'jpg' }
        
        merged = merge(dict_one, dict_two, dict_three, yo='DOGG')
        
        # print("» Checking “merge(•) …”")
        # print()
        
        assert merged == { 'compress_level' : 9,
                                 'optimize' : True,
                                   'format' : 'png',
                                       'yo' : 'DOGG' }
        
        # print("» Checking “Namespace.operator+(•) …”")
        # print()
        
        ns1 = Namespace(dict_one)
        ns2 = Namespace(dict_two)
        
        merged = ns1 + ns2 + dict_three + Namespace(yo='DOGG')
        
        assert merged == { 'compress_level' : 9,
                                 'optimize' : True,
                                   'format' : 'png',
                                       'yo' : 'dogg' }
        
        # print("» Checking “Namespace.operator+=(•) …”")
        # print()
        
        merged = Namespace(dict_one)
        ns2 = Namespace(dict_two)
        
        merged += ns2
        merged += dict_three
        merged += Namespace(yo='DOGG')
        
        assert merged == { 'compress_level' : 10,
                                 'optimize' : True,
                                   'format' : 'jpg',
                                       'yo' : 'DOGG' }
        
        # print_separator()
        # pprint(merged)
        # print_separator()
        # print()
    