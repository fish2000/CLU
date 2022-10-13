#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import shlex
import sys, os

from pprint import pprint

from clu.scripts import treeline
from clu.predicates import listify
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

valid_actions = { 'read', 'write', 'status', 'nop' }

def get_dict():
    """ Retrieve a copy of the database for this file """
    with exporter.data() as database:
        out = dict(database.get('tree', {}))
    return out

def update_dict(updates):
    """ Update the files’ database from a new dictionary """
    with exporter.data() as database:
        if 'tree' not in database:
            database['tree'] = {}
        database['tree'].update(updates)
        out = dict(database.get('tree', {}))
    return out

def get_command_history():
    """ Retrieve a copy of the command history for this file """
    with exporter.data() as database:
        out = listify(database.get('history', []))
    return out

def push_command(command):
    """ Add a new command to the end of the files’ command history """
    with exporter.data() as database:
        if 'history' not in database:
            database['history'] = []
        database['history'].append(command)
        out = listify(database.get('history', []))
    return out

def _initialize():
    """ Set up the database with empty entries for the command tree
        and the history stack. Only call this once: when running
        the script for the first time!!
    """
    with exporter.data() as database:
        database['tree'] = {}
        database['history'] = []
        out = dict(database)
    return out

def split_arguments(argv=None):
    """ Return the script arguments, in the form:
        
        >>> executable, action, *nsflags = shlex.split(command)
    """
    if not argv:
        argv = sys.argv
    return argv

def join_arguments(argv=None):
    """ Return the script arguments, joined as a single string """
    if not argv:
        argv = sys.argv
    return shlex.join(argv)

def flags_to_nodetreemap(*flags):
    """ Parse script flag arguments into a node tree, and store
        them in a new NodeTreeMap instance
    """
    root = treeline.RootNode()
    root.populate_with_arguments(*flags)
    return treeline.NodeTreeMap(tree=root)

def main(argv=None):
    """ The primary script entry point """
    # Default to `sys.argv` if we’re called without any
    # arguments specified:
    if not argv:
        argv = sys.argv
    
    # Ensure the argument vector is long enough:
    if len(argv) < 2:
        argv.append('NOP')
    
    # Initialize, if necessary:
    # _initialize()
    
    # Deal with the command:
    command = join_arguments(argv=argv)
    executable, action, *nsflags = split_arguments(argv=argv)
    ntm = flags_to_nodetreemap(*nsflags)
    
    # Print current command:
    print("THIS COMMAND:")
    print(command)
    print()
    
    # Print parsed command dict:
    for line in treeline.tree_repr(ntm.tree, treeline.Level()):
        print(line)
    print()
    
    if action.casefold() not in valid_actions:
        actions = ", ".join(sorted(map(lambda term: term.upper(), valid_actions)))
        print(f"¶ INVALID ACTION: “{action}”")
        print(f"¶ MUST BE ONE OF: «{actions}»")
        return os.EX_CONFIG
    
    action = action.casefold()
    if action == 'write':
        # Update the dict:
        print("… UPDATING DICTIONARY FROM WRITE COMMAND")
        update_dict(ntm)
    elif action == 'read':
        # Ensure we have keys to read:
        if len(ntm.keys()) < 1:
            print("¶ NO KEYS SPECIFIED FOR READ COMMAND")
            return os.EX_CONFIG
        # Print specified keys:
        nskeys = ", ".join(ntm.keys())
        print(f"… READING NAMESPACED DICTIONARY KEYS: «{nskeys}»")
        printout = lambda name, value: print("» %25s : %s" % (name, value))
        for nskey in ntm.keys():
            printout(nskey, ntm[nskey] or '«NONE»')
    elif action == 'status':
        # Do something status-y:
        pass
    elif action == 'nop':
        # Do nothing:
        pass
    
    print()
    
    # Update the command history:
    push_command(command)
    
    # Print the last ten lines of command history:
    history = get_command_history()
    length = len(history)
    lastlength = (length >= 10) and 'TEN' or f'{length}'
    startat = (length >= 10) and (length - 9) or 0
    print(f"COMMAND HISTORY (LAST {lastlength} LINES, OF {length} TOTAL):")
    for idx, line in enumerate(history[-10:]):
        print(f"• {idx + startat} {line}")
    print()
    
    # Print current dict:
    print("CURRENT DICTIONARY:")
    pprint(get_dict())
    print()
    
    # Exit cleanly:
    return os.EX_OK

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

test_command = "clu-command READ " \
               "--key0 --key1 --key2 ns0 " \
               "--key3 ns1 ns2 " \
               "--key4 --key5"

test_command = "clu-command WRITE " \
               "--key0=yo --key1=dogg --key2=i_heard ns0 " \
               "--key3=you_like ns1 ns2 " \
               "--key4=tree --key5=structures"

# test_command = "clu-command STATUS"
# test_command = "clu-command FAIL"

if __name__ == '__main__':
    # sys.exit(main(shlex.split(test_command)))
    sys.exit(main(sys.argv))
