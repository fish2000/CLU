# -*- coding: utf-8 -*-
from __future__ import print_function

# from clu.repl.modules import Mismatch, Mismatches, Result, Results
from clu.repl.modules import compare_module_lookups_for_all_things
from clu.repl.modules import isplural
from clu.repl.columnize import columnize
from clu.repl import ansi

from clu.scripts import ansicolors as colors

# chevron = colors.red.render("»")
# ronchev = colors.gray.render("»")
# colon = colors.gray.render(":")

# def printout(name, value, most=25):
#     """ Format and colorize each segment of the name/value output """
#     itemname = colors.brightblue.render(f" {name} ".rjust(most+2))
#     itemvalue = colors.gray.render(f" {value}")
#     ansi.print_ansi(chevron + itemname + colon + itemvalue, color=colors.nothing)

def show():
    """ Prettyprint the module lookup results """
    results, mismatches = compare_module_lookups_for_all_things()
    
    header0 = f'MODULE LOOKUPS ({results.total} performed)'
    header1 = f'MISMATCHES FOUND (of {mismatches.total} total)'
    footer0 = f'MISMATCHES: {len(mismatches.mismatch_records)} (of {mismatches.total} total)'
    footer1 = f'FAILURE RATE: {mismatches.failure_rate}'
    
    ansi.print_ansi_centered(filler='–', color=colors.gray)
    ansi.print_ansi_centered(header0,    color=colors.yellow)
    print()
    
    most = max(len(result.modulename) for result in results.result_records)
    
    for result in results.result_records:
        thinglength = len(result.thingnames)
        columns = columnize(result.thingnames)
        ansi.print_ansi_name_value(f"{result.modulename}",
                                   f"{thinglength} exported thing{isplural(thinglength)}", most=most)
        print()
        ansi.print_ansi(columns,         color=colors.green)
        print()
    
    ansi.print_ansi_centered(header1,    color=colors.yellow)
    print()
    
    for mismatch in mismatches.mismatch_records:
        idx = f"{mismatch.idx}"
        
        ansi.print_ansi_name_value(f"{mismatch.thingname} [{idx.zfill(2)}]",
                                   f"{mismatch.which} ≠ {mismatch.determine}", most=most)
    
    print()
    ansi.print_ansi_centered(footer0,    color=colors.cyan)
    ansi.print_ansi_centered(footer1,    color=colors.cyan)
    ansi.print_ansi_centered(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    from clu.constants import consts
    import os
    
    if consts.TEXTMATE:
        print()
        print("NO TEXTMATE VERSION AT THIS TIME SO SORRY COME BACK ANYTIME")
        print()
        return os.EX_IOERR
    
    else:
        # Show ’em and weep:
        show()
        if consts.DEBUG:
            print()
            print(f"")
    
    return os.EX_OK

if __name__ == '__main__':
    import sys
    sys.exit(main())