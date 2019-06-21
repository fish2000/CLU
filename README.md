CLU – Common Lightweight Utilities (née Command-Line Utilities)
==================================================

This is a packaged-up and sanely version-controlled version of [the Python tools I wrote for my REPLs](https://github.com/fish2000/homage/blob/master/.script-bin/replutilities.py), divided up into
a bunch of subordinate packages:

* `compilation`: Abstractions for command-line macro definitions and [JSON compilation databases](https://clang.llvm.org/docs/JSONCompilationDatabase.html).

* `constants`: Definitions of useful constants, as well as polyfills to allow certain dependencies from the Python standard library to work even when some of their moving parts are missing (i.e. Python 2, various PyPy implementations, etc).

* `fs`: Filesystem-related things. Submodules include:
    * `fs.filesystem`: classes representing filesystem primitives like `Directory`, `TemporaryDirectory`,
        `TemporaryName`; a version of `tempfile.NamedTemporaryFile` that works with or without the leading dot
        in the provided suffix (a peeve of mine); functions for common filesystem operations like `which(…)`, 
        `back_ticks(…)`, `rm_rf(…)` (be careful with that one), and so forth.
    * `fs.appdirectories`: pretty much a wholesale duplication of the popular `appdirs` package.
    * `fs.misc`: a bunch of miscellany – noteworthy standouts include a memoized `current_umask(…)`
        and a corresponding `masked_permissions(…)`
    * `fs.pypath`: functions for safe manipulation of `sys.path` – `append_paths(…)` and `remove_paths(…)`,
        respectively
* `repl`: Tools useful in Python REPL environments – currently ANSI printing functions, for the most part.

* `typespace`: Contains a submodule `typespace.namespace` defining `SimpleNamespace` (á la Python 3’s `types.SimpleNamespace`) and a slightly more useful `Namespace` ancestor class; these are used to furnish a `typespace.types` namespace that contains everything in  the standard-library `types` module, but with all the typenames shortened so they no longer gratuitously end in “Type”. Like e.g. `types.ModuleType` is  to be found in `typespace.types.Module`, `types.FunctionType` is `typespace.types.Function`, et cetera, ad nauseum, so you can just do `from clu.typespace import types` to lose the redundant “Type” naming suffix – which I don’t know about you but that annoys me, I mean we all know that these things are types because they are in the fucking `types` module and don’t need those overly verbose extra four characters there at the end.

* `dicts`: Functions for wrangling `dict`s (and actually `Mapping` and `MutableMapping` descendants in general) – tools for merging and whatnot.

* `exporting`: Classes and enums for automatically exporting module members, naming and assigning docstrings to things that aren’t classes, functions, or modules (like e.g. `lambda` functions or `Namespace` instances), categorizing such things (using a kind of enum we call a `Clade` that formulates classification predicates from typelists), and APIs for all of these things. Currently a WIP – check out the first (working!) implementation in [my dotfiles repo](https://github.com/fish2000/homage/blob/master/.script-bin/replutilities.py).

* `keyvalue`: A module that offers a super-simple key/value store for use in REPLs, based on the `zict` package – so you can stash data in one REPL instance and get it back in another separate REPL process, even those of different implementations running on disparate Python versions.

* `math`: the future home for math-related stuff. All there is right now is a `clamp(…)` function that works with `numpy` dtypes.

* `naming`: functions for determining the names of things (even module constants and other random things that generally lack things like `__name__` attributes) and for the importing and exporting of things by “qualified names” – for instance, you can use `naming.qualified_import(…)` to import a class `CurveSet` from its package `instakit.processors.curves` by doing `qualified_import('instakit.processors.curves.CurveSet')`, which that may be handier for you than composing and hard-coding an `import` statement.

* `predicates`: tons and tons and tons of useful `lambda` functions, which I call “predicates” even though that may not be totally accurate in many cases. A lot of them take the form `isXXX(thing)` e.g. `isiterable(thing)` or `isclass(thing)`, in each case returning a boolean value. There are also:
    * Convenience accessor functions: `attr(thing, 'attributeone', 'attributetwo')` will return `thing.attributeone` if it exists, `thing.attributetwo` if the first one does not exist but the second one does, and finally `None` if neither can be found. `attr(…)` and other similar accessors work with any amount of attribute names (as long as there is at least one). Shortcuts like `pyattr(…)` do the same
    thing, only they automatically expand their attributes to `__dunder__` names.
    * AND MORE!!! There really are a ton of useful things in here and one day I will list them (but not today). Have fun with it!!

* `sanitizer`: functions for cleaning up unicode. Right now there is just a list-based `sanitize(…)` function that tones down anything with high-value code points to the point where it can be safely `ascii`-ified. 

* `typology`: This is like `predicates` but with more predicates, most of which are based on typelists. The module is full of typelists and it uses them extensively in its predicates, via `isinstance(…)`, `issubclass(…)` and a custom version of same called `graceful_issubclass(…)` which tries very hard to work with what you give it (instead of just crapping out with a `False` return value). 

* `version`: This is basically my take on the `semver` package. I originally developed it for internal use in some of my Python projects, but it stands on its own decently enough. 

Yes. Like I said, there is more to come. Do enjoy!
