#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.version import version_info as version
import sys

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
sys.exit(0)