# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def append_paths(*putatives):
    """ Mutate `sys.path` by appending one or more new paths -- all of which
        are checked for both nonexistence and presence within the existing
        `sys.path` list via inode lookup, and which those failing such checks
        are summarily excluded.
    """
    out = {}
    if len(putatives) < 1:
        return out
    paths = frozenset(sys.path)
    append_paths.oldsyspath.append(tuple(sys.path))
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
        sys.path.append(pth)
        out[pth] = True
        continue
    return out

append_paths.oldpaths = [tuple(sys.path)]

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
    sys.path = list(paths)
    return out

remove_paths.oldpaths = [tuple(sys.path)]

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
