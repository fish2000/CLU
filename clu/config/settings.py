# -*- coding: utf-8 -*-
from __future__ import print_function

import abc

from clu.constants.consts import ENCODING, PYTHON_VERSION
from clu.config.base import Flat, Nested
from clu.config.fieldtypes import FieldBase
from clu.fs.misc import stringify
from clu.predicates import haspyattr, getpyattr, stattr, pyattrs, iscontainer
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NEED_NAME = PYTHON_VERSION < 3.6

class MetaSchema(abc.ABCMeta):
    
    """ The MetaSchema metaclass is used by the Schema class – q.v.
        class definition sub. – to properly record all of the field
        attributes that have been defined on its subclasses.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Create a new schema type, with bookkeeping structures
            in place for all of out defined field attributes:
        """
        
        # Use both a namespaced mapping and a standard dict
        # as class-based records of our field attributes:
        field_index = Flat()
        field_names = {}
        
        # Stow both the Python name and the namespaced name
        # for each field attribute defined on the schema,
        # additionally manually calling __set_name__(…) if
        # we’re on a pre-3.6 version of Python:
        for attribute, value in attributes.items():
            if isinstance(value, FieldBase):
                if NEED_NAME:
                    value.__set_name__(None, attribute)
                attributes[attribute] = value
                field_names[attribute] = value
                field_index.set(attribute, value,
                                namespace=value.namespace)
        
        # This is the same as the above, but for the base
        # ancestor class – this enables field inheritance:
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
        
        # Add both the field-index and the field-names mappings
        # to the class dictionary for the new type:
        attributes['__field_index__'] = field_index
        attributes['__field_names__'] = field_names
        
        # Create and return the schema type:
        return super(MetaSchema, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

@export
class Schema(abc.ABC, metaclass=MetaSchema):
    
    """ The Schema class is the root class for all configuration schemas.
        
        One defines field attributes on a schema subclass – this will seem
        familiar to veterans of SQLAlchemy or Django model-class definition –
        like so, using the “clu.config.fieldtypes.fields” pseudo-module:
            
            from clu.config.fieldtypes import fields
            
            class MySchema(Schema):
                
                appname = fields.String("YoDogg")
                version = fields.Float(1.0)
                title = fields.String(f"{appname.default} Schema v{version.default!s}")
                
                with fields.ns("debug"):
                    
                    debugging = fields.Boolean(False)
                    logging = fields.Boolean(False)
                    logdir = fields.String(f"/usr/local/var/log/{appname.default.lower()}")
                
                with fields.ns("concurrency"):
                    
                    processes = fields.UInt(os.cpu_count())
                    threads = fields.UInt(os.cpu_count() * 4)
                    lockfile = fields.String(f"/usr/local/var/lock/{appname.default.lower()}/shared.lock")
            
        … after defining your schema in this way, you can then instantiate it:
            
            >>> mine = MySchema()   # fields will initialize with default values
            >>> mine.threads = 1    # modify individual fields
            >>> mine.validate()     # ensure your modifications are within bounds
        
        … Notice that we do not need to use the namespaced name when accessing
        a field. If you wish to do so, at the time of writing, you can access
        the underlying “NamespacedMutableMapping” instance directly:
            
            >>> mine.__fields__['concurrency:threads'] = 1
            >>> mine.__fields__.set('threads', 1, namespace='concurrency')
        
        … The two preceding lines are equivalent – see the definition of 
        “clu.config.base.NamespacedMutableMapping” for further information.
    """
    
    def __init__(self, **kwargs):
        """ Initialize an instance of a Schema, passing keyword arguments
            as values with which to override the field defaults.
        """
        self.__fields__ = Flat()
        field_names, field_index = pyattrs(type(self), 'field_names',
                                                       'field_index')
        for field, nsfield in zip(field_names, field_index):
            self.__fields__[nsfield] = stattr(self, field).get_default()
        for key, value in kwargs.items():
            if key in field_names:
                setattr(self, key, value)
    
    def namespaces(self):
        """ Return a sorted tuple of all of the namespaces that have been
            defined on this Schema.
        """
        return self.__fields__.namespaces()
    
    def nestify(self):
        """ Return an instance of “clu.config.base.Nested” – a concrete
            NamespacedMutableMapping subclass – containing all of the 
            data from the Schema – including embedded sub-Schemas.
        """
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
        """ Return a nested set of dicts, suitable for serializing as JSON
            (and other similar formats).
        """
        return self.nestify().tree
    
    def to_json(self):
        """ Return a stringified JSON representation of this Schema’s data """
        import json
        return json.dumps(self.__json__(), indent=4)
    
    def to_pickle(self):
        """ Return a stringified Python pickle representation of this Schema’s data """
        import pickle
        return pickle.dumps(self.__json__())
    
    def to_plist(self):
        """ Return a stringified Apple property-list (née “plist”) representation
            of this Schema’s data
        """
        import plistlib
        return plistlib.dumps(self.__json__(), skipkeys=True)
    
    def to_toml(self):
        """ Return a stringified TOML representation of this Schema’s data """
        import toml
        return toml.dumps(self.__json__())
    
    def to_yaml(self):
        """ Return a stringified YAML representation of this Schema’s data """
        import yaml
        return yaml.dump(self.__json__())
    
    def to_string(self):
        """ Return a stringified Python representation of this Schema’s data """
        return str(self.__json__())
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return self.to_string().encode(ENCODING)
    
    def __repr__(self):
        field_names = getpyattr(type(self), 'field_names')
        return stringify(self, field_names.keys())
    
    def update(self, mapping):
        """ Update the Schema with data from a mapping instance. """
        if not ismapping(mapping):
            raise TypeError("mapping type required")
        field_names = getpyattr(type(self), 'field_names')
        for key, value in mapping.items():
            if key in field_names:
                setattr(self, key, value)
    
    def validate(self):
        """ Validate the schema data.
            
            Override this function to add additional validation logic.
        """
        field_names, field_index = pyattrs(type(self), 'field_names',
                                                       'field_index')
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
    from pprint import pprint
    
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
            andalso = fields.List(value=fields.String("«also»", allow_none=False))
    
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
    
    print("» namespaces:")
    print()
    pprint(instance.namespaces())
    print()
    
    print_separator()
    
    instance0 = MySchema(title="YO DOGG", count=666, where=-8)
    instance0.validate()
    
    instance0.considerations = "Whatever man."
    instance0.iheard = "Actually I haven’t heard."
    instance0.andalso = ['additionally', 'we', 'put', 'some', 'strings']
    
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
    
    print("» namespaces:")
    print()
    pprint(instance0.namespaces())
    print()



if __name__ == '__main__':
    test()
