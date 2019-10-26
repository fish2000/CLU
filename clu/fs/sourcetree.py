# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import os
import sys

from clu.constants.exceptions import ExecutionError
from clu.constants.polyfills import Path
from clu.abstract import Slotted
from clu.fs.filesystem import back_tick, Intermediate
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

SOURCE_SEP = '#'
MULTILINE_QUOTES = ('"""', "'''")

@export
class SourceTree(abc.ABC, metaclass=Slotted):
    
    __slots__ = ('directory', 'header_lines', 'filepath')
    
    def __init__(self, filepath, path=None, **kwargs):
        try:
            super(SourceTree, self).__init__(**kwargs)
        except TypeError:
            super(SourceTree, self).__init__()
        
        # Check the “srctree” file:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)
        
        # Stash “filepath” and initialize “header”:
        self.filepath = Path(filepath)
        self.header_lines = []
        
        # Initialize our working directory --
        # This wil be a TemporaryDirectory if “None” is passed:
        self.directory = Intermediate(pth=path,
                                      change=True)
    
    @property
    def name(self):
        return self.directory.name
    
    @property
    def basename(self):
        return self.directory.basename
    
    @property
    def dirname(self):
        return self.directory.dirname
    
    @property
    def exists(self):
        return self.directory.exists
    
    @property
    def destroy(self):
        return getattr(self.directory, 'destroy', False)
    
    def do_not_destroy(self):
        return getattr(self.directory, 'do_not_destroy', lambda: self.name)()
    
    @property
    def cython_script(self):
        import cython as cyscript
        return cyscript.__file__
    
    @property
    def python_executable(self):
        return sys.executable
    
    @property
    def header(self):
        return ''.join(self.header_lines)
    
    def prepared_headers(self):
        return (self.header
            .replace('CYTHON', f'PYTHON {self.cython_script}')
            .replace('PYTHON', f'{self.python_executable}'))
    
    def unpack(self):
        currentfile = None
        with self.filepath.open() as handle:
            lines = handle.readlines()
        try:
            for line in lines:
                if line[:5] == SOURCE_SEP * 5:
                    filename = line.strip().strip(SOURCE_SEP).strip().replace('/', os.path.sep)
                    path = self.directory.subpath(filename)
                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    if currentfile is not None:
                        f, currentfile = currentfile, None
                        f.close()
                    currentfile = open(path, 'w')
                elif currentfile is not None:
                    currentfile.write(line)
                elif line.strip() and not line.lstrip().startswith(SOURCE_SEP):
                    if line.strip() not in MULTILINE_QUOTES:
                        self.header_lines.append(line)
        finally:
            if currentfile is not None:
                currentfile.close()
        return self.prepared_headers()
    
    def __enter__(self):
        # N.B. This will change working directories:
        self.directory.__enter__()
        commands = self.unpack()
        out = []
        exs = []
        for command in commands:
            try:
                _out, _err = back_tick(command, raise_err=True,
                                                  ret_err=True)
            except ExecutionError as exc:
                exs.append(str(exc))
            else:
                out.append((_out, _err))
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        # N.B. This may destroy “self.directory”:
        return self.directory.__exit__(exc_type, exc_val, exc_tb)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
