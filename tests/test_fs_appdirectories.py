# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from clu.constants.enums import System
from clu.fs.appdirectories import AppDirs, UnusedValueWarning # ?!
from clu.fs.appdirectories import clu_appdirs
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
    
    @pytest.fixture(scope='module')
    def arbitrary(self):
        """ Fixture function furnishing exemplary initial AppDirs values """
        yield {
            'name'      : "TestApp",
            'author'    : "OST",
            'version'   : "1.2.4"
        }
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_yes_version_no_author(self, arbitrary,
                                         system,
                                         consts,
                                         environment):
        """ Arbitrary app info, with versioning, sans author """
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appversion = arbitrary['version']
        appdirs = AppDirs(appname, version=appversion, system=system)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == system
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_yes_version_yes_author(self, arbitrary,
                                          system,
                                          consts,
                                          environment):
        """ Arbitrary app info, with versioning and author """
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        appversion = arbitrary['version']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                               version=appversion,
                                system=system)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == system
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_no_version_no_author(self, arbitrary,
                                        system,
                                        consts,
                                        environment):
        """ Arbitrary app info, sans both versioning and author """
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appdirs = AppDirs(appname, system=system)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == system
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_no_version_yes_author(self, arbitrary,
                                         system,
                                         consts,
                                         environment):
        """ Arbitrary app info, sans versioning, with author """
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                                system=system)
        
        for xdg in XDGS:
            assert xdg not in environment
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.system           == system
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_clu_appdirs_versioned(self, system,
                                         consts,
                                         environment,
                                         cluversion):
        """ CLU-specific app info, with versioning """
        import clu
        
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appdirs = clu_appdirs(system=system)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.appauthor        == clu.__author__
        assert appdirs.system           == system
        assert appdirs.version          == cluversion.to_string()
        assert appdirs.version_info     == cluversion
        assert str(appdirs) == repr(appdirs)
        
        assert appdirs is clu_appdirs(system=system)
    
    @pytest.mark.parametrize('system', System.unixes())
    def test_clu_appdirs_unversioned(self, system,
                                           consts,
                                           environment):
        """ CLU-specific app info, without versioning """
        import clu
        
        # user = environment.get('USER', consts.USER)
        # home = environment.get('HOME', gethomedir())
        appdirs = clu_appdirs(system=system,
                              versioning=False)
        
        assert type(appdirs.site_config)    is Directory
        assert type(appdirs.site_data)      is Directory
        
        assert type(appdirs.user_cache)     is Directory
        assert type(appdirs.user_config)    is Directory
        assert type(appdirs.user_data)      is Directory
        assert type(appdirs.user_log)       is Directory
        assert type(appdirs.user_state)     is Directory
        
        assert appdirs.appauthor        == clu.__author__
        assert appdirs.system           == system
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
        
        assert appdirs is clu_appdirs(system=system,
                                      versioning=False)
    
    ### END OF PARAMETRIZATION W.I.P. ###
    ### END OF PARAMETRIZATION W.I.P. ###
    ### END OF PARAMETRIZATION W.I.P. ###
    
    def test_LINUX_yes_version_no_author(self, arbitrary,
                                               environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appversion = arbitrary['version']
        appdirs = AppDirs(appname, version=appversion, system=System.LINUX)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_yes_version_yes_author(self, arbitrary,
                                                environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        appversion = arbitrary['version']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                               version=appversion,
                                system=System.LINUX)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_no_version_no_author(self, arbitrary,
                                              environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appdirs = AppDirs(appname, system=System.LINUX)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX_no_version_yes_author(self, arbitrary,
                                               environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                                system=System.LINUX)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
        assert appdirs.system           == System.LINUX
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_yes_version_no_author(self, arbitrary,
                                                environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appversion = arbitrary['version']
        appdirs = AppDirs(appname, version=appversion,
                                    system=System.LINUX2)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_yes_version_yes_author(self, arbitrary,
                                                 environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        appversion = arbitrary['version']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                               version=appversion,
                                system=System.LINUX2)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}/{appversion}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/{appversion}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}/{appversion}"
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_no_version_no_author(self, arbitrary,
                                               environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appdirs = AppDirs(appname, system=System.LINUX2)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    def test_LINUX2_no_version_yes_author(self, arbitrary,
                                                environment):
        home = environment.get('HOME', gethomedir())
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                                system=System.LINUX2)
        
        assert appdirs.site_config_dir  == f"/usr/local/etc/xdg/{appname}"
        assert appdirs.site_data_dir    == f"/usr/local/share/{appname}"
        
        assert appdirs.user_cache_dir   == f"{home}/.cache/{appname}"
        assert appdirs.user_config_dir  == f"{home}/.config/{appname}"
        assert appdirs.user_data_dir    == f"{home}/.local/share/{appname}"
        assert appdirs.user_log_dir     == f"{home}/.cache/{appname}/log"
        assert appdirs.user_state_dir   == f"{home}/.local/state/{appname}"
        
        assert appdirs.system           == System.LINUX2
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_yes_version_no_author(self, arbitrary,
                                                environment,
                                                consts):
        user = environment.get('USER', consts.USER)
        appname = arbitrary['name']
        appversion = arbitrary['version']
        appdirs = AppDirs(appname, version=appversion,
                                    system=System.DARWIN)
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}/{appversion}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_yes_version_yes_author(self, arbitrary,
                                                 environment,
                                                 consts):
        user = environment.get('USER', consts.USER)
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        appversion = arbitrary['version']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                               version=appversion,
                                system=System.DARWIN)
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}/{appversion}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}/{appversion}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}/{appversion}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}/{appversion}"
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == appversion
        
        assert str(appdirs.version_info) == str(VersionInfo(appversion))
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_no_version_no_author(self, arbitrary,
                                               environment,
                                               consts):
        user = environment.get('USER', consts.USER)
        appname = arbitrary['name']
        appdirs = AppDirs(appname, system=System.DARWIN)
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}"
        
        assert appdirs.system           == System.DARWIN
        assert appdirs.version          == None
        assert appdirs.version_info     == None
        assert str(appdirs) == repr(appdirs)
    
    def test_DARWIN_no_version_yes_author(self, arbitrary,
                                                environment,
                                                consts):
        user = environment.get('USER', consts.USER)
        appname = arbitrary['name']
        appauthor = arbitrary['author']
        
        with pytest.warns(UnusedValueWarning):
            appdirs = AppDirs(appname, appauthor,
                               roaming=True,
                                system=System.DARWIN)
        
        assert appdirs.site_config_dir  == f"/Library/Preferences/{appname}"
        assert appdirs.site_data_dir    == f"/Library/Application Support/{appname}"
        
        assert appdirs.user_cache_dir   == f"/Users/{user}/Library/Caches/{appname}"
        assert appdirs.user_config_dir  == f"/Users/{user}/Library/Preferences/{appname}"
        assert appdirs.user_data_dir    == f"/Users/{user}/Library/Application Support/{appname}"
        assert appdirs.user_log_dir     == f"/Users/{user}/Library/Logs/{appname}"
        assert appdirs.user_state_dir   == f"/Users/{user}/Library/Application Support/{appname}"
        
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
