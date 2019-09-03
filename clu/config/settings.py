# -*- coding: utf-8 -*-
from __future__ import print_function

import abc

from clu.constants.consts import ENCODING, PYTHON_VERSION
from clu.config.base import Flat, Nested
from clu.config.fieldtypes import FieldBase
from clu.fs.misc import stringify
from clu.predicates import haspyattr, getpyattr, stattr, pyattrs, iscontainer, no_op
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NEED_NAME = PYTHON_VERSION < 3.6

class MetaSchema(abc.ABCMeta):
    
    """ The MetaSchema metaclass is used by the Schema class – q.v.
        class definition sub. – to properly record all of the field
        attributes and namespaces that are defined on its subclasses.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Create a new schema type, with bookkeeping structures
            in place to record all defined field attributes and
            namespaces:
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
    
    """ The Schema class is the root class for all CLU configuration schemas.
        
        One defines field attributes on a schema subclass – this will seem
        familiar to veterans of SQLAlchemy or Django model-class definition –
        like so, using the “clu.config.fieldtypes.fields” pseudo-module:‡
            
            from clu.config.fieldtypes import fields
            
            class MySchema(Schema):
                
                appname = fields.String("YoDogg")
                version = fields.Float(1.0)
                title = fields.String(f"{appname.default} Config {version.default!r}")
                
                with fields.ns("debug"):
                    
                    debugging = fields.Boolean(False)
                    logging = fields.Boolean(False)
                    logdir = fields.String(f"/var/log/{appname.default}")
                
                with fields.ns("concurrency"):
                    
                    processes = fields.UInt(os.cpu_count())
                    threads = fields.UInt(os.cpu_count() * 4)
                    lockfile = fields.String(f"/var/lock/{appname.default}/shared.lock")
            
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
        
        The Schema class initializes its instances through implementing a
        “__new__(…)” method – When defining your own Schema subclass, it is
        therefore advisable to add any initialization logic you may have in
        a custom “__init__(…)” method, as you can omit calling up to the
        superclass in such an implementation.
        
        ‡ – N.B. For the curious, what I am calling a “pseudo-module” here
            isn’t a module at all; it is an instance of a private class called
            “NamespacedFieldManager” that manages the statefulness necessary
            for implementing namespacing using context-management. When you
            import it using a “from” import statement, as above, a module-level
            “__getattr__(…)” function within the “fieldtypes” module instances
            the “NamespacedFieldManager” class and returns it anew each time.
    """
    
    def __new__(cls, **kwargs):
        """ Allocate a new instance of a Schema, passing keyword arguments
            as values with which to override the field defaults.
        """
        # Call up to allocate the new instance:
        try:
            instance = super(Schema, cls).__new__(cls, **kwargs)
        except TypeError:
            instance = super(Schema, cls).__new__(cls)
        
        # Create the “__fields__” attribute and retrieve the class-based
        # field indexes, “__field_names__” and “__field_index__”:
        instance.__fields__ = Flat()
        field_names, field_index = pyattrs(cls, 'field_names',
                                                'field_index')
        
        # Set each of the field-default values through a call to
        # the underlying descriptor instances’ “get_default()” method:
        for field, nsfield in zip(field_names, field_index):
            instance.__fields__[nsfield] = stattr(instance, field).get_default()
        
        # Override defaults with any instance-specific values,
        # as specfied through keywords:
        for key, value in kwargs.items():
            if key in field_names:
                setattr(instance, key, value)
        
        # Return the new instance:
        return instance
    
    def namespaces(self):
        """ Return a sorted tuple of all of the namespaces that have been
            defined on this Schema.
        """
        return self.__fields__.namespaces()
    
    def nestify(self, stringify=False):
        """ Return an instance of “clu.config.base.Nested” – a concrete
            NamespacedMutableMapping subclass – containing all of the data from
            the Schema instance – including any embedded sub-Schema data.
        """
        converter = stringify and str or no_op
        out = Nested()
        for key, value in self.__fields__.items():
            if haspyattr(value, 'json'):
                out[key] = value.__json__(stringify=stringify)
            elif iscontainer(value):
                out[key] = tuple(v.__json__(stringify=stringify) if haspyattr(v, 'json') else v for v in value)
            elif ismapping(value):
                out[key] = dict((k, v.__json__(stringify=stringify) if haspyattr(v, 'json') else k, v) \
                             for k, v in value.items())
            else:
                out[key] = (value is not None) and converter(value) or value
        return out
    
    def __json__(self, **kwargs):
        """ Return a nested set of dicts, suitable for serializing as JSON
            (and other similar formats).
        """
        return self.nestify(**kwargs).tree
    
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
        """ Return a prettified string representation of this Schema’s data """
        from pprint import pformat
        return str(pformat(self.__json__(), indent=4))
    
    def to_bytes(self):
        """ Return a prettified and byte-encoded representation of this Schema’s data """
        return self.to_string().encode(ENCODING)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return self.to_bytes()
    
    def __repr__(self):
        return stringify(self, getpyattr(type(self), 'field_names').keys())
    
    def update(self, mapping):
        """ Update the Schema with data from a mapping instance. """
        if not ismapping(mapping):
            raise TypeError("mapping type required")
        field_names = getpyattr(type(self), 'field_names')
        for key, value in mapping.items():
            if key in field_names:
                setattr(self, key, value)
    
    def validate(self):
        """ Validate the schema data. Override this function to add
            additional validation logic.
            
            N.B. Be sure to call up using “super(…)” when overriding.
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
        return True

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
            andalso = fields.Tuple(value=fields.String("«also»", allow_none=False))
    
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
    instance0.andalso = ('additionally', 'we', 'put', 'some', 'strings')
    
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
