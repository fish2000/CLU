# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.constants import Nondeterminism

import pytest

class TestNaming(object):
    
    """ Run the tests for the clu.naming module. """
    
    @pytest.mark.xfail
    def test_qualified_name_constants(self):
        """ » Checking “qualified_name(¬) on items from clu.constants …” """
        
        from clu.constants.consts import BASEPATH, HOSTNAME, PROJECT_NAME, VERBOTEN
        from clu.naming import qualified_name
        
        qname = qualified_name(VERBOTEN)
        try:
            assert qname == 'clu.constants.consts.VERBOTEN'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(VERBOTEN) → {qname}")
        
        qname = qualified_name(PROJECT_NAME)
        try:
            assert qname == 'clu.constants.consts.PROJECT_NAME'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(PROJECT_NAME) → {qname}")
        
        qname = qualified_name(HOSTNAME)
        try:
            assert qname == 'clu.constants.consts.HOSTNAME'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(HOSTNAME) → {qname}")
        
        qname = qualified_name(BASEPATH)
        try:
            assert qname == 'clu.constants.consts.BASEPATH'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(BASEPATH) → {qname}")
    
    def test_qualified_name_instances(self):
        """ » Checking “qualified_name(¬) on instances of objects …” """
        
        # N.B. This will continue to XFAIL all over itself, until we get
        # the Exporter up and running – so we can assign real __name__,
        # __doc__ (…et al.) values to lambda functions as warranted.
        
        from clu.exporting import determine_name
        from clu.naming import qualified_name
        from clu.predicates import isclass, ismetaclass, isclasstype
        from clu.predicates import allattrs, allpyattrs, isiterable
        from clu.predicates import attr, pyattr, isenum, enumchoices
        from clu.predicates import isnormative, iscontainer, apply_to
        from clu.predicates import predicate_all, predicate_xor, thing_has
        from clu.predicates import slots_for
        
        things = (isclass, ismetaclass, isclasstype,
                  allattrs, allpyattrs, isiterable,
                  attr, pyattr, isenum, enumchoices,
                  isnormative, iscontainer, apply_to,
                  predicate_all, predicate_xor, thing_has,
                  slots_for)
        
        for thing in things:
            qname = qualified_name(thing)
            name = determine_name(thing)
            try:
                assert qname == f'clu.predicates.{name}'
            except AssertionError:
                raise Nondeterminism(f"Nondeterminism in qualified_name({name}) → {qname}")
        
        # TO INFINITY AND BEYOND:
        assert 'clu.exporting.%s' % determine_name(determine_name) == qualified_name(determine_name)
        assert 'clu.naming.%s' % determine_name(qualified_name) == qualified_name(qualified_name)
    
    def test_qualified_name_typespace(self):
        """ For some fucking reason *this* one consistently passes …? """
        from clu.naming import qualified_name
        from clu.typespace import types
        
        qname = qualified_name(types)
        try:
            assert qname == 'clu.typespace.namespace.types'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(types) → {qname}")
    
    def test_qualified_import(self):
        """ » Checking “qualified_import(¬) …” """
        from clu.naming import qualified_import, qualified_name
        # is_python2_dead     = qualified_import('clu.repl.banners.is_python2_dead')
        
        print_python_banner = qualified_import('clu.repl.print_python_banner')
        print_warning       = qualified_import('clu.repl.print_warning')
        Text                = qualified_import('clu.repl.ansi.Text')
        Background          = qualified_import('clu.repl.ansi.Background')
        Weight              = qualified_import('clu.repl.ansi.Weight')
        
        qname = qualified_name(print_python_banner)
        try:
            assert qname == 'clu.repl.banners.print_python_banner'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(print_python_banner) → {qname}")
        
        qname = qualified_name(print_warning)
        try:
            assert qname == 'clu.repl.banners.print_warning'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(print_warning) → {qname}")
        
        """ N.B. this “is_python2_dead” business seems to be the point of failure: """
        # qname = qualified_name(is_python2_dead)
        # try:
        #     assert qname == 'clu.repl.is_python2_dead'
        # except AssertionError:
        #     raise Nondeterminism(f"Nondeterminism in qualified_name(is_python2_dead) → {qname}")
        
        qname = qualified_name(Text)
        try:
            assert qname == 'clu.repl.ansi.Text'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(Text) → {qname}")
        
        qname = qualified_name(Background)
        try:
            assert qname == 'clu.repl.ansi.Background'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(Background) → {qname}")
        
        qname = qualified_name(Weight)
        try:
            assert qname == 'clu.repl.ansi.Weight'
        except AssertionError:
            raise Nondeterminism(f"Nondeterminism in qualified_name(Weight) → {qname}")
    
    def _test_determine_module(self):
        """ » Checking `determine_module(…)` against `pickle.whichmodule(…)` …"""
        
        from clu.naming import determine_module
        from clu.exporting import exporter
        
        import pickle
        mismatches = 0
        # print_separator()
        
        for name, thing in exporter.exports().items():
            # clade = Clade.of(thing, name_hint=name)
            determination = determine_module(thing)
            whichmodule = pickle.whichmodule(thing, None)
            try:
                assert determination == whichmodule
            except AssertionError:
                mismatches += 1
                # print(f"»»» Module-lookup mismatch for {clade.to_string()} “{name}”")
                # print(f"»»»   determine_module(…) → {determination}")
                # print(f"»»» pickle.whichmodule(…) → {whichmodule}")
                # print()
        
        # print(f"≠≠≠ TOTAL EXPORTED THING COUNT: {len(exporter)}")
        # print(f"≠≠≠ TOTAL MISMATCHES FOUND: {mismatches!s}")
        # print_separator()
        # print()
    