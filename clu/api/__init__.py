# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import sys

abstract = abc.abstractmethod

from clu.constants import consts
from clu.importing import ModuleBase, initialize_types
from clu.importing import modules_for_appname_and_appspace
from clu.naming import dotpath_join
from clu.predicates import attr
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

API_APPSPACE = 'commands'

Module, Finder, Loader = initialize_types(consts.APPNAME, API_APPSPACE)

class CommandBase(ModuleBase):
    
    @property
    def commandname(self):
        return attr(self, 'commandstr', 'name')
    
    @abstract
    def statusbar(self, iterable, *extras):
        """ I completely made up this signature, it will no doubt change """
        ...
    
    @abstract
    def execute(self):
        pass

class Command(CommandBase[Module]):
    commandstr = "command" # …a reserved word?

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_command_imports():
        """ Command import test """
        from clu.commands import Command as command
        assert command
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
