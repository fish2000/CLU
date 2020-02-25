# -*- coding: utf-8 -*-
from __future__ import print_function

import nox
import sys, os
sys.path.append(os.path.dirname(__file__))

# Recycle, reduce, reuse:
nox.options.keywords = "not codecov"
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

@nox.session
def checkmanifest(session):
    """ Check CLU’s MANIFEST.in against the Git HEAD """
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')

@nox.session
@nox.parametrize('module', (
    nox.param('clu.constants',  id='consts'),
    nox.param('clu',            id='modules'),
    nox.param('clu.version',    id='version')))
def checkmodule(session, module):
    """ Show CLU consts, modules, or versioning """
    session.install("-r", "requirements/install.txt")
    if module == 'clu':
        session.install("-r", "requirements/nox/tests.txt")
    session.run('python', '-m', module)

@nox.session
def pytest(session):
    """ Run CLU’s entire unit-test suite with `pytest` """
    session.env['MACOSX_DEPLOYMENT_TARGET']         = '10.14'
    session.env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']   = '1'
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.run('pytest')

def parametrized_inline_tests():
    from clu import all
    for dotpath in all.inline_tests():
        yield nox.param(dotpath,
                     id=dotpath.lstrip('clu').lstrip('.'))

@nox.session
@nox.parametrize('module', tuple(parametrized_inline_tests()))
def inline(session, module):
    """ Run specific per-module inline tests """
    session.install("-r", "requirements/install.txt")
    if str(module).endswith('mathematics'):
        session.install("-r", "requirements/nox/tests.txt")
    session.run('python', '-m', module)

@nox.session
def codecov(session):
    """ Run `codecov`, updating CLU’s statistics on codecov.io """
    session.env['MACOSX_DEPLOYMENT_TARGET']         = '10.14'
    session.env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']   = '1'
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.install("-r", "requirements/nox/codecov.txt")
    session.run('pytest', '-p', 'pytest_cov', '--cov=clu',
                                              '--cov-report=xml:coverage.xml',
                                              '--no-cov-on-fail', 'tests/')
    session.run('codecov')