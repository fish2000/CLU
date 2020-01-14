# -*- coding: utf-8 -*-
from __future__ import print_function

import nox
import sys, os
sys.path.append(os.path.dirname(__file__))

# Recycle, reduce, reuse:
nox.options.reuse_existing_virtualenvs = True

# @nox.session(python=['3.7', '3.8', 'pypy3'])
@nox.session
def pytest(session):
    """ Run CLU’s pytest unit test suite, and check MANIFEST.in """
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')
    session.run('pytest')

@nox.session
def inlinetest(session):
    """ Run CLU inline tests, and check modules and constants """
    session.install("-r", "requirements/install.txt")
    
    # First, check CLU consts:
    session.run('python', '-m', 'clu.constants')
    
    # Next, run module export checks:
    session.run('python', '-m', 'clu')
    
    # Next, import all CLU modules:
    from clu.all import import_clu_modules
    from clu.predicates import resolve
    clumods = import_clu_modules()
    
    # Finally, find all CLU modules with inline tests,
    # and execute them:
    for dotpath, module in clumods.items():
        test_fn = resolve(module, 'test')
        if test_fn is not None:
            if callable(test_fn):
                names = resolve(test_fn, '__code__.co_names')
                if names is not None:
                    if 'inline' in names:
                        session.run('python', '-m', dotpath)
