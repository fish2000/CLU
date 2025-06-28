# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import defaultdict as DefaultDict
from functools import lru_cache
from copy import copy

import collections.abc
import clu.abstract
import clu.enums
import sys

from clu.naming import moduleof
from clu.predicates import tuplize
from clu.typology import isstring, isstringlist, subclasscheck
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

cache = lambda function: lru_cache(maxsize=128, typed=False)(function)

@export
class BaseTrie(clu.abstract.Unhashable, metaclass=clu.abstract.Slotted):
    
    __slots__ = ('is_final',
                 'identity', 'parent',
                 'children')
    
    def __init__(self):
        self.is_final = False
        self.identity = None
        self.parent = None # root nodes have no parents
        self.children = DefaultDict(type(self))
    
    def add(self, string):
        if not string:
            return
        trie = self
        for character in string:
            child = trie.children[character]
            child.identity = copy(character)
            child.parent = trie
            trie = child
        trie.is_final = True
    
    def find(self, string, pos):
        if not string:
            return False
        trie = self
        for character in string[pos:]:
            if trie.is_final:
                return True
            if character in trie.children:
                trie = trie.children[character]
            else:
                return False
        return trie.is_final
    
    def search(self, string):
        return any(self.find(string, pos) for pos in range(len(string)))

@export
class Trie(BaseTrie, collections.abc.MutableMapping):
    
    def __bool__(self):
        return bool(self.children)
    
    def __len__(self):
        return len(self.children)
    
    def __contains__(self, character):
        return character in self.children
    
    def __getitem__(self, character):
        if not character:
            raise ValueError(f"can’t index a trie with falsey value: {character}")
        return self.children[character]
    
    def __setitem__(self, character, newvalue):
        if not character:
            raise ValueError(f"can’t index a trie with falsey value: {character}")
        if not subclasscheck(BaseTrie, typeof(newvalue)):
            raise ValueError(f"what the fuck is this? --> {newvalue}")
        self.children[character] = newvalue
    
    def __delitem__(self, character):
        if not character:
            raise ValueError(f"can’t index a trie with falsey value: {character}")
        del self.children[character]
    
    def __iter__(self):
        yield from self.children
    
    def __str__(self):
        return str(self.identity)
    
    def is_rootnode(self):
        return self.parent is None
    
    def is_leafnode(self):
        return not self
    
    def whoami(self):
        out = []
        trie = self
        while not trie.is_rootnode():
            out.insert(0, str(trie))
            trie = trie.parent
        return ''.join(out)
    
    def debug_search(self, string):
        print()
        for pos in range(len(string)):
            result = self.find(string, pos)
            print(f"+++++ self.find('{string}', {pos:02}) == {result}")
        print()
        return super().search(string)

@export
class Status(clu.enums.AliasingEnum):
    
    """ Search status enum, for use with TrieSearcher (q.v. def sub.) """
    
    PENDING     = 'pending'
    RUNNING     = 'running'
    COMPLETE    = 'complete'
    INCOMPLETE  = 'incomplete'
    DIAGNOSTIC  = 'diagnostic'
    
    @classmethod
    def byname(cls, string):
        """ Get a status item by its bucket name, matching case-insensitively """
        for status in cls:
            if status.group_name == string.casefold():
                return status
        raise ValueError(f"status not found: {string}")
    
    @classmethod
    def bytitle(cls, string):
        """ Retrieve a status by its label, matching case-insensitively """
        for status in cls:
            if status.group_label.casefold() == string.casefold():
                return status
        raise ValueError(f"status not found: {string}")
    
    def to_string(self):
        return str(self.name)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.name, encoding=consts.ENCODING)
    
    @property
    def group_name(self):
        return self.to_string().casefold()
    
    @property
    def group_label(self):
        return str(self.value)

@export
class TrieSearcher(clu.abstract.ReprWrapper, metaclass=clu.abstract.Slotted):
    
    __slots__ = ('search_space', 'search_sets', 'root_node')
    
    def __init__(self, *strings):
        if not isstringlist(strings):
            raise ValueError(f"these are not strings: {stringlist}")
        self.search_space = list()
        self.search_sets = list()
        self.root_node = Trie()
        for string in strings:
            self.search_space.append(string)
            self.root_node.add(string)
    
    def add_to_search_space(self, *strings):
        if not isstringlist(strings):
            raise ValueError(f"these are not strings: {stringlist}")
        for string in strings:
            self.search_space.append(string)
            self.root_node.add(string)
    
    def _do_search(self, infodict):
        infodict['status'] = Status.RUNNING
        terms = infodict['terms']
        out = tuple(term for term in terms if self.root_node.search(term))
        infodict['results'] = out
        infodict['status'] = Status.COMPLETE
        return out
    
    def perform_simple_search(self, string):
        if not isstring(string := str(string)):
            raise ValueError(f"argument couldn’t be stringged")
        query = {
            'terms': tuplize(string),
            'status': Status.PENDING,
            'results': tuple()
        }
        response = self._do_search(query)
        return response
        

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    @inline.fixture
    def yodogg_needles():
        return tuplize('yo', 'dogg', 'yo dogg', 'yo yo', 'dogg yo')
    
    @inline
    def test_BaseTrie_basics():
        """ Try the most basic trie functionality """
        bt = BaseTrie()
        
        for needle in yodogg_needles():
            bt.add(needle)
        
        assert bt.search('yo')
        assert not bt.search('no')
        assert bt.search('yo dogg')
        assert bt.search('yo doggggggggg')
        assert bt.search('yyyyyyyoooooyoyyyyo dogg')
        assert not bt.search('yes')
        assert not bt.search('yes dog')
        assert bt.search('yes dogg') # !!!
        
        assert type(bt.children) == DefaultDict
        assert type(bt.children['y']) == BaseTrie
        assert len(bt.children) == 2
        assert len(bt.children['y'].children) == 1
    
    # …
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())