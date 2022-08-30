# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import pickle
import sys

from clu.constants.consts import pytuple
from clu.config.abc import FrozenKeyMap, KeyMap, NamespaceWalker
from clu.config.env import FrozenEnviron, Environ
from clu.config.keymap import FrozenFlat, Flat, FrozenNested, Nested
from clu.dicts import asdict
from clu.naming import qualified_import, qualified_name
from clu.predicates import allitems, item, typeof
from clu.typology import subclasscheck
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# CODEC PREDICATES: suss out what things are KeyMaps:

iskeymap = lambda putative: subclasscheck(putative, FrozenFlat, Flat, FrozenNested, Nested, FrozenEnviron, Environ)
isflatkeymap = lambda putative: subclasscheck(putative, FrozenFlat, Flat)
isnestedkeymap = lambda putative: subclasscheck(putative, FrozenNested, Nested)
isfrozenkeymap = lambda putative: subclasscheck(putative, FrozenNested, FrozenFlat, FrozenEnviron) and \
                              not subclasscheck(putative, KeyMap)
ismutablekeymap = lambda putative: subclasscheck(putative, Nested, Flat, Environ)

# CODEC INTERNAL REPRESENTATION: convert things to and from “annotated dicts”:

@export
def annotated_dict_for(thing):
    thing_t = typeof(thing)
    out = { '__qualname__' : qualified_name(thing_t) }
    if hasattr(thing_t, 'to_dict'):
        out['__dict__'] = asdict(thing)
    else:
        out['__list__'] = list(thing)
    return out

@export
def instance_for(annotated_dict):
    cls = qualified_import(annotated_dict['__qualname__'])
    inner_dict = item(annotated_dict, '__dict__', '__list__')
    return hasattr(cls, 'from_dict') and cls.from_dict(inner_dict) \
                                      or cls(inner_dict)

# JSON CODEC SUBCLASSES:

@export
class Encoder(json.JSONEncoder):
    
    def default(self, obj):
        """ Intercept our objects and dict-ify them as our
            so-called “annotated dicts” before serialization
        """
        if iskeymap(obj):
            return annotated_dict_for(obj)
        return super().default(obj)

@export
class Decoder(json.JSONDecoder):
    
    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.object_hook
        super().__init__(*args, **kwargs)
    
    def object_hook(self, obj):
        """ Look for annotated dicts, and reconstitute them
            as represented objects as necessary
        """
        if isinstance(obj, dict) and allitems(obj, *pytuple('qualname', 'dict')):
            return instance_for(obj)
        return obj

encoder = Encoder(indent=4)
decoder = Decoder()

@export
def json_encode(things):
    return encoder.encode(things)

@export
def json_decode(string):
    return decoder.decode(string)

def pickle_encode(things):
    return pickle.dumps(things)

def pickle_decode(string):
    return pickle.loads(string)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.keymap import nestedmaps, flatdict, arbitrary
    from pprint import pprint
    
    @inline
    def test_annotated_dict_for():
        """ Convert KeyMap instances to “annotated dicts” """
        flat = Flat(flatdict())
        nested = Nested(nestedmaps())
        
        anndict_flat = annotated_dict_for(flat)
        anndict_nested = annotated_dict_for(nested)
        
        assert allitems(anndict_flat, *pytuple('qualname', 'dict'))
        assert allitems(anndict_nested, *pytuple('qualname', 'dict'))
        
        # print("flat qualname:", qualified_name(Flat))
        # print("anndict_nested['__dict__']:")
        # pprint(anndict_nested['__dict__'])
        # print("nestedmaps():")
        # pprint(nestedmaps())
        
        assert anndict_flat['__qualname__'] == qualified_name(Flat)
        assert anndict_nested['__qualname__'] == qualified_name(Nested)
        assert anndict_flat['__dict__'] == flatdict()
        assert anndict_nested['__dict__'] == nestedmaps()
    
    @inline
    def test_instance_for():
        """ Convert “annotated dicts” back to KeyMap instances """
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
    
    @inline
    def test_json_encode_decode():
        """ Round-trip KeyMap instances through JSON """
        flat = Flat(flatdict())
        nested = Nested(nestedmaps())
        
        flat_json = json_encode(flat)
        nested_json = json_encode(nested)
        
        # print("flat_json:")
        # print(flat_json)
        # print()
        
        # print("nested_json:")
        # print(nested_json)
        # print()
        
        reconstituted_flat = json_decode(flat_json)
        reconstituted_nested = json_decode(nested_json)
        
        assert reconstituted_flat == reconstituted_nested
        assert reconstituted_flat == flat
        assert reconstituted_nested == nested
    
    @inline
    def test_json_encode_decode_fenv():
        """ Round-trip frozen environments through JSON """
        fenv = FrozenEnviron(appname='project')
        fenv_json = json_encode(fenv)
        reconstituted_fenv = json_decode(fenv_json)
        assert reconstituted_fenv == fenv
        assert len(fenv) > 0
        assert len(reconstituted_fenv) == len(fenv)
    
    @inline
    def test_json_encode_decode_env():
        """ Round-trip environments through JSON """
        env = Environ(appname='project')
        env_json = json_encode(env)
        reconstituted_env = json_decode(env_json)
        assert reconstituted_env == env
        assert len(env) > 0
        assert len(reconstituted_env) == len(env)
    
    @inline
    def test_pickle_encode_decode():
        """ Round-trip KeyMap instances through pickling """
        flat = Flat(flatdict())
        nested = Nested(nestedmaps())
        
        flat_pickle = pickle_encode(flat)
        nested_pickle = pickle_encode(nested)
        
        reconstituted_flat = pickle_decode(flat_pickle)
        reconstituted_nested = pickle_decode(nested_pickle)
        
        assert reconstituted_flat == reconstituted_nested
        assert reconstituted_flat == flat
        assert reconstituted_nested == nested
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())