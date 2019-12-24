# -*- coding: utf-8 -*-
from __future__ import print_function
from distutils.spawn import find_executable
from functools import lru_cache, wraps
from tempfile import _TemporaryFileWrapper as TemporaryFileWrapperBase

cache = lambda function: lru_cache(maxsize=128, typed=True)(function)

import abc
import clu.abstract
import collections
import collections.abc
import contextlib
import os
import re
import shutil
import sys
import weakref
import zipfile

from clu.constants.consts import λ, DELETE_FLAG, ENCODING, PATH, SCRIPT_PATH
from clu.constants.exceptions import ExecutionError, FilesystemError
from clu.dicts import OrderedItemsView, OrderedKeysView, OrderedValuesView
from clu.predicates import attr, allattrs, isexpandable, anyof, uniquify
from clu.repr import stringify
from clu.sanitizer import utf8_encode
from clu.typology import isnotpath, isvalidpath
from clu.fs.misc import differentfile, filesize, gethomedir, masked_permissions
from clu.fs.misc import re_searcher, suffix_searcher, re_excluder
from clu.fs.misc import swapext, u8str, extension
from clu.exporting import Exporter, path_to_dotpath

exporter = Exporter(path=__file__)
export = exporter.decorator()

DEFAULT_TIMEOUT = 60 # seconds
DEFAULT_PREFIX = "yo-dogg-"

@export
def ensure_path_is_valid(pth):
    """ Raise an exception if we can’t write to the specified path """
    if isnotpath(pth):
        raise FilesystemError(f"Operand must be a path type: {pth}")
    if os.path.exists(pth):
        if os.path.isdir(pth):
            raise FilesystemError(f"Can’t save over directory: {pth}")
        raise FilesystemError(f"Output file exists: {pth}")
    parent_dir = os.path.dirname(pth)
    if not os.path.isdir(parent_dir):
        raise FilesystemError(f"Directory doesn’t exist: {parent_dir}")

@export
def write_to_path(data, pth, relative_to=None, verbose=False):
    """ Write data to a new file using a context-managed handle """
    ensure_path_is_valid(pth)
    bytestring = utf8_encode(data)
    with open(pth, "wb") as handle:
        handle.write(bytestring)
        handle.flush()
    if verbose:
        size = len(bytestring)
        start = relative_to or os.path.dirname(pth)
        relpth = os.path.relpath(pth, start=start)
        print(f"» Wrote {size!s} bytes to {relpth}")

@export
def script_path():
    """ Return the path to the embedded scripts directory. """
    return SCRIPT_PATH

@export
def which(binary_name, pathvar=None):
    """ Deduces the path corresponding to an executable name,
        as per the UNIX command `which`. Optionally takes an
        override for the $PATH environment variable.
        Always returns a string - an empty one for those
        executables that cannot be found.
    """
    return find_executable(binary_name, pathvar or which.pathvar) or ""

which.pathvar = PATH

@export
def back_tick(command,  as_str=True,
                       ret_err=False,
                     raise_err=None, **kwargs):
    f""" Run command `command`, returning stdout – or (stdout, stderr) if `ret_err`.
        
        Parameters
        ----------
        command : str / list / tuple
            Command to execute. Can be passed as a single string (e.g "ls -la")
            or a tuple or list composed of the commands’ individual tokens (like
            ["ls", "-la"]).
        as_str : bool, optional
            Whether or not the values returned from ``proc.communicate()`` should
            be unicode-decoded from bytestrings (using the specified encoding, which
            defaults to “{ENCODING}”) to strings before `back_tick(…)` returns.
            Default is True.
        ret_err : bool, optional
            If True, the return value is (stdout, stderr). If False, it is stdout.
            In either case `stdout` and `stderr` are strings containing output
            from the commands’ execution. Default is False.
        raise_err : None or bool, optional
            If True, raise a ‘clu.fs.filesystem.ExecutionError’ when calling the
                     function results in a non-zero return code.
            If None, it is set to True if `ret_err` is False,
                                  False if `ret_err` is True.
            Default is None (exception-raising depends on the value of `ret_err`).
        encoding : str, optional
            The name of the encoding to use when decoding the command output per
            the `as_str` value. Default is “{ENCODING}”.
        directory : str / Directory / path-like, optional
            The directory in which to execute the command. Default is None (in
            which case the process working directory, unchanged, will be used).
        verbose : bool, optional
            Whether or not debug information should be spewed to `sys.stderr`.
            Default is False.
        timeout : int, optional
            Number of seconds to wait for the executed command to complete before
            forcibly killing its subprocess. Default is {DEFAULT_TIMEOUT} seconds.
        
        Returns
        -------
        out : str / tuple
            If `ret_err` is False, return stripped string containing stdout from
            `command`.  If `ret_err` is True, return tuple of (stdout, stderr)
            where ``stdout`` is the stripped stdout, and ``stderr`` is the
            stripped stderr.
        
        Raises
        ------
        A ‘clu.fs.filesystem.ExecutionError’ will raise if the executed command
        returns with any non-zero exit status, and `raise_err` is set to True.
    """
    # Step 1: Prepare for battle:
    import subprocess, shlex
    verbose = bool(kwargs.pop('verbose',  False))
    timeout =  int(kwargs.pop('timeout',  DEFAULT_TIMEOUT))
    encoding = str(kwargs.pop('encoding', ENCODING))
    raise_err = raise_err is not None and raise_err or bool(not ret_err)
    commandseq = isexpandable(command)
    command_str = commandseq and " ".join(command) or u8str(command).strip()
    directory = 'directory' in kwargs and os.fspath(kwargs.pop('directory')) or None
    textmode = as_str and encoding or False
    # Step 2: DO IT DOUG:
    if not commandseq:
        command = shlex.split(command, posix=True)
    if verbose:
        print("EXECUTING:", file=sys.stdout)
        print(f"`{command_str}`",
                            file=sys.stdout)
        print("",           file=sys.stdout)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                           cwd=directory,
                                          text=textmode,
                                         shell=False)
    try:
        output, errors = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.terminate()
        output, errors = process.communicate(timeout=None)
    returncode = process.returncode
    # Step 3: Analyze the return code:
    if returncode is None:
        process.kill()
        raise ExecutionError(f'`{command_str}` terminated without exiting cleanly')
    if raise_err and returncode != 0:
        error_str = u8str(errors).strip()
        raise ExecutionError(f'`{command_str}` exited with status {returncode}, error: “{error_str}”')
    # Step 4: Tidy the output and return it:
    if verbose:
        if returncode != 0:
            print("",                           file=sys.stderr)
            print(f"NONZERO RETURN STATUS: {returncode}",
                                                file=sys.stderr)
            print("",                           file=sys.stderr)
        if len(u8str(output.strip())) > 0:
            output_str = u8str(output).strip()
            print("")
            print("OUTPUT:",                            file=sys.stdout)
            print(f"`{output_str}`",                    file=sys.stdout)
            print("",                                   file=sys.stdout)
        if len(u8str(errors.strip())) > 0:
            error_str = u8str(errors).strip()
            print("",                                   file=sys.stderr)
            print("ERRORS:",                            file=sys.stderr)
            print(f"`{error_str}`",                     file=sys.stderr)
            print("",                                   file=sys.stderr)
    if ret_err:
        return (output.strip(),
                errors.strip())
    return output.strip()

@export
def rm_rf(path):
    """ rm_rf() does what `rm -rf` does – so, for the love of fuck,
        BE FUCKING CAREFUL WITH IT.
    """
    if not isvalidpath(path):
        raise ExecutionError(
            "Can’t rm -rf without something to rm arr-effedly")
    path = os.fspath(path)
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        return True
    except (OSError, IOError):
        pass
    return False

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
    fullpth = os.path.join(directory, f"{prefix}{suffix}")
    if os.path.exists(fullpth):
        raise FilesystemError(f"temporary(): file exists: {fullpth}")
    return fullpth

@export
class TypeLocker(abc.ABCMeta):
    
    """ clu.fs.filesystem.TypeLocker is a metaclass that does two
        things with the types for whom it is designated as meta:
        
        1) It keeps an index of those types in a dictionary member of
           the `TypeLocker` metaclass itself; and
        
        2) During class creation – the call to `TypeLocker.__new__(…)` –
           it installs a class method called “directory(…)” that will,
           when invoked, always return a new Directory instance that has
           been initialized with the one provided argument “pth” (if one
           was passed).
        
        … The point of this is to allow any of the classes throughout the
        clu.fs.filesystem module regardless of where they are defined
        or from whom they inherit, to make use of cheaply-constructed
        Directory instances wherever convenient.
        
        Because the “directory(…)” method installed by TypeLocker performs
        a lazy-lookup of the Directory class, using its own type index dict,
        the order of definition does not matter i.e. the TemporaryName class
        (q.v. definition immediately sub.) can use Directories despite its
        definition occuring before Directory – in fact TemporaryName itself
        is utilized within at least one Directory method – sans any issues.
    """
    
    # The metaclass-internal dictionary of descendant type weakrefs:
    types = weakref.WeakValueDictionary()
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ All classes are initialized with a “directory(…)”
            static method, lazily returning an instance of the
            clu.fs.filesystem.Directory(…) class.
            
            A read-only descriptor shadows the “types” attribute,
            to block access to the metaclass type-registry dict
            from generated subtypes, as well.
        """
        # Fill in the “types” attribute to prevent the metaclass’
        # registry dict from leaking into subtypes:
        attributes['types']         = clu.abstract.ValueDescriptor(tuple())
        
        # Always replace the “directory” method anew:
        directory = lambda pth=None: metacls.types['Directory'](pth=pth)
        
        directory.__name__          = 'directory'
        directory.__qualname__      = f'{name}.directory'
        directory.__lambda_name__   = λ
        attributes['directory']     = staticmethod(directory)
        
        # Call up (using a vanilla attributes dict):
        cls = super(TypeLocker, metacls).__new__(metacls, name,
                                                          bases,
                                                          attributes,
                                                        **kwargs)
        
        # Register with clu.fs.TypeLocker and os.PathLike:
        metacls.types[name] = cls
        os.PathLike.register(cls)
        
        # Return the new type
        return cls

class TemporaryFileWrapper(TemporaryFileWrapperBase,
                           collections.abc.Iterable,
                           contextlib.AbstractContextManager,
                           os.PathLike,
                           metaclass=TypeLocker):
    
    """ Local subclass of `tempfile._TemporaryFileWrapper`.
        
        We also inherit from both `contextlib.AbstractContextManager`
        and the `os.PathLike` abstract bases -- the latter requires
        that we implement an __fspath__(…) method (q.v. implementation,
        sub.) -- and additionally, `filesystem.TypeLocker` is named as
        the metaclass (q.v. metaclass __new__(…) implementation supra.)
        to cache its type and register it as an os.PathLike subclass.
        
        … Basically a better deal than the original ancestor, like
        all-around. Plus it does not have a name prefixed with an
        underscore, which if it’s not your implementation dogg that
        can be a bit lexically irritating.
    """
    
    def __fspath__(self):
        return self.name

@cache
def TemporaryNamedFile(temppath, mode='wb',
                                 delete=True,
                                 buffer_size=-1):
    """ Variation on ``tempfile.NamedTemporaryFile(…)``, for use within
        `filesystem.TemporaryName()` – q.v. class definition sub.
        
        Parameters
        ----------
        temppath : str / bytes  / filename-ish
            File name, path, or filename-ish instance to open.
        mode : str / bytes, optional
            String-like symbolic explication of mode with which to open
            the file -- q.v. ``io.open(…)`` or ``__builtins__.open(…)``
            supra.
        delete : bool, optional
            Boolean value indicating whether to delete the wrapped
            file upon scope exit or interpreter shutdown (whichever
            happens first). Default is True.
        buffer_size : int, optional
            Integer indicating buffer size to use during file reading
            and/or writing. Default value is -1 (which indicates that
            reads and writes should be unbuffered).
        
        Returns
        -------
            A ``clu.fs.filesystem.TemporaryFileWrapper`` object,
            initialized and ready to be used, as per its counterpart(s),
            ``tempfile.NamedTemporaryFile``, and
            `filesystem.NamedTemporaryFile`.
        
        Raises
        ------
            A `clu.fs.filesystem.FilesystemError`, corresponding to
            any errors that may be raised during its own internal calls to
            ``os.open(…)`` and ``os.fdopen(…)``
        
    """
    from tempfile import _bin_openflags, _text_openflags
    
    if 'b' in mode:
        flags = _bin_openflags
    else:
        flags = _text_openflags
    if delete:
        flags |= DELETE_FLAG
    
    descriptor = 0
    filehandle = None
    path = None
    
    try:
        path = os.fspath(temppath)
        descriptor = os.open(path, flags)
        filehandle = os.fdopen(descriptor, mode, buffer_size)
        return TemporaryFileWrapper(filehandle, path, delete)
    except BaseException as base_exception:
        try:
            rm_rf(path)
        finally:
            if descriptor > 0:
                os.close(descriptor)
        raise FilesystemError(str(base_exception))

@export
class TemporaryName(collections.abc.Hashable,
                    contextlib.AbstractContextManager,
                    os.PathLike,
                    metaclass=TypeLocker):
    
    """ This is like NamedTemporaryFile without any of the actual stuff;
        it just makes a file name -- YOU have to make shit happen with it.
        But: should you cause such scatalogical events to transpire, this
        class (when invoked as a context manager) will clean it up for you.
        Unless you say not to. Really it's your call dogg I could give AF
    """
    
    fields = ('name',   'exists', 
                        'destroy',
              'mode',   'binary_mode',
              'prefix', 'suffix', 'dirname')
    
    def __init__(self, prefix=None, suffix="tmp",
                       parent=None,
                     **kwargs):
        """ Initialize a new TemporaryName object.
            
            All parameters are optional; you may specify “prefix”, “suffix”,
            “mode”, and “dir” (alternatively as “parent” which I think reads
            better) as per keyword arguments accepted by `tempfile.mktemp(…)`
            and `tempfile.NamedTemporaryFile`.
            
            Additionally, an optional keyword argument “randomized” specifies
            a boolean – this value is passed straight on to the `temporary(…)`
            function (q.v. definition supra.) with which we wrap all of our
            calls to `tempfile.mktemp(…)`.
            
            Suffixes may omit a leading period without causing any problems;
            in other words, “.jpg” and “jpg” are both valid suffix arguments,
            and they both mean the same thing.
        """
        # Get the “randomized” and “mode” keyword values:
        randomized = kwargs.pop('randomized', False)
        mode = kwargs.pop('mode', 'wb')
        
        # Enable randomization if using the default prefix,
        # to avoid otherwise highly likely name collisions:
        if not prefix:
            prefix = DEFAULT_PREFIX
            randomized = True
        
        # Normalize the suffix-value leading-period sitiuation,
        # regardless of whether or not the default is in use:
        if suffix:
            if not suffix.startswith(os.extsep):
                suffix = f"{os.extsep}{suffix}"
        else:
            suffix = f"{os.extsep}tmp"
        
        # Try the “parent” argument first, fall back to the “dir”
        # keyword, and normalize with `os.fspath(¬)`:
        if parent is None:
            parent = kwargs.pop('dir', None)
        if parent:
            parent = os.fspath(parent)
        
        # Initialize the “name” value with a call to `temporary(…)`:
        self._name = temporary(prefix=prefix, suffix=suffix,
                                              parent=parent,
                                              randomized=randomized)
        
        # Initialize the rest of the TemporaryName instance values:
        self._mode = mode.casefold()
        self._destroy = True
        self._parent = parent
        self.prefix = prefix
        self.suffix = suffix
    
    @property
    def name(self):
        """ The temporary file path (which initially does not exist). """
        return self._name
    
    @property
    def basename(self):
        """ The basename (aka the filename) of the temporary file path. """
        return os.path.basename(self._name)
    
    @property
    def dirname(self):
        """ The dirname (aka the enclosing directory) of the temporary file. """
        return self.parent()
    
    @property
    def exists(self):
        """ Whether or not there is anything existant at the temporary file path.
            
            Note that this property will be true for directories created therein,
            as well as FIFOs or /dev entries, or any of the other zany filesystem
            possibilities you and the POSIX standard can imagine, in addition to
            regular files.
        """
        return os.path.exists(self._name)
    
    @property
    def destroy(self):
        """ Whether or not this TemporaryName instance should destroy any file
            that should happen to exist at its temporary file path (as per its
            “name” attribute) on scope exit.
        """
        return self._destroy
    
    @property
    def mode(self):
        """ Get the mode string for this TemporaryName instance. This is used
            if and when a filehandle is accessed (q.v. “filehandle” property
            definition sub.) in the construction of the TemporaryNamedFile that
            is handed back as the filehandle instance.
        """
        return self._mode
    
    @property
    def binary_mode(self):
        """ Whether or not the mode with which this TemporaryName instance was 
            constructed is a “binary mode” – and as such, requires the operands
            passed to its `write(…)` methods of its filehandle (q.v. the “mode”
            property definition supra., and the “filehandle” property definition
            sub.) to be of type `byte` or `bytearray`, or of a type either derived
            or compatible with these. Errors will be raised if you try to call a
            `write(…)` method with a `str`-ish operand.
            
            Filehandles constructed through “non-binary” TemporaryName instances
            are the other way around – their `write(…)` methods can only be passed
            instances of `str` (or, `unicode`, for the Python-2 diehards amongst us)
            or similar; attempt to pass anything `byte`-y and you’ll get raised on.
        """
        return 'b' in self._mode
    
    @property
    def filehandle(self):
        """ Access a TemporaryNamedFile instance, opened and ready to read and write,
            for this TemporaryName instances’ temporary file path.
            
            While this is a normal property descriptor – each time it is accessed,
            its function is called anew – the underlying `TemporaryNamedFile` call
            is a cached function and not a class constructor (despite what you might
            think because of that CamelCased identifier). That means you’ll almost
            certainly be given the same instance whenever you access the “filehandle”
            property (which is less fraught with potentially confusing weirdness,
            I do believe).
            
            Accessing this property delegates the responsibility for destroying
            the TemporaryName file contents to the TemporaryNamedFile object --
            saving the TemporaryNamedFile in, like, a variable somewhere and then
            letting the original TemporaryName go out of scope will keep the file
            alive and unclosed, for example. THE UPSHOT: be sure to call “close()”
            on the filehandle instance you use. That’s fair, right? I think that’s
            totally fair to do it like that, OK.
        """
        return TemporaryNamedFile(temppath=self.do_not_destroy(),
                                      mode=self.mode)
    
    @property
    def filesize(self):
        """ The filesize for the temporary file """
        return filesize(self._name)
    
    def split(self):
        """ Return (dirname, basename) e.g. for /yo/dogg/i/heard/youlike.jpg,
            you get back (Directory("/yo/dogg/i/heard"), "youlike.jpg")
        """
        return self.dirname, self.basename
    
    def copy(self, destination):
        """ Copy the file (if one exists) at the instances’ file path
            to a new destination.
        """
        if not destination:
            raise FilesystemError("Copying requires a place to which to copy")
        if self.exists:
            if os.path.exists(destination):
                if os.path.samefile(self._name, destination):
                    raise FilesystemError("Can’t copy to identical locations")
                if os.path.isdir(destination):
                    raise FilesystemError("Can’t copy files over a directory")
                rm_rf(destination)
            return os.path.exists(
                   shutil.copy2(self._name, os.fspath(destination),
                                follow_symlinks=True))
        return False
    
    def parent(self):
        """ Sugar for `os.path.abspath(os.path.join(self.name, os.pardir))`
            which, if you are curious, gets you the parent directory of
            the instances’ target filename, wrapped in a Directory
            instance.
        """
        return self.directory(os.path.abspath(
                              os.path.join(self.name,
                                           os.pardir)))
    
    def read(self, *, original_position=False):
        """ Read data from the temporary name, if it points to an existing file """
        orig, out = 0, b""
        if not self.exists:
            if original_position:
                return orig, out
            return out
        with open(self._name, "r+b") as handle:
            orig = handle.seek(0)
            out += handle.read()
        if original_position:
            return orig, out
        return out
    
    def write(self, data):
        """ Write data to the temporary name using a context-managed handle """
        assert self.exists or self.parent().exists
        bytestring = utf8_encode(data)
        with open(self._name, "xb") as handle:
            handle.write(bytestring)
            handle.flush()
        return self.exists
    
    def do_not_destroy(self):
        """ Mark this TemporaryName instance as one that should not be automatically
            destroyed upon the scope exit for the instance.
            
            This function returns the temporary file path, and may be called more
            than once without further side effects.
        """
        self._destroy = False
        return self._name
    
    def close(self):
        """ Destroys any existing file at this instances’ file path. """
        if self.exists:
            return rm_rf(self._name)
        return False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if self.destroy:
            self.close()
        return exc_type is None
    
    def to_string(self):
        """ Stringify the TemporaryName instance. """
        return stringify(self, type(self).fields, try_callables=False)
    
    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        if self.exists:
            return os.path.realpath(self._name)
        return self._name
    
    def __bytes__(self):
        return bytes(str(self), encoding=ENCODING)
    
    def __fspath__(self):
        return self._name
    
    def __bool__(self):
        return self.exists
    
    def __eq__(self, other):
        if isnotpath(other):
            return NotImplemented
        try:
            return os.path.samefile(self._name,
                                    os.fspath(other))
        except FileNotFoundError:
            return False
    
    def __ne__(self, other):
        if isnotpath(other):
            return NotImplemented
        try:
            return differentfile(self._name,
                                 os.fspath(other))
        except FileNotFoundError:
            return True
    
    def __hash__(self):
        return hash((self._name, self.exists))

non_dotfile_match = re.compile(r"^[^\.]").match
non_dotfile_matcher = lambda p: non_dotfile_match(p.name)

@export
class Directory(collections.abc.Hashable,
                collections.abc.Reversible,
                collections.abc.Mapping,
                collections.abc.Sized,
                contextlib.AbstractContextManager,
                os.PathLike,
                metaclass=TypeLocker):
    
    """ A context-managed directory: change in on enter, change back out
        on exit. Plus a few convenience functions for listing and whatnot.
    """
    
    fields = ('name', 'old', 'new', 'exists',
              'will_change',        'did_change',
              'will_change_back',   'did_change_back')
    
    zip_suffix = f"{os.extsep}zip"
    
    def __init__(self, pth=None):
        """ Initialize a new Directory object.
            
            There is only one parameter, “pth” -- the target path for the Directory
            object instance. When the Directory is initialized as a context manager,
            the process working directory will change to this directory (provided
            that it’s a different path than the current working directory, according
            to `os.path.samefile(…)`).
            
            The “pth” parameter is optional, in which case the instance uses the
            process working directory as its target, and no change-of-directory
            calls will be issued. Values for “pth” can be string-like, or existing
            Directory instances -- either will work.
            
            There are several decendant classes of Directory (q.v. definitions below)
            that enforce stipulations for the “pth” parameter – e.g. the `cd` class 
            requires a target path to be provided (and therefore will nearly always
            change the working directory when invoked as a context manager); its
            sibling class `wd` forbids the naming of a “pth” value, thereby always
            initializing itself with the current working directory as its target,
            and fundamentally avoids issuing any directory-change calls.
        """
        if pth is not None:
            self.target = u8str(os.fspath(pth))
        else:
            self.target = os.getcwd()
    
    @property
    def name(self):
        """ The instances’ target directory path. """
        return attr(self, 'target', 'new')
    
    @property
    def basename(self):
        """ The basename (aka the name of the directory, like as opposed to the
            entire fucking absolute path) of the target directory.
        """
        return os.path.basename(self.name)
    
    @property
    def dirname(self):
        """ The dirname (aka the path of the enclosing directory) of the target
            directory, wrapped in a new Directory instance.
        """
        return self.parent()
    
    @property
    def exists(self):
        """ Whether or not the instances’ target path exists as a directory. """
        return os.path.isdir(self.name)
    
    @property
    def initialized(self):
        """ Whether or not the instance has been “initialized” -- as in, the
            `target` instance value has been set (q.v. `ctx_initialize(…)`
            help sub.) as it stands immediately after `__init__(…)` has run.
        """
        return hasattr(self, 'target')
    
    @property
    def targets_set(self):
        """ Whether or not the instance has had targets set (the `new` and `old`
            instance values, q.v. `ctx_set_targets(…)` help sub.) and is ready
            for context-managed use.
        """
        return allattrs(self, 'old', 'new')
    
    @property
    def prepared(self):
        """ Whether or not the instance has been internally prepared for use
            (q.v. `ctx_prepare()` help sub.) and is in a valid state.
        """
        return allattrs(self, 'will_change',
                              'will_change_back',
                              'did_change',
                              'did_change_back')
    
    def split(self):
        """ Return a two-tuple containing `(dirname, basename)` – like e.g.
            for `/yo/dogg/i/heard/youlike`, your return value will be like
            `(Directory("/yo/dogg/i/heard"), "youlike")`
        """
        return self.dirname, self.basename
    
    def ctx_initialize(self):
        """ Restores the instance to the freshly-allocated state -- with one
            notable exception: if it had been previously prepared (through a
            call to `instance.ctx_prepare()`) and thus has a “new” attribute
            filled in with a target path, `ctx_initialize()` will preserve
            the contents of that attribute in the value of the `self.target` 
            instance member.
            
            The call deletes all other instance attributes from the internal
            mapping of the instance in question, leaving it in a state ready
            for either context-managed reëntry, or for reuse in an unmanaged
            fashion *provided* one firstly calls `instance.ctx_set_targets()`
            or `instance.ctx_prepare()` in order to reconfigure (the minimal
            subset of, or the full complement of) the member-variable values
            needed by the internal workings of a Directory instance.
        """
        if self.targets_set:
            self.target = attr(self, 'new', 'old')
            delattr(self, 'old')
            delattr(self, 'new')
        if self.prepared:
            delattr(self, 'will_change')
            delattr(self, 'will_change_back')
            delattr(self, 'did_change')
            delattr(self, 'did_change_back')
        return self
    
    def ctx_set_targets(self, old=None):
        """ Sets the “self.old” and “self.new” instance variable values,
            using the value of `self.target` and an (optional) string-like
            argument to use as the value for “self.old”.
            
            One shouldn’t generally call this or have a need to call this --
            although one can manually invoke `instance.ctx_set_targets(…)`
            to reconfigure a Directory instance to use it again after it has
            been re-initialized after a call to `instance.ctx_initialize()`
            (q.v. `ctx_initialize()` help supra.) in cases where it isn’t
            going to be used as part of a managed context; that is to say,
            outside of a `with` statement.
            
            (Within a `with` statement, the call issued upon scope entry to
            `Directory.__enter__(self)` will internally make a call to
            `Directory.ctx_prepare(self)` (q.v. doctext help sub.) which
            that will call `Directory.ctx_set_targets(self, …)` itself.)
        """
        if not self.initialized:
            if old is None:
                old = os.getcwd()
            setattr(self, 'old', old)
            setattr(self, 'new', old)
            return self
        setattr(self, 'old', old is not None and old or self.target)
        setattr(self, 'new', self.target)
        delattr(self, 'target')
        return self
    
    def ctx_prepare(self):
        """ Prepares the member values of the Directory instance according
            to a requisite `self.target` directory-path value; the primary
            logic performed by this function determines whether or not it
            is necessary to switch the process working directory while the
            Directory instance is actively being used as a context manager
            in the scope of a `while` block.
            
            The reason this is done herein is to minimize the number of
            calls to potentially expensive system-call-wrapping functions
            such as `os.getcwd()`, `os.path.samefile(…)`, and especially
            `os.chdir(…)` -- which the use of the latter affects the state
            of the process issuing the call in a global fashion, and can
            cause invincibly undebuggable behavioral oddities to crop up
            in a variety of circumstances. 
        """
        self.ctx_set_targets(old=os.getcwd())
        if os.path.isdir(self.new):
            self.will_change = differentfile(self.old, self.new)
        else:
            self.will_change = False
        self.did_change = False
        self.will_change_back = self.will_change
        self.did_change_back = False
        return self
    
    def __enter__(self):
        self.ctx_prepare()
        if self.will_change and self.exists:
            os.chdir(self.new)
            self.did_change = os.path.samefile(self.new,
                                               os.getcwd())
            self.will_change_back = self.did_change
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        # N.B. return False to throw, True to supress:
        if self.will_change_back and os.path.isdir(self.old):
            os.chdir(self.old)
            self.did_change_back = os.path.samefile(self.old,
                                                    os.getcwd())
            if self.did_change_back:
                # return to pristine state:
                self.ctx_initialize()
                return exc_type is None
        # return to pristine state:
        self.ctx_initialize()
        return False
    
    def realpath(self, source=None):
        """ Sugar for calling os.path.realpath(self.name) """
        return u8str(
            os.path.realpath(
            os.fspath(source or self.name)))
    
    def ls(self, suffix=None, source=None):
        """ List files -- defaults to the process’ current working directory.
            As per the UNIX custom, files whose name begins with a dot are
            omitted.
            
            Specify an optional “suffix” parameter to filter the list by a
            particular file suffix (leading dots unnecessary but unharmful).
        """
        with os.scandir(self.realpath(source)) as iterscan:
            return tuple(filter(suffix_searcher(suffix),
                        (direntry.name for direntry in filter(non_dotfile_matcher,
                                                              iterscan))))
    
    def ls_la(self, suffix=None, source=None):
        """ List all files, including files whose name starts with a dot.
            The default is to use the process’ current working directory.
            
            Specify an optional “suffix” parameter to filter the list by a
            particular file suffix (leading dots unnecessary but unharmful).
            
            (Technically speaking, `ls_la()` is a misnomer for this method,
            as it does not provide any extended meta-info like you get if
            you use the “-l” flag when invoking the `ls` command -- I just
            like calling it that because “ls -la” was one of the first shell
            commands I ever learned, and it reads better than `ls_a()` which
            I think looks awkward and goofy.)
        """
        with os.scandir(self.realpath(source)) as iterscan:
            return tuple(filter(suffix_searcher(suffix),
                        (direntry.name for direntry in iterscan)))
    
    def subpath(self, subpath, source=None, requisite=False):
        """ Returns the path to a subpath of the instances’ target path. """
        fullpath = os.path.join(os.fspath(source or self.name),
                                os.fspath(subpath))
        return (os.path.exists(fullpath) or not requisite) and fullpath or None
    
    def subdirectory(self, subdir, source=None):
        """ Returns the path to a subpath of the instances’ target path --
            much like Directory.subpath(…) -- as an instance of Directory.
        """
        path = self.subpath(subdir, source, requisite=False)
        if os.path.isfile(path):
            raise FilesystemError(f"file exists at subdirectory path: {path}")
        if os.path.islink(path):
            raise FilesystemError(f"symlink exists at subdirectory path: {path}")
        if os.path.ismount(path):
            raise FilesystemError(f"mountpoint exists at subdirectory path: {path}")
        return self.directory(path)
    
    def makedirs(self, subpath=None, mode=0o755):
        """ Creates any parts of the target directory path that don’t
            already exist, á la the `mkdir -p` shell command.
        """
        try:
            os.makedirs(os.path.abspath(
                        os.path.join(self.name,
                        os.fspath(subpath or os.curdir))),
                        exist_ok=False,
                        mode=masked_permissions(mode))
        except OSError as os_error:
            raise FilesystemError(str(os_error))
        return self
    
    def walk(self, followlinks=True):
        """ Sugar for calling os.walk(self.name)
            
            Note that the “followlinks” default here is True, whereas
            the underlying functions default to False for that argument.
        """
        return os.walk(self.name, followlinks=followlinks)
    
    def parent(self):
        """ Sugar for `os.path.abspath(os.path.join(self.name, os.pardir))`
            which, if you are curious, gets you the parent directory of
            the instances’ target directory, wrapped in a Directory
            instance.
        """
        return self.directory(os.path.abspath(
                              os.path.join(self.name,
                                           os.pardir)))
    
    def relparent(self, path):
        """ Relativize a path, relative to the parent of the directory,
            and return it as a string.
            
            Used internally in the implementations of the instance
            methods “Directory.flatten(…)”, and “Directory.zip_archive(…)”.
        """
        return os.path.relpath(path, start=os.path.abspath(
                                           os.path.join(self.name,
                                                        os.pardir)))
    
    def relprefix(self, path, separator='_'):
        """ Return a “prefix” string based on a file path –
            the actual path separators are replaced with underscores,
            with which the individual path segments are joined, creating
            a single long string that is unique to the original file path.
            
            Used internally in the implementation of “Directory.flatten(…)”.
        """
        return (self.relparent(path) + os.sep).replace(os.sep, separator)
    
    def flatten(self, destination, suffix=None, new_suffix=None):
        """ Copy the entire directory tree, all contents included, to a new
            destination path – with all files residing within the same directory
            level.
            
            That is to say, if the directory tree is like:
            
                yo/
                yo/dogg/[0..9].jpg
                yo/dogg/nodogg/[0..99].png
            
            … you end up with a single destination directory, filled with files,
            all with names like:
            
                yo_dogg_[0..9].jpg
                yo_dogg_nodogg_[0..99].png
            
           `flatten(…)` will not overwrite existant directories. Like, if
            you have yourself an instance of Directory, `directory`, and you
            want to copy it to `/home/me/myshit`, `/home/me` should already
            exist but `/home/me/myshit` should not, as the subdirectory
           `myshit` gets created by the `directory.flatten('/home/me/myshit')`
            invocation (like as a side-effect).
            
            Does that make sense to you? Try it, you’ll get a `FilesystemError`
            if it evidently did not make sense to you.
            
            The destination path may be specified using a string-like, with
            another Directory object, or anything deemed path-y enough by
           `os.fspath(…)`. Internally, this method uses `shutil.copy2(…)`
            to tell the filesystem to copy and rename each file in succession.
        """
        if destination is None:
            raise FilesystemError("“flatten(…)” destination path cannot be None")
        whereto = self.directory(pth=destination)
        if anyof(whereto.exists, os.path.isfile(whereto.name),
                                 os.path.islink(whereto.name)):
            raise FilesystemError(
                f"flatten() destination exists: {whereto.name}")
        if self.exists:
            # Create destination directory, and list for the results:
            whereto.makedirs()
            results = []
            searcher = suffix_searcher(suffix)
            # Walk source directory:
            for root, dirs, files in self.walk():
                basic_prefix = self.relprefix(root)
                filenames = tuple(filter(searcher, files))
                iinputs = (os.path.join(root, filename) for filename in filenames)
                outputs = ((whereto.subpath(basic_prefix + (new_suffix and \
                                                    swapext(filename, new_suffix) or \
                                                            filename))) \
                                                        for filename in filenames)
                for iinfile, outfile in zip(iinputs, outputs):
                    results.append(
                      shutil.copy2(iinfile, outfile, follow_symlinks=True))
            # Return the destination directory instance and the result list:
            return whereto, tuple(results)
        else:
            raise FilesystemError(
                f"flatten(…) source doesn’t exist: {self.name}")
        return None, tuple()
    
    def copy_all(self, destination):
        """ Copy the entire directory tree, all contents included, to a new
            destination path. The destination must not already exist, and
           `copy_all(…)` will not overwrite existant directories. Like, if
            you have yourself an instance of Directory, `directory`, and you
            want to copy it to `/home/me/myshit`, `/home/me` should already
            exist but `/home/me/myshit` should not, as the subdirectory
           `myshit` gets created by the `directory.copy_all('/home/me/myshit')`
            invocation (like as a side-effect).
            
            Does that make sense to you? Try it, you’ll get a `FilesystemError`
            if it evidently did not make sense to you.
            
            The destination path may be specified using a string-like, with
            another Directory object, or anything deemed path-y enough by
           `os.fspath(…)`. Internally, this method uses `shutil.copytree(…)`
            to tell the filesystem what to copy where.
        """
        if destination is None:
            raise FilesystemError("“copy_all(…)” destination path cannot be None")
        whereto = self.directory(pth=destination)
        if anyof(whereto.exists, os.path.isfile(whereto.name),
                                 os.path.islink(whereto.name)):
            raise FilesystemError(
                f"copy_all() destination exists: {whereto.name}")
        if self.exists:
            return os.path.isdir(
                   shutil.copytree(self.name, whereto.name,
                                   symlinks=False))
        else:
            raise FilesystemError(
                f"copy_all(…) source doesn’t exist: {self.name}")
        return False
    
    def zip_archive(self, destination, compression_mode=zipfile.ZIP_DEFLATED):
        """ Recursively descends through the target directory, stowing all
            that it finds into a zipfile at the specified destination path.
            
            Use the optional “compression_mode” parameter to specify the
            compression algorithm, as per the constants found in the `zipfile`
            module; the default value is `zipfile.ZIP_DEFLATED`.
        """
        if destination is None:
            raise FilesystemError("zip-archive destination path cannot be None")
        zpth = os.fspath(destination)
        zsuf = type(self).zip_suffix
        if not zpth.casefold().endswith(zsuf):
            zpth = swapext(zpth, zsuf)
        if not compression_mode:
            compression_mode = zipfile.ZIP_DEFLATED
        ensure_path_is_valid(zpth)
        with TemporaryName(prefix="ziparchive-",
                           suffix=zsuf[1:],
                           randomized=True) as ztmp:
            with zipfile.ZipFile(ztmp.name, "w", compression_mode) as ziphandle:
                for root, dirs, files in self.walk():
                    ziphandle.write(root, self.relparent(root)) # add directory
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        if os.path.isfile(filepath): # regular files only
                            arcname = os.path.join(self.relparent(root), filename)
                            ziphandle.write(filepath, arcname) # add regular file
            assert ztmp.copy(zpth)
        return self.realpath(zpth)
    
    def symlink(self, destination, source=None):
        """ Create a symlink at `destination`, pointing to this instances’
            directory path (or an alternative source path, if specified).
            
            The `destination` argument can be anything path-like: instances of
            `str`, `unicode`, `bytes`, `bytearray`, `pathlib.Path`, `os.PathLike`,
            or anything with an `__fspath__(…)` method. 
        """
        if destination is None:
            raise FilesystemError("“symlink(…)” destination path cannot be None")
        os.symlink(os.fspath(source or self.name),
                   os.fspath(destination),
                   target_is_directory=True)
        return self
    
    def importables(self, subdir, suffix='py',
                                  source=None,
                                  excludes=('-', '+', 'pytest',
                                                      'obsolete',
                                                      'scripts')):
        """ List the importable file-based modules found within “subdir”,
            matching the “suffix” string, and not matching any of the
            “excludes” strings.
        """
        excluder = re_excluder(excludes)
        searcher = suffix_searcher(suffix)
        dotpaths = []
        target = self.subdirectory(subdir or os.path.curdir, source)
        # Use a call to “os.walk(…)” directly to allow modification of
        # the “dirs” list in-place:
        for root, dirs, files in os.walk(target):
            dirs[:] = list(filter(excluder, dirs))
            filenames = filter(excluder,
                        filter(searcher, files))
            dotpaths.extend(list(path_to_dotpath(os.path.join(root, filename),
                                                 relative_to=self.name)
                                                 for filename in filenames))
        return uniquify(sorted(dotpaths))
    
    def suffix_histogram(self, subdir=None,
                               source=None,
                               excludes=('~', '#', 'ds_store', '.git')):
        """ Return a ‘collections.Counter’ filled with a histogram of the
            file suffixes for all files found in the given subdirectory,
            excluding anything matching any of the “excludes” strings
        """
        excluder = re_excluder(excludes)
        searcher = re_searcher(re.escape(os.path.extsep))
        suffixes = collections.Counter()
        target = self.subdirectory(subdir or os.path.curdir, source)
        # Use a call to “os.walk(…)” directly to allow modification of
        # the “dirs” list in-place:
        for root, dirs, files in os.walk(target):
            dirs[:] = list(filter(excluder, dirs))
            for ext in filter(None,
                       map(lambda filename: extension(filename).casefold(),
                       filter(excluder,
                       filter(searcher, files)))):
                suffixes[ext] += 1
        return suffixes
    
    def close(self):
        """ Stub method -- always returns True: """
        return True
    
    def to_string(self):
        """ Stringify the Directory instance. """
        return stringify(self, type(self).fields)
    
    @wraps(dict.items)
    def items(self):
        return OrderedItemsView(self)
    
    @wraps(dict.keys)
    def keys(self):
        return OrderedKeysView(self)
    
    @wraps(dict.values)
    def values(self):
        return OrderedValuesView(self)
    
    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        if self.exists:
            return self.realpath()
        return self.name
    
    def __bytes__(self):
        return bytes(str(self), encoding=ENCODING)
    
    def __fspath__(self):
        return self.name
    
    def __bool__(self):
        return self.exists
    
    def __iter__(self):
        out = self.exists \
              and (k.name for k in os.scandir(
                                   os.path.realpath(self.name))) \
               or iter(tuple())
        yield from out
    
    def __reversed__(self):
        out = self.exists \
              and (k.name for k in reversed(os.scandir(
                                   os.path.realpath(self.name)))) \
               or iter(tuple())
        yield from out
    
    def __len__(self):
        return self.exists \
               and len(os.listdir(
                       os.path.realpath(self.name))) \
                or 0
    
    def __getitem__(self, filename):
        pth = self.subpath(filename, requisite=True)
        if not pth:
            raise KeyError(
                f"file not found: {os.fspath(filename)}")
        return pth
    
    def __contains__(self, filename):
        return self.subpath(filename, requisite=True) is not None
    
    def __truediv__(self, filename):
        return self.subpath(filename, requisite=False)
    
    def __rtruediv__(self, filepath):
        return self.directory(filepath).subdirectory(self)
    
    def __eq__(self, other):
        if isnotpath(other):
            return NotImplemented
        try:
            return os.path.samefile(self.name,
                                    os.fspath(other))
        except FileNotFoundError:
            return False
    
    def __ne__(self, other):
        if isnotpath(other):
            return NotImplemented
        try:
            return differentfile(self.name,
                                 os.fspath(other))
        except FileNotFoundError:
            return True
    
    def __hash__(self):
        return hash((self.name, self.exists))

@export
class cd(Directory):
    
    def __init__(self, pth):
        """ Change to a new directory (the target path `pth` must be specified).
        """
        super(cd, self).__init__(pth)

@export
class wd(Directory):
    
    def __init__(self):
        """ Initialize a Directory instance for the current working directory.
        """
        super(wd, self).__init__(pth=None)

@export
class td(Directory):
    
    def __init__(self):
        """ Initialize a Directory instance for the current temporary directory.
        """
        from tempfile import gettempdir
        super(td, self).__init__(pth=gettempdir())

@export
class hd(Directory):
    
    def __init__(self):
        """ Initialize a Directory instance for the current user’s home directory.
        """
        super(hd, self).__init__(pth=gethomedir())

@export
class TemporaryDirectory(Directory):
    
    """ It’s funny how this code looks, like, 99 percent exactly like the above
        TemporaryName class -- shit just works out that way. But this actually
        creates the directory in question; much like filesystem::TemporaryDirectory
        from `libimread`, this class wraps tempfile.mkdtemp() and can be used as
        a context manager (the C++ orig used RAII).
    """
    
    fields = ('name', 'old', 'new', 'exists',
              'destroy', 'prefix',  'suffix', 'parent',
              'will_change',        'did_change',
              'will_change_back',   'did_change_back')
    
    def __init__(self, prefix="TemporaryDirectory-", suffix="",
                                                     parent=None,
                                                     change=True,
                                                   **kwargs):
        """ Initialize a new TemporaryDirectory object.
            
            All parameters are optional; you may specify “prefix”, “suffix”,
            and “dir” (alternatively as “parent” which I think reads better)
            as per `tempfile.mkdtemp(…)`. Suffixes may omit the leading period
            without confusing things. 
            
            The boolean “change” parameter determines whether or not the
            process working directory will be changed to the newly created
            temporary directory; it defaults to `True`.
        """
        from tempfile import mkdtemp
        if suffix:
            if not suffix.startswith(os.extsep):
                suffix = f"{os.extsep}{suffix}"
        if parent is None:
            parent = kwargs.pop('dir', None)
        if parent:
            parent = os.fspath(parent)
        self._name = mkdtemp(prefix=prefix, suffix=suffix, dir=parent)
        self._destroy = True
        self._parent = parent
        self.prefix = prefix
        self.suffix = suffix
        self.change = change
        super(TemporaryDirectory, self).__init__(self._name)
    
    @property
    def name(self):
        """ The temporary directory pathname. """
        return self._name
    
    @property
    def exists(self):
        """ Whether or not the temporary directory exists. """
        return os.path.isdir(self._name)
    
    @property
    def destroy(self):
        """ Whether or not the TemporaryDirectory instance has been marked
            for automatic deletion upon scope exit (q.v __exit__(…) method
            definition sub.)
        """
        return self._destroy
    
    @wraps(Directory.ctx_prepare)
    def ctx_prepare(self):
        change = super(TemporaryDirectory, self).ctx_prepare().change
        self.will_change = self.will_change_back = bool(self.will_change and change)
        return self
    
    def symlink(self, *args, **kwargs):
        """ Symlinking to TemporaryDirectory instances is disabled –
            why do you want to symlink to something that is about
            to delete itself?? That is just asking for a whole bunch of
            dangling references dogg.
        """
        raise FilesystemError("can’t symlink to a TemporaryDirectory")
    
    def close(self):
        """ Delete the directory pointed to by the TemporaryDirectory
            instance, and everything it contains. USE WITH CAUTION.
        """
        out = super(TemporaryDirectory, self).close()
        if self.exists:
            return rm_rf(self.name) and out
        return False
    
    def do_not_destroy(self):
        """ Mark this TemporaryDirectory instance as one that should not
            be automatically destroyed upon the scope exit for the instance.
            
            This function returns the temporary directory path, and may
            be called more than once without further side effects.
        """
        self._destroy = False
        return self.name
    
    def __enter__(self):
        if not self.exists:
            self.makedirs()
        super(TemporaryDirectory, self).__enter__()
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        out = super(TemporaryDirectory, self).__exit__(exc_type, exc_val, exc_tb)
        if self.destroy:
            out &= self.close()
        return out

@export
class Intermediate(TemporaryDirectory, Directory):
    
    """ clu.fs.filesystem.Intermediate isn’t a class, per se – rather,
        it is a class factory proxy that normally constructs a new Directory
        instance in leu of itself, except for when it it is constructed without
        a `pth` argument, in which case, it falls back to the construction of
        a new TemporaryDirectory instance instead.
    """
    
    def __new__(cls, pth=None, change=False):
        """ The constructor simply delegates to the creation of either a new
            Directory or a new TemporaryDirectory.
        """
        if pth is not None:
            return Directory(pth=pth)
        return TemporaryDirectory(prefix=f"{cls.__name__}-",
                                  change=change)
    
    def __init__(self, pth=None, change=False):
        """ The initializer explicitly does nothing, as it will always be called
            on an already-initialized instance of some other class.
        """
        pass

@export
def NamedTemporaryFile(mode='w+b', buffer_size=-1,
                       suffix="tmp", prefix=DEFAULT_PREFIX,
                       directory=None,
                       delete=True):
    """ Variation on ``tempfile.NamedTemporaryFile(…)``, such that suffixes
        are passed WITHOUT specifying the period in front (versus the
        standard library version which makes you pass suffixes WITH
        the fucking period, ugh).
    """
    from tempfile import (gettempdir, _bin_openflags,
                                      _text_openflags,
                                      _mkstemp_inner)
    
    parent = Directory(pth=directory or gettempdir())
    
    if suffix:
        if not suffix.startswith(os.extsep):
            suffix = f"{os.extsep}{suffix}"
    else:
        suffix = f"{os.extsep}tmp"
    
    if 'b' in mode:
        flags = _bin_openflags
    else:
        flags = _text_openflags
    if delete:
        flags |= DELETE_FLAG
    
    (descriptor, name) = _mkstemp_inner(parent.name, prefix,
                                                     suffix, flags,
                                               bytes(suffix, encoding=ENCODING))
    try:
        filehandle = os.fdopen(descriptor, mode, buffer_size)
        return TemporaryFileWrapper(filehandle, name, delete)
    except BaseException as base_exception:
        rm_rf(name)
        if descriptor > 0:
            os.close(descriptor)
        raise FilesystemError(str(base_exception))

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()