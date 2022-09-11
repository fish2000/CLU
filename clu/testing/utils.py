# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps, lru_cache

import collections.abc
import clu.abstract
import enum
import sys, os, re

import pprint
import textwrap

from clu.constants import consts
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
    from clu.typology import iterlen
    count = 0
    searcher = suffix_searcher(suffix)
    for root, dirs, files in os.walk(os.fspath(target)):
        count += iterlen(filter(searcher, files))
    return count

WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 100) \
                             or consts.SEPARATOR_WIDTH

asterisks = lambda filler='*': print(filler * WIDTH)
printout = lambda name, value: print("» %25s : %s" % (name, value))

@export
def natural_millis(millis):
    """ Convert a quantity of milliseconds to an English expression """
    import humanize, datetime
    return humanize.naturaldelta(
           datetime.timedelta(milliseconds=millis))

MOST = 38

@export
def format_report(aggregated_report, show_buckets=False,
                                     show_annotations=False):
    """ Pretty-prints the data from a dbx-stopwatch aggregated report """
    # Copypasta-ed from the ‘stopwatch’ source –
    # N.B. This function is a total dog’s breakfast for reals
    values = aggregated_report.aggregated_values
    root_tr_data = aggregated_report.root_timer_data
    
    # fetch all values only for main stopwatch, ignore all the tags
    log_names = sorted(log_name for log_name in values if "+" not in log_name)
    
    if not log_names:
        return
        
    root = log_names[0]
    root_time_ms, root_count, bucket = values[root]
    
    root_time = root_time_ms / root_count
    
    entries = [
        " %s %sx  %.24s [%6.3fs] %.f%%" % (root.ljust(MOST), "   1",
                                             natural_millis(root_time).ljust(12),
                                                            root_time * 0.001,
                                                            100),
    ]
    
    for log_name in log_names[1:]:
        
        delta_ms, count, bucket = values[log_name]
        depth = log_name[len(root):].count("#")
        
        if show_buckets:
            bucket_name = f"«{bucket.name}» " if bucket else ""
            normal_name = log_name.rpartition('#')[-1]
            short_name = f"{bucket_name}{normal_name}"
        else:
            short_name = log_name.rpartition('#')[-1]
        
        entries.append("%s %s %sx  %.24s [%6.3fs] %.f%%" % (
            "  " * depth, short_name.ljust(MOST - (depth*2)),
                          f"{count}".rjust(4),
                          natural_millis(delta_ms).ljust(12),
            delta_ms * 0.001,
            delta_ms / root_time_ms * 100.0,
        ))
    
    if show_annotations:
        annotations = sorted(ann.key for ann in root_tr_data.trace_annotations)
        if annotations:
            entries.append("Annotations: %s" % (', '.join(annotations)))
    
    return "\n".join(entries)

def json_report(aggregated_report):
    import json
    return json.dumps(aggregated_report.aggregated_values, indent=4, default=str)

@export
def get_title(function):
    """ Harvest a title string from a functions’ doctext """
    from inspect import getdoc
    
    # Get docstring, if one exists:
    doc = getdoc(function)
    if doc:
        title = doc.splitlines().pop(0).strip()
        title = f"“{title}”"
    else:
        title = "«untitled»"
    
    return title

@export
def multiple(number):
    """ Is it singular or plural…??!?! """
    if number == 1:
        return ''
    return 's'

@export
def format_environment(environment=None):
    """ Format environment variables """
    # Default to “os.environ” when None is passed –
    # this keeps mutables out of the call signature:
    if environment is None:
        environment = os.environ
    
    if hasattr(environment, 'environment'):
        environment = environment.environment
    
    if not environment:
        return
    
    most = max(len(key) for key in environment.keys()) + 2
    printer = pprint.PrettyPrinter(indent=(most + 6), width=WIDTH)
    wrapper = textwrap.TextWrapper(initial_indent='',
                                subsequent_indent=' ' * (most + 5),
                                 break_long_words=False,
                                 break_on_hyphens=False,
                                      placeholder='…',
                                        max_lines=8,
                                            width=WIDTH - most)
    
    pformat = lambda thing: format_environment.outdenter.sub(r"\g<bracket>",
                                                 printer.pformat(thing))
    
    for key, value in sorted(environment.items()):
        jkey = f"{key}".ljust(most)
        begin = f"» {jkey} : "
        if key.endswith('PATH') and os.pathsep in value:
            wvalue = pformat(value.split(os.pathsep))
        else:
            wvalue = wrapper.fill(value)
        yield f"{begin}{wvalue}"

format_environment.outdenter = re.compile(r'^(?P<bracket>[\[\{\(])\s+')

@export
class Bucket(enum.Enum):
    
    """ Testing bucket enum, for use with @inline.test() """
    
    MAIN        = 'test'
    CHECK       = 'pre-check'
    POSTEXEC    = 'diagnostic'
    FIXTURE     = 'fixture'     # not in use
    
    @classmethod
    def byname(cls, string):
        """ Get a bucket by its bucket name, matching case-insensitively """
        for bucket in cls:
            if bucket.group_name == string.casefold():
                return bucket
        raise ValueError(f"bucket not found: {string}")
    
    @classmethod
    def bytitle(cls, string):
        """ Retrieve a bucket by its title, matching case-insensitively """
        for bucket in cls:
            if bucket.group_title.casefold() == string.casefold():
                return bucket
        raise ValueError(f"bucket not found: {string}")
    
    def to_string(self):
        return str(self.name)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.name, encoding=consts.ENCODING)
    
    @property
    def group_name(self):
        return self.to_string().casefold()
    
    @property
    def group_title(self):
        return str(self.value)

@export
class InlineTester(collections.abc.Set,
                   collections.abc.Sequence,
                   collections.abc.Callable,
                   clu.abstract.ReprWrapper,
                   metaclass=clu.abstract.Slotted):
    
    """ Function decorator for marking and running inline tests. Example usage:
            
            def test():
                
                from clu.testing.utils import inline # †
                
                @inline.precheck
                def before_everything_else():
                   # ...
                
                @inline
                def test_one():
                    # ...
                
                @inline
                def test_two():
                    # ...
                
                @inline.runif(something == something_else)
                def test_conditionally_run():
                    # ...
                
                @inline.diagnostic
                def apres_testing():
                   # ...
            
            return inline.test() # ‡
            
            if __name__ == '__main__':
                sys.exit(test())
        
        † This `import` statement specifically instances and returns a
          new copy of the “InlineTester” class, as the “@inline” decorator,
          allowing the instance to guarantee its uniqueness in each modules’
          main inline test function, as per this example.
        
        ‡ Optionally you can call this method with an integer, in order to
          run your test functions that many times over, instead of just once.
          …If you do so, any output produced by the functions will be printed
          only on the first go-around, and will be discarded on all subsequent
          executions. In any case, this number doesn’t apply to the execution
          of “precheck” and “diagnostic” functions – they are always each run
          exactly once, before or after (respectively) the main test functions
          are run.
    """
    
    __slots__ = ('fixtures',
                 'prechecks',
                 'test_functions',
                 'diagnostics',
                 'watch', '__weakref__')
    
    def __new__(cls, iterable=None):
        instance = super().__new__(cls)
        instance.fixtures = {}
        instance.prechecks = []
        instance.test_functions = []
        instance.diagnostics = []
        instance.watch = None
        return instance
    
    def __init__(self, iterable=None):
        if iterable is not None:
            self.test_functions.extend(iterable)
    
    def wrap(self, function, bucket=Bucket.MAIN):
        """ Wrap an inline function with timing, banner-printing,
            and all sorts of other useful bookkeeping code used
            internally by the inline testing harness.
        """
        from clu.naming import nameof
        from clu.predicates import item
        from clu.typology import isstring
        from contextlib import ExitStack
        import stopwatch
        
        # Get the name of the decorated function:
        name = nameof(function, default='<unnamed>')
        
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Get index:
            idx = int(kwargs.pop('idx', 0))
            max = int(kwargs.pop('max', 0))
            
            # Get verbosity:
            verbose = kwargs.pop('verbose', False)
            
            # Get a stopwatch instance:
            watch = getattr(self, 'watch',
                    kwargs.pop('watch', None))
            stack = ExitStack()
            
            if watch is None:
                watch = stopwatch.StopWatch()
                stack.enter_context(watch.timer('root'))
            
            if verbose:
                title = get_title(function)
                
                # Print header:
                print()
                print(f"§ RUNNING {bucket.group_title.upper()} #{idx+1}: `{name}(¬)` – {title}")
                asterisks('-')
                print()
            
            # Run the wrapped function, timing it:
            label_idx = f"{idx+1}".zfill(len(f"{max}"))
            label_timer = f"{label_idx} – {name}"
            with watch.timer(label_timer, bucket=bucket):
                out = function(*args, **kwargs)
            
            if verbose:
                # Give us a line-break on non-main verbose runs:
                if bucket is not Bucket.MAIN:
                    print()
                
                # Get the reported timer value *before* closing out
                # the root-level stopwatch timer:
                timervals = item(watch._reported_values, label_timer,
                                                 f'root#{label_timer}',
                                  f'{bucket.group_name}#{label_timer}',
                             f'root#{bucket.group_name}#{label_timer}',
                              'root')
            
            # Close the context stack,
            # regardless of verbosity:
            stack.close()
            
            if verbose:
                # Print the results and execution time:
                asterisks('~')
                
                if out is not None:
                    print("» RESULTS:")
                    pprint.pprint(isstring(out) and { 'string' : f"{out!s}" } or out, indent=4)
                    asterisks('~')
                
                if timervals:
                    dt = timervals[0] * 0.001
                    dtout = "%6.3f" % dt
                    ndtout = natural_millis(timervals[0])
                    print(f"→ {bucket.group_title.capitalize()} function “{name}(¬)” ran in about {ndtout} –{dtout}s")
                    
                asterisks('=')
            
            # Return as per the decorated function:
            return out
        
        return wrapper
    
    def __call__(self, function):
        """ Decorate a testing function, marking it as an inline test. """
        wrapper = self.wrap(function, bucket=Bucket.MAIN)
        
        # Add the wrapper to the internal test function list:
        self.test_functions.append(wrapper)
        
        # Return the test wrapper function:
        return wrapper
    
    def add_function(self, function, name=None):
        """ Explictly add a testing function to use as an inline test.
            Optionally, a name may be specified.
        """
        from clu.exporting import determine_name
        from clu.predicates import getpyattr
        
        # Stash the old name before assigning the new one:
        if name is not None:
            dname = determine_name(function)
            qname = getpyattr(function, 'qualname')
            if qname:
                function.__qualname__ = qname.replace(
                                        getpyattr(function, 'name'), name)
            function.__name__ = name
            function.__function_name__ = dname
        
        # Wrap and return:
        return self.__call__(function)
    
    @property
    def precheck(self):
        """ Decorate a preflight-check function.
            
            Preflight-check functions (née just “prechecks”) each run exactly
            once, prior to the main test-execution run. They are always run
            in “verbose” mode. They can be used to print out initial conditions
            for assessment, or to set up elements of the testing environment
            ahead of the main test run.
        """
        def decoration(function):
            wrapper = self.wrap(function, bucket=Bucket.CHECK)
            
            # Add the wrapper to the internal precheck function list:
            self.prechecks.append(wrapper)
            
            # Return the wrapper, in leu of the function:
            return wrapper
        
        # Return the decoration function as the property value:
        return decoration
    
    @property
    def diagnostic(self):
        """ Decorate a diagnostic function.
            
            Diagnostic functions (née just “diagnostics”) each run exactly
            once, after the main test-execution run. They are always run
            in “verbose” mode – their purpose is to print out a bunch of
            informational shit; hence the name “diagnostics”.
        """
        def decoration(function):
            wrapper = self.wrap(function, bucket=Bucket.POSTEXEC)
            
            # Add the wrapper to the internal diagnostic list:
            self.diagnostics.append(wrapper)
            
            # Return the wrapper, in leu of the function:
            return wrapper
        
        # Return the decoration function as the property value:
        return decoration
    
    @property
    def runtwice(self):
        """ Decorate a function as both a precheck and a diagnostic. """
        def decoration(function):
            begin_wrapper = self.wrap(function, bucket=Bucket.CHECK)
            end_wrapper = self.wrap(function, bucket=Bucket.POSTEXEC)
            self.prechecks.insert(0, begin_wrapper)
            self.diagnostics.insert(0, end_wrapper)
            return function
        
        return decoration
    
    @property
    def fixture(self):
        """ Decorate a function as a fixture, memoizing its output. """
        from clu.naming import nameof
        
        def decoration(function):
            name = nameof(function)
            
            if name is None:
                raise ValueError("couldn’t determine a name for fixture function: {function!r}")
            
            self.fixtures[name] = wrapper = lru_cache(maxsize=16, typed=False)(function)
            return wrapper
        
        return decoration
    
    def runif(self, boolean):
        """ Run a test function only if a boolean condition is true. Like so:
            
            @inline.runif(consts.TEXTMATE)
            def test_in_textmate_only():
                # … insert test code here …
            
        """
        from clu.predicates import none_function
        
        def decoration(function):
            if boolean:
                return self.__call__(function)
            return self.__call__(wraps(function)(none_function))
        
        return decoration
    
    def test(self, exec_count=1, *args, **kwargs):
        """ Run all functions marked as @inline within the modules’ main
            inline test function, using individual context timers for each
            test function call (provided by dbx-stopwatch).
        """
        from contextlib import redirect_stdout
        import stopwatch
        import io
        
        # Get the mode
        mode = kwargs.get('mode', None)
        verbosity = mode != 'json'
        
        # Count the test functions:
        precount = len(self.prechecks)
        funcount = len(self.test_functions)
        diacount = len(self.diagnostics)
        most = max(precount, funcount, diacount)
        
        # Initialize the stopwatch:
        self.watch = stopwatch.StopWatch()
        
        # Root timer for everything:
        with self.watch.timer('root'):
            
            # Run preflight checks:
            if precount > 0:
                with self.watch.timer('check'):
                    
                    # Call preflight checks each exactly once:
                    for idx, precheck in enumerate(self.prechecks):
                        precheck(*args, verbose=verbosity, idx=idx, max=most)
            
            # Main timer for execution times:
            with self.watch.timer('main'):
                
                # Call testing functions once, initially:
                for idx, function in enumerate(self.test_functions):
                    function(*args, verbose=verbosity, idx=idx, max=most)
                
                # Call them twice through «adnauseumn» –
                # Redirecting `stdout` so we only get the
                # verbose output once:
                if exec_count - 1 > 0:
                    iosink = io.StringIO()
                    with redirect_stdout(iosink):
                        for edx in range(exec_count-1):
                            for idx, function in enumerate(self.test_functions):
                                function(*args, idx=idx, max=most)
                            iosink.truncate(0)
                    iosink.close()
            
            # Run diagnostics:
            if diacount > 0:
                with self.watch.timer('postexec'):
                    
                    # Call diagnostics each exactly once:
                    for idx, diagnostic in enumerate(self.diagnostics):
                        diagnostic(*args, verbose=verbosity, idx=idx, max=most)
        
        # REPORT IN:
        report = self.watch.get_last_aggregated_report()
        
        if not mode:
            out = format_report(report)
            
            # Cough up the final report data:
            print()
            count_text = f"{exec_count} times"
            
            # Some trivial english-ification:
            if exec_count == 1:
                count_text = "once"
            elif exec_count == 2:
                count_text = "twice"
            elif exec_count == 3:
                count_text = "thrice"
            elif exec_count == 100:
                count_text = "a hundred times"
            
            # Header:
            print(f"⌀ TIME TOTALS "
                  f"– ran {funcount} test{multiple(funcount)} {count_text} "
                  f"– {precount} precheck{multiple(precount)}"
                  f", {diacount} diagnostic{multiple(diacount)}")
            
            # Body:
            asterisks('∆')
            print(out)
            
            # Footer:
            asterisks('∇')
        
        elif mode == 'json':
            out = json_report(report)
            print()
            print(out)
            print()
        
        # Clear the stopwatch instance:
        self.watch = None
        
        # Return successfully:
        return os.EX_OK
    
    def __len__(self):
        return len(self.test_functions)
    
    def __iter__(self):
        yield from self.test_functions
    
    def __getitem__(self, idx):
        return self.test_functions[idx]
    
    def __contains__(self, value):
        return value in self.test_functions
    
    def __bool__(self):
        return len(self.test_functions) > 0
    
    def inner_repr(self):
        return repr(self.test_functions)

@export
def stdpout():
    """ Switch the default output stream used by the “pout” module
        to “sys.stdout” from “sys.stderr” using the “logging”
        module internals.
    """
    # N.B. I fucking hate this Javaesque boilerplate-tastic shit
    import logging, pout
    from clu.stdio import std
    
    # If we’ve been here before we don’t need to bother:
    if not getattr(pout, '__WTF_HAX__', False):
        
        try:
            # Step one: pop off the old stderr-bound handler:
            pout.stream.logger.handlers.pop()
            
            # Step two: set up a new logging StreamHandler:
            loghandler = logging.StreamHandler(stream=std.OUT)
            loghandler.setFormatter(logging.Formatter('%(message)s'))
            pout.stream.logger.addHandler(loghandler)
            pout.stream.logger.propagate = False
            
            # Step three: instantiate a “pout.StderrStream” and root
            # around with that shit to use `clu.stdio.std.OUT`:
            streamy = pout.StderrStream()
            streamy.logger = pout.stream.logger
            streamy.logger.setLevel(logging.DEBUG)
            streamy.logger.handlers[0].setStream(std.OUT)
            streamy.logger.handlers[0].set_name('stderr')
            streamy.logger.handlers[0].setLevel(logging.DEBUG)
            
            # Step four DONT CROSS THE STREAMS WHATEVER YOU DO
            stdpout.oldstreamy = pout.stream
            pout.stream = streamy
        
        except AttributeError:
            pass
        
        # Step five: doctor the “pout” module reflecting our change:
        pout.__WTF_HAX__ = True
    
    # Step six: return the “pout” module object:
    return pout

def __getattr__(key):
    """ Module __getattr__(…) patches the “pout” module on-demand, and
        also live-instances the “@inline” decorator from “InlineTester”
    """
    if key == 'inline':
        return InlineTester()
    elif key == 'pout':
        return stdpout()
    raise AttributeError(f"module {__name__} has no attribute {key}")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir('pout', 'inline')

def test():
    
    # Normally, we’d be like, “from clu.testing.utils import inline”
    # …like, right about say here:
    from clu.fs import pypath
    inline = InlineTester()
    
    @inline.fixture
    def get_data_dir():
        from clu.fs.filesystem import Directory
        return Directory(consts.TEST_PATH).subdirectory('data')
    
    @inline.precheck
    def show_python():
        print("PYTHON EXECUTABLE:", sys.executable)
    
    @inline
    def test_one():
        """ Busywork, mark I. """
        # Fuck around with the “yodogg” app’s environment overrides:
        from clu.fs.filesystem import Directory
        
        prefix0 = Directory(consts.TEST_PATH).subdirectory('yodogg')
        prefix1 = prefix0.subdirectory('yodogg')
        assert prefix0.exists
        assert prefix1.exists
        pypath.enhance(prefix0, prefix1)
        
        from yodogg.config import Env
        from clu.config.env import Environ
        
        env0 = Env()
        envy = Environ(appname=Env.appname)
        
        for key in env0.keys():
            print(f"» [old] ENVIRONMENT KEY: {key}")
            assert envy[key] == env0[key]
        
        for key in envy.keys():
            print(f"» [new] ENVIRONMENT KEY: {key}")
            assert envy[key] == env0[key]
        
        pypath.remove_paths(prefix0, prefix1)
    
    @inline
    def test_two():
        """ Busywork, mark II. """
        # Fuck around with the CLU app’s environment overrides:
        from clu.config.base import Env
        from clu.config.env import Environ
        
        env0 = Env()
        envy = Environ(appname=Env.appname)
        
        for key in env0.keys():
            print(f"» [old] ENVIRONMENT KEY: {key}")
            assert envy[key] == env0[key]
        
        print()
        
        for key in envy.keys():
            print(f"» [new] ENVIRONMENT KEY: {key}")
            assert envy[key] == env0[key]
        
        print()
    
    @inline
    def test_three_countfiles():
        """ Testing “clu.testing.utils.countfiles(…)” """
        from clu.typology import isvalidpathlist
        from clu.fs.filesystem import TemporaryDirectory
        
        prefix = 'test-five-countfiles-'
        datadir = get_data_dir()
        
        with TemporaryDirectory(prefix=prefix,
                                change=False) as temporarydir:
            
            target = temporarydir.subdirectory('yodogg')
            destination, files = datadir.flatten(target)
            assert target == destination
            assert isvalidpathlist(files)
            
            assert countfiles(datadir) \
                == countfiles(target) \
                == countfiles(destination) \
                == len(files)
            
            for f in files:
                assert os.path.exists(f)
                assert os.path.basename(f) in destination
        
        assert not temporarydir.exists
    
    @inline
    def test_four_show_empty_env():
        for envline in format_environment(environment={}):
            print(envline)
    
    @inline.diagnostic
    def show_environment():
        """ Show environment variables """
        for envline in format_environment():
            print(envline)
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        total = len(inline.fixtures)
        for idx, name in enumerate(inline.fixtures):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {name} ({idx+1} of {total})")
            print(inline.fixtures[name].cache_info())
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())