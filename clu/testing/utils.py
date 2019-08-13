# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def countfiles(target, suffix=None):
    """ Return a count of all files in the target directory,
        including those found in all subdirectories.
        
        Optionally pass a “suffix” argument to only count files
        matching a specific suffix.
    """
    from clu.fs.misc import suffix_searcher
    count = 0
    searcher = suffix_searcher(suffix)
    for root, dirs, files in target.walk():
        count += len(tuple(filter(searcher, files)))
    return count

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()