# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import os
import re
import sys

from clu.constants.consts import ENCODING, SINGLETON_TYPES
from clu.constants.polyfills import lru_cache
from clu.predicates import negate, ismetaclass, typeof, or_none, isenum, enumchoices, pyname
from clu.typology import isvalidpath, isnumeric, isbytes, isstring
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# OS UTILITIES: get the current users’ home directory

gethomedir = lambda: os.path.expanduser("~")
isinvalidpath = negate(isvalidpath)

@export
def wrap_value(value):
    """ Get a “lazified” copy of a value, wrapped in a lamba """
    return lambda *args, **kwargs: value

none_function = wrap_value(None)
true_function = wrap_value(True)

hexid = lambda thing: hex(id(thing))
typenameof = lambda thing: pyname(typeof(thing))
typename_hexid = lambda thing: (pyname(typeof(thing)), hex(id(thing)))

def stringify_value(v):
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
    typename, hex_id = typename_hexid(instance)
    if all(len(param) < 1 for param in (fields, extras, attributes)):
        return f"{typename}(¬) @ {hex_id}"
    attrs = dict(attributes)
    for field in chain(fields, extras):
        field_value = or_none(instance, field)
        if try_callables and callable(field_value):
            field_value = field_value()
        if field_value:
            attrs[field] = stringify_value(field_value)
    attr_string = ", ".join(f'{k}={v}' for k, v in attrs.items()) or "…"
    return f"{typename}({attr_string}) @ {hex_id}"

ex = os.path.extsep
dolla = '$'

@lru_cache(maxsize=32)
def re_matcher(string):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches from the beginning of the
        string, and False when it doesn’t.
    """
    if not string:
        return true_function
    match_function = re.compile(string, re.IGNORECASE).match
    return lambda searching: bool(match_function(searching))

@lru_cache(maxsize=32)
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
    return lambda searching: bool(search_function(searching))

@export
def re_suffix(string):
    """ Remove any “os.path.extsep” prefixing a string and ensure
        it ends with a “$” – to indicate a regular expression suffix.
    """
    if string is None:
        return None
    return rf"{string.lower().lstrip(ex).rstrip(dolla)}$"

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
    return re_searcher(re_suffix(string))

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
    if isinvalidpath(path):
        return -1
    return os.lstat(path).st_size

differentfile = negate(os.path.samefile)

@export
def samesize(path0, path1):
    """ Compare the on-disk file sizes (in bytes) of two files by their paths,
        returning True if they are the same, and False otherwise
        
        “FilesystemError” will be raised if either of the paths are invalid
    """
    from clu.constants.exceptions import FilesystemError
    if any(p is None for p in (path0, path1)):
        raise FilesystemError('paths must both be non-None')
    if any(isinvalidpath(p) for p in (path0, path1)):
        raise FilesystemError('paths must both be valid and existent')
    if differentfile(path0, path1):
        return filesize(path0) == filesize(path1)
    else:
        return True

@export
def differentsize(path0, path1):
    """ Compare the on-disk file sizes (in bytes) of two files by their paths,
        returning True if they are different, and False otherwise
        
        “FilesystemError” will be raised if either of the paths are invalid
    """
    from clu.constants.exceptions import FilesystemError
    if any(p is None for p in (path0, path1)):
        raise FilesystemError('paths must both be non-None')
    if any(isinvalidpath(p) for p in (path0, path1)):
        raise FilesystemError('paths must both be valid and existent')
    if differentfile(path0, path1):
        return filesize(path0) != filesize(path1)
    else:
        return False

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
    elif isstring(source):
        return u8encode(source)
    elif type(source) is bool:
        return source and b'True' or b'False'
    elif source is None:
        return b'None'
    elif isnumeric(source):
        return u8encode(str(source))
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

@export
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
export(isinvalidpath,           name='isinvalidpath',       doc="isinvalidpath(thing) → boolean predicate, True if `thing` does not represent a valid path on the filesystem")
export(none_function,           name='none_function',       doc="none_function() → A function that always returns None")
export(true_function,           name='true_function',       doc="true_function() → A function that always returns True")

export(hexid,                   name='hexid',               doc="hexid(thing) → Return the hex-ified representation of “thing”’s ID – Equivalent to “hex(id(thing))”")
export(typenameof,              name='typenameof',          doc="typenameof(thing) → Return the string name of the type of “thing” – Equivalent to “pyname(typeof(thing))”, q.v. “clu.predicates”")
export(typename_hexid,          name='typename_hexid',      doc="typename_hexid(thing) → Return a two-tuple containing “thing”’s hex-ified ID and the string name of the type of “thing” – Equivalent to “(hexid(thing), typenameof(thing))”")
export(differentfile,           name='differentfile',       doc="differentfile(path0, path1) → Return True if path0 and path1 point to different locations on the filesystem")

export(re_matcher,              name='re_matcher')
export(re_searcher,             name='re_searcher')

export(octalize,                name='octalize',            doc="octalize(integer) → Format an integer value as an octal number")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()