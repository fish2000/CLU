# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os

def boilerplate_copy_command(): # pragma: no cover
    """ Actually execute the copy-to-clipboard operation """
    try:
        import xerox
    except (ImportError, ModuleNotFoundError) as exc:
        print("ERROR: This command requires the “xerox” module.")
        print("ERROR: Install “xerox” into your Python enviroment to use it!")
        sys.exit(os.EX_CONFIG)
    
    from clu.repl.cli import boilerplate
    return boilerplate.boilerplate_command(function=xerox.copy)

if __name__ == '__main__':
    print("Copying boilerplate to clipboard…")
    out = boilerplate_copy_command()
    if out == os.EX_OK:
        print("Boilerplate copied successfully")
    else:
        raise OSError(f"bad return value: {out}")
    sys.exit(out)