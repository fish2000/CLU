# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestDicts(object):
    
    """ Run the tests for merging dicts (the clu.dicts module), and
        ChainMaps (both “clu.dicts.ChainMap” and the stdlib version)
    """
    
    @pytest.fixture(scope='module')
    def arbitrary(self):
        """ Fixture function providing an arbitrary flat directory """
        yield {
            'yo'    : "dogg",
            'i'     : "heard",
            'you'   : "liked",
            'dict'  : "chains"
        }
    
    @pytest.fixture
    def fsdata(self, dirname):
        """ Return the “data” subdirectory of the “tests” directory """
        yield dirname.subdirectory('data')
    
    def test_chainmap(self, arbitrary, fsdata, environment):
        """ clu.dicts.ChainMap basic training """
        from clu.dicts import ChainMap
        
        # Create a ChainMap from a dict, a Directory instance,
        # and an environment mapping:
        hey = ChainMap(arbitrary, fsdata, environment)
        
        # Check length and boolean value:
        assert len(hey) == len(arbitrary) + len(fsdata) + len(environment)
        assert bool(hey)
        
        # Check keys from respective sub-maps:
        for key in ('yo', 'i', 'you', 'dict'):
            assert key in hey
            assert hey.mapcontaining(key) == arbitrary
            assert hey.get(key) == arbitrary.get(key)
        
        for key in ('config', 'yodata', 'yodogg',
                    '8ba.png', '3472236406_1fbf1a567d_o.jpg', 'shutterstock_90194617.jpg',
                    'IMG_20180505_205153567.jpg', '3471426989_aa8e83cac5_o.jpg'):
            assert key in hey
            assert hey.mapcontaining(key) == fsdata
            assert hey.get(key) == fsdata.get(key)
        
        for key in ('SHELL', 'LESS', 'HOME', 'LANG'):
            assert key in hey
            assert hey.mapcontaining(key) == environment
            assert hey.get(key) == environment.get(key)
        
        # Check for KeyErrors on bad item access:
        with pytest.raises(KeyError) as exc:
            hey['WTF-HAX']
        assert "WTF-HAX" in str(exc.value)
        
        with pytest.raises(KeyError) as exc:
            hey.get('WTF-HAX')
        assert "WTF-HAX" in str(exc.value)
        
        # Check for default return on bad item access with default:
        assert hey.get('WTF-HAX', default='nodogg') == 'nodogg'
        
        # SHIFT » like collections.ChainMap.parents:
        beentrying = hey.shift()
        
        assert len(beentrying.maps) < len(hey.maps)
        assert len(beentrying.keys()) < len(hey.keys())
        assert len(beentrying.values()) < len(hey.values())
        
        assert frozenset(hey).issuperset(beentrying)
        assert frozenset(hey.keys()).issuperset(beentrying.keys())
        
        for map in beentrying.maps:
            assert map in hey.maps
        
        # UNSHIFT » like collections.ChainMap.new_child(…):
        tomeetyou = hey.unshift()
        
        assert len(tomeetyou.maps) == len(hey.maps) + 1
        assert len(tomeetyou.keys()) == len(hey.keys())
        assert len(tomeetyou.values()) == len(hey.values())
        assert len(tomeetyou.keys()) > len(beentrying.keys())
        assert len(tomeetyou.values()) > len(beentrying.values())
        
        assert frozenset(tomeetyou).issuperset(hey)
        assert frozenset(tomeetyou.keys()).issuperset(hey.keys())
        
        for map in hey.maps:
            assert map in tomeetyou.maps
        
        tomeetyou['mustbe'] = "a devil"
        tomeetyou['betweenus'] = "or whores in my head"
        tomeetyou['whoredoor'] = "whores in my bed"
        
        for key in ('mustbe', 'betweenus', 'whoredoor'):
            assert key in tomeetyou
            # assert key not in hey
            assert key not in beentrying
            assert len(tomeetyou.mapcontaining(key)) == 3
            assert type(tomeetyou.get(key)) is str
        
        # CLONE » not via “clu.config.abc.Cloneable” …yet:
        
        buthey = hey.clone()
        where = beentrying.clone(deep=True)
        haveyou = tomeetyou.clone(deep=True)
        
        assert len(hey) == len(buthey)
        assert len(beentrying) == len(where)
        assert len(tomeetyou) == len(haveyou)
        
        '''
        for orig, clone in ((hey, buthey), (beentrying, where), (tomeetyou, haveyou)):
            for key in orig.keys():
                assert key in clone
                assert key in clone.flatten()
                # assert orig.get(key) == clone.get(key)
                assert key in orig
                assert key in orig.flatten()
                assert try_items(key, *orig.maps, default=None) is not None
                assert try_items(key, *clone.maps, default=None) is not None
                assert try_items(key, *orig.maps, default=None) == try_items(key, *clone.maps, default=None)
                # FAILS:
                # assert try_items(key, *orig.maps, default=None) == orig[key]
                # assert try_items(key, *clone.maps, default=None) == clone[key]
        '''
        
        # ONE LAST CHECK. And we’ll call it a day.
        been = ChainMap(arbitrary, fsdata, environment)
        assert frozenset(buthey).issuperset(where)
        assert not frozenset(hey).issuperset(haveyou)
        assert frozenset(buthey).issuperset(been)
    
    def test_chainmap_shallow_clone(self, arbitrary, fsdata, environment):
        """ Shallow clone membership check """
        from clu.dicts import ChainMap
        from clu.predicates import try_items
        
        chain0 = ChainMap(arbitrary, fsdata, environment)
        
        chain1 = chain0.clone()
        assert len(chain0) == len(chain1)
        
        for key in chain0.keys():
            assert key in chain0
            assert key in chain1
            
            # N.B. SLOW AS FUCK:
            assert key in chain0.flatten()
            
            assert try_items(key, *chain0.maps, default=None) == try_items(key, *chain1.maps, default=None)
            assert try_items(key, *chain0.maps, default=None) == chain0[key]
            assert try_items(key, *chain0.maps, default=None) == chain1[key]
    
    def test_chainmap_deep_clone(self, arbitrary, fsdata, environment):
        """ Deep clone membership check """
        from clu.dicts import ChainMap
        from clu.predicates import try_items
        
        chain0 = ChainMap(arbitrary, fsdata, environment)
        
        chainX = chain0.clone(deep=True)
        assert len(chain0) == len(chainX)
        
        for key in chain0.keys():
            assert key in chain0
            assert key in chainX
            
            # N.B. SLOW AS FUCK:
            assert key in chain0.flatten()
            
            assert try_items(key, *chain0.maps, default=None) == try_items(key, *chainX.maps, default=None)
            assert try_items(key, *chain0.maps, default=None) == chain0[key]
            assert try_items(key, *chain0.maps, default=None) == chainX[key]
    
    def test_chainmap_equality_comparisons(self, arbitrary):
        """ Equality comparisons across the board """
        from clu.dicts import ChainMap
        from clu.config.keymap import flatdict, Flat
        from itertools import product
        
        chain0 = ChainMap(arbitrary, Flat(flatdict()))
        chain1 = chain0.clone()
        chainX = chain0.clone(deep=True)
        chainZ = ChainMap(arbitrary, Flat(flatdict()))
        
        chains = (chain0, chain1, chainX, chainZ)
        
        # assert that they’re all equal to one another:
        for first, second in product(chains, chains):
            if first is not second:
                assert first == second
    
    def test_chainmap_compatibilty_stdlib_collections_chainmap(self):
        """ Compatibility checks with “collections.ChainMap” """
        from clu.dicts import ChainMap
        # from clu.dicts import ChainRepr
        from clu.config.keymap import Flat, Nested
        from clu.constants.data import arbitrary, nested
        import collections
        
        chain00 = ChainMap(Flat(arbitrary), Nested(nested))
        chainOO = collections.ChainMap(Flat(arbitrary), Nested(nested))
        
        assert len(chain00) == len(chainOO)
        
        for key in chainOO.keys():
            assert chain00[key]
            assert chain00[key] == chainOO[key]
        
        chainZ = ChainMap(chainOO)
        
        assert chainZ == chain00
        assert chainZ == chainOO
        
        # repr_instance = ChainRepr()
        # assert repr_instance.repr(chain0) == repr_instance.repr(chainO)
    
    def test_ordered_mapping_views(self, dirname, fsdata):
        """ The ordered mapping views are returned from “clu.fs.filesystem.Directory”
            mapping-view methods: “directory.items()”, “directory.keys()”, and
            “directory.values()”.
        """
        from clu.dicts import OrderedItemsView, OrderedKeysView, OrderedValuesView
        from clu.fs.filesystem import Directory
        from clu.typology import ismapping, issequence
        
        # Ensure type:
        assert type(dirname) is Directory
        assert type(fsdata) is Directory
        assert type(fsdata.items()) is OrderedItemsView
        assert type(fsdata.keys()) is OrderedKeysView
        assert type(fsdata.values()) is OrderedValuesView
        
        # Ensure it’s a mapping:
        assert ismapping(dirname)
        assert ismapping(fsdata)
        
        # Ensure it’s a sequence:
        assert issequence(fsdata.items())
        assert issequence(fsdata.keys())
        assert issequence(fsdata.values())
        
        # Ensure repr:
        assert repr(dirname).startswith('Directory')
        assert repr(fsdata).startswith('Directory')
        assert repr(fsdata.items()).startswith('OrderedItemsView')
        assert repr(fsdata.keys()).startswith('OrderedKeysView')
        assert repr(fsdata.values()).startswith('OrderedValuesView')
        
        # Redundant, but correct:
        assert len(fsdata.items()) == len(fsdata.keys()) == len(fsdata.values())
        assert len(list(fsdata.items())) == len(list(fsdata.keys())) == len(list(fsdata.values()))
        assert len(fsdata.items()) == len(list(fsdata.items()))
        assert len(fsdata.keys()) == len(list(fsdata.keys()))
        assert len(fsdata.values()) == len(list(fsdata.values()))
        
        # Nonexistent subdirectory:
        assert len(fsdata.subdirectory('wat').items()) == 0
        assert len(fsdata.subdirectory('wat').keys()) == 0
        assert len(fsdata.subdirectory('wat').values()) == 0
        
        # Real subdirectory with at least one item:
        assert len(fsdata.subdirectory('yodogg').items()) > 0
        assert len(fsdata.subdirectory('yodogg').keys()) > 0
        assert len(fsdata.subdirectory('yodogg').values()) > 0
        
        # Set properties:
        k1 = fsdata.subdirectory('yodogg').keys()
        k2 = fsdata.subdirectory('yodata').keys()
        kU = k1 | k2
        assert type(kU) is set
        assert len(kU) == len(k1) + len(k2)
        assert kU.issuperset(k1)
        assert kU.issuperset(k2)
        
        # Sequence properties:
        keys = fsdata.keys()
        for idx in range(len(keys)):
            assert keys[idx] == list(keys)[idx]
            assert keys[idx] in fsdata
    