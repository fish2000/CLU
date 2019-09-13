# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.dicts import merge
from clu.typespace import Namespace

class TestDicts(object):
    
    """ Run the tests for merging dicts (the clu.dicts module), and
        namespaces (the clu.typespace and clu.typespace.namespace modules).
    """
    
    def test_dict_and_namespace_merge(self):
        
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
    