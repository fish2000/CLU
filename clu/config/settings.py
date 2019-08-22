# -*- coding: utf-8 -*-
from __future__ import print_function

import abc

from clu.constants.consts import ENCODING, PYTHON_VERSION
from clu.config.base import Flat, Nested
from clu.config.fieldtypes import FieldBase
from clu.fs.misc import stringify
from clu.predicates import haspyattr, getpyattr, stor_none, iscontainer
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NEED_NAME = PYTHON_VERSION < 3.6

class MetaSchema(abc.ABCMeta):
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        
        field_index = Flat()
        field_names = {}
        
        for attribute, value in attributes.items():
            if isinstance(value, FieldBase):
                if NEED_NAME:
                    value.__set_name__(None, attribute)
                attributes[attribute] = value
                field_names[attribute] = value
                field_index.set(attribute, value,
                                namespace=value.namespace)
        
        for base in bases:
            parent = base.__mro__[0]
            for attribute, value in vars(parent).items():
                if isinstance(value, FieldBase) and attribute not in attributes:
                    if NEED_NAME:
                        value.__set_name__(None, attribute)
                    attributes[attribute] = value
                    field_names[attribute] = value
                    field_index.set(attribute, value,
                                    namespace=value.namespace)
        
        attributes['__field_index__'] = field_index
        attributes['__field_names__'] = field_names
        
        return super(MetaSchema, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

@export
class Schema(abc.ABC, metaclass=MetaSchema):
    
    def __init__(self, **kwargs):
        self.__fields__ = Flat()
        field_names = getpyattr(type(self), 'field_names')
        field_index = getpyattr(type(self), 'field_index')
        for field, nsfield in zip(field_names, field_index):
            self.__fields__[nsfield] = stor_none(self, field).default
        for key, value in kwargs.items():
            if key in field_names:
                setattr(self, key, value)
    
    def nestify(self):
        out = Nested()
        for key, value in self.__fields__.items():
            if haspyattr(value, 'json'):
                out[key] = value.__json__()
            elif iscontainer(value):
                out[key] = [v.__json__() if haspyattr(v, 'json') else v for v in value]
            elif ismapping(value):
                out[key] = dict((k, v.__json__() if haspyattr(v, 'json') else k, v) \
                             for k, v in value.items())
            else:
                out[key] = value
        return out
    
    def __json__(self):
        return self.nestify().tree
    
    def to_json(self):
        import json
        return json.dumps(self.__json__(), indent=4)
    
    def to_pickle(self):
        import pickle
        return pickle.dumps(self.__json__())
    
    def to_plist(self):
        import plistlib
        return plistlib.dumps(self.__json__(), skipkeys=True)
    
    def to_toml(self):
        import toml
        return toml.dumps(self.__json__())
    
    def to_yaml(self):
        import yaml
        return yaml.dump(self.__json__())
    
    def to_string(self):
        return str(self.__json__())
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return self.to_string().encode(ENCODING)
    
    def __repr__(self):
        field_names = getpyattr(type(self), 'field_names')
        return stringify(self, field_names.keys())
    
    def update(self, mapping):
        if not ismapping(mapping):
            raise TypeError("mapping type required")
        field_names = getpyattr(type(self), 'field_names')
        for key, value in mapping.items():
            if key in field_names:
                setattr(self, key, value)
    
    def validate(self):
        field_names = getpyattr(type(self), 'field_names')
        field_index = getpyattr(type(self), 'field_index')
        for field, nsfield in zip(field_names, field_index):
            setattr(self, field, self.__fields__[nsfield])
        for value in self.__fields__.values():
            if hasattr(value, 'validate'):
                value.validate()
            elif iscontainer(value):
                for v in value:
                    if hasattr(v, 'validate'):
                        v.validate()


# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.config.fieldtypes import fields
    from clu.repl.ansi import print_separator
    
    class MySchema(Schema):
        
        title = fields.String("«title»")
        count = fields.UInt(0)
        where = fields.Int()
        
        with fields.ns('other'):
            
            additional = fields.String("«additional»")
            considerations = fields.String()
        
        with fields.ns('yodogg'):
            
            yodogg = fields.String("Yo dogg,")
            iheard = fields.String("I heard")
    
    instance = MySchema()
    instance.validate()
    
    print_separator()
    
    print("» JSON:")
    print()
    print(instance.to_json())
    print()
    
    # YOU CAN’T HANDLE THE “NoneType”:
    # print("» PLIST:")
    # print()
    # print(instance.to_plist())
    # print()
    
    print("» TOML:")
    print()
    print(instance.to_toml())
    print()
    
    print("» YAML:")
    print()
    print(instance.to_yaml())
    print()
    
    print("» __repr__(…):")
    print()
    print(repr(instance))
    print()
    
    print_separator()
    
    instance0 = MySchema(title="YO DOGG", count=666, where=-8)
    instance0.validate()
    
    print("» JSON:")
    print()
    print(instance0.to_json())
    print()
    
    # YOU CAN’T HANDLE THE “NoneType”:
    # print("» PLIST:")
    # print()
    # print(instance0.to_plist())
    # print()
    
    print("» TOML:")
    print()
    print(instance0.to_toml())
    print()
    
    print("» YAML:")
    print()
    print(instance0.to_yaml())
    print()
    
    print("» __repr__(…):")
    print()
    print(repr(instance0))
    print()
    
    print("» __str__(…):")
    print()
    print(str(instance0))
    print()
    
    print("» __bytes__(…):")
    print()
    print(bytes(instance0))
    print()



if __name__ == '__main__':
    test()
