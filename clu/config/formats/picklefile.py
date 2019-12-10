# -*- coding: utf-8 -*-
from __future__ import print_function

import pickle

from clu.constants.consts import PROJECT_NAME
from clu.config.defg import FrozenNested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()
    
options = { 'protocol' : -1 }

@export
class PickleFileBase(FileBase, FrozenNested):
    
    """ The base class for “clu.config.picklefile.PickleFile”. Override this
        class in your own project to use pickle file data in your Schema
        pipelines as a NamespacedMutableMapping – q.v. the docstring for
        “clu.config.picklefile.PickleFile” sub.
        
        This class uses two mixins: both “clu.config.base.AppName” and
        “clu.config.filebase.FileName” are part of its inheritance chain.
        The “AppName” mixin acts on the “appname” class keyword, and the
        “FileName” mixin acts on the “filename” class keyword (furnishing
        many related class methods). 
    """
    
    def loads(self, loaded):
        """ Load nested namespaced dictionary data from a pickle-encoded string """
        self.tree = pickle.loads(loaded)
    
    def dumps(self):
        """ Dump a pickle-encoded string from nested namespaced dictionary data """
        return pickle.dumps(self.tree, **options)

pickle_appname  = PROJECT_NAME
pickle_filename = f'{PROJECT_NAME}-config.p'

@export
class PickleFile(PickleFileBase, appname=pickle_appname,
                                filename=pickle_filename):
    
    """ A representation of a pickle file’s data as a NamespacedMutableMapping.
        
        This class is specifically germane to the CLU project – note
        that the “appname” and “filename” class keywords are used to
        assign values that are CLU-specific.
        
        CLU users who wish to use pickle files as NamespacedMutableMappings
        in their own projects should create a subclass of PickleFileBase of
        their own. Like this one, it needs to assign both the “appname”
        and the “filename” class keywords; it is unnecessary (but OK!) to
        define further methods, properties, class constants, and whatnot.
    """
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
