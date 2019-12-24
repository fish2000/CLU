# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os

from clu.repl.cli.boilerplate import boilerplate_command

def boilerplate_copy_command():
    import xerox
    return boilerplate_command(function=xerox.copy)

if __name__ == '__main__':
    print("Copying boilerplate to clipboard…")
    out = boilerplate_copy_command()
    if out == os.EX_OK:
        print("Boilerplate copied successfully")
    else:
        raise OSError(f"bad return value: {out}")
    sys.exit(out)
