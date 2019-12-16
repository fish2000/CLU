#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import pickle

from clu.all import import_all_modules
from clu.constants import consts
from clu.exporting import Exporter
from clu.naming import nameof, moduleof
from clu.repl import ansi
from clu.repl.columnize import columnize
from ansicolors import (green, lightgreen, red, lightred,
                        cyan, dimcyan, lightcyan, dimlightcyan,
                        gray, dimgray,
                        yellow, blue, lightblue, brightblue,
                        green_bg, cyan_bg, yellow_bg, nothing)

# socking them all in a tuple gets PyFlakes to shut up:
colors = (green, lightgreen, red, lightred,
          cyan, dimcyan, lightcyan, dimlightcyan,
          gray, dimgray,
          yellow, blue, lightblue, brightblue,
          green_bg, cyan_bg, yellow_bg, nothing)

chevron = red.render("»")
ronchev = gray.render("»")
colon = gray.render(":")

def printout(name, value):
    """ Format and colorize each segment of the name/value output """
    itemname = brightblue.render(" %25s " % name)
    itemvalue = gray.render(f" {value}")
    ansi.print_ansi(chevron + itemname + colon + itemvalue, color=nothing)

Mismatch = NamedTuple('Mismatch', ('which',
                                   'determine',
                                   'modulename',
                                   'thingname',
                                   'idx'))

Mismatches = NamedTuple('Mismatches', ('total',
                                       'mismatch_records',
                                       'failure_rate'))

Result = NamedTuple('Result', ('modulename',
                               'thingnames',
                               'idx'))

Results = NamedTuple('Results', ('total',
                                 'modulenames',
                                 'result_records'))

def compare_module_lookups_for_all_things():
    """ Iterate through each exported item, for each exported module,
        and look up the original module of the exported item with both:
            
            1) “pickle.whichmodule(…)” and
            2) “clu.naming.moduleof(…)”
        
        … comparing the results of the two search functions and computing
        the overall results.
    """
    idx = 0
    total = 0
    mismatch_count = 0
    mismatches = []
    results = []
    clumodules = import_all_modules(consts.BASEPATH,
                                    consts.PROJECT_NAME)
    modulenames = Exporter.modulenames()
    
    assert len(clumodules) <= len(modulenames)
    
    for modulename in modulenames:
        exports = Exporter[modulename].exports()
        total += len(exports)
        results.append(Result(modulename, tuple(exports.keys()), idx))
        for name, thing in exports.items():
            whichmodule = pickle.whichmodule(thing, None)
            determination = moduleof(thing)
            try:
                assert determination == whichmodule
            except AssertionError:
                mismatches.append(Mismatch(whichmodule,
                                           determination,
                                           modulename,
                                           nameof(thing),
                                           mismatch_count))
                mismatch_count += 1
            idx += 1
    
    # In practice the failure rate seemed to be around 7.65 %
    failure_rate = 100 * (float(mismatch_count) / float(total))
    # assert failure_rate < 8.0 # percent
    
    return Results(idx, modulenames, tuple(results)), \
           Mismatches(total,         tuple(mismatches),
                                           failure_rate)

isplural = lambda integer: integer != 1 and 's' or ''

def show():
    """ Prettyprint the module lookup results """
    # Terminal width:
    WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 125) \
                                 or consts.SEPARATOR_WIDTH
    
    results, mismatches = compare_module_lookups_for_all_things()
    
    header0 = f'MODULE LOOKUPS ({results.total} performed)'
    header1 = f'MISMATCHES FOUND (of {mismatches.total} total)'
    footer0 = f'MISMATCHES: {len(mismatches.mismatch_records)} (of {mismatches.total} total)'
    footer1 = f'FAILURE RATE: {mismatches.failure_rate}'
    
    ansi.print_ansi('–' * WIDTH,         color=gray)
    ansi.print_ansi_centered(header0,    color=yellow)
    print()
    
    # lineprefix=f"{ronchev}    "
    for result in results.result_records:
        thinglength = len(result.thingnames)
        columns = columnize(result.thingnames, displaywidth=WIDTH)
        printout(f"{result.modulename}",
                 f"{thinglength} exported thing{isplural(thinglength)}")
        print()
        ansi.print_ansi(columns,         color=green)
        print()
    
    ansi.print_ansi_centered(header1,    color=yellow)
    print()
    
    for mismatch in mismatches.mismatch_records:
        idx = f"{mismatch.idx}"
        
        printout(f"{mismatch.thingname} [{idx.zfill(2)}]",
                 f"{mismatch.which} ≠ {mismatch.determine}")
    
    print()
    ansi.print_ansi_centered(footer0,   color=cyan)
    ansi.print_ansi_centered(footer1,   color=cyan)
    ansi.print_ansi('–' * WIDTH,        color=gray)

def main():
    """ Main CLI entry point """
    if consts.TEXTMATE:
        # # Textmate: delegate to “consts.print_all()”:
        # consts.print_all()
        print()
        print("NO TEXTMATE VERSION AT THIS TIME SO SORRY COME BACK ANYTIME")
        print()
    else:
        # Show ’em and weep:
        show()
        if consts.DEBUG:
            print()
            print(f"")

if __name__ == '__main__':
    main()