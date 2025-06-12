# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache
from itertools import groupby

import sys, re, os

from clu.constants.consts import DOLLA, ENCODING, QUALIFIER
from clu.predicates import negate, true_function, itervariadic
from clu.typology import isvalidpath, isnumeric, isstring
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

cache           = lambda function: export(lru_cache(maxsize=32)(function))
onecache        = lambda function: export(lru_cache(maxsize=1)(function))

# OS UTILITIES: get the current users’ home directory

gethomedir      = lru_cache(maxsize=1)(lambda: os.path.expanduser("~"))
isinvalidpath   = negate(isvalidpath)

@cache
def re_matcher(string, *, flags=re.IGNORECASE | re.MULTILINE):
    """ Return a boolean function that will search for the given
        regular-expression within any strings with which it is called,
        returning True when the regex matches from the beginning of the
        string, and False when it doesn’t.
        
        Results are cached, via “functools.lru_cache(…)”
    """
    if not string:
        return true_function
    match_function = re.compile(string, flags).match
    return lambda searching: bool(match_function(searching))

@cache
def re_searcher(string, *, flags=re.IGNORECASE | re.MULTILINE):
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
    search_function = re.compile(string, flags).search
    return lambda searching: bool(search_function(searching))

@export
def re_suffix(string):
    """ Remove any “os.extsep” prefixing a string, and ensure that
        it ends with a “$” – to indicate a regular expression suffix.
    """
    if not string:
        return None
    return rf"{string.casefold().removeprefix(QUALIFIER).removesuffix(DOLLA)}{DOLLA}"

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
def re_excluder(*excludes, flags=re.IGNORECASE | re.MULTILINE):
    """ Return a boolean function that will search for any of the given
        strings (provided as variadic arguments) and return False whenever
        any of them are found – True otherwise.
    """
    if len(excludes) < 1:
        return true_function
    exclude_re = '|'.join(re.escape(exclude) for exclude in excludes)
    exclude_function = re.compile(f"(?P<XXX>{exclude_re})", flags).search
    return lambda filename: not bool(exclude_function(filename))

@export
def extension(path, dotted=False):
    """ Return the extension – the file suffix – from a file pathname. """
    out = os.path.splitext(u8str(path))[-1]
    if dotted:
        return out
    return out.removeprefix(QUALIFIER)

@export
def swapext(path, new_extension=None):
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
    bulk = os.path.splitext(u8str(path))[0]
    if new_extension is None:
        return bulk
    return QUALIFIER.join((bulk, u8str(new_extension).removeprefix(QUALIFIER)))

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
def modeflags(mode, delete=True):
    """ Convert a file-open modestring to an integer flag.
        
        Helper function, used by “clu.fs.filesystem.TemporaryNamedFile(…)”
        and “clu.fs.filesystem.NamedTemporaryFile(…)” functions internally.
    """
    from tempfile import _bin_openflags, _text_openflags
    from clu.constants.consts import DELETE_FLAG
    
    if 'b' in u8str(mode):
        flags = _bin_openflags
    else:
        flags = _text_openflags
    
    if delete:
        flags |= DELETE_FLAG
    
    return flags

@export
def temporary(suffix='', prefix='', parent=None, **kwargs):
    """ Wrapper around `tempfile.mktemp()` that allows full overriding of the
        prefix and suffix by the caller -- that is to say, no random elements
        are used in the returned filename if both a prefix and a suffix are
        supplied.
        
        To avoid problems, the function will throw a FilesystemError if it is
        called with arguments that result in the computation of a filename
        that already exists.
    """
    from clu.constants.exceptions import FilesystemError
    from tempfile import mktemp, gettempdir
    
    directory = os.fspath(kwargs.pop('dir', parent) or gettempdir())
    if suffix:
        if not suffix.startswith(os.extsep):
            suffix = f"{os.extsep}{suffix}"
    
    tempmade = mktemp(prefix=prefix, suffix=suffix, dir=directory)
    tempsplit = os.path.splitext(os.path.basename(tempmade))
    
    if not suffix:
        suffix = tempsplit[1][1:]
    if not prefix or kwargs.pop('randomized', False):
        prefix, _ = os.path.splitext(tempsplit[0]) # WTF, HAX!
    
    fullpath = os.path.join(directory, f"{prefix}{suffix}")
    
    if os.path.exists(fullpath):
        raise FilesystemError(f"temporary(): file exists: {fullpath}")
    
    return fullpath

@export
def grouped(iterator, predicate=true_function):
    """ Sugar for calling “itertools.groupby(…)” as follows:
        
        >>> groupby(sorted(iterator, key=predicate), key=predicate)
    
        ... which that’s basically how you have to call it usefully.
    """
    yield from groupby(sorted(iterator, key=predicate),
                                        key=predicate)

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