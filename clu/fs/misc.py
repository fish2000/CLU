# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import os

from clu.constants import ENCODING, lru_cache
from clu.typology import string_types
from clu.exporting import Exporter

exporter = Exporter()
export = exporter.decorator()

@export
def wrap_value(value):
    """ Get a “lazified” copy of a value, wrapped in a lamba """
    return lambda *args, **kwargs: value

none_function = wrap_value(None)

@export
def stringify(instance, fields):
    """ Stringify an object instance, using an iterable field list to
        extract and render its values, and printing them along with the 
        typename of the instance and its memory address -- yielding a
        repr-style string of the format:
        
            TypeName(fieldname="val", otherfieldname="otherval") @ 0x0FE
        
        The `stringify(…)` function is of use in `__str__()` and `__repr__()`
        definitions, e.g. something like:
        
            def __repr__(self):
                return stringify(self, type(self).__slots__)
        
    """
    field_dict = {}
    for field in fields:
        field_value = getattr(instance, field, "")
        field_value = callable(field_value) and field_value() or field_value
        if field_value:
            field_dict.update({ u8str(field) : field_value })
    field_dict_items = []
    for k, v in field_dict.items():
        field_dict_items.append('''%s="%s"''' % (k, v))
    typename = type(instance).__name__
    field_dict_string = ", ".join(field_dict_items)
    hex_id = hex(id(instance))
    return "%s(%s) @ %s" % (typename, field_dict_string, hex_id)

@export
def suffix_searcher(suffix):
    """ Return a boolean function that will search for the given
        file suffix in strings with which it is called, returning
        True when they are found and False when they aren’t.
        
        Useful in filter(…) calls and comprehensions, e.g.:
        
        >>> plists = filter(suffix_searcher('plist'), os.listdir())
        >>> mmsuffix = suffix_searcher('mm')
        >>> objcpp = (f for f in os.listdir() where mmsuffix(f))
    """
    if len(suffix) < 1:
        return lambda searching_for: True
    regex_str = r""
    if suffix.startswith(os.extsep):
        regex_str += r"\%s$" % suffix
    else:
        regex_str += r"\%s%s$" % (os.extsep, suffix)
    searcher = re.compile(regex_str, re.IGNORECASE).search
    return lambda searching_for: bool(searcher(searching_for))

@export
def u8encode(source):
    """ Encode a source as bytes using the UTF-8 codec """
    return bytes(source, encoding=ENCODING)

@export
def u8bytes(source):
    """ Encode a source as bytes using the UTF-8 codec, guaranteeing
        a proper return value without raising an error
    """
    if type(source) is bytes:
        return source
    elif type(source) is bytearray:
        return bytes(source)
    elif isinstance(source, string_types):
        return u8encode(source)
    elif isinstance(source, (int, float)):
        return u8encode(str(source))
    elif type(source) is bool:
        return source and b'True' or b'False'
    elif source is None:
        return b'None'
    return bytes(source)

@export
def u8str(source):
    """ Encode a source as a Python string, guaranteeing a proper return
        value without raising an error
    """
    return type(source) is str and source \
                        or u8bytes(source).decode(ENCODING)

# OS UTILITIES: deal with the umask value

octalize = lambda integer: "0o%04o" % integer

@lru_cache(maxsize=1)
def current_umask():
    """ Get the current umask value (cached on Python 3 and up). """
    mask = os.umask(0)
    os.umask(mask)
    return mask

@export
def masked_permissions(perms=0o666):
    """ Compute the permission bitfield, using the current umask value
        and a given permission octal number.
    """
    return perms & ~current_umask()

@export
def masked_chmod(pth, perms=0o666):
    """ Perform the `os.chmod(…)` operation, respecting the current
        umask value (q.v. `current_umask()` supra.)
    """
    masked_perms = masked_permissions(perms=perms)
    os.chmod(pth, mode=masked_perms)
    return octalize(masked_perms)

# MODULE EXPORTS:
export(current_umask,           name='current_umask')
export(none_function,           name='none_function',       doc="none_function() → A function that always returns None")
export(octalize,                name='octalize',            doc="octalize(integer) → Format an integer value as an octal number")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()