# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import sys

from clu.constants import consts
from clu.constants.data import banners
from clu.repl import ansi
from clu.stdio import std
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# Determine if we’re on PyPy and/or Python 3:
prefix = consts.PYPY and 'pypy' or 'python'

# Configure ANSI-color python banner, per python version:
if consts.PY3:
    banner = banners.get(f'{prefix}3.{sys.version_info.minor}', banners[f'{prefix}3.x'])
    banner_color = ansi.Text.CYAN
else:
    banner = banners[f'{prefix}2.7']
    banner_color = ansi.Text.LIGHTGREEN

now = datetime.datetime.now
python2_expires = 'January 1st, 2020'
is_python2_dead = now() >= now().strptime(python2_expires, '%B %dst, %Y') and ['YES'] or []

@export
def print_python_banner(text, color,
                              reset=ansi.ANSIFormat.RESET_ALL,
                               file=std.OUT):
    for line in text.splitlines():
        print(color + line, sep='', file=file)
    print(reset, end='', file=file)

@export
def print_warning(text, color=ansi.Text.RED,
                        reset=ansi.ANSIFormat.RESET_ALL,
                         file=std.OUT):
    print(color + text, sep='', file=file)
    print(reset, end='', file=file)

@export
def print_banner():
    # If we’re running in TextMate, use `sys.stderr` instead of ANSI colors,
    # as that’s the only way to get any sort of colored output in TextMate’s
    # console output window:
    if consts.TEXTMATE:
        print(banner, file=std.ERR)
    
    else:
        print_python_banner(banner, banner_color)
    
    if consts.DEBUG:
        ansi.print_ansi_centered("DEBUG MODE INITIATED",
                                 color=(consts.TEXTMATE and ansi.Text.NOTHING \
                                                         or ansi.Text.LIGHTYELLOW_EX))
        print()
    
    if not consts.PY3:
        
        if is_python2_dead:
            warning = u"∞§• ¡LOOK OUT! Python 2.x has been officially declared DEAD!!!!!!!\n"
        else:
            warning = u"∞§• ¡BEWARE! Python 2.x will perish when the clock strikes 2020!!!\n"
        
        if consts.TEXTMATE:
            print(warning, file=std.ERR)
        else:
            print_warning(warning)
            ansi.flush_all()

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

if __name__ == '__main__':
    print_banner()