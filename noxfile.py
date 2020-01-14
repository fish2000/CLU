# -*- coding: utf-8 -*-
from __future__ import print_function

import nox
import sys, os
sys.path.append(os.path.dirname(__file__))

# Recycle, reduce, reuse:
nox.options.reuse_existing_virtualenvs = True

@nox.session
def checkmanifest(session):
    """ Check CLU’s MANIFEST.in against the Git HEAD """
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')

@nox.session
@nox.parametrize('module', ['clu.constants', 'clu'])
def checkmodule(session, module):
    """ Check CLU modules and constants """
    session.install("-r", "requirements/install.txt")
    session.run('python', '-m', module)

# @nox.session(python=['3.7', '3.8', 'pypy3'])
@nox.session
def pytest(session):
    """ Run CLU’s `pytest` unit test suite """
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.run('pytest')

@nox.session
def inlinetest(session):
    """ Run CLU’s per-moduyle inline tests """
    session.install("-r", "requirements/install.txt")
    
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
