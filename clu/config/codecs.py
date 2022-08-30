# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys

from clu.constants.consts import pytuple
from clu.config.abc import FrozenKeyMap, KeyMap, NamespaceWalker
from clu.config.keymap import FrozenFlat, Flat, FrozenNested, Nested
from clu.naming import qualified_import, qualified_name
from clu.predicates import allitems, typeof
from clu.typology import subclasscheck
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

iskeymap = lambda putative: subclasscheck(putative, FrozenFlat, Flat, FrozenNested, Nested)
isflatkeymap = lambda putative: subclasscheck(putative, FrozenFlat, Flat)
isnestedkeymap = lambda putative: subclasscheck(putative, FrozenNested, Nested)
isfrozenkeymap = lambda putative: subclasscheck(putative, FrozenNested, FrozenFlat) and \
                              not subclasscheck(putative, KeyMap)
ismutablekeymap = lambda putative: subclasscheck(putative, Nested, Flat)

def annotated_dict_for(thing):
    return { '__qualname__' : qualified_name(typeof(thing)),
             '__dict__'     : dict(thing) }

def instance_for(annotated_dict):
    cls = qualified_import(annotated_dict['__qualname__'])
    return cls(annotated_dict['__dict__'])

@export
class Encoder(json.JSONEncoder):
    
    def default(self, obj):
        if iskeymap(obj):
            return annotated_dict_for(thing)
        return super().default(self, obj)

@export
class Decoder(json.JSONDecoder):
    
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, obj):
        if isinstance(obj, dict) and allitems(obj, *pytuple('qualname', 'dict')):
            return instance_for(obj)
        return obj

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.keymap import nestedmaps, flatdict, arbitrary
    from pprint import pprint
    
    @inline
    def test_annotated_dict_for():
        flat = Flat(flatdict())
        nested = Nested(nestedmaps())
        
        anndict_flat = annotated_dict_for(flat)
        anndict_nested = annotated_dict_for(nested)
        
        assert allitems(anndict_flat, *pytuple('qualname', 'dict'))
        assert allitems(anndict_nested, *pytuple('qualname', 'dict'))
        
        # print("flat qualname:", qualified_name(Flat))
        
        assert anndict_flat['__qualname__'] == qualified_name(Flat)
        assert anndict_nested['__qualname__'] == qualified_name(Nested)
        assert anndict_flat['__dict__'] == flatdict()
        assert anndict_nested['__dict__'] == flatdict()
    
    @inline
    def test_instance_for():
        anndict_flat = {
            '__qualname__'  : 'clu.config.keymap.Flat',
            '__dict__'      : flatdict() }
        anndict_nested = {
            '__qualname__'  : 'clu.config.keymap.Nested',
            '__dict__'      : nestedmaps() }
        
        instance_flat = instance_for(anndict_flat)
        instance_nested = instance_for(anndict_nested)
        
        assert typeof(instance_flat) == Flat
        assert typeof(instance_nested) == Nested
        
        assert instance_flat == instance_nested
        
        assert instance_flat.dictionary == flatdict()
        assert instance_nested.tree == nestedmaps()
        
        # print("instance_nested.tree:")
        # pprint(instance_nested.tree)
        # print("nestedmaps():")
        # pprint(nestedmaps())
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())