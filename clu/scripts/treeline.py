# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import collections.abc
import contextlib
import sys

from clu.naming import qualified_name, nameof
from clu.predicates import typeof, isnormative
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

"""
TREELINE – tree ± command-line

• Turn a command like this:

    $ clu-command WRITE --key0=yo --key1=dogg \
                        --key2=i_heard ns0 \
                        --key3=you_like ns1 ns2 --key4=tree --key5=structures

• … into a tree of nodes! In order to eventually make it
    into a “clu.config.keymap.Flat” instance like this:

    {
        "key0"              : "yo",
        "key1"              : "dogg",
        "key2"              : "i_heard",
        "ns0:key3"          : "you_like",
        "ns0:ns1:ns2:key4"  : "tree",
        "ns0:ns1:ns2:key5"  : "structures"
    }

"""

command = "clu-command WRITE " \
          "--key0=yo --key1=dogg --key2=i_heard ns0 " \
          "--key3=you_like ns1 ns2 " \
          "--key4=tree --key5=structures"

executable, action, *nsflags = command.split(" ")

class Level(contextlib.AbstractContextManager,
            metaclass=clu.abstract.Slotted):
    
    """ A context manager to babysit indent levels. """
    
    slots = ('level', 'tab')
    
    def __init__(self, initial_value=0, tab="    "):
        self.level = initial_value
        self.tab = tab
    
    def indent(self, string):
        return self.level * self.tab + string
    
    def __enter__(self):
        self.level += 1
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        # N.B. return False to throw, True to supress
        self.level -= 1
        return exc_type is None
    

class NodeBase(collections.abc.Hashable,
               metaclass=clu.abstract.Slotted):
    
    __slots__ = ('node_parent', 'node_name', 'node_value', 'child_nodes')
    
    def __new__(cls, parent, name, *children, value=None):
        
        try:
            instance = super().__new__(cls, parent, name, *children, value=value) # type: ignore
        except TypeError:
            instance = super().__new__(cls)
        
        instance.node_parent = parent
        instance.node_name = str(name)
        instance.node_value = value
        instance.child_nodes = list()
        
        if children:
            self._append_nodes(*children)
        
        return instance
    
    @property
    def name(self):
        return self.node_name
    
    @property
    def value(self):
        return self.node_value
    
    # @value.setter
    # def value(self, assignee):
    #     self.node_value = assignee
    
    def is_leafnode(self):
        return bool(len(self.child_nodes))
    
    def _append_nodes(self, *children):
        for child in children:
            if type(self) not in type(child).__mro__:
                badtype = nameof(typeof(child))
                raise ValueError(f"Children must be Node types, not {badtype}")
            if child in self.child_nodes:
                raise ValueError(f"WTF: Node “{child!s}” is already a child")
            self.child_nodes.append(child)
    
    def add_child(self, name, value=None):
        self._append_nodes(type(self)(parent=self, name=name, value=value))
    
    def __len__(self):
        return len(self.child_nodes)
    
    def __iter__(self):
        yield from self.child_nodes
    
    def __getitem__(self, idx):
        if isinstance(idx, (int, slice)):
            return self.child_nodes[idx]
        elif isnormative(idx):
            strkey = str(idx)
            for child in self.child_nodes:
                if strkey == str(child):
                    return child
            raise KeyError(strkey)
        thistype = nameof(typeof(self))
        badtype = nameof(typeof(idx))
        raise TypeError(f"{thistype} indices must be integers or slices, not {badtype}")
    
    def __hash__(self):
        # So nice it’s twice!
        return hash(self.name) & hash(self.name) & hash(id(self))
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        child_count = len(self.child_nodes)
        out = f"Node({self.node_name})"
        if self.node_value:
            valuetype = qualified_name(typeof(self.node_value))
            out += f" = “{self.node_value}” ({valuetype})"
        if child_count:
            out += f" → [{child_count}]"
        return out

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    @inline.precheck
    def show_command_details():
        print(f"EXECUTABLE: {executable}")
        print(f"ACTION: {action}")
        print("NAMESPACED FLAGS:")
        pprint(nsflags, indent=4)
    
    @inline
    def test_nodebase_basics():
        emptynode = NodeBase(parent=None, name='yo')
        print("EMPTY NODE: {emptynode!s}")
        print(repr(emptynode))
        print()
        
        datanode = NodeBase(parent=None, name='dogg', value="ALL_TYPES_OF_SHIT")
        print("DATA NODE: {datanode!s}")
        print(repr(datanode))
        print()
        
        emptynode.add_child('i_heard', value="you like")
        emptynode._append_nodes(datanode)
        
        print("EMPTY NODE REDUX: {emptynode!s}")
        print(repr(emptynode))
        print()
        
        assert emptynode[0].name == "i_heard"
        assert emptynode[0].value == "you like"
        assert emptynode['i_heard'].name == "i_heard"       # SLOW
        assert emptynode['i_heard'].value == "you like"     # SLOW
        assert emptynode[1].name == "dogg"
        assert emptynode[1].value == "ALL_TYPES_OF_SHIT"
    
    @inline
    def test_nodebase_repr():
        root = NodeBase(parent=None, name='root')
        root.add_child('yo')
        root.add_child('dogg')
        root.add_child('i_heard')
        root.add_child('you_like')
        
        nsX = NodeBase(parent=root, name="ns0")
        nsY = NodeBase(parent=root, name="ns1")
        root._append_nodes(nsX, nsY)
        
        nsX.add_child('namespaced')
        nsY.add_child('commands')
        
        # level = Level()
        
        def node_repr(node):
            if not node.value:
                return f"• {node!s}"
            return f"• {node!s} = {node.value}"
        
        def tree_repr(root_node, level):
            with level:
                yield level.indent(node_repr(root_node))
                for node in root_node:
                    yield from tree_repr(node, level)
        
        for line in tree_repr(root, Level()):
            print(line)
    
        print()
    
    #@inline.diagnostic
    def show_me_some_values():
        pass # INSERT DIAGNOSTIC CODE HERE
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
