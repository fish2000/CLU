#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

if __name__ == '__main__':
    from clu.repl.cli.print_version import print_version_command
    import sys
    sys.exit(print_version_command())