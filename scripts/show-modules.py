# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import importlib
import pickle

from clu.constants.data import MODNAMES
from clu.exporting import Exporter
from clu.naming import nameof, moduleof
from clu.constants import consts
from clu.repl import ansi
from ansicolors import (green, red, lightred, cyan, dimcyan,
                        lightcyan, dimlightcyan, gray, dimgray,
                        yellow, blue, lightblue,
                        green_bg, cyan_bg, yellow_bg, nothing)

# socking them all in a tuple gets PyFlakes to shut up:
colors = (green, red, lightred, cyan, dimcyan,
          lightcyan, dimlightcyan, gray, dimgray,
          yellow, blue, lightblue,
          green_bg, cyan_bg, yellow_bg, nothing)

chevron = red.render("»")
colon = gray.render(":")

def printout(name, value):
    """ Format and colorize each segment of the name/value output """
    itemname = lightblue.render(" %25s " % name)
    itemvalue = gray.render(f" {value}")
    ansi.print_ansi(chevron + itemname + colon + itemvalue, color=nothing)

def import_clu_modules(modnames=MODNAMES):
    """ Import all exporter-equipped CLU modules. """
    modules = {}
    
    for modname in modnames:
        module = importlib.import_module(modname)
        if type(getattr(module, 'exporter', None)).__name__ == 'Exporter':
            modules[modname] = module
    
    return modules

Mismatch = NamedTuple('Mismatch', ('which',
                                   'determine',
                                   'modulename',
                                   'thingname',
                                   'idx'), module=__file__)

Results = NamedTuple('Results', ('total',
                                 'modulenames',
                                 'mismatches',
                                 'failure_rate'), module=__file__)

def compare_module_lookups_for_all_things():
    """ Iterate through each exported item, for each exported module,
        and look up the original module of the exported item with both:
            
            1) “pickle.whichmodule(…)” and
            2) “clu.naming.moduleof(…)”
        
        … comparing the results of the two search functions and computing
        the overall results.
    """
    total = 0
    mismatch_count = 0
    mismatches = []
    clumodules = import_clu_modules()
    modulenames = Exporter.modulenames()
    
    assert len(clumodules) == len(modulenames) <= len(MODNAMES)
    
    for modulename in modulenames:
        exports = Exporter[modulename].exports()
        total += len(exports)
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
    
    # In practice the failure rate seemed to be around 7.65 %
    failure_rate = 100 * (float(mismatch_count) / float(total))
    # assert failure_rate < 8.0 # percent
    
    return Results(total, modulenames, mismatches, failure_rate)


def show():
    """ Prettyprint the module lookup results """    
    # Terminal width:
    WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 125) \
                                 or consts.SEPARATOR_WIDTH
    
    results = compare_module_lookups_for_all_things()
    
    header = f'MODULE LOOKUPS ({results.total} performed)'
    footer0 = f'MISMATCHES: {len(results.mismatches)} (of {results.total} total)'
    footer1 = f'FAILURE RATE: {results.failure_rate}'
    
    ansi.print_ansi('–' * WIDTH,        color=gray)
    ansi.print_ansi_centered(header,    color=yellow)
    print()
    
    for mismatch in results.mismatches:
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