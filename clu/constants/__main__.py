#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from clu.constants import consts
from clu.predicates import isiterable, isnormative
from clu.typology import isnumber, isbytes, ispath
from clu.repl import ansi
from clu.scripts import ansicolors as colors

chevron = colors.red.render("»")
colon = colors.gray.render(":")

def printout(name, value, most=25):
    """ Format and colorize each segment of the name/value output """
    itemname = colors.lightblue.render(f" {name} ".rjust(most+2))
    itemvalue = colors.gray.render(f" {value!s}")
    ansi.print_ansi(chevron + itemname + colon + itemvalue, color=colors.nothing)

def show():
    """ Print out all of the constant variables defined in consts.py,
        only nice-looking, and with ANSI
    """
    from clu.naming import qualified_name
    
    # Header + footer:
    length = len(consts.__all__)
    mdname = qualified_name(consts)
    header = f'CONSTS MODULE ({length} consts defined)'
    footer = f'Module: {mdname}'
    
    # Print header:
    ansi.print_ansi_centered(filler='–', color=colors.gray)
    ansi.print_ansi_centered(header,     color=colors.yellow)
    print()
    
    # Calculate the longest constant name,
    # used to align multi-line value outputs and name-value pairs:
    most = max(len(name) for name in consts.__all__)
    
    G = vars(consts)
    SEP = ",\n" + (" " * (most + 5))
    
    for const_name in consts.__all__:
        if isnormative(G[const_name]):
            if isbytes(G[const_name]):
                G[const_name] = str(G[const_name], encoding=consts.ENCODING)
            elif ispath(G[const_name]):
                G[const_name] = os.fspath(G[const_name])
            if const_name.endswith('PATH') and os.pathsep in G[const_name]:
                printout(const_name, G[const_name].replace(os.pathsep, SEP), most=most)
            else:
                printout(const_name, f"“{G[const_name]}”", most=most)
        elif isiterable(G[const_name]):
            printout(const_name, SEP.join(f"“{g!s}”" for g in G[const_name]), most=most)
        elif isnumber(G[const_name]):
            printout(const_name, f"«{G[const_name]!r}»", most=most)
        else:
            printout(const_name, G[const_name], most=most)
    
    # Print footer:
    print()
    ansi.print_ansi_centered(footer,     color=colors.cyan)
    ansi.print_ansi_centered(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    if consts.TEXTMATE:
        # Textmate: delegate to “consts.print_all()”:
        consts.print_all()
    else:
        # Show ’em and weep:
        show()
        if consts.DEBUG:
            print()
            print(f"")

if __name__ == '__main__':
    main()
