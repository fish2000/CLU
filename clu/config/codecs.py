# -*- coding: utf-8 -*-
from __future__ import print_function
import json

from clu.constants.consts import pytuple
from clu.config.abc import FrozenKeyMap, KeyMap, NamespaceWalker
from clu.config.keymap import FrozenFlat, Flat, FrozenNested, Nested
from clu.naming import qualified_import, qualified_name
from clu.predicates import allitems
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
    return { '__qualname__' : qualified_name(thing),
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
