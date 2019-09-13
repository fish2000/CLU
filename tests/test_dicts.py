# -*- coding: utf-8 -*-
from __future__ import print_function

class TestDicts(object):
    
    """ Run the tests for merging dicts (the clu.dicts module), and
        namespaces (the clu.typespace and clu.typespace.namespace modules).
    """
    
    def test_ordered_mapping_views(self, dirname):
        """ The ordered mapping views are returned from “clu.fs.filesystem.Directory”
            mapping-view methods: “directory.items()”, “directory.keys()”, and
            “directory.values()”.
        """
        from clu.dicts import OrderedItemsView, OrderedKeysView, OrderedValuesView
        from clu.typology import issequence
        
        # READ-ONLY:
        data = dirname.subdirectory('data')
        
        # Ensure type:
        assert type(data.items()) is OrderedItemsView
        assert type(data.keys()) is OrderedKeysView
        assert type(data.values()) is OrderedValuesView
        
        # Ensure it’s a sequence:
        assert issequence(data.items())
        assert issequence(data.keys())
        assert issequence(data.values())
        
        # Ensure repr:
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
        
        # print_separator()
        # pprint(merged)
        # print_separator()
        # print()
        
        # print("» Checking “Namespace.operator+(•) …”")
        # print()
        
        ns1 = Namespace(dict_one)
        ns2 = Namespace(dict_two)
        
        merged = ns1 + ns2 + dict_three + Namespace(yo='DOGG')
        
        assert merged == { 'compress_level' : 9,
                                 'optimize' : True,
                                   'format' : 'png',
                                       'yo' : 'dogg' }
        
        # print_separator()
        # pprint(merged)
        # print_separator()
        # print()
        
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
    