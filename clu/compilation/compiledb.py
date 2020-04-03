# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
# import clu.abstract
import collections.abc
import contextlib
import json
import sys, os

abstract = abc.abstractmethod

from clu.constants.consts import ENCODING
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
    
    # @abstract
    # def to_string(self):
    #     ...
    
    @abstract
    def inner_repr(self):
        ...
    
    @abstract
    def __str__(self):
        ...
    
    @abstract
    def __bytes__(self):
        ...
    
    @abstract
    def __bool__(self):
        ...

@export
class CDBBase(CDBSubBase):
    
    fields = tuple()
    
    def __init__(self):
        self.clear()
    
    def push(self, source, command, directory=None,
                                    destination=None):
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
        self.entries = {} # type: dict
        return self
    
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
        raise KeyError(f"not found: {key}")
    
    def inner_repr(self):
        return strfields(self, type(self).fields)
    
    def rollout(self):
        # out = []
        # for k, v in self.entries.items():
        #     out.append(v)
        # return out
        return list(self)
    
    def __str__(self):
        return u8str(json.dumps(self.rollout()))
    
    def __bytes__(self):
        return bytes(json.dumps(self.rollout()), encoding=ENCODING)
    
    def __bool__(self):
        return True

@export
class CDBJsonFile(CDBBase, contextlib.AbstractContextManager):
    
    fields = ('filename', 'name', 'exists')
    filename = 'compilation_database.json'
    splitname = os.path.splitext(filename)
    
    @classmethod
    def in_directory(cls, directory):
        return cls.filename in Directory(directory)
    
    def __init__(self, directory=None):
        super().__init__()
        self.contextdir = Directory(directory)
        self.target = self.contextdir.subpath(self.filename)
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
                raise CDBError(str(json_error))
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
                handle.write(str(self))
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
        if os.path.isfile(self.target):
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
        cdb = CDBJsonFile()
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