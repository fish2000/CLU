# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache

import os
import re
import sys

from clu.constants.consts import ENCODING
from clu.predicates import negate, true_function, itervariadic
from clu.typology import isvalidpath, isnumeric, isstring
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

cache = lambda function: export(lru_cache(maxsize=32)(function))
onecache = lambda function: export(lru_cache(maxsize=1)(function))

# OS UTILITIES: get the current users’ home directory

gethomedir = lambda: os.path.expanduser("~")
isinvalidpath = negate(isvalidpath)

ex = os.path.extsep
dolla = '$'

@cache
def re_matcher(string):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches from the beginning of the
        string, and False when it doesn’t.
        
        Results are cached, via “functools.lru_cache(…)”
    """
    if not string:
        return true_function
    match_function = re.compile(string, re.IGNORECASE).match
    return lambda searching: bool(match_function(searching))

@cache
def re_searcher(string):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches and False when it doesn’t.
        
        Results are cached, via “functools.lru_cache(…)”
        
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
    if not string:
        return None
    return rf"{string.casefold().lstrip(ex).rstrip(dolla)}$"

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
@itervariadic
def re_excluder(*excludes):
    """ Return a boolean function that will search for any of the given
        strings (provided as variadic arguments) and return False whenever
        any of them are found – True otherwise.
    """
    if len(excludes) < 1:
        return true_function
    exclude_re = '|'.join(re.escape(exclude) for exclude in excludes)
    exclude_function = re.compile(f"(?P<XXX>{exclude_re})", re.IGNORECASE).search
    return lambda filename: not bool(exclude_function(filename))

@export
def extension(path, dotted=False):
    """ Return the extension – the file suffix – from a file pathname. """
    out = os.path.splitext(u8str(path))[-1]
    if dotted:
        return out
    return out.lstrip(ex)

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
    elif type(source) is bool:
        return source and b'True' or b'False'
    elif source is None:
        return b'None'
    elif isnumeric(source):
        return u8encode(str(source))
    elif isstring(source):
        return u8encode(source)
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

@onecache
def current_umask():
    """ Get the current umask value. Results are cached, via “functools.lru_cache(…)” """
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
export(differentfile,           name='differentfile',       doc="differentfile(path0, path1) → Return True if path0 and path1 point to different locations on the filesystem")
export(octalize,                name='octalize',            doc="octalize(integer) → Format an integer value as an octal number")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()