# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

from clu.constants.consts import ENCODING, SINGLETON_TYPES
from clu.fs.misc import hoist
from clu.predicates import (ismetaclass, typeof,
                            resolve, attr,
                            isenum, enumchoices, pyname)
from clu.typology import isnumeric, isbytes, isstring
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

hexid = lambda thing: hex(id(thing))
typenameof = lambda thing: pyname(typeof(thing))
typename_hexid = lambda thing: (pyname(typeof(thing)), hex(id(thing)))

def strfield(v):
    """ Basic, simple, straightforward type-switch-based sub-repr """
    T = type(v)
    if isstring(T):
        return f"“{v}”"
    elif T in SINGLETON_TYPES:
        return str(v)
    elif isnumeric(T):
        return str(v)
    elif isbytes(T):
        return f"“{v.decode(ENCODING)}”"
    elif ismetaclass(T):
        if isenum(v):
            typename, hex_id = typename_hexid(v)
            choices = ", ".join(enumchoices(v))
            return f"‘{typename}<{v.__name__}({choices}) @ {hex_id}>’"
        return repr(v)
    return f"‘{v!r}’"

@export
def strfields(instance, fields,
                       *extras, try_callables=True,
                      **attributes):
    """ Stringify an object instance, using an iterable field list to
        extract and render its values, and printing them along with the 
        typename of the instance and its memory address -- yielding a
        repr-style string of the format:
        
            “fieldname="val", otherfieldname="otherval"”
        
        The `strfields(…)` function is of use in `__str__()` and `__repr__()`
        definitions, e.g. something like:
            
            def inner_repr(self):
                return strfields(self, type(self).__slots__)
            
            def __repr__(self):
                typename, hex_id = typename_hexid(self)
                attr_string = self.inner_repr()
                return f"{typename}({attr_string}) @ {hex_id}"
        
        Callable fields, by default, will be called with no arguments
        to obtain their value. To supress this behavior – if you wish
        to represent callable fields that require arguments – you can
        pass the keyword-only “try_callables” flag as False:
            
            def inner_repr(self):
                return strfields(self,
                            type(self).__slots__,
                            try_callables=False)
    """
    if fields is None:
        fields = tuple(hoist(attr(instance, 'fields',
                                            '__all__',
                                            '__dir__',
                                            '__slots__',
                                            '__dict__.keys', default=tuple()))())
    if all(len(param) < 1 for param in (fields, extras, attributes)):
        return "¬"
    attrs = dict(attributes)
    for field in chain(fields, extras):
        field_value = resolve(instance, field)
        if try_callables and callable(field_value):
            field_value = field_value()
        if field_value:
            attrs[field] = strfield(field_value)
    return ", ".join(f'{k}={v}' for k, v in attrs.items()) or "…"

@export
def stringify(instance, fields,
                       *extras, try_callables=True,
                      **attributes):
    """ Stringify an object instance, using an iterable field list to
        extract and render its values, and printing them along with the 
        typename of the instance and its memory address -- yielding a
        repr-style string of the format:
        
            TypeName(fieldname="val", otherfieldname="otherval") @ 0x0FE
        
        The `stringify(…)` function is of use in `__str__()` and `__repr__()`
        definitions, e.g. something like:
        
            def __repr__(self):
                return stringify(self, type(self).__slots__)
        
        Callable fields, by default, will be called with no arguments
        to obtain their value. To supress this behavior – if you wish
        to represent callable fields that require arguments – you can
        pass the keyword-only “try_callables” flag as False:
            
            def __repr__(self):
                return stringify(self,
                            type(self).__slots__,
                            try_callables=False)
    """
    attr_string = strfields(instance, fields,
                                     *extras, try_callables=try_callables,
                                    **attributes)
    typename, hex_id = typename_hexid(instance)
    return f"{typename}({attr_string}) @ {hex_id}"

export(hexid,                   name='hexid',               doc="hexid(thing) → Return the hex-ified representation of “thing”’s ID – Equivalent to “hex(id(thing))”")
export(typenameof,              name='typenameof',          doc="typenameof(thing) → Return the string name of the type of “thing” – Equivalent to “pyname(typeof(thing))”, q.v. “clu.predicates”")
export(typename_hexid,          name='typename_hexid',      doc="typename_hexid(thing) → Return a two-tuple containing “thing”’s hex-ified ID and the string name of the type of “thing” – Equivalent to “(hexid(thing), typenameof(thing))”")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
