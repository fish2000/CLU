# -*- coding: utf-8 -*-
from __future__ import print_function

import abc

from clu.constants.consts import PROJECT_NAME
from clu.config.base import AppName, NamespacedMutableMapping
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class FileName(abc.ABC):
    
    @classmethod
    def __init_subclass__(cls, filename=None, **kwargs):
        super(FileName, cls).__init_subclass__(**kwargs)
        cls.filename = ValueDescriptor(filename)
    
    def __init__(self, *args, **kwargs):
        if type(self).filename is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(filename is None)")

class FileBase(NamespacedMutableMapping, AppName, FileName, appname=PROJECT_NAME):
    
    @classmethod
    def find_file(cls):
        pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
