# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.exceptions import ExecutionError
from clu.fs.filesystem import Directory, back_tick, td
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def are_we_gitted(directory=None):
    with Directory(pth=directory):
        try:
            back_tick('git status')
        except ExecutionError:
            return False
        else:
            return True

@export
def git_version_tags(directory=None):
    if are_we_gitted(directory=directory):
        return back_tick('git describe --tags')
    return None

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        """ Check if we’re in a Git repo """
        assert are_we_gitted()
        assert not are_we_gitted(directory=td())
    
    @inline
    def test_two():
        """ Get the Git version tags """
        vtags0 = git_version_tags()
        assert vtags0 is not None
        assert vtags0.startswith('v')
        
        vtags1 = git_version_tags(directory=td())
        assert vtags1 is None
        
        return vtags0
    
    inline.test(10)

if __name__ == '__main__':
    test()