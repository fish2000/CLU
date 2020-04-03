# -*- coding: utf-8 -*-
from __future__ import print_function # pragma: no cover
import sys                            # pragma: no cover

if __name__ == '__main__':
    from clu.repl.cli.print_version import print_version_command
    sys.exit(print_version_command())