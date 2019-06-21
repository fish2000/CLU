# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import re, os

from constants import ENCODING, lru_cache
from predicates import tuplize
from typology import string_types

def wrap_value(value):
    return lambda *args, **kwargs: value

none_function = wrap_value(None)

class Memoizer(dict):
    
    """ Very simple memoizer (only works with positional args) """
    
    def __init__(self, function):
        super(Memoizer, self).__init__()
        self.original = function
    
    def __missing__(self, key):
        function = self.original
        self[key] = out = function(*key)
        return out
    
    @property
    def original(self):
        return self.original_function
    
    @original.setter
    def original(self, value):
        if not value:
            self.original_function = none_function
        elif not callable(value):
            self.original_function = wrap_value(value)
        else:
            self.original_function = value
    
    @property
    def __wrapped__(self):
        return self.original_function
    
    def __call__(self, function=None):
        if function is None:
            function = self.original
        else:
            self.original = function
        @wraps(function)
        def memoized(*args):
            return self[tuplize(*args)]
        memoized.__wrapped__ = function
        memoized.__instance__ = self
        return memoized

def memoize(function):
    memoinstance = Memoizer(function)
    @wraps(function)
    def memoized(*args):
        return memoinstance[tuplize(*args)]
    memoized.__wrapped__ = function
    memoized.__instance__ = memoinstance
    return memoized

def stringify(instance, fields):
    """ Stringify an object instance, using an iterable field list to
        extract and render its values, and printing them along with the 
        typename of the instance and its memory address -- yielding a
        repr-style string of the format:
        
            TypeName(fieldname="val", otherfieldname="otherval") @ 0x0FE
        
        The `stringify(…)` function is of use in `__str__()` and `__repr__()`
        definitions, E.G. something like:
        
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

def u8encode(source):
    """ Encode a source as bytes using the UTF-8 codec """
    return bytes(source, encoding=ENCODING)

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

def u8str(source):
    """ Encode a source as a Python string, guaranteeing a proper return
        value without raising an error
    """
    return type(source) is str and source \
                        or u8bytes(source).decode(ENCODING)
# OS UTILITIES: get the current process’ umask value

@lru_cache(maxsize=1)
def current_umask():
    """ Get the current umask value (cached on Python 3 and up). """
    mask = os.umask(0)
    os.umask(mask)
    return mask

def masked_permissions(perms=0o666):
    """ Compute the permission bitfield, using the current umask value
        and a given permission octal number.
    """
    return perms & ~current_umask()
