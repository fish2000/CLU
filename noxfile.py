# -*- coding: utf-8 -*-
from __future__ import print_function

import nox
import sys, os
sys.path.append(os.path.dirname(__file__))

# Recycle, reduce, reuse:
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

@nox.session
def checkmanifest(session):
    """ Check CLU’s MANIFEST.in against the Git HEAD """
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')

@nox.session
@nox.parametrize('module', [
    nox.param('clu.constants',  id='consts'),
    nox.param('clu',            id='modules'),
    nox.param('clu.version',    id='version'),
])
def checkmodule(session, module):
    """ Check CLU modules and constants """
    session.install("-r", "requirements/install.txt")
    session.run('python', '-m', module)

# @nox.session(python=['3.7', '3.8', 'pypy3'])
@nox.session
def pytest(session):
    """ Run CLU’s `pytest` unit test suite """
    session.env['MACOSX_DEPLOYMENT_TARGET']         = '10.14'
    session.env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']   = '1'
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.run('pytest')

def parametrized_inline_tests():
    from clu.all import inline_tests
    for dotpath in inline_tests():
        yield nox.param(dotpath,
                     id=dotpath.lstrip('clu').lstrip('.'))

@nox.session
@nox.parametrize('module', list(parametrized_inline_tests()))
def inline(session, module):
    """ Run CLU’s per-module inline test suite """
    session.install("-r", "requirements/install.txt")
    session.run('python', '-m', module)