#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

MODE = 0o700
BASEDIR = "/usr/local/var/run/xdg"
SSID = os.getenv('SECURITYSESSIONID')

from clu.constants import HOSTNAME
from clu.fs import rm_rf, Directory

basedir = Directory(BASEDIR)

def name_xdg_runtime_dir(namebase=SSID):
    return HOSTNAME.lower() + '-' + namebase.lower()

def make_xdg_runtime_dir(directory=basedir, mode=MODE):
    runtime_dir = directory.subdirectory(name_xdg_runtime_dir())
    if runtime_dir.exists:
        rm_rf(runtime_dir)
    runtime_dir.makedirs(mode=mode)
    return runtime_dir

def enumerate_dirs(directory=basedir):
    return (pth for pth in iter(directory) \
                 if pth.startswith("%s%s" % (HOSTNAME.lower(), '-')))

def remove_existing_dirs(directory=basedir):
    if len(directory) > 0:
        return all(rm_rf(pth) for pth in enumerate_dirs(directory))
    return True


