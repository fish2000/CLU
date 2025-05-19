#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import shlex

def actually_print_ansidocs(dotpath):
    from clu.naming import qualified_import
    from clu.repl.ansi import DocFormat
    from importlib import import_module
    
    # Attempt to import it:
    try:
        thing = qualified_import(dotpath)
    except ValueError:
        thing = import_module(dotpath)
    
    ansidocs = DocFormat()
    ansidocs(thing)

def ansidocs_command():
    """ Print out the ANSI-ified docstring for the given thing"""
    from clu.scripts.treeline import RootNode, NodeTreeMap
    
    command = " ".join(sys.argv)
    executable, *dotpaths = shlex.split(command)
    root = RootNode.populate(*dotpaths)
    nodemap = NodeTreeMap(tree=root)
    
    namespaces = tuple(nodemap.namespaces())
    items = tuple(nodemap.items())
    
    print(f"NAMESPACES: {namespaces}")
    print(f"NODEMAP THINGS: {items}")
    
    # Return nice-nice for my POSI(X)ES:
    return os.EX_OK

if __name__ == '__main__':
    sys.argv.append('clu.exporting.Exporter')
    sys.argv.append('clu.repl.ansi.Text')
    sys.exit(ansidocs_command())