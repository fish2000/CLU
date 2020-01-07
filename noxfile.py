# -*- coding: utf-8 -*-
from __future__ import print_function

import nox

# @nox.session(python=['3.7', '3.8', 'pypy3'])
@nox.session
def pytest(session):
    """ Run pytest unit tests and check MANIFEST.in """
    session.install("-r", "requirements/install.txt")
    session.install("-r", "requirements/nox/tests.txt")
    session.install("-r", "requirements/nox/manifest.txt")
    session.run('python', '-m', 'check_manifest', '-v')
    session.run('pytest')

@nox.session
def check_clu_basics(session):
    """ Check CLU constants and module exports """
    session.install("-r", "requirements/install.txt")
    session.run('python', '-m', 'clu.constants')
    session.run('python', '-m', 'clu')
