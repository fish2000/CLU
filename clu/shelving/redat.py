# -*- encoding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import collections
import collections.abc
import logging
import multidict
import os
import re
import redis
import subprocess
import time

from clu.constants.consts import NoDefault
from clu.predicates import resolve, uniquify

from clu.dispatch import (signal_for,
                          exithandle,
                          shutdown)

from clu.fs.filesystem import (which,
                               TemporaryName,
                               TemporaryDirectory,
                                        Directory,
                                        Intermediate)

from clu.importing import Module
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

DO_IT_DOUG = False

@export
class RedisConf(clu.abstract.ManagedContext,
                collections.abc.MutableMapping,
                collections.abc.Sized,
                os.PathLike):
    
    """ Process Redis configuration-file options, and generate
        temporary configuration files, per use of instance methods
    """
    
    DEFAULT_SOURCE = '/usr/local/etc/redis.conf'
    COMMENT_RE = re.compile(r"#+(?:[\s\S]*)$")
    
    @staticmethod
    def compose(iterable):
        return ' '.join(iterable)
    
    @staticmethod
    def decompose(value):
        return tuple(value.split())
    
    @classmethod
    def decommentizer(cls):
        return lambda line: cls.COMMENT_RE.sub('', line).rstrip()
    
    def __init__(self, source=None,
                       directory=None,
                       port=6379, *,
                       follow_includes=True):
        """ Initialize a RedisConf instance – optionally with a given
            path to a configuration file and/or a specified port number
        """
        self.config = multidict.MultiDict()
        self.source = source or type(self).DEFAULT_SOURCE
        self.directory = directory
        self.port = port
        self.active = False
        self.process(self.source, follow_includes=follow_includes)
    
    def process(self, source, *, follow_includes=True):
        self.parse(source)
        if follow_includes:
            for include in self.get_includes():
                self.process(include)
    
    def parse(self, source):
        with open(source, 'r') as handle:
            lines = map(self.decommentizer(),
                    filter(None,
                    filter(lambda line: not line.startswith('#'),
                    map(lambda line: line.strip(),
                        handle.readlines()))))
        for line in lines:
            key, value = line.split(None, 1)
            self.add(key, value)
    
    def add(self, key, value):
        self.config.add(key, self.decompose(value))
    
    def set(self, key, value):
        self.config[key] = self.decompose(value)
    
    def get(self, key, default=NoDefault):
        if key in self.config:
            return self.compose(self.config.get(key))
        if default is NoDefault:
            raise KeyError(key)
        return default
    
    def set_boolean(self, key, value):
        self.set(key, value and 'yes' or 'no')
    
    def get_boolean(self, key):
        return self.get(key).casefold().strip() == 'yes'
    
    def get_host(self):
        return self.config.get('bind')[0]
    
    def set_port(self, port):
        if port == 0:
            self.set_unix_socket()
            return
        rdir = self.get_dir()
        self.set('port',            str(port))
        self.set('pidfile',         rdir.subpath(f"redis-tcp-{port}.pid"))
        if 'unixsocket' in self:
            del self['unixsocket']
        if 'unixsocketperm' in self:
            del self['unixsocketperm']
    
    def get_port(self):
        return int(self.get('port'), base=10)
    
    def set_unix_socket(self, perm=755):
        rdir = self.get_dir()
        self.set('port',            '0') # disable
        self.set('pidfile',         rdir.subpath("redis-unixsocket.pid"))
        self.set('unixsocket',      rdir.subpath("redis.sock"))
        self.set('unixsocketperm',  f'{perm!s}') # this may be bad
    
    def get_unix_socket(self):
        return self.get('unixsocket', None)
    
    def get_unix_socket_perm(self):
        return int(self.get('unixsocketperm', '755'), base=10)
    
    def set_dir(self, directory):
        self.set('dir', os.fspath(directory))
    
    def get_dir(self):
        return Directory(self.get('dir'))
    
    def get_includes(self):
        includes = []
        for value_parts in self.config.popall('include', tuple()):
            value = os.path.abspath(self.compose(value_parts))
            if not os.path.isfile(value):
                raise ValueError(f"bad include directive: {value}")
            includes.append(value)
        return tuple(includes)
    
    def getline(self, key):
        value = self.get(key)
        return f"{key} {value}"
    
    def getlines(self, key):
        if key not in self:
            raise KeyError(key)
        lines = []
        for value_parts in self.config.getall(key):
            value = self.compose(value_parts)
            lines.append(f"{key} {value}")
        return lines
    
    def getall(self):
        lines = []
        for key in uniquify(self.config.keys()):
            lines.extend(self.getlines(key))
        return lines
    
    def assemble(self):
        return "\n".join(self)
    
    @property
    def path(self):
        return resolve(self, 'file.name') or self.source
    
    @property
    def is_temporary(self):
        return resolve(self, 'rdir.__class__') is TemporaryDirectory
    
    def setup(self):
        if not self.active:
            rdir = Intermediate(self.directory)
            conf = TemporaryName(prefix='redis-config-',
                                 suffix='conf',
                                 parent=rdir,
                                 randomized=True)
            self.set_dir(rdir)
            self.set_port(self.port)
            self.set_boolean('appendonly', True)
            conf.write(self.assemble())
            self.rdir = rdir
            self.file = conf
            self.active = True
        return self
    
    def teardown(self):
        if self.active:
            # zout = '/tmp/redis-artifacts.zip'
            # if self.rdir:
            #     self.rdir.zip_archive(zout)
            if self.file:
                self.file.close()
                del self.file
            if self.rdir:
                self.rdir.close()
                del self.rdir
            self.active = False
    
    def get_command(self):
        return (which('redis-server'), self.path)
    
    def get_client(self):
        if not self.active:
            raise RuntimeError("RedisConf instance inactive")
        opts = {}
        if self.get_port() == 0:
            opts['unix_socket_path'] = self.get_unix_socket()
        else:
            opts['host'] = self.get_host()
            opts['port'] = self.get_port()
        return redis.Redis(**opts)
    
    def __fspath__(self):
        return self.path
    
    def __len__(self):
        return len(self.config)
    
    def __iter__(self):
        yield from self.getall()
    
    def __contains__(self, key):
        return key in self.config
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
    
    def __delitem__(self, key):
        del self.config[key]
    
    def __repr__(self):
        typename = type(self).__name__
        instance_id = hex(id(self))
        length = self.__len__()
        return f"{typename}<[{length} items]> @ {instance_id}"
    
    def __str__(self):
        return self.assemble()

class redprocess(Module):
    
    @export
    def get_config(self):
        return getattr(self, 'config', None)
    
    def set_config(self, config):
        self.config = config
    
    @export
    def get_process(self):
        return getattr(self, 'process', None)
    
    def set_process(self, process):
        self.process = process
    
    def __execute__(self):
        if DO_IT_DOUG:
            import logging
            
            formats = ('%(relativeCreated)6d',
                       '%(threadName)s',
                      '[%(module)s', '»', '%(funcName)s]',
                       '%(message)s')
            
            logging.basicConfig(level=logging.DEBUG,
                                format=' '.join(formats))
            
            logging.debug("Configuring Redis…")
            thisdir = Directory(os.path.dirname(__file__))
            thisconf = thisdir.subpath('redis.conf', requisite=True)
            assert os.path.exists(thisconf)
            
            self.set_config(RedisConf(thisconf, port=0))
            self.get_config().setup()
            
            logging.debug("Starting Redis server…")
            process = subprocess.Popen(self.get_config().get_command(),
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                     shell=False)
            time.sleep(RedRun.PAUSE_SETUP)
            self.set_process(process)
            
            @exithandle
            def gratuitous(signum, frame=None):
                logging.debug("Entering gratuitous exit handler…")
                sig = signal_for(signum)
                logging.debug(f"Received signal: {sig.name} ({sig.value})")
                keycount = len(self.get_config().config.keys())
                logging.debug(f"Redis config has {keycount} keys")
                time.sleep(RedRun.PAUSE_TEARDOWN)
                return True
            
            @exithandle
            def cleanup_process(signum, frame=None):
                logging.debug("Entering process cleanup…")
                sig = signal_for(signum)
                logging.debug(f"Received signal: {sig.name} ({sig.value})")
                logging.debug("Stopping Redis server…")
                process.terminate()
                time.sleep(RedRun.PAUSE_TEARDOWN)
                if process.returncode is None:
                    process.kill()
                    process.wait(timeout=RedRun.PAUSE_TEARDOWN)
                retval = process.returncode
                logging.debug(f"RETVAL: {retval}")
                return retval == 0
            
            @exithandle
            def cleanup_config(signum, frame=None):
                logging.debug("Entering config cleanup…")
                sig = signal_for(signum)
                logging.debug(f"Received signal: {sig.name} ({sig.value})")
                logging.debug("Tearing down Redis config…")
                config = self.get_config()
                config.teardown()
                retval = not config.active
                logging.debug(f"RETVAL: {retval}")
                return retval
        
        super().__execute__()

@export
class RedRun(clu.abstract.ManagedContext):
    
    PAUSE_SETUP = 1
    PAUSE_TEARDOWN = 2
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.process = None
        self.active = False
    
    def get_process(self):
        process = subprocess.Popen(self.config.get_command(),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                 shell=False)
        time.sleep(type(self).PAUSE_SETUP)
        return process
    
    def destroy_process(self, process):
        process.terminate()
        time.sleep(type(self).PAUSE_TEARDOWN)
        if process.returncode is None:
            process.kill()
            process.wait(timeout=type(self).PAUSE_TEARDOWN)
        return process.returncode
    
    def setup(self):
        if not self.active:
            from clu.app import redprocess
            self.process = redprocess.get_process()
            self.client = self.config.get_client()
            self.active = True
        return self
    
    def teardown(self):
        if self.active:
            self.client.close()
            self.process = None
            self.active = False
    
    def pid(self):
        if not self.active:
            return -1
        return self.process.pid
    
    def ping(self):
        if not self.active:
            return False
        try:
            return self.client.ping()
        except redis.exceptions.ConnectionError:
            return False
    
    def __repr__(self):
        typename = type(self).__name__
        instance_id = hex(id(self))
        pid = self.pid()
        state = self.active and "active" or "inactive"
        if self.active:
            temporary = self.config.is_temporary and "temporary" or "permanent"
            conflength = self.config.__len__()
        else:
            temporary = 'unconfigured'
            conflength = 'zero'
        return f"{typename}<[PID #{pid}, {state}/{temporary}, {conflength} config entries]> @ {instance_id}"

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test_context():
    
    logging.debug("Starting Redis server…")
    
    thisdir = Directory(os.path.dirname(__file__))
    thisconf = thisdir.subpath('redis.conf', requisite=True)
    assert os.path.exists(thisconf)
    redconf = RedisConf(source=thisconf)
    # redconf.setup()
    
    with redconf:
        with RedRun(redconf) as redrun:
            logging.debug(repr(redrun))
            assert redrun.config.active
            assert redrun.active
            assert redrun.ping()
            
            logging.debug("Stopping Redis server…")
    
    logging.debug(repr(redrun))
    logging.debug(repr(redconf))
    # redconf.teardown()
    
    # assert not redrun.config.active
    assert not redrun.active
    assert not redrun.ping()

def test():
    global DO_IT_DOUG
    DO_IT_DOUG = True
    
    from clu.app import redprocess
    from clu.repl.ansi import print_separator
    from clu.constants.data import GREEKOUT
    import signal
    import logging
    
    formats = ('%(relativeCreated)6d',
               '%(threadName)s',
              '[%(module)s', '»', '%(funcName)s]',
               '%(message)s')
    
    logging.basicConfig(level=logging.DEBUG,
                        format=' '.join(formats))
    
    redconf = redprocess.get_config()
    
    print_separator()
    print(str(redconf))
    print_separator()
    
    with RedRun(redconf) as redrun:
        logging.debug(repr(redrun))
        assert redrun.config.active
        assert redrun.active
        assert redrun.ping()
        
        for key, greek in GREEKOUT.items():
            redrun.client[key] = str(greek)
        
        redrun.client.flushdb()
        redrun.client.flushall()
        
        # try:
        #     redrun.process.wait()
        #
        # except (KeyboardInterrupt,
        #         subprocess.TimeoutExpired):
        #     logging.info("Commencing shutdown…")
        #     logging.debug(repr(redrun))
        #     logging.debug(repr(redconf))
        #     shutdown(signal.SIGTERM)
        
        try:
            time.sleep(10)
        except KeyboardInterrupt: # signal.SIGINT
            logging.info("Commencing shutdown…")
            shutdown(signal.SIGTERM)
    
    logging.debug(repr(redrun))
    logging.debug(repr(redconf))

if __name__ == '__main__':
    test()