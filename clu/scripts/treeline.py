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

SPACETABS = " " * 2

@export
class Level(contextlib.AbstractContextManager,
            metaclass=clu.abstract.Slotted):
    
    """ A context manager to babysit indent levels. """
    
    slots = ('value', 'tab')
    
    def __init__(self, initial_value=0, tab=SPACETABS):
        self.value = initial_value
        self.tab = tab
    
    def indent(self, string):
        return self.value * self.tab + string
    
    def __int__(self):
        return self.value
    
    def __enter__(self):
        self.value += 1
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        # N.B. return False to throw, True to supress
        self.value -= 1
        return exc_type is None

@export
class NodeBase(collections.abc.Hashable,
               metaclass=clu.abstract.Slotted):
    
    """ The base class for all tree nodes. """
    
    __slots__ = ('node_parent', 'node_name',
                                'node_value',
                 'child_nodes')
    
    def __new__(cls, parent, name, *children, value=None):
        
        try:
            instance = super().__new__(cls, parent,
                                            name,
                                           *children,
                                            value=value) # type: ignore
        except TypeError:
            instance = super().__new__(cls)
        
        instance.node_name = str(name)
        instance.node_value = value
        instance.node_parent = parent
        instance.child_nodes = {}
        
        if children:
            self._append_nodes(*children)
        
        return instance
    
    @property
    def name(self):
        return self.node_name
    
    @property
    def value(self):
        return self.is_leafnode() and self.node_value or None
    
    def is_leafnode(self):
        return not bool(len(self.child_nodes))
    
    def _append_nodes(self, *children):
        for child in children:
            if type(child) is RootNode:
                raise ValueError(f"Children must be standard nodes – not root nodes")
            if type(child) not in acceptable_types:
                badtype = nameof(typeof(child))
                raise ValueError(f"Children must be Node types, not {badtype}")
            if child in set(self.child_nodes.values()):
                thistype = nameof(typeof(self))
                raise ValueError(f"WTF: {thistype} “{child!s}” is already a child")
            self.child_nodes[child.name] = child
    
    def add_child(self, name, value=None):
        node = Node(parent=self, name=name, value=value)
        self._append_nodes(node)
        return node
    
    def get_child(self, key):
        return self.child_nodes[key]
    
    def leaf(self, leafname):
        node = self.get_child(leafname)
        if not node.is_leafnode():
            raise KeyError(leafname)
        return node
    
    def namespace(self, nsname):
        node = self.get_child(nsname)
        if node.is_leafnode():
            raise KeyError(nsname)
        return node
    
    def leaves(self):
        yield from filter(lambda node: node.is_leafnode(),
                          self.child_nodes.values())
    
    def namespaces(self):
        yield from filter(lambda node: not node.is_leafnode(),
                          self.child_nodes.values())
    
    def __len__(self):
        return len(self.child_nodes)
    
    def __iter__(self):
        yield from self.child_nodes.values()
    
    def __getitem__(self, idx):
        if isinstance(idx, (int, slice)):
            return tuple(self.child_nodes.values())[idx]
        elif isnormative(idx):
            return self.get_child(str(idx))
        thistype = nameof(typeof(self))
        badtype = nameof(typeof(idx))
        message = f"{thistype} indices must be integers, slices, or strings – not {badtype}"
        raise TypeError(message)
    
    def __hash__(self):
        # So nice it’s thrice!
        return hash(self.name) \
             & hash(self.name) \
             & hash(id(self))
    
    def __bool__(self):
        return True # ?!
    
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

class RootNode(NodeBase):
    
    """ A root node, anchoring a tree.
        
        There may only be one of these in a tree, and it must be
        the trees’ root node (like duh). When building up a tree
        from scratch, you instantiate a RootNode and use its methods
        to craft the tree in place. 
    """
    
    def __new__(cls, *children, name='root'):
        instance = super().__new__(cls, None,       # no parent
                                        name,       # if you insist
                                       *children,
                                        value=None) # value isn’t necessary
        return instance
    
    @property
    def value(self):
        """ A root node has no value, by definition """
        return None

class Node(NodeBase):
    
    """ A standard tree node. """
    
    def __new__(cls, parent, name, *children, value=None):
        
        if not parent:
            raise ValueError("Nodes require a valid parent node")
        
        instance = super().__new__(cls, parent,
                                        name,
                                       *children,
                                        value=value) # type: ignore
        return instance

# Used in RootNode._append_nodes(…):
acceptable_types = set(NodeBase.__mro__)
acceptable_types.add(Node)
acceptable_types.add(RootNode)

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
        """ Check some of the basic NodeBase functions """
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
    def test_nodebase_repr_simple():
        """ Test a tree of raw NodeBase instances """
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
        
        def node_repr(node):
            if not node.value:
                return f"• {node!s}"
            return f"• {node!s} = {node.value}"
        
        def tree_repr(node, level):
            with level:
                yield level.indent(node_repr(node))
                for child in node:
                    yield from tree_repr(child, level)
        
        for line in tree_repr(root, Level()):
            print(line)
    
        print()
    
    @inline
    def test_node_rootnode_repr_sorted():
        """ Test an anchored tree of Node instances """
        root = RootNode()
        root.add_child('yo')
        root.add_child('dogg')
        root.add_child('i_heard')
        root.add_child('you_like')
        
        nsX = Node(parent=root, name="ns0")
        nsY = Node(parent=root, name="ns1")
        root._append_nodes(nsX, nsY)
        
        nsX.add_child('namespaced')
        nsY.add_child('commands')
        
        def node_repr(node):
            if not node.value:
                return f"• {node!s}"
            return f"• {node!s} = {node.value}"
        
        def tree_repr(node, level):
            yield level.indent(node_repr(node))
            for leaf in node.leaves():
                with level:
                    yield level.indent(node_repr(leaf))
            for namespace in node.namespaces():
                with level:
                    yield from tree_repr(namespace, level)
        
        for line in tree_repr(root, Level()):
            print(line)
    
        print()
    
    @inline
    def test_parse_command_line():
        """ Transform a command into a node tree """
        
        # Create an empty tree:
        root = RootNode()
        
        def parse_argument_to_child_node(arg, parent):
            """ Function to parse an argument into its values,
                and then add a node with those corresponding values
                to a provided parent node – then returning this
                parent node (if we created a leaf) or our freshly
                created node (if we created a namespace).
                … this allows us to keep attaching stuff to whatever
                gets returned here, wherever we are in the process
                of parsing the command line
            """
            # Examine the argument:
            if arg.startswith('--'):
                if '=' in arg:
                    # It’s a leaf with a value specified:
                    name, value = arg.removeprefix('--').split('=')
                else:
                    # It’s a leaf with no value provided:
                    name, value = arg.removeprefix('--'), None
            else:
                # It’s a namespace:
                name, value = arg, None
            
            # Add and recover a new node, containing the values
            # we parsed out:
            node = parent.add_child(name=name, value=value)
            
            # Return the node if it’s a namespace, otherwise
            # hand back the original parent:
            return arg.startswith('--') and parent or node
        
        # Starting with the root node, go through the list of
        # namespaced argument flags and whatnot, parsing each
        # in turn, advancing the “node” in question to namespaces
        # as we encounter and create them:
        node = root
        for argument in nsflags:
            node = parse_argument_to_child_node(argument, parent=node)
        
        # The follwing tree-repr stuff is copied from the test function
        # “test_node_rootnode_repr_sorted()” above:
        def node_repr(node):
            if not node.is_leafnode():
                child_count = len(node)
                return f"• {node!s} → [{child_count}]"
            if not node.value:
                return f"• {node!s}"
            return f"• {node!s} = {node.value}"
    
        def tree_repr(node, level):
            yield level.indent(node_repr(node))
            for leaf in node.leaves():
                with level:
                    yield level.indent(node_repr(leaf))
            for namespace in node.namespaces():
                with level:
                    yield from tree_repr(namespace, level)
    
        for line in tree_repr(root, Level()):
            print(line)
        
        print()
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
