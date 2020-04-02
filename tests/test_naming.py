# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from clu.constants.exceptions import Nondeterminism

yo_dogg_rename = lambda: print("Yo dogg.")
i_heard_rename = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))

class TestNaming(object):
    
    """ Run the tests for the clu.naming module. """
    
    def test_renamer(self, consts):
        """ N.B. compare this to the “legacy callable” q.v. test sub. """
        from clu.naming import renamer
        from clu.predicates import pyname
        
        yo_dogg_lambda = lambda: print("Yo dogg.")
        i_heard_lambda = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        # renaming creates duplicate functions:
        yo_dogg = renamer('yo_dogg')(yo_dogg_lambda)
        i_heard = renamer('i_heard')(i_heard_lambda)
        
        # confirm new names:
        assert pyname(yo_dogg) == 'yo_dogg'
        assert yo_dogg.__qualname__.endswith('yo_dogg')
        assert yo_dogg.__qualname__.startswith(yo_dogg_lambda.__qualname__.rpartition(consts.QUALIFIER)[0])
        assert pyname(i_heard) == 'i_heard'
        assert i_heard.__qualname__.endswith('i_heard')
        assert i_heard.__qualname__.startswith(i_heard_lambda.__qualname__.rpartition(consts.QUALIFIER)[0])
        
        # these are duplicates, they do *not* compare equal:
        assert yo_dogg != yo_dogg_lambda
        assert i_heard != i_heard_lambda
    
    @pytest.mark.TODO
    def test_duplicate(self):
        # TODO: 1) verify lambdas renamed via @export or clu.naming.rename,
        #       2) verify __annotations__, __kwdefaults__, and __dict__ updates
        from functools import recursive_repr, wraps
        from clu.naming import duplicate
        from clu.predicates import haspyattr, pyattr
        from clu.typology import ΛΛ
        
        # Normal function:
        def no_dogg(yo, dogg='no'):
            """ NO, DOGG. """
            print('YO:',  f"{yo!s}")
            print('DOGG:' f"{dogg!s}")
        
        yo_dogg = duplicate(no_dogg, 'yo_dogg')
        
        assert yo_dogg.__name__ == 'yo_dogg'
        assert yo_dogg.__qualname__.endswith('yo_dogg')
        assert yo_dogg.__defaults__.index('no') == 0
        assert yo_dogg.__doc__.strip() == "NO, DOGG."
        assert not haspyattr(yo_dogg, 'wrapped')
        
        # Wrapped function:
        @wraps(recursive_repr)
        def oh_dogg(yo, dogg='oh!'):
            """ OH, DOGG! """
            print('YO:',  f"{yo!s}")
            print('DOGG:' f"{dogg!s}")
        
        so_dogg = duplicate(oh_dogg, 'so_dogg')
        
        assert so_dogg.__name__ == 'so_dogg'
        assert so_dogg.__qualname__.endswith('so_dogg')
        assert so_dogg.__defaults__.index('oh!') == 0
        assert so_dogg.__doc__.strip() == recursive_repr.__doc__.strip()
        assert ΛΛ(pyattr(oh_dogg, 'wrapped'))
        assert ΛΛ(pyattr(so_dogg, 'wrapped'))
        
        # Bound method:
        class DoggNamespaceEncapsulation(object):
            def bro_dogg(yo, dogg='bro.'):
                """ Bro. Dogg. """
                print('YO:',  f"{yo!s}")
                print('DOGG:' f"{dogg!s}")
        
        dogg_ns = DoggNamespaceEncapsulation()
        faux_dogg = duplicate(dogg_ns.bro_dogg, 'faux_dogg')
        
        assert faux_dogg.__name__ == 'faux_dogg'
        assert faux_dogg.__qualname__.endswith('faux_dogg')
        assert faux_dogg.__defaults__.index('bro.') == 0
        assert faux_dogg.__doc__.strip() == "Bro. Dogg."
        assert not haspyattr(faux_dogg, 'wrapped')
    
    def test_rename_legacy_callable(self):
        from clu.naming import rename
        from clu.predicates import pyname
        fake_dotpath = 'yodogg.iheard'
        
        renaming_callable = rename(dotpath=fake_dotpath)
        
        # yo_dogg = lambda: print("Yo dogg.")
        # i_heard = lambda *wat: print("I heard you like %s" % ", ".join(repr(w) for w in wat))
        
        yo_dogg = renaming_callable(yo_dogg_rename)
        i_heard = renaming_callable(i_heard_rename)
        
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
        
        for modulename in Exporter.modulenames():
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
