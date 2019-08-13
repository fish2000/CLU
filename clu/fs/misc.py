# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re
import sys

from clu.constants.consts import ENCODING
from clu.constants.polyfills import lru_cache
from clu.typology import string_types
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# OS UTILITIES: get the current users’ home directory

gethomedir = lambda: os.path.expanduser("~")

@export
def wrap_value(value):
    """ Get a “lazified” copy of a value, wrapped in a lamba """
    return lambda *args, **kwargs: value

none_function = wrap_value(None)
true_function = wrap_value(True)

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
        field_dict_items.append(f'''{k}="{v}"''')
    typename = type(instance).__name__
    field_dict_string = ", ".join(field_dict_items)
    hex_id = hex(id(instance))
    return f"{typename}({field_dict_string}) @ {hex_id}"

ex = os.path.extsep
dolla = '$'

@export
def suffix(string):
    """ Ensure that a string begins with “os.path.extsep” """
    if string is None:
        return None
    return rf"{string.lstrip(ex).rstrip(dolla)}$"

@export
def re_matcher(string):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches from the beginning of the
        string, and False when it doesn’t.
    """
    if not string:
        return true_function
    match_function = re.compile(string, re.IGNORECASE).match
    return lambda searching_for: bool(match_function(searching_for))

@export
def re_searcher(string):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches and False when it doesn’t.
        
        Useful in filter(…) calls and comprehensions, e.g.:
        
        >>> plists = filter(re_searcher(r'.plist$'), os.listdir())
        >>> mmsuffix = suffix_searcher(r'.mm$')
        >>> objcpp = (f for f in os.listdir() where mmsuffix(f))
    """
    if not string:
        return true_function
    search_function = re.compile(string, re.IGNORECASE).search
    return lambda searching_for: bool(search_function(searching_for))

@export
def suffix_searcher(string):
    """ Return a boolean function that will search for the given
        string within any strings with which it is called, returning
        True when they are found and False when they aren’t.
        
        Useful in filter(…) calls and comprehensions, e.g.:
        
        >>> plists = filter(suffix_searcher('plist'), os.listdir())
        >>> mmsuffix = suffix_searcher('mm')
        >>> objcpp = (f for f in os.listdir() where mmsuffix(f))
    """
    return re_searcher(suffix(string))

@export
def swapext(path, new_extension):
    """ Swap the file extension of the path with a newly specified one –
        if no extension is present, the newly specified extension will be
        amended to the path; the new extension can provide or omit its
        leading extension-separator (or a “period” in most human usage).
        
        Like E.G.:
            
            >>> swapext('/yo/dogg.obj', 'odb')
            '/yo/dogg.odb'
            >>> swapext('/yo/dogg.obj', '.odb')
            '/yo/dogg.odb'
            >>> swapext('/yo/dogg', 'odb')
            '/yo/dogg.odb'
    """
    bulk = os.path.splitext(path)[0]
    if new_extension is None:
        return bulk
    return ex.join((bulk, new_extension.lstrip(ex)))

@export
def filesize(path):
    """ Return the on-disk size (in bytes) of the file located at a path """
    if not os.path.exists(path):
        return -1
    return os.lstat(path).st_size

@export
def samesize(path0, path1):
    """ Compare the on-disk file sizes (in bytes) of two files by their paths """
    from clu.constants.exceptions import FilesystemError
    if any(p is None for p in (path0, path1)):
        raise FilesystemError('paths must both be non-None')
    if os.path.samefile(path0, path1):
        return True
    return filesize(path0) == filesize(path1)

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

# OS UTILITIES: make a path on windows into a “long path”: (…?)

@export
def win32_longpath(path):
    """ Helper function to add the long path prefix for Windows, so that shutil.copytree
        won't fail while working with paths with 255+ chars.
        
        Vendored in from pytest-datadir – q.v. https://git.io/fjMWl supra.
    """
    if sys.platform == 'win32':
        # The use of os.path.normpath here is necessary since "the "\\?\" prefix to a path string
        # tells the Windows APIs to disable all string parsing and to send the string that follows
        # it straight to the file system".
        # (See https://docs.microsoft.com/pt-br/windows/desktop/FileIO/naming-a-file)
        return '\\\\?\\' + os.path.normpath(path)
    else:
        return path

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
def masked_chmod(path, perms=0o666):
    """ Perform the `os.chmod(…)` operation, respecting the current
        umask value (q.v. `current_umask()` supra.)
    """
    masked_perms = masked_permissions(perms=perms)
    os.chmod(path, mode=masked_perms)
    return octalize(masked_perms)

# MODULE EXPORTS:
export(gethomedir,              name='gethomedir',          doc="gethomedir() → Return the current user’s home directory")
export(current_umask,           name='current_umask')
export(none_function,           name='none_function',       doc="none_function() → A function that always returns None")
export(true_function,           name='true_function',       doc="true_function() → A function that always returns True")
export(octalize,                name='octalize',            doc="octalize(integer) → Format an integer value as an octal number")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()