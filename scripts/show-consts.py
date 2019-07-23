# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from clu.constants import consts
from clu.repl import ansi
    
# ANSI colors:
green       = ansi.ANSIFormat(text=ansi.Text.GREEN)

red         = ansi.ANSIFormat(text=ansi.Text.RED)
lightred    = ansi.ANSIFormat(text=ansi.Text.LIGHTRED)

cyan        = ansi.ANSIFormat(text=ansi.Text.CYAN)
dimcyan     = ansi.ANSIFormat(text=ansi.Text.CYAN,
                              weight=ansi.Weight.DIM)
lightcyan   = ansi.ANSIFormat(text=ansi.Text.LIGHTCYAN)
dimlightcyan = ansi.ANSIFormat(text=ansi.Text.LIGHTCYAN,
                              weight=ansi.Weight.DIM)

gray        = ansi.ANSIFormat(text=ansi.Text.GRAY)
dimgray     = ansi.ANSIFormat(text=ansi.Text.GRAY,
                              weight=ansi.Weight.DIM)

yellow      = ansi.ANSIFormat(text=ansi.Text.YELLOW)
blue        = ansi.ANSIFormat(text=ansi.Text.BLUE)
lightblue   = ansi.ANSIFormat(text=ansi.Text.LIGHTBLUE)


green_bg    = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.GREEN,
                              weight=ansi.Weight.DIM)
cyan_bg     = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.CYAN,
                              weight=ansi.Weight.DIM)
yellow_bg   = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.YELLOW,
                              weight=ansi.Weight.DIM)

nothing     = ansi.ANSIFormat()

# Printout lambda:
printmono = lambda name, value: ansi.print_ansi("» %25s : %s" % (name, value),
                                                 color=cyan)

chevron = red.render("»")
colon = gray.render(":")

def printout(name, value):
    """ Format and colorize each segment of the name/value output """
    itemname = lightblue.render(" %25s " % name)
    itemvalue = gray.render(f" {value}")
    ansi.print_ansi(chevron + itemname + colon + itemvalue, color=nothing)

def show():
    """ Print out all of the constant variables defined in consts.py,
        only nice-looking, and with ANSI
    """
    from clu.naming import nameof
    
    # Terminal width:
    WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 125) \
                                 or consts.SEPARATOR_WIDTH
    
    # Header:
    # count = f'{len(consts.__all__)} defined'
    header = f'CONSTS ({len(consts.__all__)} defined)'
    footer = f'Module: {nameof(consts)}'
    
    # ansi.print_ansi('≠' * WIDTH,        color=yellow_bg)
    # ansi.print_ansi_centered('CONSTS:', color=gray)
    # ansi.print_ansi('≠' * WIDTH,        color=dimgray)
    # ansi.print_ansi_centered(count,     color=gray)
    # ansi.print_ansi('≠' * WIDTH,        color=dimgray)
    # ansi.print_ansi_centered(count,     color=gray)
    # ansi.print_ansi('≠' * WIDTH,        color=gray)
    ansi.print_ansi('–' * WIDTH,        color=gray)
    ansi.print_ansi_centered(header,    color=yellow)
    print()
    
    G = vars(consts)
    SEP = ",\n" + (" " * 30)
    
    for const_name in consts.__all__:
        if const_name.endswith('PATH') and os.pathsep in G[const_name]:
            printout(const_name, G[const_name].replace(os.pathsep, SEP))
        elif type(G[const_name]) is tuple:
            printout(const_name, SEP.join(f"“{g!s}”" for g in G[const_name]))
        elif type(G[const_name]) is str:
            printout(const_name, f"“{G[const_name]}”")
        else:
            printout(const_name, G[const_name])
    
    print()
    ansi.print_ansi_centered(footer,    color=cyan)
    ansi.print_ansi('–' * WIDTH,        color=gray)

def main():
    """ Main CLI entry point """
    if consts.TEXTMATE:
        # Textmate: delegate to “consts.print_all()”:
        consts.print_all()
    else:
        # Show ’em and weep:
        show()

if __name__ == '__main__':
    main()
