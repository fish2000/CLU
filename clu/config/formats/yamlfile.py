# -*- coding: utf-8 -*-
from __future__ import print_function

import yaml

from clu.constants.consts import PROJECT_NAME
# from clu.config.defg import FrozenNested
from clu.config.base import Nested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()
    
options = { 'default_flow_style' : True,
                'explicit_start' : True,
                  'explicit_end' : True,
                        'indent' : 4 }

@export
class YamlFileBase(FileBase, Nested):
    
    """ The base class for “clu.config.yamlfile.YamlFile”. Override this
        class in your own project to use YAML file data in your Schema
        pipelines as a NamespacedMutableMapping – q.v. the docstring for
        “clu.config.yamlfile.YamlFile” sub.
        
        This class uses two mixins: both “clu.config.base.AppName” and
        “clu.config.filebase.FileName” are part of its inheritance chain.
        The “AppName” mixin acts on the “appname” class keyword, and the
        “FileName” mixin acts on the “filename” class keyword (furnishing
        many related class methods). 
    """
    
    def loads(self, loaded):
        """ Load nested namespaced dictionary data from a YAML-encoded string """
        self.tree = yaml.load(loaded)
    
    def dumps(self):
        """ Dump a YAML-encoded string from nested namespaced dictionary data """
        return yaml.dump(self.tree, **options)

yaml_appname  = PROJECT_NAME
yaml_filename = f'{PROJECT_NAME}-config.yaml'

@export
class YamlFile(YamlFileBase, appname=yaml_appname,
                            filename=yaml_filename):
    
    """ A representation of a YAML file’s data as a NamespacedMutableMapping.
        
        This class is specifically germane to the CLU project – note
        that the “appname” and “filename” class keywords are used to
        assign values that are CLU-specific.
        
        CLU users who wish to use YAML files as NamespacedMutableMappings
        in their own projects should create a subclass of YamlFileBase of
        their own. Like this one, it needs to assign both the “appname”
        and the “filename” class keywords; it is unnecessary (but OK!) to
        define further methods, properties, class constants, and whatnot.
    """
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
