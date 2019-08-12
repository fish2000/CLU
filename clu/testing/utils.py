# -*- coding: utf-8 -*-
from __future__ import print_function

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
