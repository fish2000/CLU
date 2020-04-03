# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
# import clu.abstract
import collections.abc
import contextlib
import json
import sys, os

abstract = abc.abstractmethod

from clu.constants import consts
from clu.constants.exceptions import CDBError
from clu.fs.abc import BaseFSName
from clu.fs.filesystem import TemporaryName, Directory, rm_rf
from clu.fs.misc import u8str
# from clu.predicates import tuplize
from clu.repr import strfields
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class CDBSubBase(BaseFSName, collections.abc.Sequence):
    
    @abstract
    def push(self, filepath, command, directory=None,
                                      destination=None):
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    @abstract
    def __len__(self):
        ...
    
    @abstract
    def __getitem__(self, key):
        ...
    
    @abstract
    def inner_repr(self):
        ...
    
    @abstract
    def to_json(self):
        """ Dump the contents of the CDB as a JSON UTF-8 string. """
        ...
    
    @abstract
    def __str__(self):
        ...
    
    @abstract
    def __bytes__(self):
        ...

@export
class CDBBase(CDBSubBase):
    
    def __init__(self):
        """ Initialize the CDB base type.
            
            The CDBBase ancestor type takes no constructor arguments.
        """
        self.clear()
    
    def __iter__(self):
        yield from self.entries.values()
    
    def __len__(self):
        return len(self.entries)
    
    def __getitem__(self, key):
        try:
            return self.entries[int(key)]
        except (ValueError, KeyError):
            skey = str(key)
            if os.extsep in skey:
                for entry in self.entries:
                    if entry['file'] == skey:
                        return entry
        raise KeyError(key)
    
    def push(self, source, command, directory=None,
                                    destination=None):
        """ Add an entry to the CDB. """
        if not source:
            raise CDBError("a file source is required per entry")
        
        entry = {
            'directory'     : os.fspath(directory or os.getcwd()),
            'command'       : u8str(command),
            'file'          : source
        }
        
        if destination:
            entry.update({
                'output'    : destination
            })
        self.entries[source] = entry
    
    def clear(self):
        """ Reset the CDB’s “entries” mapping to a fresh empty dict. """
        self.entries = {}
        return self
    
    def rollout(self):
        """ Call to “roll” the CDB values out into a new list. """
        return list(self)
    
    def inner_repr(self):
        return strfields(self, type(self).fields)
    
    def to_json(self):
        return json.dumps(self.rollout())
    
    def __str__(self):
        return self.to_json()
    
    def __bytes__(self):
        return bytes(self.to_json(), encoding=consts.ENCODING)
    
    def __bool__(self):
        # N.B. Can’t use BaseFSName.__bool__(…) as it will
        # always be Falsey for any instances that haven’t
        # yet been written to disk:
        return bool(self.entries)

@export
class CDBJsonFile(CDBBase, contextlib.AbstractContextManager):
    
    fields = ('filename',
              'contextdir',
              'target') # ‘name’ and ‘exists’ come from BaseFSName
    
    filename = 'compilation_database.json'
    splitname = os.path.splitext(filename)
    
    @classmethod
    def in_directory(cls, directory):
        """ The compilation database filename is a constant –
            use this function to check if a file by that name
            exists in a given directory (which may be passed
            as string data, bytes data, or an instance of the
            “os.PathLike” ABC).
            
            Like so:
                
                >>> builddir = pathlib.Path('/var/tmp/build')
                >>> if CDBJsonFile.in_directory(builddir):
                >>>     # …do something!
        """
        return cls.filename in Directory(directory)
    
    def __init__(self, directory=None, hidden=False):
        """ Initialize a JSON-backed compilation database (CDB).
            
            Pass a path-like instance as “directory” to specify where
            on the filesystem the CDB should be created. The default
            directory is whatever the current working directory happens
            to be when you initialize the CDB instance.
            
            The filename of a JSON compilation database is hardcoded
            to “compilation_database.json” – this is part of the LLVM
            specification for such things.  Optionally, you may specify
            a “hidden=True” argument in order to prefix this filename
            with a dot, thus hiding it as per the long-standing UNIX-ish
            custom. Doing so may be somehow “non-conformant”, though;
            you have been warned.
        """
        super().__init__()
        self.contextdir = Directory(directory)
        filename = hidden and f"{consts.QUALIFIER}{self.filename}" or self.filename
        self.target = self.contextdir.subpath(filename)
        self.read_from = None
        self.written_to = None
    
    @property
    def name(self):
        return self.target
    
    @property
    def exists(self):
        return os.path.isfile(self.name)
    
    def read(self, path=None):
        readpath = path or self.target
        
        if not readpath:
            raise CDBError("no path value from which to read")
        
        readpath = os.fspath(readpath)
        if not os.path.exists(readpath):
            raise CDBError("no file from which to read")
        
        with open(readpath, mode="r") as handle:
            try:
                cdblist = json.load(handle)
            except json.JSONDecodeError as json_error:
                raise CDBError("JSON decoder error") from json_error
            else:
                for cdbentry in cdblist:
                    key = cdbentry.get('file')
                    self.entries[key] = dict(cdbentry)
        self.read_from = readpath
        return self
    
    def write(self, path=None):
        with TemporaryName(prefix=self.splitname[0],
                           suffix=self.splitname[1][1:]) as tn:
            with open(tn.name, mode='w') as handle:
                handle.write(self.to_json())
            if path is None:
                if self.exists:
                    rm_rf(self.name)
                tn.copy(self.name)
                self.written_to = self.name
            else:
                writepath = os.fspath(path)
                if os.path.isdir(writepath):
                    raise CDBError("can't overwrite a directory")
                if os.path.isfile(writepath) or \
                   os.path.islink(writepath):
                    rm_rf(writepath)
                tn.copy(writepath)
                self.written_to = writepath
        return self
    
    def __enter__(self):
        if self.exists:
            self.read()
        return self
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        self.write()

export(CDBError)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        from clu.fs.filesystem import td
        tmp = td()
        
        cdb = CDBJsonFile(directory=tmp)
        assert os.path.samefile(tmp, cdb.contextdir)
        assert not cdb # no entries yet
        assert not os.path.isfile(cdb.name)
        assert not cdb.exists
        
        print("CDB file path:", cdb.name)
        
        cdb.push('yo_dogg.cc', 'clang++ -o yo_dogg.o -pipe -Wall -pedantic')
        assert cdb
    
    #@inline
    def test_two():
        pass # INSERT TESTING CODE HERE, pt. II
    
    #@inline.diagnostic
    def show_me_some_values():
        pass # INSERT DIAGNOSTIC CODE HERE
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())