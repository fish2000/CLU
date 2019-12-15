#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

def print_version_command():
    """ Print a simple string with CLU’s current semantic version tag """
    from clu.constants import consts
    from clu.version import version_info, VersionInfo
    from clu.version.git_version import git_version_tags
    
    version = VersionInfo(git_version_tags(consts.BASEPATH) or version_info)
    semantic = f"{version.major}.{version.minor}.{version.patch}"
    
    if version.pre:
        semantic += f"-{version.pre}"
        if version.build:
            semantic += f"+{version.build}"
        semantic += " [SNAPSHOT]"
    else:
        semantic += " [release]"
    
    copyright = f"CLU version {semantic} © 2010-2032 Alexander Böhn"
    
    print(copyright)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(print_version_command())