# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.exceptions import ExecutionError
from clu.fs.filesystem import Directory, which, back_tick
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

git = which('git')

GIT_STATUS = f'{git} status'
GIT_TAGS = f'{git} describe --tags'

@export
def are_we_gitted(directory=None):
    """ Check if we’re in a Git repo """
    with Directory(pth=directory):
        try:
            back_tick(GIT_STATUS)
        except ExecutionError:
            return False
        else:
            return True

@export
def git_version_tags(directory=None):
    """ Get the Git version tags """
    if not are_we_gitted(directory=directory):
        return None
    with Directory(pth=directory):
        try:
            return back_tick(GIT_TAGS)
        except ExecutionError:
            return None

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.fs.filesystem import td
    from clu.version import version_info
    
    @inline
    def test_one():
        """ Check if we’re in a Git repo """
        assert are_we_gitted()
        assert not are_we_gitted(directory=td())
    
    @inline
    def test_two():
        """ Get the Git version tags """
        version = version_info.to_string()
        
        vtags0 = git_version_tags()
        assert vtags0 is not None
        assert vtags0.startswith(f'v{version}')
        
        vtags1 = git_version_tags(directory=td())
        assert vtags1 is None
        
        return vtags0
    
    inline.test(10)

if __name__ == '__main__':
    test()