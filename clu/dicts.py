# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import collections
import collections.abc

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# DICT VIEWS: OrderedMappingView and friends

class ClassWrapRepr(abc.ABC):
    
    def __repr__(self):
        clsname = type(self).__name__
        mapping = repr(self._mapping)
        return f"{clsname}<{mapping}>"

@export
class OrderedMappingView(collections.abc.MappingView,
                         collections.abc.Reversible,
                         ClassWrapRepr):
    
    """ A mapping view class implementing “collections.abc.Reversible” """
    
    def __reversed__(self):
        yield from reversed(self._mapping)
    
    __repr__ = ClassWrapRepr.__repr__

@export
class OrderedItemsView(collections.abc.ItemsView,
                       collections.abc.Reversible,
                       ClassWrapRepr):
    
    """ An items-view class implementing “collections.abc.Reversible” """
    
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield (key, self._mapping[key])
    
    __repr__ = ClassWrapRepr.__repr__

@export
class OrderedKeysView(collections.abc.KeysView,
                      collections.abc.Reversible,
                      ClassWrapRepr):
    
    """ A keys-view class implementing “collections.abc.Reversible” """
    
    def __reversed__(self):
        yield from reversed(self._mapping)
    
    __repr__ = ClassWrapRepr.__repr__

@export
class OrderedValuesView(collections.abc.ValuesView,
                        collections.abc.Reversible,
                        ClassWrapRepr):
    
    """ A values-view class implementing “collections.abc.Reversible” """
    
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield self._mapping[key]
    
    __repr__ = ClassWrapRepr.__repr__

# DICT FUNCTIONS: dictionary-merging

@export
def merge_two(one, two, cls=dict):
    """ Merge two dictionaries into an instance of the specified class
        Based on this docopt example source: https://git.io/fjCZ6
    """
    from clu.predicates import getitem
    if not cls:
        cls = type(one)
    keys = frozenset(one) | frozenset(two)
    merged = ((key, getitem(one, key) or getitem(two, key)) for key in keys)
    return cls(merged)

@export
def merge_as(*dicts, cls=dict, **overrides):
    """ Merge all dictionary arguments into a new instance of the specified class,
        passing all additional keyword arguments to the class constructor as overrides
    """
    if not cls:
        cls = len(dicts) and type(dicts[0]) or dict
    merged = cls(**overrides)
    for d in dicts:
        merged = merge_two(merged, d, cls=cls)
    return merged

@export
def merge(*dicts, **overrides):
    """ Merge all dictionary arguments into a new `dict` instance, using any
        keyword arguments as item overrides in the final `dict` instance returned
    """
    if 'cls' in overrides:
        raise NameError('Cannot override the `cls` value')
    return merge_as(*dicts, cls=dict, **overrides)

# DICT STUFF: asdict(…)

@export
def asdict(thing):
    """ asdict(thing) → returns either thing, thing.__dict__, or dict(thing) as necessary """
    from clu.predicates import haspyattr
    from clu.typology import ismapping
    if isinstance(thing, dict):
        return thing
    if haspyattr(thing, 'dict'):
        return asdict(thing.__dict__)
    if hasattr(thing, '_asdict'):
        return asdict(thing._asdict())
    if hasattr(thing, 'to_dict'):
        return asdict(thing.to_dict())
    if hasattr(thing, 'dict'):
        return asdict(thing.dict)
    if ismapping(thing):
        return dict(thing)
    return dict(thing)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()