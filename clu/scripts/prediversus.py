# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from clu.naming import nameof
from clu.repr import strfield
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

predicate_test      = lambda predicate, argument: (          predicate,          argument,              predicate(argument))
predicate_test_repr = lambda predicate, argument: (f"{nameof(predicate)}({nameof(argument)})", strfield(predicate(argument)))

# LAMBDA EXPORTS:
export(predicate_test,          name='predicate_test',      doc="predicate_test(predicate, argument) → executes `predicate(argument)`, returning (`predicate`, `argument`, `predicate(argument)`)")
export(predicate_test_repr,     name='predicate_test_repr', doc="predicate_test_repr(predicate, argument) → stringifies `predicate` and `argument` – both individually and as the complete expression `predicate(argument)` – returning («operand string», «expression string»)")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    # from pprint import pprint
    
    @inline.fixture
    def dunder_mifflins():
        """ Get a sequence of interrogation-ready string identifiers """
        return ('yo-dogg', 'yo_dogg', '_yo_dogg_', '__yodogg__',
                                      '_yo_dogg',  '__yodogg',
                                                     'yodogg__')
    
    @inline
    def test_one():
        """ Basic “predicate_test(…)” generator-expression check """
        from clu.predicates import ispyname, ismifflin, ispublic
        
        pyname_results = tuple(predicate_test(ispyname, name)[-1] for name in dunder_mifflins())
        mifflin_results = tuple(predicate_test(ismifflin, name)[-1] for name in dunder_mifflins())
        public_results = tuple(predicate_test(ispublic, name)[-1] for name in dunder_mifflins())
        
        # from pprint import pprint
        # pprint(public_results)
        
        assert pyname_results   == (False, False, False, True, False, False, False)
        #                                                ^^^^^
        #                                                  └─« only hit: '__yodogg__'
        
        assert mifflin_results  == (False, False, True, False, False, False, False)
        #                                         ^^^^^
        #                                           └────────« only hit: '_yodogg_'
        
        assert public_results   == (True, True, False, False, True, True, True)
        #                                       ^^^^^^^^^^^^^
        #                                           └└└└└────« two misses: '_yo_dogg_' and '__yodogg__' –
        #                                                    … correspoinding to the two lone hits above
    
    @inline
    def test_two():
        """ String-compare “predicate_test_repr(…)” gen-exp check """
        from clu.predicates import ispyname, ismifflin, ispublic
        
        pyname_results = tuple("%s = %s" % predicate_test_repr(ispyname, name) for name in dunder_mifflins())
        mifflin_results = tuple("%s = %s" % predicate_test_repr(ismifflin, name) for name in dunder_mifflins())
        public_results = tuple("%s = %s" % predicate_test_repr(ispublic, name) for name in dunder_mifflins())
        
        # print("PYNAME RESULTS:")
        # pprint(pyname_results)
        # print()
        
        # print("MIFFLIN RESULTS:")
        # pprint(mifflin_results)
        # print()
        
        # print("PUBLIC RESULTS:")
        # pprint(public_results)
        # print()
        
        assert pyname_results   == ('ispyname(None) = «False»',
                                    'ispyname(None) = «False»',
                                    'ispyname(None) = «False»',
                                    'ispyname(None) = «True»',
                                    'ispyname(None) = «False»',
                                    'ispyname(None) = «False»',
                                    'ispyname(None) = «False»')
        
        assert mifflin_results  == ('ismifflin(None) = «False»',
                                    'ismifflin(None) = «False»',
                                    'ismifflin(None) = «True»',
                                    'ismifflin(None) = «False»',
                                    'ismifflin(None) = «False»',
                                    'ismifflin(None) = «False»',
                                    'ismifflin(None) = «False»')
        
        assert public_results   == ('ispublic(None) = «True»',
                                    'ispublic(None) = «True»',
                                    'ispublic(None) = «False»',
                                    'ispublic(None) = «False»',
                                    'ispublic(None) = «True»',
                                    'ispublic(None) = «True»',
                                    'ispublic(None) = «True»')
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

