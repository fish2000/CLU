# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from clu.constants.consts import PROJECT_NAME
from clu.config.defg import Nested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()
    
options = { 'separators' : (',', ' : '),
             'sort_keys' : True,
                'indent' : 4 }

@export
class JsonFileBase(FileBase, Nested):
    
    """ The base class for “clu.config.jsonfile.JsonFile”. Override this
        class in your own project to use JSON file data in your Schema
        pipelines as a NamespacedMutableMapping – q.v. the docstring for
        “clu.config.jsonfile.JsonFile” sub.
        
        This class uses two mixins: both “clu.config.base.AppName” and
        “clu.config.filebase.FileName” are part of its inheritance chain.
        The “AppName” mixin acts on the “appname” class keyword, and the
        “FileName” mixin acts on the “filename” class keyword (furnishing
        many related class methods). 
    """
    
    def loads(self, loaded):
        """ Load nested namespaced dictionary data from a JSON-encoded string """
        self.tree = json.loads(loaded)
    
    def dumps(self):
        """ Dump a JSON-encoded string from nested namespaced dictionary data """
        return json.dumps(self.tree, **options)

json_appname  = PROJECT_NAME
json_filename = f'{PROJECT_NAME}-config.json'

@export
class JsonFile(JsonFileBase, appname=json_appname,
                            filename=json_filename):
    
    """ A representation of a JSON file’s data as a NamespacedMutableMapping.
        
        This class is specifically germane to the CLU project – note
        that the “appname” and “filename” class keywords are used to
        assign values that are CLU-specific.
        
        CLU users who wish to use JSON files as NamespacedMutableMappings
        in their own projects should create a subclass of JsonFileBase of
        their own. Like this one, it needs to assign both the “appname”
        and the “filename” class keywords; it is unnecessary (but OK!) to
        define further methods, properties, class constants, and whatnot.
    """
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
