# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract
import collections.abc
import contextlib
import os
import sys
import weakref

abstract = abc.abstractmethod

from clu.constants.consts import λ, ENCODING
from clu.constants.exceptions import FilesystemError
from clu.fs.misc import u8str
from clu.repr import strfields
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class TypeLocker(abc.ABCMeta):
    
    """ clu.fs.abc.TypeLocker is a metaclass that does two things
        with the types for whom it is designated as meta:
        
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

@export
class BaseFSName(collections.abc.Hashable,
                 contextlib.AbstractContextManager,
                 os.PathLike, metaclass=TypeLocker):
    
    @property
    @abstract
    def name(self):
        """ The instances’ target directory path. """
        ...
    
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
    
    def split(self):
        """ Return a two-tuple containing `(dirname, basename)` – like e.g.
            for `/yo/dogg/i/heard/youlike`, your return value will be like
            `(Directory("/yo/dogg/i/heard"), "youlike")`
        """
        return self.dirname, self.basename
    
    def realpath(self, source=None):
        """ Sugar for calling os.path.realpath(self.name) """
        return u8str(
            os.path.realpath(
            os.fspath(source or self.name)))
    
    def parent(self):
        """ Sugar for `os.path.abspath(os.path.join(self.name, os.pardir))`
            which, if you are curious, gets you the parent directory of
            the instances’ target directory, wrapped in a Directory
            instance.
        """
        return self.directory(os.path.abspath(self.basename))
    
    def close(self):
        """ Stub method -- always returns True: """
        return True
    
    @abstract
    def to_string(self):
        ...
    
    def __str__(self):
        if self.exists:
            return os.path.realpath(self.name)
        return self.name
    
    def __bytes__(self):
        return bytes(str(self), encoding=ENCODING)
    
    def __repr__(self):
        return self.to_string()
    
    def __fspath__(self):
        return self.name
    
    @abstract
    def __enter__(self):
        ...
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        # if self.destroy:
        #     self.close()
        return exc_type is None
    
    def __bool__(self):
        return self.exists
    
    @abstract
    def __eq__(self, other):
        ...
    
    @abstract
    def __ne__(self, other):
        ...
    
    @abstract
    def __hash__(self):
        ...

@export
class FileName(BaseFSName,
               clu.abstract.Cloneable,
               clu.abstract.ReprWrapper):
    
    def relparent(self, path):
        """ Relativize a path, relative to the parent of the directory,
            and return it as a string.
            
            Used internally in the implementations of the instance
            methods “Directory.flatten(…)”, and “Directory.zip_archive(…)”.
        """
        return os.path.relpath(path, start=os.path.abspath(self.basename))
    
    def relprefix(self, path, separator='_'):
        """ Return a “prefix” string based on a file path –
            the actual path separators are replaced with underscores,
            with which the individual path segments are joined, creating
            a single long string that is unique to the original file path.
            
            Used internally in the implementation of “Directory.flatten(…)”.
        """
        return (self.relparent(path) + os.sep).replace(os.sep, separator)
    
    def symlink(self, destination, source=None):
        """ Create a symlink at `destination`, pointing to this instances’
            directory path (or an alternative source path, if specified).
            
            The `destination` argument can be anything path-like: instances of
            `str`, `unicode`, `bytes`, `bytearray`, `pathlib.Path`, `os.PathLike`,
            or anything with an `__fspath__(…)` method. 
        """
        if destination is None:
            raise FilesystemError("“symlink(…)” destination path cannot be None")
        target = source or self.name
        os.symlink(os.fspath(target),
                   os.fspath(destination),
                   target_is_directory=os.path.isdir(target))
        return self
    
    def to_string(self):
        # N.B. without a “fields” attribute on the class,
        # this method could act somewhat peculiar:
        cls = type(self)
        return strfields(self,
               getattr(cls, 'fields', None),
                       try_callables=False)
    
    @abstract
    def clone(self, deep=False, memo=None):
        ...
    
    def inner_repr(self):
        return self.to_string()


# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    # from clu.testing.utils import inline
    
    # @inline
    def test_one():
        pass # INSERT TESTING CODE HERE, pt. I
    
    #@inline.diagnostic
    def show_me_some_values():
        pass # INSERT DIAGNOSTIC CODE HERE
    
    # return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

