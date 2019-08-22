# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import os
import sys

from clu.config.base import Nested
from clu.config.fieldtypes import FieldBase
from clu.predicates import haspyattr, getpyattr, stor_none
from clu.typology import ismapping, issequence
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

PYTHON_VERSION = float("%s%s%s" % (sys.version_info.major, os.extsep,
                                   sys.version_info.minor))

NEED_NAME = PYTHON_VERSION < 3.6

class MetaSchema(abc.ABCMeta):
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        
        field_index = Nested()
        
        for attribute, value in attributes.items():
            if isinstance(value, FieldBase):
                if NEED_NAME:
                    value.__set_name__(None, attribute)
                attributes[attribute] = value
                field_index.set(attribute, value,
                                namespace=value.namespace)
        
        for base in bases:
            parent = base.__mro__[0]
            for attribute, value in vars(parent).items():
                if isinstance(value, FieldBase) and attribute not in attributes:
                    if NEED_NAME:
                        value.__set_name__(None, attribute)
                    attributes[attribute] = value
                    field_index.set(attribute, value,
                                    namespace=value.namespace)
        
        attributes['__field_index__'] = field_index
        return super(MetaSchema, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

class Schema(abc.ABC, metaclass=MetaSchema):
    
    def __init__(self, **kwargs):
        self.__fields__ = Nested()
        field_index = getpyattr(type(self), 'field_index')
        for field in field_index:
            self.__fields__[field] = stor_none(self, field).default
        for key, value in kwargs.items():
            if key in field_index:
                setattr(self, key, value)
    
    def to_json(self):
        import json
        return json.dumps(self.__json__(), indent=4)
    
    def to_pickle(self):
        import pickle
        return pickle.dumps(self.__json__())
    
    def to_plist(self):
        import plistlib
        return plistlib.dumps(self.__json__())
    
    def to_toml(self):
        import toml
        return toml.dumps(self.__json__())
    
    def to_yaml(self):
        import yaml
        return yaml.dumps(self.__json__())
    
    def __json__(self):
        out = {}
        for key, value in self.__fields__.items():
            if haspyattr(value, 'json'):
                out[key] = value.__json__()
            elif issequence(value):
                out[key] = [v.__json__() if haspyattr(v, 'json') else v for v in value]
            elif ismapping(value):
                out[key] = dict((k,  v.__json__() if haspyattr(v, 'json') else k, v) for k, v in value.items())
            else:
                out[key] = value
        return out
    
    def update(self, mapping):
        if not ismapping(mapping):
            raise TypeError("mapping type required")
        for key, value in mapping.items():
            if key in self.__fields__:
                setattr(self, key, value)
    
    def validate(self):
        for key in self.__fields__:
            setattr(self, key, self.__fields__[key])
        for key, value in self.__fields__.items():
            if hasattr(value, 'validate'):
                value.validate()
            elif issequence(value):
                for v in value:
                    if hasattr(v, 'validate'):
                        v.validate()


# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.config.fieldtypes import fields
    
    Schema.__field_index__['wat:thefuck'] = "IS GOING ON"
    
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
    
    print(instance.to_toml())


if __name__ == '__main__':
    test()
