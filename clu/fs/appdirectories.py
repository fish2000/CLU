# -*- coding: utf-8 -*-
from __future__ import print_function

"""
Utilities for determining application-specific dirs.

Copyright (c) 2005-2010 ActiveState Software Inc.
Copyright (c) 2013 Eddy Petrișor
Copyright  ©  2019 Alexander Böhn

For details and usage, q.v. https://github.com/fish2000/CLU sub.

Dev Notes:
- MSDN on where to store app data files:
  http://support.microsoft.com/default.aspx?scid=kb;en-us;310294#XSLTH3194121123120121120120
- Mac OS X: http://developer.apple.com/documentation/MacOSX/Conceptual/BPFileSystem/index.html
- XDG spec for Un*x: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

import sys
import os
import platform
import warnings

from clu.constants.consts import ENCODING, PY3
from clu.constants.enums import CSIDL, System, SYSTEM
from clu.constants.exceptions import UnusedValueWarning
from clu.fs.filesystem import Directory
from clu.repr import stringify
from clu.version import VersionInfo
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# Module-specific version/version-info:
__version__ = "2.2.0"
__version_info__ = VersionInfo(__version__)

@export
class AppDirs(object):
    
    """ Convenience wrapper for getting application dirs. """
    
    fields = ('appname', 'appauthor',
              'roaming', 'multipath',
              'system',  'version',
                         'version_info',
              
              'site_config', 'site_data',
              'user_cache',  'user_config',
              'user_data',   'user_log',
              'user_state')
    
    def __new__(cls, *args, **kwargs):
        """ Overriden `__new__(…)` installs version variables –
            the names of which would cause a shadow-name situation
            if they were to be set normally within `__init__(…)`
        """
        instance = super(AppDirs, cls).__new__(cls)
        setattr(instance, '__version__',      __version__)
        setattr(instance, '__version_info__', __version_info__)
        return instance
    
    def __init__(self, appname=None,
                       appauthor=None,
                       roaming=False,
                       multipath=False,
                       system=None,
                       version=None):
        """ Call `__init__(…)` to initialize an AppDirs instance with
            whichever of the myriad naming options are important to you
            and whatever it is you happen to be doing
        """
        # The name of the application:
        self.appname = appname
        
        # These next three data only matter on Windows:
        self.appauthor = appauthor
        self.roaming = bool(roaming)
        self.multipath = bool(multipath)
        
        # System and Version can be specified as instances of the System enum
        # or of clu.version.VersuionInfo, respectively:
        self.system = system and System.match(system) or SYSTEM
        self.version = version and str(version) or None
        self.version_info = version and VersionInfo(version) or None
        
        if self.system == System.WIN32:
            # On Windows, choose the most expedient Win32 interface for
            # getting user- and system-related folder paths:
            self._win_folder_function = self.determine_win_folder_function()
            
        else:
            # On non-Windows platforms, warn when options relevant only to
            # Windows-y OSes have been specified:
            if appauthor is not None:
                warnings.warn("The “appauthor” value is currently only used under Windows",
                              UnusedValueWarning, stacklevel=2)
            if roaming:
                warnings.warn("The “roaming” option is currently only used under Windows",
                              UnusedValueWarning, stacklevel=2)
            if multipath:
                warnings.warn("The “multipath” option is currently only used under Windows",
                              UnusedValueWarning, stacklevel=2)
    
    def determine_system_string(self):
        """ Determine upon which system this AppDirs instance has been brought
            into existence – DEPRECIATED, see the appdirectories.System enum
            class (and the System.determine() class method in particular) for
            the replcaement logic
        """
        if sys.platform.startswith('java'):
            os_name = platform.java_ver()[3][0]
            if os_name.startswith('Windows'): # "Windows XP", "Windows 7", etc.
                system = 'win32'
            elif os_name.startswith('Mac'): # "Mac OS X", etc.
                system = 'darwin'
            else: # "Linux", "SunOS", "FreeBSD", etc.
                # Setting this to "linux2" is not ideal, but only Windows or Mac
                # are actually checked for and the rest of the module expects
                # *sys.platform* style strings.
                system = 'linux2'
        else:
            system = sys.platform
        return system
    
    def determine_win_folder_function(self):
        """ Use successive imports to determine the best folder-finding method
            to employ on Windows.
            
            These are all dummy imports – they differ from actual (albiet similar
            and related) modules imported by each of the respective Windows-native
            functions; that’s why we delete whatever we managed to import before
            returning the function.
        """
        try:
            import win32com.shell as win32api
            out = get_win_folder_with_pywin32
        except ImportError:
            try:
                from ctypes import windll as win32api
                out = get_win_folder_with_ctypes
            except ImportError:
                try:
                    import com.sun.jna as win32api
                    out = get_win_folder_with_jna
                except ImportError:
                    win32api = None
                    out = get_win_folder_from_registry
        del win32api
        return out
    
    def to_string(self):
        """ Stringify the AppDirs instance. """
        return stringify(self, type(self).fields)
    
    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)
    
    @property
    def user_data_dir(self):
        """ The userland application-specific data directory """
        return self.get_user_data_dir(self.appname, self.appauthor,
                                                    version=self.version,
                                                    roaming=self.roaming)
    
    @property
    def site_data_dir(self):
        """ The system-wide application-specific data directory """
        return self.get_site_data_dir(self.appname, self.appauthor,
                                                    version=self.version,
                                                    multipath=self.multipath)
    
    @property
    def user_config_dir(self):
        """ The userland configuration directory """
        return self.get_user_config_dir(self.appname, self.appauthor,
                                                      version=self.version,
                                                      roaming=self.roaming)
    
    @property
    def site_config_dir(self):
        """ The system-wide configuration directory """
        return self.get_site_config_dir(self.appname, self.appauthor,
                                                      version=self.version,
                                                      multipath=self.multipath)
    
    @property
    def user_cache_dir(self):
        """ The userland cache directory """
        return self.get_user_cache_dir(self.appname, self.appauthor,
                                                     version=self.version)
    
    @property
    def user_state_dir(self):
        """ The userland state-stash directory """
        return self.get_user_state_dir(self.appname, self.appauthor,
                                                     version=self.version)
    
    @property
    def user_log_dir(self):
        """ The userland log directory """
        return self.get_user_log_dir(self.appname, self.appauthor,
                                                   version=self.version)
    
    @property
    def site_config(self):
        return Directory(self.site_config_dir)
    
    @property
    def site_data(self):
        return Directory(self.site_data_dir)
    
    @property
    def user_cache(self):
        return Directory(self.user_cache_dir)
    
    @property
    def user_config(self):
        return Directory(self.user_config_dir)
    
    @property
    def user_data(self):
        return Directory(self.user_data_dir)
    
    @property
    def user_log(self):
        return Directory(self.user_log_dir)
    
    @property
    def user_state(self):
        return Directory(self.user_state_dir)
    
    def get_win_folder(self, argument):
        """ Retrieve the module-private Win32 API access function from
            the AppDirs instance (so as not to invoke it as a bound method)
            before calling it with the supplied argument
        """
        return os.path.normpath(
                        getattr(self, '_win_folder_function',
                                       lambda thing: str(thing))(argument))
    
    def get_user_data_dir(self, appname=None,
                                appauthor=None,
                                version=None,
                                roaming=False):
        r"""Return full path to the user-specific data dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "roaming" (boolean, default False) can be set True to use the Windows
                roaming appdata directory. That means that for users on a Windows
                network setup for roaming profiles, this user data will be
                sync'd on login. See
                <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
                for a discussion of issues.
                
        Typical user data directories are:
            Mac OS X:               ~/Library/Application Support/<AppName>
            Unix:                   ~/.local/share/<AppName>    # or in $XDG_DATA_HOME, if defined
            Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\<AppAuthor>\<AppName>
            Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>
            Win 7  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
            Win 7  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>
        
        For Unix, we follow the XDG spec and support $XDG_DATA_HOME.
        That means, by default "~/.local/share/<AppName>".
        """
        if self.system == System.WIN32:
            if appauthor is None:
                appauthor = appname
            path = self.get_win_folder(roaming and CSIDL.APPDATA \
                                          or CSIDL.LOCAL_APPDATA)
            if appname:
                if appauthor is not False:
                    path = os.path.join(path, appauthor, appname)
                else:
                    path = os.path.join(path, appname)
        elif self.system == System.DARWIN:
            path = os.path.expanduser('~/Library/Application Support/')
            if appname:
                path = os.path.join(path, appname)
        else:
            path = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))
            if appname:
                path = os.path.join(path, appname)
        if appname and version:
            path = os.path.join(path, version)
        return path
    
    def get_site_data_dir(self, appname=None,
                                appauthor=None,
                                version=None,
                                multipath=False):
        r"""Return full path to the user-shared data dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "multipath" is an optional parameter only applicable to *nix
                which indicates that the entire list of data dirs should be
                returned. By default, the first item from XDG_DATA_DIRS is
                returned, or '/usr/local/share/<AppName>',
                if XDG_DATA_DIRS is not set
                
        Typical site data directories are:
            Mac OS X:   /Library/Application Support/<AppName>
            Unix:       /usr/local/share/<AppName> or /usr/share/<AppName>
            Win XP:     C:\Documents and Settings\All Users\Application Data\<AppAuthor>\<AppName>
            Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)
            Win 7:      C:\ProgramData\<AppAuthor>\<AppName>   # Hidden, but writeable on Win 7.
        
        For Unix, this is using the $XDG_DATA_DIRS[0] default.
        
        WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
        """
        if self.system == System.WIN32:
            if appauthor is None:
                appauthor = appname
            path = self.get_win_folder(CSIDL.COMMON_APPDATA)
            if appname:
                if appauthor is not False:
                    path = os.path.join(path, appauthor, appname)
                else:
                    path = os.path.join(path, appname)
        elif self.system == System.DARWIN:
            path = '/Library/Application Support'
            if appname:
                path = os.path.join(path, appname)
        else:
            # XDG default for $XDG_DATA_DIRS
            # only first, if multipath is False
            path = os.getenv('XDG_DATA_DIRS',
                              os.pathsep.join(('/usr/local/share', '/usr/share')))
            pathlist = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
            if appname:
                if version:
                    appname = os.path.join(appname, version)
                pathlist = [os.sep.join([x, appname]) for x in pathlist]
                
            if multipath:
                path = os.pathsep.join(pathlist)
            else:
                path = pathlist[0]
            return path
        
        if appname and version:
            path = os.path.join(path, version)
        return path
    
    def get_user_config_dir(self, appname=None,
                                  appauthor=None,
                                  version=None,
                                  roaming=False):
        r"""Return full path to the user-specific config dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "roaming" (boolean, default False) can be set True to use the Windows
                roaming appdata directory. That means that for users on a Windows
                network setup for roaming profiles, this user data will be
                sync'd on login. See
                <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
                for a discussion of issues.
                
        Typical user config directories are:
            Mac OS X:               ~/Library/Preferences/<AppName>
            Unix:                   ~/.config/<AppName>     # or in $XDG_CONFIG_HOME, if defined
            Win *:                  same as user_data_dir
        
        For Unix, we follow the XDG spec and support $XDG_CONFIG_HOME.
        That means, by default "~/.config/<AppName>".
        """
        if self.system == System.WIN32:
            path = self.get_user_data_dir(appname, appauthor, None, roaming)
        elif self.system == System.DARWIN:
            path = os.path.expanduser('~/Library/Preferences/')
            if appname:
                path = os.path.join(path, appname)
        else:
            path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
            if appname:
                path = os.path.join(path, appname)
        if appname and version:
            path = os.path.join(path, version)
        return path
    
    def get_site_config_dir(self, appname=None,
                                  appauthor=None,
                                  version=None,
                                  multipath=False):
        r"""Return full path to the user-shared data dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "multipath" is an optional parameter only applicable to *nix
                which indicates that the entire list of config dirs should be
                returned. By default, the first item from XDG_CONFIG_DIRS is
                returned, or '/etc/xdg/<AppName>', if XDG_CONFIG_DIRS is not set
                
        Typical site config directories are:
            Mac OS X:   same as site_data_dir
            Unix:       /etc/xdg/<AppName> or $XDG_CONFIG_DIRS[i]/<AppName> for each value in
                        $XDG_CONFIG_DIRS
            Win *:      same as site_data_dir
            Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)
        
        For Unix, this is using the $XDG_CONFIG_DIRS[0] default, if multipath=False
        
        WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
        """
        if self.system == System.WIN32:
            path = self.get_site_data_dir(appname, appauthor)
            if appname and version:
                path = os.path.join(path, version)
        elif self.system == System.DARWIN:
            path = '/Library/Preferences'
            if appname:
                path = os.path.join(path, appname)
        else:
            # XDG default for $XDG_CONFIG_DIRS
            # only first, if multipath is False
            path = os.getenv('XDG_CONFIG_DIRS',
                              os.pathsep.join(('/usr/local/etc/xdg', '/etc/xdg')))
            pathlist = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
            if appname:
                if version:
                    appname = os.path.join(appname, version)
                pathlist = [os.sep.join([x, appname]) for x in pathlist]
            
            if multipath:
                path = os.pathsep.join(pathlist)
            else:
                path = pathlist[0]
        return path
    
    def get_user_cache_dir(self, appname=None,
                                 appauthor=None,
                                 version=None,
                                 opinion=True):
        r"""Return full path to the user-specific cache dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "opinion" (boolean) can be False to disable the appending of
                "Cache" to the base app data dir for Windows. See
                discussion below.
        
        Typical user cache directories are:
            Mac OS X:   ~/Library/Caches/<AppName>
            Unix:       ~/.cache/<AppName> (XDG default)
            Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Cache
            Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Cache
        
        On Windows the only suggestion in the MSDN docs is that local settings go in
        the `CSIDL_LOCAL_APPDATA` directory. This is identical to the non-roaming
        app data dir (the default returned by `user_data_dir` above). Apps typically
        put cache data somewhere *under* the given dir here. Some examples:
            ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
            ...\Acme\SuperApp\Cache\1.0
        OPINION: This function appends "Cache" to the `CSIDL_LOCAL_APPDATA` value.
        This can be disabled with the `opinion=False` option.
        """
        if self.system == System.WIN32:
            if appauthor is None:
                appauthor = appname
            path = self.get_win_folder(CSIDL.LOCAL_APPDATA)
            if appname:
                if appauthor is not False:
                    path = os.path.join(path, appauthor, appname)
                else:
                    path = os.path.join(path, appname)
                if opinion:
                    path = os.path.join(path, "Cache")
        elif self.system == System.DARWIN:
            path = os.path.expanduser('~/Library/Caches')
            if appname:
                path = os.path.join(path, appname)
        else:
            path = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
            if appname:
                path = os.path.join(path, appname)
        if appname and version:
            path = os.path.join(path, version)
        return path
    
    def get_user_state_dir(self, appname=None,
                                 appauthor=None,
                                 version=None,
                                 roaming=False):
        r"""Return full path to the user-specific state dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "roaming" (boolean, default False) can be set True to use the Windows
                roaming appdata directory. That means that for users on a Windows
                network setup for roaming profiles, this user data will be
                sync'd on login. See
                <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
                for a discussion of issues.
        
        Typical user state directories are:
            Mac OS X:  same as user_data_dir
            Unix:      ~/.local/state/<AppName>   # or in $XDG_STATE_HOME, if defined
            Win *:     same as user_data_dir
        
        For Unix, we follow this Debian proposal <https://wiki.debian.org/XDGBaseDirectorySpecification#state>
        to extend the XDG spec and support $XDG_STATE_HOME.
        
        That means, by default "~/.local/state/<AppName>".
        """
        if self.system in (System.WIN32, System.DARWIN):
            path = self.get_user_data_dir(appname, appauthor, None, roaming)
        else:
            path = os.getenv('XDG_STATE_HOME', os.path.expanduser("~/.local/state"))
            if appname:
                path = os.path.join(path, appname)
        if appname and version:
            path = os.path.join(path, version)
        return path
    
    def get_user_log_dir(self, appname=None,
                               appauthor=None,
                               version=None,
                               opinion=True):
        r"""Return full path to the user-specific log dir for this application.
            
            "appname" is the name of application.
                If None, just the system directory is returned.
            "appauthor" (only used on Windows) is the name of the
                appauthor or distributing body for this application. Typically
                it is the owning company name. This falls back to appname. You may
                pass False to disable it.
            "version" is an optional version path element to append to the
                path. You might want to use this if you want multiple versions
                of your app to be able to run independently. If used, this
                would typically be "<major>.<minor>".
                Only applied when appname is present.
            "opinion" (boolean) can be False to disable the appending of
                "Logs" to the base app data dir for Windows, and "log" to the
                base cache dir for Unix. See discussion below.
        
        Typical user log directories are:
            Mac OS X:   ~/Library/Logs/<AppName>
            Unix:       ~/.cache/<AppName>/log  # or under $XDG_CACHE_HOME if defined
            Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Logs
            Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Logs
        
        On Windows the only suggestion in the MSDN docs is that local settings
        go in the `CSIDL_LOCAL_APPDATA` directory. (Note: I'm interested in
        examples of what some windows apps use for a logs dir.)
        
        OPINION: This function appends "Logs" to the `CSIDL_LOCAL_APPDATA`
        value for Windows and appends "log" to the user cache dir for Unix.
        This can be disabled with the `opinion=False` option.
        """
        if self.system == System.DARWIN:
            path = os.path.join(
                os.path.expanduser('~/Library/Logs'),
                appname)
        elif self.system == System.WIN32:
            path = self.get_user_data_dir(appname, appauthor, version)
            version = False
            if opinion:
                path = os.path.join(path, "Logs")
        else:
            path = self.get_user_cache_dir(appname, appauthor, version)
            version = False
            if opinion:
                path = os.path.join(path, "log")
        if appname and version:
            path = os.path.join(path, version)
        return path

# Internal Windows directory-retrieval support stuff:

def get_win_folder_from_registry(csidl):
    """ This is a fallback technique at best. I'm not sure if using the
        sregistry for this guarantees us the correct answer for all CSIDL_*
        names.
            – Eddy Petrișor
    """
    if PY3:
        import winreg
    else:
        import _winreg as winreg
    
    key = winreg.OpenKey(
          winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    directory, _ = winreg.QueryValueEx(key, csidl.shell_folder_name)
    return directory

def get_win_folder_with_pywin32(csidl):
    """ Use the PyWin32 Python C-API wrappers to make a fairly direct
        win32 filesystem API call
    """
    from win32com.shell import shellcon, shell
    
    directory = shell.SHGetFolderPath(0, getattr(shellcon, csidl.fullname), 0, 0)
    
    # Try to make this a unicode path because SHGetFolderPath does
    # not return unicode strings when there is unicode data in the
    # path.
    try:
        directory = str(directory, encoding=ENCODING)
        
        # Downgrade to short path name if have highbit chars. See
        # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
        has_high_char = False
        for char in directory:
            if ord(char) > 255:
                has_high_char = True
                break
        if has_high_char:
            try:
                import win32api
                directory = win32api.GetShortPathName(directory)
            except ImportError:
                pass
    except UnicodeError:
        pass
    
    return directory

def get_win_folder_with_ctypes(csidl):
    """ Use ctypes to call into the win32 filesystem API """
    import ctypes
    
    buf = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl.const, None, 0, buf)
    
    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for char in buf:
        if ord(char) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf2 = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2
    
    return buf.value

def get_win_folder_with_jna(csidl):
    """ Use the Python Java wrappers to invoke – circuitously,
        I might add – a win32 filesystem API call
    """
    import array
    from com.sun import jna
    from com.sun.jna.platform import win32
    
    buf_size = win32.WinDef.MAX_PATH * 2
    buf = array.zeros('c', buf_size)
    shell = win32.Shell32.INSTANCE
    shell.SHGetFolderPath(None, getattr(win32.ShlObj, csidl.fullname),
                          None, win32.ShlObj.SHGFP_TYPE_CURRENT, buf)
    
    directory = jna.Native.toString(buf.tostring()).rstrip("\0")
    
    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for char in directory:
        if ord(char) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf = array.zeros('c', buf_size)
        kernel = win32.Kernel32.INSTANCE
        if kernel.GetShortPathName(directory, buf, buf_size):
            directory = jna.Native.toString(buf.tostring()).rstrip("\0")
    
    return directory

export(System)
export(CSIDL)
export(SYSTEM,  name='SYSTEM')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    """ Inline tests for appdirectories """
    from clu.repl.ansi import print_separator
    
    appname = "MyApp"
    appauthor = "MyCompany"
    
    props = ("system", "version", "version_info",
             "site_config_dir", "site_data_dir",
             "user_cache_dir", "user_config_dir",
                               "user_data_dir",
                               "user_log_dir",
                               "user_state_dir")
    
    print(f"-- “appdirectories” __version__: {__version__} --")
    print()
    print()
    
    for system in System:
        
        print_separator()
        default = (system is SYSTEM) and "(DEFAULT)" or ""
        print(f"-- System: {system.to_string()} {default}")
        # print()
        
        if (system is not System.WIN32) or ((system is System.WIN32) \
                                        and (SYSTEM is System.WIN32)):
            
            print("-- app dirs (with optional 'version')")
            dirs = AppDirs(appname, appauthor, version="1.0", system=system)
            for prop in props:
                print("%20s : %s" % (prop, getattr(dirs, prop)))
            print()
            
            print("-- app dirs (without optional 'version')")
            dirs = AppDirs(appname, appauthor, system=system)
            for prop in props:
                print("%20s : %s" % (prop, getattr(dirs, prop)))
            print()
            
            print("-- app dirs (without optional 'appauthor')")
            dirs = AppDirs(appname, system=system)
            for prop in props:
                print("%20s : %s" % (prop, getattr(dirs, prop)))
            print()
            
            print("-- app dirs (with disabled 'appauthor')")
            dirs = AppDirs(appname, appauthor=False, system=system)
            for prop in props:
                print("%20s : %s" % (prop, getattr(dirs, prop)))
            print()
        
        else:
            
            print("-- skipping Win32 tests (Win32 API access required)")
            print()

if __name__ == "__main__":
    test()