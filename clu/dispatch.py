# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import atexit
import signal
import sys

from clu.config.abc import functional_and
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# The master list of exit-handle functions:
exithandles = []

# The list of signals to which we’ll be listening:
signals = (signal.SIGHUP,
           signal.SIGQUIT,
           signal.SIGTERM,
           signal.SIGWINCH)

def wraphandler(function):
    """ Wrap a signal handler in a system-exit function """
    @wraps(function)
    def wrapper(*args):
        atexit.unregister(function)
        out = not function(*args)
        sys.exit(int(out))
    return wrapper

def bindhandles():
    """ Freshly bind all exit handles listed in “clu.shelving.dispatch.exithandles” """
    # If there’s a handle set already registered with “atexit”,
    # unregister it first:
    if callable(bindhandles.last):
        atexit.unregister(bindhandles.last)
    
    # Create a new callable handle set from the function list:
    handles = functional_and(*exithandles)
    
    # Register the handle set with “atexit”:
    atexit.register(handles, signal.SIGSTOP, None)
    
    # Register the handle set with all specified signals:
    for sig in signals:
        signal.signal(sig, wraphandler(handles))
    
    # Stow the handle set instance for possible unregistration:
    bindhandles.last = handles

# The handle-set memo:
bindhandles.last = None

@export
def signal_for(signum):
    """ Return the signal enum value for a given signal number """
    for sig in signal.Signals:
        if sig.value == int(signum):
            return sig
    return signal.SIG_DFL

@export
def exithandle(function):
    """ Register a function with “atexit” and various program-exit signals """
    if function not in exithandles:
        exithandles.append(function)
        bindhandles()
    return function

@export
def unregister(function):
    """ Unregister a previously-registered exit handle function """
    if function in exithandles:
        exithandles.remove(function)
        bindhandles()
    return function

@export
def unregister_all():
    """ Unregister *all* previously-registered exit handle functions """
    global exithandles
    exithandles[:] = list()
    bindhandles()

@export
def nhandles():
    """ Return the number of registered exit-handle functions """
    return len(exithandles)

@export
def trigger(send=signal.SIGSTOP, frame=None):
    """ Run and unregister all exit handle functions without exiting """
    if bindhandles.last is not None:
        handles = bindhandles.last.clone()
        unregister_all()
        out = True
        for handle in handles:
            try:
                out &= handle(send, frame)
            except SystemExit:
                pass
        return out
    return False

@export
def shutdown(send=signal.SIGSTOP, frame=None):
    """ Run all exit handles, and commence an orderly shutdown """
    if callable(bindhandles.last):
        atexit.unregister(bindhandles.last)
    out = not trigger(send, frame)
    sys.exit(int(out))

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    @exithandle
    def xhandle0(signum, frame=None):
        print("Entering xhandle0")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    @exithandle
    def xhandle1(signum, frame=None):
        print("Entering xhandle1")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    # Won’t register an already-registered handle:
    exithandle(xhandle1)
    
    global exithandles
    assert len(exithandles) == 2
    
    print("Triggering…")
    assert trigger()
    assert len(exithandles) == 0
    
    @exithandle
    def xhandleX(signum, frame=None):
        print("Entering xhandleX")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    assert len(exithandles) == 1
    print("About to exit function test()…")
    return 0

def test_sync():
    import time
    out = test()
    while True:
        time.sleep(1)
    print('WAT')
    return out

def test_async():
    """ YOU ARE DOING IT WRONG:
        https://asyncio-wrong.herokuapp.com/#/8/9
    """
    from dataclasses import dataclass, fields
    
    import asyncio
    import logging
    import random
    import string
    import uuid
    
    from clu.repr import stringify
    
    formats = ('%(relativeCreated)6d',
               '%(threadName)s',
               '[%(module)s', '»',
               '%(funcName)s]',
               '%(message)s')
    
    logging.basicConfig(level=logging.DEBUG,
                        format=' '.join(formats))
    
    @dataclass(repr=False)
    class Message:
        msg_id: str
        inst_name: str
        
        def __repr__(self):
            return stringify(self, tuple(field.name \
                                         for field in fields(self)))
    
    async def publish(queue):
        choices = string.ascii_lowercase + string.digits
        while True:
            host_id = ''.join(random.choices(choices, k=4))
            msg = Message(
                msg_id=str(uuid.uuid4()).split('-')[-1],
                inst_name=f'dogg-{host_id}')
            await queue.put(msg)
            logging.debug(f'Published {msg}')
            await asyncio.sleep(random.random())
    
    async def save(msg):
        # unhelpful simulation of i/o work
        await asyncio.sleep(random.random())
        logging.debug(f'Saved {msg} into database')
    
    async def restart_host(msg):
        # unhelpful simulation of i/o work
        await asyncio.sleep(random.random())
        logging.debug(f'Restarted {msg.inst_name}')
    
    async def consume(queue):
        while True:
            msg = await queue.get()
            logging.debug(f'Pulled {msg}')
            asyncio.create_task(save(msg))
            asyncio.create_task(restart_host(msg))
    
    async def shutdown(signal, loop):
        logging.debug(f"Received exit signal {signal.name}…")
        tasks = [task \
                 for task in asyncio.all_tasks() \
                 if task is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks)
        loop.stop()
        logging.debug("Shutdown complete!")
    
    async def handle_exception(coro, loop):
        try:
            return await coro
        except asyncio.CancelledError:
            logging.debug('Coroutine cancelled')
        # except Exception:
        #     logging.debug('Caught exception')
        # finally:
        #     loop.stop()
    
    loop = asyncio.get_event_loop()
    
    for sig in signals:
        loop.add_signal_handler(
            sig, lambda sig=sig: asyncio.create_task(shutdown(sig, loop)))
    
    queue = asyncio.Queue()
    publisher_coro = handle_exception(publish(queue), loop)
    consumer_coro = handle_exception(consume(queue), loop)
    
    try:
        loop.create_task(publisher_coro)
        loop.create_task(consumer_coro)
        loop.run_forever()
    finally:
        logging.debug("Cleaning up")
        loop.stop()
    
    return 0

if __name__ == '__main__':
    sys.exit(test())
    # sys.exit(test_sync())
    # sys.exit(test_async())
