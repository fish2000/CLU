# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from clu.constants import System
from clu.fs import AppDirs, Directory
from clu.version import VersionInfo

XDGS = ('XDG_CONFIG_DIRS', 'XDG_DATA_HOME',
        'XDG_CONFIG_HOME', 'XDG_DATA_DIRS',
                          'XDG_CACHE_HOME',
                          'XDG_STATE_HOME',
                         'XDG_RUNTIME_DIR')

@pytest.fixture
def environment(keys=XDGS):
    """ Yield an instance of `os.environ` free of XDG variables """
    import os
    stash = {}
    
    # Setup: remove XDG variables from environment:
    for key in keys:
        if key in os.environ:
            stash[key] = os.environ.get(key)
            del os.environ[key]
    
    yield os.environ
    
    # Teardown: restore environment:
    for key, value in stash.items():
        os.environ[key] = value

class TestFsAppdirectories(object):
    
    """ Run the tests for the clu.fs.appdirectories module. """
    # DARWIN, WIN32, LINUX, LINUX2
    
    appname = "TestApp"
    appauthor = "OST"
    appversion = "1.2.4"
    
    def test_LINUX_yes_version_no_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s/%s" % (appname, appversion)
        assert appdirs.site_data_dir    == "/usr/local/share/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s/%s" % (home, appname, appversion)
        assert appdirs.user_config_dir  == "%s/.config/%s/%s" % (home, appname, appversion)
        assert appdirs.user_data_dir    == "%s/.local/share/%s/%s" % (home, appname, appversion)
        assert appdirs.user_log_dir     == "%s/.cache/%s/%s/log" % (home, appname, appversion)
        assert appdirs.user_state_dir   == "%s/.local/state/%s/%s" % (home, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_LINUX_yes_version_yes_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        appdirs = AppDirs(appname, appauthor, version=appversion, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s/%s" % (appname, appversion)
        assert appdirs.site_data_dir    == "/usr/local/share/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s/%s" % (home, appname, appversion)
        assert appdirs.user_config_dir  == "%s/.config/%s/%s" % (home, appname, appversion)
        assert appdirs.user_data_dir    == "%s/.local/share/%s/%s" % (home, appname, appversion)
        assert appdirs.user_log_dir     == "%s/.cache/%s/%s/log" % (home, appname, appversion)
        assert appdirs.user_state_dir   == "%s/.local/state/%s/%s" % (home, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_LINUX_no_version_no_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s" % appname
        assert appdirs.site_data_dir    == "/usr/local/share/%s" % appname
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s" % (home, appname)
        assert appdirs.user_config_dir  == "%s/.config/%s" % (home, appname)
        assert appdirs.user_data_dir    == "%s/.local/share/%s" % (home, appname)
        assert appdirs.user_log_dir     == "%s/.cache/%s/log" % (home, appname)
        assert appdirs.user_state_dir   == "%s/.local/state/%s" % (home, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_LINUX_no_version_yes_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appdirs = AppDirs(appname, appauthor, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s" % appname
        assert appdirs.site_data_dir    == "/usr/local/share/%s" % appname
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s" % (home, appname)
        assert appdirs.user_config_dir  == "%s/.config/%s" % (home, appname)
        assert appdirs.user_data_dir    == "%s/.local/share/%s" % (home, appname)
        assert appdirs.user_log_dir     == "%s/.cache/%s/log" % (home, appname)
        assert appdirs.user_state_dir   == "%s/.local/state/%s" % (home, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_LINUX2_yes_version_no_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion, system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s/%s" % (appname, appversion)
        assert appdirs.site_data_dir    == "/usr/local/share/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s/%s" % (home, appname, appversion)
        assert appdirs.user_config_dir  == "%s/.config/%s/%s" % (home, appname, appversion)
        assert appdirs.user_data_dir    == "%s/.local/share/%s/%s" % (home, appname, appversion)
        assert appdirs.user_log_dir     == "%s/.cache/%s/%s/log" % (home, appname, appversion)
        assert appdirs.user_state_dir   == "%s/.local/state/%s/%s" % (home, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_LINUX2_yes_version_yes_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        appdirs = AppDirs(appname, appauthor, version=appversion, system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s/%s" % (appname, appversion)
        assert appdirs.site_data_dir    == "/usr/local/share/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s/%s" % (home, appname, appversion)
        assert appdirs.user_config_dir  == "%s/.config/%s/%s" % (home, appname, appversion)
        assert appdirs.user_data_dir    == "%s/.local/share/%s/%s" % (home, appname, appversion)
        assert appdirs.user_log_dir     == "%s/.cache/%s/%s/log" % (home, appname, appversion)
        assert appdirs.user_state_dir   == "%s/.local/state/%s/%s" % (home, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_LINUX2_no_version_no_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s" % appname
        assert appdirs.site_data_dir    == "/usr/local/share/%s" % appname
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s" % (home, appname)
        assert appdirs.user_config_dir  == "%s/.config/%s" % (home, appname)
        assert appdirs.user_data_dir    == "%s/.local/share/%s" % (home, appname)
        assert appdirs.user_log_dir     == "%s/.cache/%s/log" % (home, appname)
        assert appdirs.user_state_dir   == "%s/.local/state/%s" % (home, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_LINUX2_no_version_yes_author(self, environment):
        home = environment.get('HOME', '/tmp')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appdirs = AppDirs(appname, appauthor, system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/usr/local/etc/xdg/%s" % appname
        assert appdirs.site_data_dir    == "/usr/local/share/%s" % appname
        
        assert appdirs.user_cache_dir   == "%s/.cache/%s" % (home, appname)
        assert appdirs.user_config_dir  == "%s/.config/%s" % (home, appname)
        assert appdirs.user_data_dir    == "%s/.local/share/%s" % (home, appname)
        assert appdirs.user_log_dir     == "%s/.cache/%s/log" % (home, appname)
        assert appdirs.user_state_dir   == "%s/.local/state/%s" % (home, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_DARWIN_yes_version_no_author(self, environment):
        user = environment.get('USER', 'nobody')
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion, system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/Library/Preferences/%s" % appname
        assert appdirs.site_data_dir    == "/Library/Application Support/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "/Users/%s/Library/Caches/%s/%s" % (user, appname, appversion)
        assert appdirs.user_config_dir  == "/Users/%s/Library/Preferences/%s/%s" % (user, appname, appversion)
        assert appdirs.user_data_dir    == "/Users/%s/Library/Application Support/%s/%s" % (user, appname, appversion)
        assert appdirs.user_log_dir     == "/Users/%s/Library/Logs/%s/%s" % (user, appname, appversion)
        assert appdirs.user_state_dir   == "/Users/%s/Library/Application Support/%s/%s" % (user, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_DARWIN_yes_version_yes_author(self, environment):
        user = environment.get('USER', 'nobody')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        appdirs = AppDirs(appname, appauthor, version=appversion, system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/Library/Preferences/%s" % appname
        assert appdirs.site_data_dir    == "/Library/Application Support/%s/%s" % (appname, appversion)
        
        assert appdirs.user_cache_dir   == "/Users/%s/Library/Caches/%s/%s" % (user, appname, appversion)
        assert appdirs.user_config_dir  == "/Users/%s/Library/Preferences/%s/%s" % (user, appname, appversion)
        assert appdirs.user_data_dir    == "/Users/%s/Library/Application Support/%s/%s" % (user, appname, appversion)
        assert appdirs.user_log_dir     == "/Users/%s/Library/Logs/%s/%s" % (user, appname, appversion)
        assert appdirs.user_state_dir   == "/Users/%s/Library/Application Support/%s/%s" % (user, appname, appversion)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
    
    def test_DARWIN_no_version_no_author(self, environment):
        user = environment.get('USER', 'nobody')
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/Library/Preferences/%s" % appname
        assert appdirs.site_data_dir    == "/Library/Application Support/%s" % appname
        
        assert appdirs.user_cache_dir   == "/Users/%s/Library/Caches/%s" % (user, appname)
        assert appdirs.user_config_dir  == "/Users/%s/Library/Preferences/%s" % (user, appname)
        assert appdirs.user_data_dir    == "/Users/%s/Library/Application Support/%s" % (user, appname)
        assert appdirs.user_log_dir     == "/Users/%s/Library/Logs/%s" % (user, appname)
        assert appdirs.user_state_dir   == "/Users/%s/Library/Application Support/%s" % (user, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_DARWIN_no_version_yes_author(self, environment):
        user = environment.get('USER', 'nobody')
        appname = type(self).appname
        appauthor = type(self).appauthor
        appdirs = AppDirs(appname, appauthor, system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == "/Library/Preferences/%s" % appname
        assert appdirs.site_data_dir    == "/Library/Application Support/%s" % appname
        
        assert appdirs.user_cache_dir   == "/Users/%s/Library/Caches/%s" % (user, appname)
        assert appdirs.user_config_dir  == "/Users/%s/Library/Preferences/%s" % (user, appname)
        assert appdirs.user_data_dir    == "/Users/%s/Library/Application Support/%s" % (user, appname)
        assert appdirs.user_log_dir     == "/Users/%s/Library/Logs/%s" % (user, appname)
        assert appdirs.user_state_dir   == "/Users/%s/Library/Application Support/%s" % (user, appname)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == None
        assert appdirs.version_info     == None
    
    def test_WIN32_yes_version_no_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    def test_WIN32_yes_version_yes_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    def test_WIN32_no_version_no_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    def test_WIN32_no_version_yes_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
