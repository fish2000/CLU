# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from clu.constants.enums import System
from clu.fs.appdirectories import AppDirs, UnusedValueWarning # ?!
from clu.fs.filesystem import Directory
from clu.fs.misc import gethomedir
from clu.version import VersionInfo

XDGS = ('XDG_CONFIG_DIRS', 'XDG_DATA_HOME',
        'XDG_CONFIG_HOME', 'XDG_DATA_DIRS',
                          'XDG_CACHE_HOME',
                          'XDG_STATE_HOME',
                         'XDG_RUNTIME_DIR')

class TestFsAppdirectories(object):
    
    """ Run the tests for the clu.fs.appdirectories module. """
    # DARWIN, WIN32, LINUX, LINUX2
    
    appname = "TestApp"
    appauthor = "OST"
    appversion = "1.2.4"
    
    def test_LINUX_yes_version_no_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_yes_version_yes_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               version=appversion,
                                system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_no_version_no_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_no_version_yes_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appauthor = type(self).appauthor
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                                system=System.LINUX)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_yes_version_no_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion,
                                    system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_yes_version_yes_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               version=appversion,
                                system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_no_version_no_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_no_version_yes_author(self, environment):
        home = environment.get('HOME', gethomedir())
        appname = type(self).appname
        appauthor = type(self).appauthor
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                                system=System.LINUX2)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_yes_version_no_author(self, environment, consts):
        user = environment.get('USER', consts.USER)
        appname = type(self).appname
        appversion = type(self).appversion
        appdirs = AppDirs(appname, version=appversion,
                                    system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}/{appversion}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_yes_version_yes_author(self, environment, consts):
        user = environment.get('USER', consts.USER)
        appname = type(self).appname
        appauthor = type(self).appauthor
        appversion = type(self).appversion
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               version=appversion,
                                system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}/{appversion}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_no_version_no_author(self, environment, consts):
        user = environment.get('USER', consts.USER)
        appname = type(self).appname
        appdirs = AppDirs(appname, system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_no_version_yes_author(self, environment, consts):
        user = environment.get('USER', consts.USER)
        appname = type(self).appname
        appauthor = type(self).appauthor
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                                system=System.DARWIN)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}"
        
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
        assert str(appdirs) == repr(appdirs)
    
    @pytest.mark.TODO
    def test_WIN32_yes_version_no_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    @pytest.mark.TODO
    def test_WIN32_yes_version_yes_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    @pytest.mark.TODO
    def test_WIN32_no_version_no_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
    
    @pytest.mark.TODO
    def test_WIN32_no_version_yes_author(self, environment):
        """ Win32 tests TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
