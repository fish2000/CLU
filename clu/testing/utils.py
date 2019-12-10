# -*- coding: utf-8 -*-
from __future__ import print_function
from contextlib import redirect_stdout
from functools import wraps

import io
import humanize
import stopwatch
import sys

from clu.constants.consts import (QUALIFIER,
                                  SEPARATOR_WIDTH,
                                  TEXTMATE)

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def countfiles(target, suffix=None):
    """ Return a count of all files in the target directory,
        including those found in all subdirectories.
        
        Optionally pass a “suffix” argument to only count files
        matching a specific suffix.
    """
    from clu.fs.misc import suffix_searcher
    import os
    count = 0
    searcher = suffix_searcher(suffix)
    for root, dirs, files in os.walk(os.fspath(target)):
        count += len(tuple(filter(searcher, files)))
    return count

WIDTH = TEXTMATE and max(SEPARATOR_WIDTH, 100) or SEPARATOR_WIDTH
asterisks = lambda filler='*': print(filler * WIDTH)
printout = lambda name, value: print("» %25s : %s" % (name, value))

def natural_millis(millis):
    return humanize.naturaldelta(
           humanize.time.timedelta(milliseconds=millis))

@export
def inline(function):
    """ Function decorator for an individual inline test. Example usage:
            
            def test():
                
                @inline
                def test_one():
                    # ...
                
                @inline
                def test_two():
                    # ...
            
            test_one()
            test_two()
            
            if __name__ == '__main__':
                test()
    """
    from clu.naming import nameof
    from clu.predicates import item
    from pprint import pprint
    
    # Get the name of the decorated function:
    name = nameof(function, default='<unnamed>')
    
    @wraps(function)
    def test_wrapper(*args, **kwargs):
        # Get stopwatch:
        watch = kwargs.pop('watch', None)
        rootless = False
        if watch is None:
            rootless = True
            watch = stopwatch.StopWatch()
            watch.start('root')
        
        # Print header:
        print()
        print(f"TESTING: “{name}”")
        asterisks('-')
        print()
        
        # Run the wrapped function, timing it:
        with watch.timer(name):
            out = function(*args, **kwargs)
        
        # If we’re rootless, end the root span:
        if rootless:
            watch.end('root')
        
        timervals = item(watch._reported_values, name,
                                          f'run#{name}',
                                     f'root#run#{name}')
        
        # Print the results and execution time:
        asterisks('-')
        if out is not None:
            print("RESULTS:")
            pprint(out)
            asterisks('-')
        if timervals:
            dt = str(timervals[0] * 0.001)
            dtout = dt[:(dt.find(QUALIFIER) + 4)]
            ndtout = natural_millis(timervals[0])
            print(f"Test function “{name}(¬)” ran for about {ndtout} ({dtout}s)")
        asterisks('=')
        
        # Return as per the decorated function:
        return out
    
    # mark the wrapper as an inline test function:
    test_wrapper.__test__ = True
    
    # Return the test wrapper function:
    return test_wrapper

def format_report(aggregated_report, show_buckets=False):
    """ Returns a pretty printed string of reported values """
    # Copypasta-ed from the ‘stopwatch’ source:
    values = aggregated_report.aggregated_values
    root_tr_data = aggregated_report.root_timer_data
    
    # fetch all values only for main stopwatch, ignore all the tags
    log_names = sorted(log_name for log_name in values if "+" not in log_name)
    
    if not log_names:
        return
        
    root = log_names[0]
    root_time_ms, root_count, bucket = values[root]
    
    root_time = root_time_ms / root_count
    
    buf = [
        " %s %sx  %.24s [%6.3fs] %.f%%" % (root.ljust(24), "   1",
                                             natural_millis(root_time).ljust(12),
                                                            root_time * 0.001,
                                                            100),
    ]
    
    for log_name in log_names[1:]:
        
        delta_ms, count, bucket = values[log_name]
        depth = log_name[len(root):].count("#")
        if show_buckets:
            bucket_name = f"«{bucket.name}» " if bucket else ""
            normal_name = log_name[log_name.rfind("#") + 1:]
            short_name = f"{bucket_name}{normal_name}"
        else:
            short_name = log_name[log_name.rfind("#") + 1:]
        
        buf.append("%s %s %sx  %.24s [%6.3fs] %.f%%" % (
            "  " * depth, short_name.ljust(24 - (depth*2)),
                          str(count).rjust(4),
                          natural_millis(delta_ms).ljust(12),
            delta_ms * 0.001,
            delta_ms / root_time_ms * 100.0,
        ))
    
    annotations = sorted(ann.key for ann in root_tr_data.trace_annotations)
    if annotations:
        buf.append("Annotations: %s" % (', '.join(annotations)))
    
    return "\n".join(buf)

@export
def test_inlines(mapping, exec_count=1):
    """ Run all functions marked @inline from “mapping”, using
        individual context timers for each function (via stopwatch)
    """
    watch = stopwatch.StopWatch()
    functions = []
    
    # Root timer for everything:
    with watch.timer('root'):
        
        with watch.timer('collect'):
            for key, value in mapping.items():
                if getattr(value, '__test__', False):
                    functions.append((key, value))
        
        with watch.timer('run'):
            
            for name, function in functions:
                function(watch=watch)
            
            if exec_count - 1 > 0:
                iosink = io.StringIO()
                with redirect_stdout(iosink):
                    for idx in range(exec_count-1):
                        for name, function in functions:
                            function(watch=watch)
                        iosink.truncate(0)
    
    report = watch.get_last_aggregated_report()
    funcount = len(functions)
    out = format_report(report)
    
    # Cough up the final report:
    print()
    count_text = f"{exec_count} times"
    if exec_count == 1:
        count_text = "once"
    elif exec_count == 2:
        count_text = "twice"
    print(f"TIME TOTALS – ran {funcount} functions {count_text}")
    asterisks('•')
    print(out)
    asterisks('•')

# One less import to forget about:
inline.test = test_inlines

@export
def stdpout():
    """ Switch the default output stream used by the “pout” module
        to “sys.stdout” from “sys.stderr” using the “logging”
        module internals.
    """
    # N.B. I fucking hate this Javaesque boilerplate-tastic shit
    import logging, pout
    
    # If we’ve been here before we don’t need to bother:
    if not getattr(pout, '__WTF_HAX__', False):
        
        # Step one: pop off the old stderr-bound handler:
        pout.stream.logger.handlers.pop()
        
        # Step two: set up a new logging StreamHandler:
        loghandler = logging.StreamHandler(stream=sys.stdout)
        loghandler.setFormatter(logging.Formatter('%(message)s'))
        pout.stream.logger.addHandler(loghandler)
        pout.stream.logger.propagate = False
        
        # Step three: instantiate a “pout.StderrStream” and root
        # around with that shit to use `sys.stdout`:
        streamy = pout.StderrStream()
        streamy.logger = pout.stream.logger
        streamy.logger.setLevel(logging.DEBUG)
        streamy.logger.handlers[0].setStream(sys.stdout)
        streamy.logger.handlers[0].set_name('stderr')
        streamy.logger.handlers[0].setLevel(logging.DEBUG)
        
        # Step four DONT CROSS THE STREAMS WHATEVER YOU DO
        stdpout.oldstreamy = pout.stream
        pout.stream = streamy
        
        # Step five: doctor the “pout” module reflecting our change:
        pout.__WTF_HAX__ = True
    
    # Step six: return the “pout” module object:
    return pout

def __getattr__(key):
    """ Module __getattr__(…) patches the “pout” module on-demand """
    if key == 'pout':
        return stdpout()
    raise AttributeError(f"module {__name__} has no attribute {key}")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir('pout')