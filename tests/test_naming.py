# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from clu.constants import consts
from clu.constants.exceptions import Nondeterminism

yo_dogg_rename = lambda: print("Yo dogg.")
i_heard_rename = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))

class TestNaming(object):
    
    """ Run the tests for the clu.naming module. """
    
    def test_renamer(self):
        from clu.naming import rename
        from clu.predicates import pyname
        fake_dotpath = 'yodogg.iheard'
        
        renamer = rename(dotpath=fake_dotpath)
        
        # yo_dogg = lambda: print("Yo dogg.")
        # i_heard = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        yo_dogg = renamer(yo_dogg_rename)
        i_heard = renamer(i_heard_rename)
        
        assert pyname(yo_dogg) == pyname(yo_dogg_rename) == 'yo_dogg_rename'
        assert pyname(i_heard) == pyname(i_heard_rename) == 'i_heard_rename'
    
    def test_module_inspectors_0(self):
        from clu.naming import isbuiltin
        
        assert isbuiltin(callable)
        assert isbuiltin(set)
        assert not isbuiltin(isbuiltin)
    
    def test_module_inspectors_1(self):
        from clu.naming import isnativemodule
        
        imaging = pytest.importorskip('PIL._imaging')
        zict = pytest.importorskip('zict')
        import os
        
        assert isnativemodule(imaging)
        assert not isnativemodule(zict)
        assert not isnativemodule(os) # builtins don’t qualify
    
    def test_module_inspectors_2(self):
        from clu.naming import isnative
        
        imaging = pytest.importorskip('PIL._imaging')
        Image = pytest.importorskip('PIL.Image')
        
        assert isnative(imaging.alpha_composite)
        assert not isnative(Image)
        assert not isnative(callable) # builtins don’t qualify
        assert not isnative(dict) # I just said they don’t qualify
    
    def test_dotpath_to_prefix_and_path_to_prefix(self):
        from clu.naming import dotpath_to_prefix, path_to_prefix
        
        dp = "yo.dogg.iheard.youlike"
        px0 = "yo-dogg-iheard-youlike-"
        px1 = "yo-dogg-iheard-youlike≠"
        px2 = "yo•dogg•iheard•youlike≠"
        
        pp = "/yo/dogg/iheard/youlike.py"
        
        # Ensure ValueError gets raised when arguments are bad:
        with pytest.raises(ValueError) as exc:
            dotpath_to_prefix(dp, end=None)
        assert "must be non-None" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            dotpath_to_prefix(dp, sep=None)
        assert "must be non-None" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            dotpath_to_prefix(dp, sep=None, end=None)
        assert "must be non-None" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            dotpath_to_prefix('')
        assert "cannot be None or zero-length" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            dotpath_to_prefix(None)
        assert "cannot be None or zero-length" in str(exc.value)
        
        # Check dotpath conversion:
        assert px0 == dotpath_to_prefix(dp)
        assert px1 == dotpath_to_prefix(dp, end="≠")
        assert px2 == dotpath_to_prefix(dp, sep="•", end="≠")
        
        # Check path conversion:
        assert px0 == path_to_prefix(pp)
        assert px1 == path_to_prefix(pp, end="≠")
        assert px2 == path_to_prefix(pp, sep="•", end="≠")
    
    @pytest.mark.skipif(consts.PYPY, reason="Failure on PyPy")
    @pytest.mark.nondeterministic
    def test_qualified_name_constants(self, clumods, consts):
        """ » Checking “qualified_name(¬) on items from clu.constants …” """
        from clu.naming import qualified_name
        
        names = ('BASEPATH', 'HOSTNAME', 'VERBOTEN', 'SCRIPT_PATH', 'TEST_PATH')
        constants = (getattr(consts, name) for name in names)
        
        for name, const in zip(names, constants):
            qname = qualified_name(const)
            assert qname == f'clu.constants.consts.{name}'
        
        """ This commented-out bit fails because “clu.__title__” (defined in clu/__init__.py)
            is the same string – and interning makes them into the same object. """
        # qname = qualified_name(consts.PROJECT_NAME)
        # try:
        #     assert qname == 'clu.constants.consts.PROJECT_NAME'
        # except AssertionError:
        #     raise Nondeterminism(f"Nondeterminism in qualified_name(consts.PROJECT_NAME) → {qname}")
    
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
    
    @pytest.mark.nondeterministic
    def test_qualified_import(self):
        """ » Checking “qualified_import(¬) …” """
        from clu.naming import qualified_import, qualified_name
        # is_python2_dead     = qualified_import('clu.repl.banners.is_python2_dead')
        
        print_python_banner = qualified_import('clu.repl.banners.print_python_banner')
        print_warning       = qualified_import('clu.repl.banners.print_warning')
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
    
    @pytest.mark.nondeterministic
    def test_moduleof_failure_rate(self, clumods):
        """ » Checking `moduleof(…)` against `pickle.whichmodule(…)` …"""
        from clu.exporting import Exporter
        from clu.naming import moduleof
        import pickle
        
        total = 0
        mismatches = 0
        modulenames = Exporter.modulenames()
        
        assert len(clumods) <= len(modulenames)
        
        for modulename in modulenames:
            exports = Exporter[modulename].exports()
            total += len(exports)
            for name, thing in exports.items():
                whichmodule = pickle.whichmodule(thing, None)
                determination = moduleof(thing)
                try:
                    assert determination == whichmodule
                except AssertionError:
                    mismatches += 1
        
        # In practice the failure rate seemed to be around 7.65 %
        failure_rate = 100 * (float(mismatches) / float(total))
        assert failure_rate < 8.0 # percent
