# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import collections.abc
import contextlib
import shlex
import sys

from itertools import filterfalse

from clu.config.abc import NamespaceWalker
from clu.config.keymap import articulate, FrozenNested
from clu.config.ns import get_ns_and_key, split_ns, unpack_ns, pack_ns
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

executable, action, *nsflags = shlex.split(command)

SPACETABS = " " * 2

@export
class Level(contextlib.AbstractContextManager,
            metaclass=clu.abstract.Slotted):
    
    """ A context manager to babysit indent levels. """
    
    __slots__ = ('value', 'tab')
    
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

# Boolean predicate to filter leafnodes:
leaf_predicate = lambda node: node.is_leafnode()

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
        """ The name of this node. """
        return self.node_name
    
    @property
    def nsname(self):
        """ The fully namespaced name of this node. Namespaces are enumerated
            from the root upward.
        """
        if self.is_rootnode():
            return self.node_name
        parent = self
        namespaces = []
        while True:
            parent = parent.node_parent
            if parent.is_rootnode():
                break
            namespaces.append(parent.node_name)
        if not namespaces:
            return self.node_name
        return pack_ns(self.node_name, *reversed(namespaces))
    
    @property
    def value(self):
        """ The value of this node. """
        return self.is_leafnode() and self.node_value or None
    
    def is_leafnode(self):
        """ Return True if this node is a leafnode, otherwise False. """
        return not bool(len(self.child_nodes))
    
    def is_rootnode(self):
        """ Return True if this node is a root node, otherwise False. """
        return False
    
    def _append_nodes(self, *children):
        """ Append some nodes as children to this node. """
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
        """ Add a child node to this node.
            
            Specify a name, and optionally a value for the node.
        """
        node = Node(parent=self, name=name, value=value)
        self._append_nodes(node)
        return node
    
    def has_child(self, nskey):
        """ Return True if a child exists for a (possibly namespaced) name,
            otherwise False.
        """
        key, namespaces = unpack_ns(nskey)
        node = self
        for namespace in namespaces:
            node = node.namespace(namespace)
        return key in node.child_nodes
    
    def get_child(self, nskey):
        """ Retrieve a child node of a (possibly namespaced) given name. """
        key, namespaces = unpack_ns(nskey)
        node = self
        for namespace in namespaces:
            node = node.namespace(namespace)
        return node.child_nodes[key]
    
    def assemble_subcommand(self, recursive=False):
        """ Reassemble the command-line string for a given node.
            
            Optionally, recurse through the child nodes, adding
            their values to the command-line string.
        """
        if self.is_leafnode():
            name, value = self.name, self.value
            if value is None:
                return f"--{name}"
            return f"--{name}={value!s}"
        iterable = recursive and self or self.leaves()
        assembler = lambda node: node.assemble_subcommand(recursive=recursive)
        nsflags = " ".join(map(assembler, iterable))
        return f"{self.name} {nsflags}"
    
    def leaf(self, leafname):
        """ Retrieve a child leafnode of a given name from this node. """
        node = self.child_nodes[leafname]
        if not node.is_leafnode():
            raise KeyError(leafname)
        return node
    
    def namespace(self, nsname):
        """ Retrieve a child namespace of a given name from this node. """
        node = self.child_nodes[nsname]
        if node.is_leafnode():
            raise KeyError(nsname)
        return node
    
    def leaves(self):
        """ Iterator over this nodes’ child leafnodes. """
        yield from filter(leaf_predicate, self.child_nodes.values())
    
    def namespaces(self):
        """ Iterator over this nodes’ child namespaces. """
        yield from filterfalse(leaf_predicate, self.child_nodes.values())
    
    def to_dict(self):
        return { 'name' : self.name,
                'value' : self.value,
               'parent' : self.node_parent.name }
    
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

@export
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
        """ A root node has no value, by definition. """
        return None
    
    def is_rootnode(self):
        return True
    
    @staticmethod
    def parse_argument_to_child(argument, parent):
        """ Static method for parsing an argument into its values,
            and adding a node with those corresponding values
            to a provided parent node – then returning this
            parent node (if we created a leaf) or our freshly
            created node (if we created a namespace).
            … this allows us to keep attaching stuff to whatever
            gets returned here, wherever we are in the process
            of parsing the command line.
        """
        # Examine the argument:
        if argument.startswith('--'):
            if '=' in argument:
                # It’s a leaf with a value specified:
                name, value = argument.removeprefix('--').split('=')
            else:
                # It’s a leaf with no value provided:
                name, value = argument.removeprefix('--'), None
        else:
            # It’s a namespace:
            name, value = argument, None
    
        # Add and recover a new node, containing the values
        # we parsed out:
        node = parent.add_child(name=name, value=value)
    
        # Return the node if it’s a namespace, otherwise
        # hand back the original parent:
        return argument.startswith('--') and parent or node
    
    def populate_with_arguments(self, *arguments):
        """ Populate the root node from a sequence of command-line arguments. """
        node = self
        for argument in arguments:
            node = self.parse_argument_to_child(argument, parent=node)

@export
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

@export
def node_repr(node):
    """ Print a pithy string representation of a node. """
    if not node.is_leafnode():
        child_count = len(node)
        return f"• {node!s} → [{child_count}]"
    if not node.value:
        return f"• {node!s}"
    return f"• {node!s} = {node.value}"

@export
def tree_repr(node, level):
    """ Recursively walk, stringify, and print a node tree. """
    yield level.indent(node_repr(node))
    for leaf in node.leaves():
        with level:
            yield level.indent(node_repr(leaf))
    for namespace in node.namespaces():
        with level:
            yield from tree_repr(namespace, level)

# NodeTreeMap – a NamespaceWalker-derived KeyMap hosting a node tree

@export
def treewalk(node, pre=None):
    """ Iteratively walk a node tree.
        
        Based on https://stackoverflow.com/a/12507546/298171
    """
    pre = pre and pre[:] or []
    if node.is_leafnode():
        yield pre + [node.name, node.value]
    elif node.is_rootnode():
        for child in node:
            yield from treewalk(child, pre)
    else:
        for child in node:
            yield from treewalk(child, pre + [node.name])

@export
class NodeTreeMap(NamespaceWalker, clu.abstract.ReprWrapper,
                                   clu.abstract.Cloneable):
    
    """ NodeTreeMap – a NamespaceWalker-derived KeyMap hosting a node tree """
    
    __slots__ = 'tree'
    
    @classmethod
    def from_dict(cls, instance_dict):
        """ Used by `clu.config.codecs` to deserialize NodeTreeMaps """
        # Create a new NodeTreeMap instance with an empty
        # node tree – and an interim FrozenNested instance
        # using the instance dict data:
        instance = cls(tree=RootNode())
        interim = FrozenNested.from_dict(instance_dict)
        
        # instance.update(interim)
        # Go through the namespaces, creating them within
        # the new instance as needed:
        for namespace in interim.namespaces():
            node = instance.tree
            for nsfragment in split_ns(namespace):
                try:
                    node = node.namespace(nsfragment)
                except KeyError:
                    node = node.add_child(nsfragment)
        
        # With namespaces in places, go through the items,
        # using the newly created namespaces to anchor
        # namespaced items as needed:
        for nskey, value in interim.items():
            ns, key = get_ns_and_key(nskey)
            if not ns:
                instance.tree.add_child(key, value)
            else:
                instance.tree.get_child(ns).add_child(key, value)
        
        # Return the new instance:
        return instance
    
    def __init__(self, tree=None, **updates):
        """ Initialize a NodeTreeMap, hosting a given node tree """
        try:
            super().__init__(**updates)
        except TypeError:
            super().__init__()
        if hasattr(tree, 'tree'):
            tree = getattr(tree, 'tree')
        # “mnq gvfc” – Nellie
        if tree is not None:
            if type(tree) not in acceptable_types:
                badtype = nameof(typeof(tree))
                raise TypeError(f"NodeTreeMap requires a Node instance, not type {badtype}")
        self.tree = tree
        # N.B. – deal with updates here
    
    def walk(self):
        yield from treewalk(self.tree)
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        pass
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the NodeTreeMap """
        # Using clu.config.keymap.articulate(…) to build the dict –
        # This sets up an instance dict matching a Nested KeyMap’s
        # internal layout:
        return articulate(self.tree, walker=treewalk)
    
    def __contains__(self, nskey):
        # Delegate to the root node of the internal node tree:
        return self.tree.has_child(nskey)
    
    def __getitem__(self, nskey):
        # Delegate to the root node of the internal node tree:
        return self.tree.get_child(nskey).value

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
        print(f"EMPTY NODE: {emptynode!s}")
        print(repr(emptynode))
        print()
        
        datanode = NodeBase(parent=None, name='dogg', value="ALL_TYPES_OF_SHIT")
        print(f"DATA NODE: {datanode!s}")
        print(repr(datanode))
        print()
        
        emptynode.add_child('i_heard', value="you like")
        emptynode._append_nodes(datanode)
        
        print(f"EMPTY NODE REDUX: {emptynode!s}")
        print(repr(emptynode))
        print()
        
        assert emptynode[0].name == "i_heard"
        assert emptynode[0].value == "you like"
        assert emptynode['i_heard'].name == "i_heard"
        assert emptynode['i_heard'].value == "you like"
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
    def test_rootnode_repr_sorted():
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
        
        for line in tree_repr(root, Level()):
            print(line)
        
        print()
    
    @inline
    def test_parse_command_line():
        """ Transform a command into a node tree """
        
        def parse_argument_to_child_node(arg, parent):
            """ Function to parse an argument into its values,
                and then add a node with those corresponding values
                to a provided parent node – then returning this
                parent node (if we created a leaf) or our freshly
                created node (if we created a namespace).
                … this allows us to keep attaching stuff to whatever
                gets returned here, wherever we are in the process
                of parsing the command line.
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
                
        # Create an empty tree:
        root = RootNode()
        
        # Starting with the root node, go through the list of
        # namespaced argument flags and whatnot, parsing each
        # in turn, advancing the “node” in question to namespaces
        # as we encounter and create them:
        node = root
        for argument in nsflags:
            node = parse_argument_to_child_node(argument, parent=node)
        
        for line in tree_repr(root, Level()):
            print(line)
        
        print()
    
    @inline
    def test_assemble_subcommand():
        """ Reassemble the model command-line invocation """
        
        # The root node is named for the model command:
        root = RootNode(name="WRITE")
        
        # Add child leaves and namespaces to match
        # the model command:
        root.add_child('key0', 'yo')
        root.add_child('key1', 'dogg')
        root.add_child('key2', 'i_heard')
        
        ns0 = root.add_child('ns0')
        ns0.add_child('key3', 'you_like')
        
        ns1 = ns0.add_child('ns1')
        ns2 = ns1.add_child('ns2')
        ns2.add_child('key4', 'tree')
        ns2.add_child('key5', 'structures')
        
        # Assemble subcommands for namespaces:
        root_command = root.assemble_subcommand()
        ns0_command = ns0.assemble_subcommand()
        ns2_command = ns2.assemble_subcommand()
        
        assert root_command in command
        assert ns0_command in command
        assert ns2_command in command
        
        print("ROOT COMMAND:")
        print(root_command)
        print()
        
        print("NS0 SUBCOMMAND:")
        print(ns0_command)
        print()
        
        print("NS2 SUBCOMMAND:")
        print(ns2_command)
        print()
        
        # Assemble full command recursively:
        full_command = root.assemble_subcommand(recursive=True)
        
        print("FULL ASSEMBLED COMMAND:")
        print(full_command)
        print()
        
        assert full_command in command
        
        for line in tree_repr(root, Level()):
            print(line)
        
        print()
    
    @inline
    def test_roundtrip_command_line():
        """ Parse and subsequently reassemble the command """
        
        # Create an empty tree:
        root = RootNode(name="WRITE")
        
        # Populate it from the model command line:
        root.populate_with_arguments(*nsflags)
        
        # Re-assemble the full model command recursively:
        full_command = root.assemble_subcommand(recursive=True)
        
        assert full_command in command
        
        for line in tree_repr(root, Level()):
            print(line)
        
        print()
    
    @inline
    def test_nodetreemap_basics():
        """ Check the basic functions of NodeTreeMap """
        
        # Fill a tree, per the command line:
        root = RootNode()
        root.populate_with_arguments(*nsflags)
        
        # Stick it in a NodeTreeMap:
        itemlist = []
        ntm = NodeTreeMap(tree=root)
        for nskey, value in ntm.items():
            itemlist.append((nskey, value))
        pprint(itemlist)
        print()
        
        pprint(ntm.flatten().submap())
        print()
    
    @inline
    def test_nodetree_namespaces():
        """ Check node namespaced names """
        
        # Fill a tree, per the command line:
        root = RootNode()
        root.populate_with_arguments(*nsflags)
        
        assert root.get_child('key0').nsname == 'key0'
        assert root.get_child('key0').value == 'yo'
        assert root.get_child('key1').nsname == 'key1'
        assert root.get_child('key1').value == 'dogg'
        assert root.get_child('key2').nsname == 'key2'
        assert root.get_child('key2').value == 'i_heard'
        
        assert root.get_child('ns0:key3').name == 'key3'
        assert root.get_child('ns0:key3').nsname == 'ns0:key3'
        assert root.get_child('ns0:key3').value == 'you_like'
        
        assert root.get_child('ns0:ns1:ns2:key4').name == 'key4'
        assert root.get_child('ns0:ns1:ns2:key4').nsname == 'ns0:ns1:ns2:key4'
        assert root.get_child('ns0:ns1:ns2:key4').value == 'tree'
        assert root.get_child('ns0:ns1:ns2:key5').name == 'key5'
        assert root.get_child('ns0:ns1:ns2:key5').nsname == 'ns0:ns1:ns2:key5'
        assert root.get_child('ns0:ns1:ns2:key5').value == 'structures'
        
        assert root.has_child('ns0:key3')
        assert root.has_child('ns0:ns1:ns2:key4')
        assert root.has_child('ns0:ns1:ns2:key5')
        
        ntm = NodeTreeMap(tree=root)
        
        assert ntm['key0'] == 'yo'
        assert ntm['key1'] == 'dogg'
        assert ntm['key2'] == 'i_heard'
        
        assert ntm['ns0:key3'] == 'you_like'
        assert ntm['ns0:ns1:ns2:key4'] == 'tree'
        assert ntm['ns0:ns1:ns2:key5'] == 'structures'
        
        assert 'ns0:key3' in ntm
        assert 'ns0:ns1:ns2:key4' in ntm
        assert 'ns0:ns1:ns2:key5' in ntm
    
    @inline
    def test_roundtrip_nodetree_dict():
        """ Check NodeTreeMap to/from dict functions """
        
        # Fill a tree, per the command line:
        root = RootNode()
        root.populate_with_arguments(*nsflags)
        ntm = NodeTreeMap(tree=root)
        
        instance_dict = ntm.to_dict()
        instance = NodeTreeMap.from_dict(instance_dict)
        
        # pprint(ntm.flatten().submap())
        # pprint(instance.flatten().submap())
        
        # pprint(tuple(ntm.namespaces()))
        # pprint(tuple(instance.namespaces()))
        
        assert ntm == instance
        assert instance_dict == instance.to_dict()
    
    @inline
    def test_roundtrip_nodetree_json():
        """ Check NodeTreeMap to/from json functions """
        from clu.config.codecs import json_encode, json_decode
        
        # Fill a tree, per the command line:
        root = RootNode()
        root.populate_with_arguments(*nsflags)
        ntm = NodeTreeMap(tree=root)
        
        ntm_json = json_encode(ntm)
        ntm_reconstituted = json_decode(ntm_json)
        
        assert ntm == ntm_reconstituted
        
        print(ntm_json)
        print()
    
    @inline
    def test_nodetree_halfviz():
        """ Generate Halfviz from a node tree """
        # Fill a tree, per the command line:
        root = RootNode()
        root.populate_with_arguments(*nsflags)
        
        def edge_repr(parent, node):
            return f"{parent.name} -> {node.name}"
        
        def tree_repr(parent, node, level):
            with level:
                if parent:
                    yield level.indent(edge_repr(parent, node))
                for child in node:
                    yield from tree_repr(node, child, level)
        
        for line in tree_repr(None, root, Level()):
            print(line)
        
        print()
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
