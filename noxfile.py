# -*- coding: utf-8 -*-
from __future__ import print_function

import nox
import sys, os
sys.path.append(os.path.dirname(__file__))

# Recycle, reduce, reuse:
nox.options.keywords = "not coverage"
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

# Skip manifest check if we’re not running in a Git repo:
from clu.version.git_version import are_we_gitted
if not are_we_gitted():
    nox.options.keywords += " and not checkmanifest"

@nox.session
def checkmanifest(session):
    """ Check CLU’s MANIFEST.in against the Git HEAD """
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')

@nox.session
@nox.parametrize('module', (
    nox.param('clu.constants',      id='consts'),
    nox.param('clu',                id='modules'),
    nox.param('clu.version',        id='version'),
    nox.param('clu.scripts.repl',   id='repl')))
def checkmodule(session, module):
    """ Check CLU consts, modules, importing, REPL, or version """
    session.install("-r", "requirements/install.txt")
    if module == 'clu':
        session.install("-r", "requirements/nox/tests.txt")
    elif module == 'clu.scripts.repl':
        session.install("-r", "requirements/nox/repl.txt")
    session.run('python', '-m', module)

@nox.session
def pytest(session):
    """ Run CLU’s entire unit-test suite with `pytest` """
    session.env['MACOSX_DEPLOYMENT_TARGET']       = '10.14'
    # session.env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/repl.txt")
    session.run('pytest', '--no-delete-temps')

def parametrized_inline_tests():
    import clu.all
    for dotpath in clu.all.inline_tests():
        yield nox.param(dotpath,
                     id=dotpath.removeprefix('clu.'))

@nox.session
@nox.parametrize('module', tuple(parametrized_inline_tests()))
def inline(session, module):
    """ Run specific per-module inline tests """
    session.install("-r", "requirements/install.txt")
    if str(module).endswith('mathematics'):
        session.install("-r", "requirements/nox/tests.txt")
    session.run('python', '-m', module)

@nox.session
def coverage(session):
    """ Run `codecov`, updating CLU’s statistics on codecov.io """
    import clu.all
    from clu.fs.filesystem import TemporaryName
    coveragefile = TemporaryName(prefix='coverage-',
                                 suffix='bin',
                                 randomized=True)
    
    session.env['MACOSX_DEPLOYMENT_TARGET']       = '10.14'
    session.env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    session.env['COVERAGE_FILE'] = coveragefile.do_not_destroy()
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/repl.txt")
    session.install("-r", "requirements/nox/codecov.txt")
    
    # Erase existing data:
    session.run('coverage', 'erase')
    
    # Run command modules:
    for modulename in ('clu.constants',
                       'clu.constants.consts',
                       'clu.config.codecs',
                       'clu',
                       'clu.version',
                       'clu.dispatch',
                       'clu.importing',
                       'clu.fs.appdirectories',
                       'clu.repl.banners',
                       'clu.repl.columnize',
                       'clu.scripts.repl'):
        session.run('coverage',
                    'run', '--append', '-m', modulename,
                    silent=True)
    
    # Run each inline-test function:
    for modulename in clu.all.inline_tests():
        session.run('coverage',
                    'run', '--append', '-m', modulename,
                     silent=True)
    
    # pytest-cov ignores COVERAGE_FILE:
    coveragefile.copy('.coverage')
    
    # Run “pytest” with the “pytest-cov” plugin:
    session.run('pytest', '-p', 'pytest_cov', '--cov=clu',
                                              '--cov-append',
                                              '--cov-report=xml:coverage.xml',
                                              '--no-cov-on-fail',
                                              'tests/')
    
    # Run ‘codecov’ to upload the results to codecov.io:
    session.run('codecov', '--required')
    
    # Destroy temporary coverage data files:
    coveragefile.close()
    session.run('/bin/rm', '.coverage', external=True)