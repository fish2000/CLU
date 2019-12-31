# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class NamespaceKeyError(KeyError):
    pass

class TestNamespace(object):
    
    """ Run the tests for namespaces – “clu.typespace.namespace” """
    
    def test_implicit_recursive_namespaces(self):
        """ Implicit recursive namespaces """
        from clu.typespace.namespace import Namespace
        
        ROOT = Namespace()
        
        ROOT.title = "«title»"
        ROOT.count = 666
        ROOT.idx = 0
        
        with ROOT.other as ns:
            ns.additional = "«additional»"
            ns.considerations = "…"
        
        ROOT.yo.dogg = "yo dogg"
        ROOT.yo.wat = "¡WAT!"
        
        assert ROOT.other.additional        == "«additional»"
        assert ROOT.other.considerations    == "…"
        assert ROOT.yo.dogg                 == "yo dogg"
        assert ROOT.yo.wat                  == "¡WAT!"
        
        with ROOT.other as ns:
            assert ns.additional            == "«additional»"
            assert ns.considerations        == "…"
    
    def test_namespace_subclass_missing(self):
        """ Namespace subclass “__missing__(…)” check """
        from clu.typespace.namespace import Namespace
        
        class MissingNamespace(Namespace):
            
            def __missing__(self, key):
                """ Raise a bespoke exception on missing key access """
                raise NamespaceKeyError(key)
        
        with pytest.raises(NamespaceKeyError) as exc:
            MissingNamespace()['wat']
        assert 'wat' in str(exc.value)
        
        try:
            MissingNamespace()['wat']
        except NamespaceKeyError as exc:
            assert bool(exc)
    
    def test_dict_and_namespace_merge(self):
        """ Check both “clu.dicts.merge(…)” and “clu.typespace.namespace” addition operators """
        from clu.dicts import merge
        from clu.typespace.namespace import Namespace
        
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
    