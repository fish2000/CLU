# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import site
import sys

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def add_paths(*putatives, prepend=False):
    """ Mutate `sys.path` by adding one or more new paths -- all of which
        are checked for both nonexistence and presence within the existing
        `sys.path` list via inode lookup, and which those failing such checks
        are summarily excluded.
        
        Paths are added to `sys.path` by appending, unless “add_paths(…)”
        is called with the keyword arg ‘prepend=True’.
    """
    out = {}
    if len(putatives) < 1:
        return out
    paths = frozenset(sys.path)
    add_paths.oldpaths.append(tuple(sys.path))
    for pth in (os.fspath(putative) for putative in putatives):
        if not os.path.exists(pth):
            out[pth] = False
            continue
        # if pth in paths:
        #     out[pth] = False
        #     continue
        for p in paths:
            if os.path.samefile(p, pth):
                out[pth] = False
                continue
        if prepend:
            sys.path.insert(0, pth)
        else:
            sys.path.append(pth)
        out[pth] = True
    return out

add_paths.oldpaths = []

def mutate_syspath(container):
    """ Remove paths from `sys.path` that don’t match the input. """
    from clu.predicates import isiterable
    if not isiterable(container):
        raise ValueError("iterable required")
    new_syspath = list()
    for path in sys.path:
        if path in container:
            new_syspath.append(path)
    sys.path = new_syspath
    return new_syspath

@export
def remove_paths(*putatives):
    """ Mutate `sys.path` by removing one or more existing paths --
        all of which are checked for presence within the existing `sys.path`
        list via inode lookup before being marked for removal, which that
        (the removal) is done atomically.
    """
    out = {}
    if len(putatives) < 1:
        return out
    removals = set()
    paths = set(sys.path)
    for pth in (os.fspath(putative) for putative in putatives):
        for p in paths:
            if os.path.samefile(p, pth):
                out[pth] = True
                removals |= { p }
                continue
        out[pth] = False
        continue
    paths -= removals
    remove_paths.oldpaths.append(tuple(sys.path))
    mutate_syspath(paths)
    return out

remove_paths.oldpaths = []

@export
def remove_invalid_paths():
    """ Mutate `sys.path` by removing any existing paths that don’t
        actually lead to a valid place somewhere on the filesystem
        (according to “os.path.exists(…)”). Path removal, as with
        “remove_paths(…)”, is done atomically.
    """
    site.removeduppaths()
    out = {}
    removals = set()
    paths = set(sys.path)
    for p in paths:
        if not os.path.exists(p):
            out[p] = True
            removals |= { p }
            continue
        out[p] = False
        continue
    paths -= removals
    remove_invalid_paths.oldpaths.append(tuple(sys.path))
    mutate_syspath(paths)
    return out

remove_invalid_paths.oldpaths = []

@export
def enhance(*putatives):
    """ Convenience function for calling “remove_invalid_paths(…)”
        before calling “add_paths(•putatives)”
    """
    remove_invalid_paths()          # cleans “sys.path”
    return add_paths(*putatives)    # extends “sys.path”

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
