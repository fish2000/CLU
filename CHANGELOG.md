# Changelog


## v0.12.6 (2025-05-19)

### Other

* Bumped version: 0.12.5 → 0.12.6. [Alexander Böhn]

* [make] New changelog added. [Alexander Böhn]

* The ANSI docstring CLU command seems to be up to snuff. [Alexander Böhn]

* Further along the prettyprinting path. [Alexander Böhn]

* Started on a new CLU command to prettyprint ANSI docstrings. [Alexander Böhn]

  … please bear with as we travel on this journey together

* Gratuitously expanded the docstring for `negate(…)` in `clu.predicates` [Alexander Böhn]

  … comparing the function to a child with oppositional-defiant disorder.
    It makes a lot of sense, no?

* Spruced up the ANSI inline tests. [Alexander Böhn]


## v0.12.5 (2025-05-19)

### Add

* Adding TOML module discussion screenshot. [Alexander Böhn]

### Other

* Bumped version: 0.12.4 → 0.12.5. [Alexander Böhn]

* [make] New changelog added. [Alexander Böhn]

* Starting to remove the legacy parts of `clu.config` [Alexander Böhn]

  … fucking finally. These bits were an early draft of what became
    the KeyMap system – they’ve been removed thoroughly from all the
    farthest and darkest corners CLU has grown over the years. All
    the legacy shit was pretty much only used in testing, and like
    accedentally in some of the config file stuff. Good riddance I
    say – the only thing that broke is a bunch of tests as old as the
    legacy code itself. Yeah!

* Updated the TOML file config reader (using native parsers) [Alexander Böhn]

  … which can I ask, what the fuck is this dog’s breakfast with the
    native TOML modules?! The standard-library pure-python thing is
    just called “toml”. Fine, so far so good. Then, if you want
    native TOML I/O, you have to install *two* native modules. The
    one with “load(…)” and “loads(…)” is called ‘tomli’. Like, it’s
    like “The ‘i’ is for input! Like accelerated input!” Sure. That’s
    somewhat reasonable, it’d be nice if it was all in one module.
    Because the other TOML native module has your “dump(…)” and your
    “dumps(…)”, right, so what’s that one called though? Is it, by any
    chance, ‘tomlo’? as in “The ‘o’ is for output”. Well no, that is
    not the name of this module. In some sort of fit of solidarity
    with ‘tomli’ the author of this shit decided to call it – wait
    for it now…

  			« tomli_w »

  … yes you read that correctly. Not ‘tomlo’, not ‘tomlw’, none of
    any sort of sense-making moniker, nor any moniker that doesn’t
    make sense but at least was crafted with some sort of follow-able
    logic. Nor, heaven forbid, would these modules be *combined* into
    something sort of like the pure-python TOML thing, only native.
    THAT WOULD BE WAY TOO MUCH TO ASK.

  … so of course I did what I did in this commit, which was to firstly
    import ‘tomli_w’ (The ‘w’ is for whatever!) as ‘tomlo’. And then
    I stitched them together in a class called “toml” (crazy, right?)
    that just had static alias methods to the native module functions.
    Aesthetics are important, and they ain’t easy, it would seem. Yo.

* Sometimes, I prefer to ask permission first. [Alexander Böhn]

* Removed `setup.cfg` entry from `MANIFEST.in` [Alexander Böhn]

* Minor `README.md` tweak. [Alexander Böhn]

* Updated `README.md` with information on `clu.enums` and `clu.all` [Alexander Böhn]

* EVEN MORE syntax-highlighted `README.md` code. [Alexander Böhn]

* More syntax-highlighted	`README.md` code. [Alexander Böhn]

* Trying out syntax-highlighted fenced code block in `README.md` [Alexander Böhn]

* A few more addenda in `pyproject.toml` [Alexander Böhn]

* Removed the old `setup.cfg` file. [Alexander Böhn]


## v0.12.4 (2025-05-19)

### Add

* Added a symbolic link to the old treatment file name. [Alexander Böhn]

  … because sometimes, I am lame

### Other

* Bumped version: 0.12.3 → 0.12.4. [Alexander Böhn]

* [make] New changelog added. [Alexander Böhn]

* More refinements to the whole `pyproject.toml` deal. [Alexander Böhn]

* Fixed a few `pyproject.toml` build-related things. [Alexander Böhn]

* Removed the CLU Treatment.md symlink. [Alexander Böhn]

  … ooooooooof.

* Seriously fleshing out `pyproject.toml` stuff. [Alexander Böhn]

* The `clu-version` command’s prerelease string format is better. [Alexander Böhn]

  … at least I think it is. You try it and tell me!

* The `clu-version` command takes a flag to only print the number. [Alexander Böhn]

  … after installing CLU, use “clu-version --version-only” or
    “clu-version -V” to just print the version number string,
    sans copyright attributions and appelations

* Fixed the display of a code block in `README.md` [Alexander Böhn]

* Fixed embarrasing `README.md` mistake. [Alexander Böhn]

  … it said “man” instead of “many”. HURR DURR

* Minor `README.md` styling issue fix. [Alexander Böhn]

  … the HTML anchor was looking too link-ish

* A minor `README.md` link tweak. [Alexander Böhn]

  … the “clu.testing” time totals image now just links to a larger
    version of itself

* Updated direct-download link in `README.md`, yet again. [Alexander Böhn]

* Updated direct-download link in `README.md` [Alexander Böhn]


## v0.12.3 (2025-05-19)

### Add

* Added a `__dir__()` function to `repl.py` [Alexander Böhn]

### Other

* Bumped version: 0.12.2 → 0.12.3. [Alexander Böhn]

* Fixing inclusion of `CLU_Treatment.md` [Alexander Böhn]

  … this required modifying the filename and “MANIFEST.in”, again

* Removed old `COPYING.md` reference from `MANIFEST.in` [Alexander Böhn]

* Cleaned up some requirements and REPL imports. [Alexander Böhn]

* Removed old-and-outdated COPYING.md. [Alexander Böhn]


## v0.12.2 (2025-05-19)

### Add

* Added the image files in the scratch/ directory. [Alexander Böhn]

### Other

* Bumped version: 0.12.1 → 0.12.2. [Alexander Böhn]


## v0.12.1 (2025-05-19)

### Other

* Bumped version: 0.12.0 → 0.12.1. [Alexander Böhn]

* Another README.md clarifying edit. [Alexander Böhn]

* Updated README.md’s download link. [Alexander Böhn]


## v0.12.0 (2025-05-19)

### Add

* Added a “treadment” document describing CLU. [Alexander Böhn]

### Other

* Bumped version: 0.11.6 → 0.12.0. [Alexander Böhn]

* Updated the “dagger” anchor links in README.md. [Alexander Böhn]

* More README.md edits and link updates. [Alexander Böhn]

* Completely overhauled README.md with new words and links. [Alexander Böhn]

  … and images! Using the text from the “CLU Treatment.md” document.

* Note to self (and anyone else): do NOT use floats for versioning. [Alexander Böhn]

* Cleaned up some `super(…)` calls in `clu.repl.ansi` [Alexander Böhn]

* Removed unnecessary check in `clu.repl.ansi` [Alexander Böhn]

* Notes for `clu.abstract.Serializable` [Alexander Böhn]

* `ANSIFormat` is also a `clu.abstract.Serializable` [Alexander Böhn]

* `FlatOrderedSet` is also a `clu.abstract.Serializable` [Alexander Böhn]

* Such a small nitpick I can’t believe I am making an issue of it. [Alexander Böhn]

* This was annoying me. [Alexander Böhn]


## v0.11.6 (2025-05-07)

### Other

* Bumped version: 0.11.5 → 0.11.6. [Alexander Böhn]

* Removed licensing classifier. [Alexander Böhn]

* Keep `clu.exporting.ExporterBase` subclasses *sans* appname from registering. [Alexander Böhn]

  … this keeps the “clu.exporting.appnames” set from being polluted
    with e.g. technical classes like ExporterBase itself and whatnot

* Fixed an old docstring typo, again. [Alexander Böhn]

* Fixed an old docstring typo. [Alexander Böhn]

* Minor `super(…)` cleanup in `clu.exporting` [Alexander Böhn]

* Updated docstring for `path_to_dotpath(…)` [Alexander Böhn]

  … reflecting the convert-to-underscores whole change bit there.

* Now converting dashes to underscores by default in `path_to_dotpath(…)` [Alexander Böhn]

* Clarification in `filesystem.Directory::ctx_set_targets(…)` [Alexander Böhn]

* Allowed `filesystem.Directory.ctx_prepare(…)` to take an “old” argument. [Alexander Böhn]


## v0.11.5 (2025-05-06)

### Add

* Added `clu.fs.abc.BaseFSName::parent(followlinks=True)` method flag. [Alexander Böhn]

  … this enables the `clu.fs.filesystem.Directory::walkback(…)` method
    to use the “followlinks=True” flag – which it’d been taking this
    whoooole time but totally ignoring (see the programmer notes). But
    now it means something. Yes!

* Added “ismarkedprivate(…)” predicate to `clu.predicates` [Alexander Böhn]

  … this simply checks a string to see if it starts with an underscore

### Other

* Bumped version: 0.11.4 → 0.11.5. [Alexander Böhn]

* Updated the (rare) manually-updated __all__ tuple for `clu.abstract` [Alexander Böhn]

* Name change, reflecting the functions’ new genericism. [Alexander Böhn]

* Minor cleanup in `clu.repl.modules` [Alexander Böhn]

* Allowed specifying a module-indexer function in the big function here. [Alexander Böhn]

  … the “big function” to which we are referring is the classic, but
    long- and ungainly-named “compare_module_lookups_for_all_things(…)”
    …whose long, ungainly name I quite like, but it precludes mentioning
    it in the commit note summary. That’s what is happening here.

* Corrected actual-module check (that was initially bad, oof) [Alexander Böhn]

* Actually checked the returned reloaded module. [Alexander Böhn]

  … which, actually, will not == the preëxisting module, so we ensure
    it isn’t actually equal therein, yes.

* Allowed clu.repl.modules.ModuleMap::reload(…) to actually reload a module. [Alexander Böhn]

  … like as in, calling “modulemap.reload()” will actually reload the
    thing using “importlib.reload(…)” which, I think, is cool.

* Testing line for `clu.repl.modules.ModuleMap::reload(…)` [Alexander Böhn]

  … is it just one line of code? Yes. Does it test the new shit right?
    Also yes. There you go.

* Made `clu.repl.modules.ModuleMap::reload(…)` actually reload modules. [Alexander Böhn]

  … like as in, calling “modulemap.reload()” will actually reload the
    thing using “importlib.reload(…)” which, I think, is cool.

* Fixed up `clu.repl.modules` indexing and related tests. [Alexander Böhn]

  … also corrected a big ol’ WHOOPSIE MOTHERFUCKING DAISY in that
    recently-committed “clu.predicates.ismarkedprivate(…)” function

* Moved PIL.Image import into `try/except` block in “clu/scripts/repl.py” [Alexander Böhn]

* Using `clu.predicates.ismarkedprivate(…)` in “clu/scripts/repl.py” [Alexander Böhn]

* Corrected programmer notes for “Directory::walkback(…)” function. [Alexander Böhn]

* Even better looking. [Alexander Böhn]

* It looks better this way. [Alexander Böhn]


## v0.11.4 (2025-05-03)

### Add

* Added a few missing elements to REPL `__all__` list. [Alexander Böhn]

### Other

* Bumped version: 0.11.3 → 0.11.4. [Alexander Böhn]

* Updated the Python version banners accordingly. [Alexander Böhn]

  … incedentally is anything special planned for Python 3.14? It will
    be, after all, the “Pi-thon” release, hardy har

* Aesthetic improvements to the code in `clu/scripts/repl.py` [Alexander Böhn]

* Tweaked that last adjustment, again. [Alexander Böhn]

* More REPL fixes (specifically `__all__` now works right) [Alexander Böhn]

* Minor tweak to new REPL script-loader hook. [Alexander Böhn]


## v0.11.3 (2025-05-03)

### Add

* Added a hook in the repl script to additionally run a user-specified script. [Alexander Böhn]

  … if such a thing exists. Use the environment variable CLU_USER_SCRIPT
    to point to your script, and it’ll all happen. Yes!

* Added the “pip install” command to `README.md` [Alexander Böhn]

### Other

* Bumped version: 0.11.2 → 0.11.3. [Alexander Böhn]


## v0.11.2 (2025-05-03)

### Other

* Bumped version: 0.11.1 → 0.11.2. [Alexander Böhn]

* Fixed a subtle but show-stopping bug in `clu.scripts.treeline` [Alexander Böhn]

  … used “self” in a `__new__(…)` function definition, blech!

* Cleaned up `super(…)` calls in `clu.abstract` [Alexander Böhn]

* Cleaned up `super(…)` calls in `clu.fs.filesystem` [Alexander Böhn]

* Cleaned up `super(…)` calls in `clu.importing.proxy` [Alexander Böhn]

* Cleaned up `super(…)` calls in `clu.importing.base` [Alexander Böhn]

* Subtle but crucial update in `clu.fs.pypath.mutate_syspath(…)` [Alexander Böhn]

* Every code review offers a chance for some things to DRY out. [Alexander Böhn]

* Everything old is, indeed, new again. [Alexander Böhn]

* Everything old is new again. [Alexander Böhn]

  … because oh shit I thought 2025 was like super generous


## v0.11.1 (2025-05-02)

### Other

* Bumped version: 0.11.0 → 0.11.1. [Alexander Böhn]


## v0.11.0 (2025-05-02)

### Add

* Added a `clu.abstract.Serializable` abstract base class. [Alexander Böhn]

  … basically it just defines `from_json(…)` (as a class method) and
    then `to_json(…)` (as a regular ol’ instance method), each of which
    are so self-explanatory I could just puke

* Added additional `pprint(…)` REPL alias `pp(…)` [Alexander Böhn]

### Other

* Bumped version: 0.10.1 → 0.11.0. [Alexander Böhn]

* Subtle fix in `clu.fs.pypath` add-path logic. [Alexander Böhn]

* Fixed faulty operator in `noxfile.py` [Alexander Böhn]

* Such minutiae. [Alexander Böhn]


## v0.10.1 (2025-04-28)

### Other

* Bumped version: 0.10.0 → 0.10.1. [Alexander Böhn]

* Adjusted `MANIFEST.in` for `bump-my-version` [Alexander Böhn]

* The CLU project `Makefile` also knows how to Bump My Version™ [Alexander Böhn]


## v0.10.0 (2025-04-24)

### Add

* Added tests in `clu.config.ns` for the environment-variable API. [Alexander Böhn]

* Added a “clu.scripts.treeline.node_print(…)” function; updated inline tests accordingly. [Alexander Böhn]

### Other

* Bumped version: 0.9.0 → 0.10.0. [Alexander Böhn]

* Bumped version: 0.8.5 → 0.9.0. [Alexander Böhn]

* Amended and tweaked the new `bump-my-version` config file. [Alexander Böhn]

* Gratuitous nice-ification in REPL “explain(…)” [Alexander Böhn]

* Solved this test problem once and for all … to wit: changing around this class would reorder certain tuples in a slightly nondeterministic fashion. So here we go, yes. Yes! [Alexander Böhn]

* One little negative check in the `treeline.py` inline tests. [Alexander Böhn]

* MORE ASSERTS!!!!!! [Alexander Böhn]

* Switched from using `pkg_resources` to `packaging` … this only comes up once or twice in `clu.version` stuff … also the config FileBase stuff inherits from non-legacy keymaps. [Alexander Böhn]

* MORE ASSERTS!!!!!! [Alexander Böhn]

* Trimmed some programmer notes. [Alexander Böhn]

* Rewrote most of the tests in `clu.config.ns` … as they were completely busted. [Alexander Böhn]

* Sane test names for `clu.config.proxy` [Alexander Böhn]

* Better variable names in `clu.extending` [Alexander Böhn]

* Using `pyattr(…)` in place of one of the `attr(…)` calls … in `clu.extending` [Alexander Böhn]

* Removed yet another legacy import from the “clu.extending” testsuite. [Alexander Böhn]

* Legacy gunk removed. [Alexander Böhn]

* Better reprs for better living. [Alexander Böhn]

* One more “clu.extending” assertion. [Alexander Böhn]

* Better asserts in a “clu.extending” test. [Alexander Böhn]

* Real test names and freedom from legacy garbage … in “clu.extending” [Alexander Böhn]

* Using “copy.deepcopy(…)” in the construction of “clu.importing.ArgumentSink” [Alexander Böhn]

* What the fuck was I thinking, invoking a fucking Java program in the test code? Why would I do that, like ever? N.B. rewrite this fucking garbage. [Alexander Böhn]

* Made some “clu.fs.filesystem.Directory” methods yield-from, instead of returning stupid tuples. [Alexander Böhn]

* Exported functions in “clu.scripts.dictroast” can be invoked with an alternative exporter instance, to like e.g. allow for reasonable use elsewhere. [Alexander Böhn]

* Made some components of “clu.scripts.dictroast” less one-off-y. [Alexander Böhn]

* Trivial comment edit. [Alexander Böhn]

* Some returns in “keyvalue.py” are now yield-froms. [Alexander Böhn]

* Fix for the lack of params in the new ‘zict’ [Alexander Böhn]

* Use `contextlib.closing(…)` whilst yielding database. [Alexander Böhn]

  … like just in case

* Minute simplification in `clu.scripts.treeline` [Alexander Böhn]


## v0.8.5 (2022-12-19)

### Add

* Added on-the-fly filepath-based hashing to `clu.exporting.Exporter` [Alexander Böhn]

### Other

* Bump version: 0.8.4 → 0.8.5. [Alexander Böhn]

* Switched the PYTHON_VERSION constant to a `VersionInfo` instance … it had previously been a float value composed of just the running   Python major and minor version numbers – which oh yes that was   very clever, right up until Python 3.10 became 3.1… woooooof. … With the tweaks to `VersionInfo` allowing string comparisons,   this meant that the few places that looked at the PYTHON_VERSION   value could merely be switched to string comparisons, which that   was easy, and it all seems to work. … It was kind of nerve-wracking to mess around with any of the   `VersionInfo` innards, as that was the first part of CLU that I   properly wrote, before porting the stuff from my old REPL env   scripts†, and as such 1) it was written to have zero other CLU   dependencies, and 2) a lot of weird random low-level forgotton   shit depends upon it in turn. I think everything works but   we shall see… ergh. Yes! [Alexander Böhn]

  † archived, for the curious, at:
  https://gist.github.com/fish2000/51cf4ea3977abbd7ea6ce74c442eb870#file-replutilities-py

* One can now compare `VersionInfo` instances with version strings. [Alexander Böhn]

* Many gratuitous match/case-related additions • There’s a match/case in `clu.scripts.treeline` for, like, no reason • There’s a new `clu.abstract.SlotMatch` metaclass, which assigns the   new `__match_args__` attribute to a slotted class, as per the   ancestral union of all `__slots__` attributes   … which is a use-case for `clu.predicates.slots_for(…)`, which     makes me happy like Simple Jack • There are tests for `clu.abstract.SlotMatch` • There is a fix for a fucking irritating pytest warning that was,   unrelatedly, happening in the `clu.repr` testsuite, due to pytest   trying to execute a random fucking lambda that was in there as if   it were a test, and then boo-hoo-ing about how this particular   “test function” was returning a fucking value. WELL SHIT. [Alexander Böhn]

* Exporting the `clu.exporting.stringhash(…)` function … also repositioned the `hashlib` import. [Alexander Böhn]

* Adjustments to `clu.exporting.stringhash(…)` and friends • `Exporter.hash()` and `Exporter.datafile()` are plain methods,    instead of properties • `Exporter.hash()` will return `None` if the exporter instance is    lacking a valid dotpath, and `Exporter.datafile()` checks for    this possibility •  There’s a post-test diagnostic for inspecting the LRU cache    used by the `stringhash(…)` function. [Alexander Böhn]

* Implemented `submap(…)` specifically for `NodeTreeMap` [Alexander Böhn]

* Say hello to my very first production `match`/`case` statement … taking the first step into a larger world, as it were, FUCK YES. [Alexander Böhn]

* Actually nodes are collections. [Alexander Böhn]

* Nodes are iterable, and soooooo… [Alexander Böhn]

* Recursive `to_dict(¬)` serialization output for tree nodes … no way to reconstitute those dicts yet, but hey. [Alexander Böhn]

* KeyMaps (including `NodeTreeMap`) correctly handle kwarg updates. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Directly inserting new nodes in `NodeBase.add_child(…)` … should be faster by like nanoseconds or somesuch. [Alexander Böhn]

* Mode `clu.scripts.treeline.RootNode` a `clu.abstract.ReprWrapper` [Alexander Böhn]

* Ensure node name strings are copied anew when cloning. [Alexander Böhn]

* Implementations for `clone(¬)` for the node tree class tower. [Alexander Böhn]

* Ensure nodes added with `_append_node(…)` have the proper parentage. [Alexander Böhn]

* Inline documentation corrections. [Alexander Böhn]

* No longer hardcoding the appname in `ExporterBase.datafile` [Alexander Böhn]

* Forgot to propagate the `cls` arg to `clu.config.keymap.dictify(…)` [Alexander Böhn]

* Simplified creating and populating a `RootNode` from a command. [Alexander Böhn]

* Only retrieve the command history once in `dictroast.py` [Alexander Böhn]

* Exporting a few functions from `clu.scripts.dictroast` [Alexander Böhn]

* Non-spammy and accurate command line history in `dictroast.py` … as in: we only print the last ten commands, and the logic that   does that printing reports stuff about how many lines there were,   and correctly numbers those lines. [Alexander Böhn]

* Removed inline test stubs from `clu.scripts.dictroast` … as they were causing the module to get picked up by Nox as one   with actual tests present; running the module with no arguments   produces a non-zero error code (by design) and that was screwing   things up a bit. [Alexander Böhn]

* Allow an arbitrary dict class in `clu.config.keymap.dictify(…)` … also stop star-importing everything in “clu.version”, because   that module contains one-off functions that have to run without   the rest of CLU, and are not fit for general human consumption,   generally speaking. [Alexander Böhn]

* WHOOOOOOPS … I’m 44 years old, you’d think I’d know how to correctly call a   fucking function by now. [Alexander Böhn]

* Specify walking function in `FrozenFlat`’s `articulate(…)` call … defaults be damned; explicit is better than implicit, rite?? [Alexander Böhn]

* Implemented `__index__(…)` in `clu.scripts.treeline.Level` [Alexander Böhn]

* Ensure non-negative values are used by `clu.scripts.treeline.Level` [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Quick-n-dirty node tree visualization … using halfviz and arbor.js:   • http://arborjs.org/halfviz/   • https://github.com/samizdatco/arbor. [Alexander Böhn]

* Stubbed out the “read” feature in `dictroast.py` [Alexander Böhn]

* Making dictroast.py executable. [Alexander Böhn]

* Casefolding the “action” argument. [Alexander Böhn]

* Initial start of a command-line test/analysis script. [Alexander Böhn]

* One more assertion in the `clu.exporting.Exporter` data API test. [Alexander Böhn]

* Exporters can have arbitrary data associated with them … this works by generating a unique filename for each explorer,   based on the explorers’ assigned dotpath (although, of course,   you the user are free to specify your own file path) … the generated file path is saved to the “user_config” directory,   as per what a `clu.fs.appdirectories` determines … the mechanism for accessing the arbitrary-data interface is based   on the Python “shelve” standard-library module; you basically do: [Alexander Böhn]

  >>> with exporter.data() as database:
    >>>     database['yo-dogg'] = "I heard you like shelving"

  … et cetera – look up `shelve` for the deets, my doggie. Yes!

* No longer exporting a redundant function in `treeline.py` [Alexander Böhn]


## v0.8.4 (2022-10-02)

### Add

* Adding the built docs HTML file. [Alexander Böhn]

* Added a test to check `NodeTreeMap` json serialization. [Alexander Böhn]

* Added a `clu.scripts.treeline.treewalk(…) function … which that iteratively walks a node tree, yielding values in the   established `*namespaces, key, value` style used by other walking   functions, as required by `clu.config.abc.NamespaceWalker` [Alexander Böhn]

* Added a skeleton for a treenode-backed NamespaceWalker KeyMap. [Alexander Böhn]

* Add a REPL shortcut for `pprint(tuple(thing))` … which I do all the fucking time. [Alexander Böhn]

* Added `popitem()` definitions for `ExporterBase` and `Namespace` [Alexander Böhn]

* Added `FlatOrderedSet.sort(…)` and unittests to match. [Alexander Böhn]

* Added checks for the exporter’s `__code__` attribute reassignment. [Alexander Böhn]

### Other

* Bump version: 0.8.3 → 0.8.4. [Alexander Böhn]

* Fixing bump2version configuration. [Alexander Böhn]

* Taking a stab at moving away from `setup.py` [Alexander Böhn]

* Properly using `clu.config.ns.pack_ns(¬)` where needed. [Alexander Böhn]

* It’s not great, but it’s a start. [Alexander Böhn]

* Updating docs requirements. [Alexander Böhn]

* Trying again to bootstrat ReadTheDocs. [Alexander Böhn]

* Implemened roundtrip dict methods for `NodeTreeMap` … This required a `clu.config.ns` function to simply partition a   namespaced key into the packed namespace string and the raw key … Also a minor adjustment to `clu.config.keymap.articulate(…)`,   allowing one to specify a map-walking function (which I feel like   this one will be handy in other circumstances) … The `from_dict(…)` class method uses the new namespace function,   and the `to_dict(…)` method makes use of the new  `articulate(…)`   calling convention … The `from_dict(…)` internals mutate the NodeTreeMap’s node tree   instance – which this points a way forward for the development   of a possible mutable NodeTreeMap class, if we want that shit   down the road … BOOOIOIOINNG. [Alexander Böhn]

* Direct access to underlying data in `NodeBase.{leaf,namespace}(…)` [Alexander Böhn]

* Moved namespaced access logic to the `NodeBase` class. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Using `itertools.filterfalse(…)` to iterate child namespaces … Also added some docstrings. [Alexander Böhn]

* Splitting it like we should. [Alexander Böhn]

* I make stupid mistakes sometimes. [Alexander Böhn]

* NodeTreeMap is a working NamespaceWalker-backed KeyMap!! [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* First `__contains__(¬)` and `__getitem__(¬)` NodeTreeMap implementations. [Alexander Böhn]

* Making all the new node-tree stuff available in the REPL, pt. II. [Alexander Böhn]

* Making all the new node-tree stuff available in the REPL. [Alexander Böhn]

* Moved argument parsing into RootNode. [Alexander Böhn]

* Exporting RootNode and Node. [Alexander Böhn]

* Nodes can reassemble the subcommands from which they had resulted. [Alexander Böhn]

* Shit’s faster. [Alexander Böhn]

* Printing child node count in `node_repr(…)` during CLI parsing test. [Alexander Böhn]

* Docstrings and programmer notes for CLI parsing test. [Alexander Böhn]

* Initial command-line parsing works for fucks’ sakegit push! [Alexander Böhn]

* Made `acceptable_types` a set. [Alexander Böhn]

* Docstrings, methods, miscellany, et cetera. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Backing `BaseNode.child_nodes` with a dict instead of a list … which is demonstrably faster, and also subjectively betterer. [Alexander Böhn]

* Code formatting OCD. [Alexander Böhn]

* Avoid incrementing the level manager initially in `node_repr(…)` [Alexander Böhn]

* Name clarification, pt. II. [Alexander Böhn]

* Name clarification. [Alexander Böhn]

* Exporting these new things. [Alexander Böhn]

* Because doing `level.level` looks like someone fucked something up. [Alexander Böhn]

* TAKE HEED OF THIS. [Alexander Böhn]

* Trying to contend with leaves and namespaces separately. [Alexander Böhn]

* Broke out `Node.get_child(…)` [Alexander Böhn]

* Started work on a tree-node-based command-line parser thing. [Alexander Böhn]

* Meaningful inline test names for `clu.importing.proxy` [Alexander Böhn]

* Meaningful inline test names for `clu.typespace.namespace` [Alexander Böhn]

* Meaningful inline test names for `clu.typespace` [Alexander Böhn]

* Using our `pythonpy-fork` package in the dev requirements. [Alexander Böhn]

* Efficient `FlatOrderedSet` addition operators, and tests for same. [Alexander Böhn]

* Meaningful inline test names for `clu.imporing.base` [Alexander Böhn]

* Meaningful inline test names for `clu.config.env` [Alexander Böhn]

* Programmer note for `clu.config.abc.KeyMap.pop(…)` default value. [Alexander Böhn]

* Spelling. [Alexander Böhn]

* Proper recursion on error in `clu.importing.modules_for_appname(…)` [Alexander Böhn]

* Inline tests in `clu.config.ns` check for `java` executable. [Alexander Böhn]

* Inline tests for `clu.config.keymap.{Frozen}Nested.submap(…)` … also removal of the pointless LRU caching for the underlying   namespace iterators. [Alexander Böhn]

* Further `clu.exporting` inline-test adventures. [Alexander Böhn]

* Fleshing out some of the `clu.exporting` inline tests. [Alexander Böhn]

* Fixed wonky `clu.exporting.Registry` class-registration logic. [Alexander Böhn]

* Programmer-note minutiae. [Alexander Böhn]

* The export mechanism updates `__code__.co_name` for callables … The `clu.exporting.determine_name(…)` function inspects this   attribute, and it was lopsided that we weren’t updating it with   our new names accordingly. [Alexander Böhn]

* Cleaned up the `clu.config.env` test diagnostics. [Alexander Böhn]

* Preventing false positives in `FrozenNested.__contains__(¬)` … the problem was, if you had a nested instance with a namespace   such as “yo:dogg:wat” that contained items (e.g. a value at the   key “yo:dogg:wat:thefuck”) the `__contains__(¬)` implementation   would have returned True for like e.g. `instance['yo:dogg']` and   `instance['yo']` when those aren’t actual values, despite them   looking like values when looking at the underlying implementation   which is a nested dict. … now it behaves the same way as a flat instance, where a key named   “yo:dogg:wat:thefuck” has no implications about anything within   the encompassing outer namespaces (“yo”, “dogg” and “wat”). … OH YES!!!! [Alexander Böhn]

* Clarified a variable name in `clu.all.import_all_modules(…)` [Alexander Böhn]

* Serializing `FlatOrderedSet` instances preserve their predicates … at least as long as the predicates are properly defined functions   that aren’t lambdas – or if they are lambdas, they’re ensconced   in a module somewhere and exported with `clu.exporting` so they   have a sensible name. Basically. [Alexander Böhn]

* Printing qualified name of the thing in `clu.repl.ansi.ansidoc(…)` [Alexander Böhn]


## v0.8.3 (2022-09-10)

### Other

* Bump version: 0.8.2 → 0.8.3. [Alexander Böhn]

* Updated Makefile. [Alexander Böhn]

* Fixed docstring on `clu.config.env.FrozenEnviron` … it was giving the wrong instructions for using a KeyMap key to   access a namespaced environment variable. [Alexander Böhn]

* Whitespace. [Alexander Böhn]


## v0.8.2 (2022-09-10)

### Add

* Added tests for serialization of `clu.config.abc.FlatOrderedSet` [Alexander Böhn]

* Added support for `clu.config.abc.FlatOrderedSet` in serialization … at least for JSON serialization, it works. Yes! [Alexander Böhn]

* Added basic pickling support to the KeyMaps. [Alexander Böhn]

* Added a `from_dict(…)` class method to the KeyMap ABC tower … the default just instantiates the class using the instance dict   as the first argument. [Alexander Böhn]

* Additional checks in Environ JSON rountrip test. [Alexander Böhn]

* Added some docstrings and notes to `clu.config.codecs` [Alexander Böhn]

* Added basic inline tests and harness to `clu.config.codecs` [Alexander Böhn]

### Other

* Bump version: 0.8.1 → 0.8.2. [Alexander Böhn]

* Spelling! [Alexander Böhn]

* Keeping a `__slots__` definition simple. [Alexander Böhn]

* Support for `clu.typespace.namespace.Typespace` in our `ChainMap` … specifically in the `clu.dicts.ChainRepr` “reprlib” implementation. [Alexander Böhn]

* Fleshed out a docstring in `clu.config.env.FrozenEnviron` [Alexander Böhn]

* Minor cleanup. [Alexander Böhn]

* Fixed the `clu.constants.consts.BPYTHON` REPL detection. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Serializing `clu.config.env.Environ` uses live environment dicts … clarified the relevant tests, too. [Alexander Böhn]

* Testing JSON serialization of both `FrozenEnviron` and `Environ` [Alexander Böhn]

* Enhanced JSON serialization support … you can serialize and deserialize `clu.config.env` KeyMaps … there are `to_json(…)` and `from_json(…)` instance and class   methods, respectively – `to_json(…)` has a straightforward   implementation in the KeyMap ABCs … serializable things lacking `to_json(…)` methods get serialized   as flat lists (this is in anticipation of serialization support   for `clu.config.abc.FlatOrderedSet` which is forthcoming … Oh yes!! [Alexander Böhn]

* Did you know `nox` shouldn’t be installed inside virtualenvs? … I didn’t! [Alexander Böhn]

* Cleaning up the Nox configuration. [Alexander Böhn]

* Roundtripping KeyMaps through JSON totally works! [Alexander Böhn]

* Now using `clu.dicts.asdict(…)` in `clu.config.codecs` serializers … This allows one to intercept the dict-ification in instances to   be serialized, by providing a `to_dict(…)` method. … The reason you might want to do this is because, at the moment,   re-instance-ification is done by taking the serialized dict and   passing it blindly to the class constructor as the first and only   argument. In the case of KeyMaps, doing `dict(keymap)` always   gives you a flattened dict, with namespaced keys – but not all   KeyMaps can be roundtripped thusly, like e.g. Nested which   expects a nested dict (like duh). So that’s special. [Alexander Böhn]

* Fleshing out the new JSON codec stuff. [Alexander Böhn]


## v0.8.1 (2022-08-30)

### Add

* Added `clu.config.codecs` … for the purpose of housing customized subclasses of e.g. json   encoding plumbing, and the like. [Alexander Böhn]

### Other

* Bump version: 0.8.0 → 0.8.1. [Alexander Böhn]


## v0.8.0 (2022-08-30)

### Add

* Added some lines in “test_importing.py” for the new properties … those being `__args__` and `__origin__` [Alexander Böhn]

* Added `__origin__` and `__args__` props to clu.importing.ModuleAlias. [Alexander Böhn]

* Added a `clu.fs.filesystem.Directory.subdirectories(…)` method. [Alexander Böhn]

* Added a test for `Directory.walkback()` … also reverted the check from the last push within the method,   whose behavior was not what I’d intended. [Alexander Böhn]

* Added an additional check in Directory.walkback() [Alexander Böhn]

* Added a ROOT_PATH constant representing the filesystem root. [Alexander Böhn]

* Added a “walkback(…)” method to fs.filesystem.Directory … this works like “os.walk(…)”, “Directory.walk()” et al. except   in reverse: it yields parent directories and their listings until   it hits the filesystem root. [Alexander Böhn]

* Adding a “clu.csv” test suite ... for some reason. [Alexander Böhn]

* Adding inline tests to “clu.exporting” [Alexander Böhn]

* Adding a test for the “clu.exporting.thismodule()” hack. [Alexander Böhn]

* Adding the Git hooks directory to MANIFEST.in ... also starting to brush up some of the “clu.compilation” stuff. [Alexander Böhn]

* Adding inline tests to codecov.io coverage reporting. [Alexander Böhn]

* Added a testsuite for “clu.fs.abc” ... the main test function uses a trivial subclass of the primary     ABC “clu.fs.abc.BaseFSName”, and is paramatrized with a list     of the systems’ temporary directories ... there’s also a check for the “clu.fs.abc.TypeLocker” type cache. [Alexander Böhn]

* Added assert check for “clu.repl.modules.ModuleMap.most()” [Alexander Böhn]

* Added a testsuite for “clu.repl.modules” based off the inlines. [Alexander Böhn]

* Added tests for the “clu.repl.columnize” string format types. [Alexander Böhn]

* Added a pytest boolean fixture “gitrun”, True if tests run from Git ... which is now leveraged in the “clu.version” tests – like in     case someone should run the testsuite from like a tarball or     some shit like that. [Alexander Böhn]

* Added testsuite for the “clu/scripts/repl.py” loader code ... specifically: a sandboxed importer/runner and integration tests     for the “explain(…)”, “star_export(…)” and “module_export(…)”     functions defined therein ... also trimmed some dead code from the “clu.naming” testsuite,     and updated the suites for “clu.scripts.boilerplate” and     “clu.dispatch” to use the “environment” fixture to set their     respective «PYTHONPATH» values (instead of hacky bullshit which     they were using up until now). ... Also included are related updates to the noxfile. [Alexander Böhn]

* Added nox module-check session to test “clu.scripts.repl” [Alexander Böhn]

* Added a function to get the “current module” using hacky nonsense ... specifically, “inspect.currentframe()” and globals inspection ... UGH. [Alexander Böhn]

* Added missing “__repr__(…)” method to “clu.version.VersionInfo” [Alexander Böhn]

* Added new const “DEFAULT_APPSPACE”, originally in “clu.application” [Alexander Böhn]

* Added an “appspaces” iterable class property via metaclass subtype ... uses the recently-added “clu.importing.appspaces_for_appname()”     function to return a generator over the appspaces that pertain     to the appname of the class in question. [Alexander Böhn]

* Added “appspaces_for_appname(…)” to “clu.importing” ... along with “clu.importing.all_registered_appspaces()” and the     lambda helper function “clu.importing.get_appspace(…)” ... this allows the importer methods “FinderBase.find_spec(…)” and     “LoaderBase.create_module(…)” to a) be more specific in what     they say “yes” to, essentially, and b) avoid having to use the     polymer cache, which is a separate thing and shouldn’t be being     leveraged in the lower-level import hook stuff. [Alexander Böhn]

* Added an inline test for class-module overrides to “clu.importing” ... this demonstrably ensures that definitions on a ProxyModule     will take precedent over any of the values that are furnished     by any of the ProxyModule’s targets. [Alexander Böhn]

* Added a hacky fix to show signatures for non-inspectable functions ... as in, externally-defined extension functions, or builtins, or     what have you ... based on https://stackoverflow.com/a/43845679/298171. [Alexander Böhn]

* Added “experimental” “clu.dicts.ChainMapPlusPlus” variant ... it uses a “clu.config.abc.FlatOrderedSet” internally, instead     of a plain list ... this took some playing-around with a bunch of things: first,     I had to rig “clu.typespace.namespace” to lazily import stuff     from “clu.dicts” (which it used non-trivially) just to even get     FlatOrderedSet imported safely; then, of course, there had to     be like a bunch of little nudgey changes in the FlatOrderedSet     code itself, just like to support mappings in general; then I     went on a tangent to fix a bunch of general problems with the     “clu.dicts.ChainRepr” custom repr-izer that ChainMap uses, and     which OK that was actually super-satisfying to do that and I’m     not compolaining there; and THEN I could subclass ChainMap and     write a few basic tests, which is where we are right now dogg. [Alexander Böhn]

* Added mini-type-tower of ABCs for descriptors (data and non-data) ... available now in “clu.abstract” ... also further streamlined the textwrap-related kwargs situation     in “clu.repl.ansi” [Alexander Böhn]

* Added an ANSICodeHighlighter formatter type. [Alexander Böhn]

* Added ANSI filtering ... for awkward-interim displays, e.g. TextMate’s HTML output. [Alexander Böhn]

* Added “flags” and “change” properties to some filesystem classes ... plus the respective and related unit-test additions, too. [Alexander Böhn]

* Added an abstract “Format” class to “clu.repl.ansi” [Alexander Böhn]

* Added ptpython REPL Makefile targets. [Alexander Böhn]

* Added IPython REPL Makefile target. [Alexander Böhn]

* Added a const indicating if we’re running inside bpython or not ... which incidentally they don’t make it easy for you, those wacky     bpythoneers – they make a mean ANSI REPL but not one with an     API that I’d call pin-down-able. [Alexander Böhn]

* Added a const indicating if we’re running inside IPython or not. [Alexander Böhn]

* Added a “clu.config.env.Environ” instance to “clu.application.AppBase” [Alexander Böhn]

* Added Python 3.8 classifier. [Alexander Böhn]

* Added function to compute the name of the “__main__” module. [Alexander Böhn]

* Adding bespoke class- and instance-repr methods to “ExporterBase” ... the former of which requires an intermediate metaclass, oh well. [Alexander Böhn]

* Added a test for “clu.fs.filesystem.Directory.suffixes(…)” [Alexander Böhn]

* Added a test for “clu.fs.misc.re_excluder(…)” [Alexander Böhn]

* Added a test in “test_version.py” for “clu.repl.cli.print_version” [Alexander Böhn]

* Added “clu.naming.duplicate(…)” and a “clu.naming.renamer” decorator ... which I originally stole them from PyPy, but then kitted them     out for CLU so thoroughly that yeah they’re mine now, OK? ... I mean I give credit to the orig for inspiration but yeah judge     for yourself doggie:     • http://bit.ly/func-with-new-name. [Alexander Böhn]

* Added some asserts to “clu.importing” tests related to new constants. [Alexander Böhn]

* Added a “clu.fs.appdirectories.clu_appdirs(…)” convenience function ... returns an instance of “clu.fs.appdirectories.AppDirs” specific     to the CLU project itself ... caches the return value with “functools.lru_cache(…)” ... as a result “clu.fs.appdirectories.AppDirs” is now hashable –     it inherits from “collections.abc.Hashable” and implements a     (reasonably hacky) “__hash__()” method ... specifying an “appauthor” value when constructing an AppDir on     a non-Windows system will no longer raise ‘UnusedValueWarning’     – some unit tests were updated to reflect this ... the most cursory of sanity-check-iness code calling this new     convenience function has been tacked onto the existant inline     print-vomit test function run… indicating all systems nominal. [Alexander Böhn]

* Added a pytest option to control the temporary-deletion exit handle. [Alexander Böhn]

* Addings “docs/” subdirectory to MANIFEST.in. [Alexander Böhn]

* Adding yolk1977 as a dev requirement. [Alexander Böhn]

* Added “__missing__(…)” to “clu.typespace.namespace.Namespace” ... and an inline test for same ... and a refinement to the use of the “__missing__(…)” method in     “clu.dicts.ChainMap.mapcontaining(…)” – the method that tries     to find and return the mapping within the chainmap containing     a given index ... and an error trap in “clu.importing.modules_for_appname(…)”     that retries the “yield from” if the monomer-registry cache     (which is implemented using ‘weakref.WeakValueDictionary’) that     underlies that function should happen to change size in the     middle of the iteration. [Alexander Böhn]

* Added ChainMaps to the types “clu.repr.strfield(…)” can handle. [Alexander Böhn]

* Added “fast” ‘flatten(¬)’ implementation, about 400% speedier – ... good but not stellar. [Alexander Böhn]

* Added weakref types to the typespace, and SimpleNamespace inline tests. [Alexander Böhn]

* Added the fixture-cache-stats diagnostic to “clu.config.defg” [Alexander Böhn]

* Added a diagnostic to print a report on the fixture cache stats. [Alexander Böhn]

* Added metafunction capabilities to “clu.testing.utils.InlineTester” [Alexander Böhn]

* Added unit tests for the boilerplate generation command. [Alexander Böhn]

* Added a “shortrepr(…)” method to show namespace info, sans newlines ... also added the “show-consts.py” and “show-modules.py” script     invocations to the Makefile. [Alexander Böhn]

* Added a “clu.importing.PerApp.appspaces()” convenience function ... does precisely what you think it does. [Alexander Böhn]

* Added inline test for “clu.importing.ProxyModule” fallbacks. [Alexander Böhn]

* Addressing automated GitHub security alert. [Alexander Böhn]

* Additional sanity-check in “Environ.__exit__(…)” [Alexander Böhn]

* Added wildcard «‽» to the semantic-version regex “build” field. [Alexander Böhn]

* Additional testing to ensure that “FrozenEnv” is frozen. [Alexander Böhn]

* Added API to directly access the backing environment dictionary. [Alexander Böhn]

* Added proper error-handling when calling Git commands. [Alexander Böhn]

* Added “version” make target. [Alexander Böhn]

* Added a “clu.version.git_version” module and trivial functions ... simple shit to get the git tag version ... unlike the other stuff under “clu.version” which are pretty     much entirely self-contained, “clu.version.git_version” uses     standard CLU stuff (e.g. the Exporter, the inline test harness,     et cetera) so WE’LL JUST SEE HOW THIS GOES NOW WON’T WE. [Alexander Böhn]

* Added ‘ValuesView’ and ‘ItemsView’ tailored for “NamespaceWalker” ... which these types each implement much faster, less circuitous     versions of the “__contains__(…)” and “__iter__()” methods,     utilizing the “walk()” method of their associated mappings ... the necessity for these was no gamble or – oddly enough in my     personal case – wasn’t premature. No! I saw the need for speed     reflected in the timing reports coming from my own new outfit     for running inline tests – see all those recent changes to the     “clu.testing.utils” module, specifically regarding “@inline”     and friends. Yes!!!!! [Alexander Böhn]

* Added “iterlen(…)” to put an end to like e.g. “len(tuple(¬))” ... pretty much a straight-up ⌘-c ⌘-v from the “more-itertools”     source – namely their function “ilen(…)” [Alexander Böhn]

* Added a bunch of ancestors to “clu.testing.utils.@inline” [Alexander Böhn]

* Added “@inline” decorator to bpython REPL script. [Alexander Böhn]

* Added note about executing test functions multiple times. [Alexander Böhn]

* Added baseline environment-variable-access function API ... also differentiated the testing of the “old-style” Flat and     Nested classes, versus the new shit. [Alexander Böhn]

* Added a “FrozenNested.mapwalk()” method, delegates to “mapwalk(…)” [Alexander Böhn]

* Added namespaced “KeyMap.pop(…)” and “KeyMap.clear(…)” [Alexander Böhn]

* Added a test illustrating “try_items(…)” particular behavior ... w/r/t DefaultDict factories and “getitem(…)” [Alexander Böhn]

* Added a “consts” fixture to the pytest plugin. [Alexander Böhn]

* Added ‘has_appname’ to “clu.exporting.ExporterBase.__dir__(…)”’s filter. [Alexander Böhn]

* Added a “clu.shelving.dispatch.shutdown(…)” function ... like “clu.shelving.dispatch.trigger(…)” but with an actual call     to ‘sys.exit(¬)’ at the end ... also more bells & whistles to “clu.shelving.redat.RedisConf”     have been grafted on, somehow. [Alexander Böhn]

* Added a bunch of async shit I don’t quite understand. [Alexander Böhn]

* Adding default Redis config file. [Alexander Böhn]

* Added a few diagnostic lines to the Redis inline test. [Alexander Böhn]

* Added some gratuitous asserts to the Redis inline test. [Alexander Böhn]

* Adding the Exporter to “clu.shelving.redat” [Alexander Böhn]

* Adding a “shelving” module and initial Redis process-handler. [Alexander Böhn]

* Adding conftest.py to MANIFEST.in. [Alexander Böhn]

* Adding one-liner “conftest.py” to load the pytest plugin module ... this re-enables running pytest just as ‘pytest’ – instead of     having to be all like ‘python -m pytest -p clu.testing.pytest’     via make each and every time. [Alexander Böhn]

* Added “issingleton(…)” and “issingletonlist(…)” to “clu.typology” ... plus we’re using the former now in “clu.repr.strfield(…)” which     is cleaner than what it was doing before (which was dirtier) [Alexander Böhn]

* Added notes about caching where relevant to “clu.fs.misc” docstrings. [Alexander Böhn]

* Added a “clu.fs.misc” test for checking the users’ home directory. [Alexander Böhn]

* Added a “clu.fs.misc” test for checking the process’ umask values. [Alexander Böhn]

* Added tests for “clu.fs.misc.u8{bytes,str}(…)” functions. [Alexander Böhn]

* Added a test for “clu.fs.misc.suffix_searcher(…)” [Alexander Böhn]

* Added a test for “clu.fs.misc.swapext(…)” ... literally pulled right out of the functions’ docstring. [Alexander Böhn]

* Added a test for “clu.fs.misc.re_suffix(…)” [Alexander Böhn]

* Added a test for “clu.fs.misc.filesize(…)” [Alexander Böhn]

* Added some tests to the “clu.fs.misc” testsuite. [Alexander Böhn]

* Added walrus-operator-related nota-benne. [Alexander Böhn]

* Added “clu.importing.ModuleBase.__execute__()” hook method ... this allows class-module implementations to run code at the     analogous point in the module lifecycle to, like, e.g. when a     file-based modules’ code is run by the Python interpreter. ... There’s lots of explanatory docstrings and a working example in     the testsuite, doggie, yes. [Alexander Böhn]

* Adding “setproctitle” to the dev requirements. [Alexander Böhn]

* Added another inline test to “clu.importing” using “importlib.import_module(…)” [Alexander Böhn]

* Added “clu.importing.SubModule” context-manager ... for creating temporary class-module subtypes, suitable for     testing, among other things ... includes an inline test and a support predicate “newtype(…)” [Alexander Böhn]

* Added “clu.predicates.union(…)” as a shortcut for “set().union(…)” [Alexander Böhn]

* Added method “clu.exporting.Registry.has_appname(…)” [Alexander Böhn]

* Added docstring note about “__slots__” to ModuleBase. [Alexander Böhn]

* Added a nota benne about the instance/class name. [Alexander Böhn]

* Adding “clu.abstract” ABCs module and class-module tests. [Alexander Böhn]

* Added “array.ArrayType” to the typespace as “types.Array” [Alexander Böhn]

* Added “__getstate__(…)” and “__setstate__(…)” to “clu.config.base” ... specifically, the “clu.config.base.NamespacedMutableMapping”     subclasses “Flat” and “Nested” [Alexander Böhn]

* Added new field types and spruced up the existing ones ... also began adding the new configuration schema stuff to the     demo “yodogg” project found in tests/. [Alexander Böhn]

* Adding “clu.constants.enums” to the hardcoded module list. [Alexander Böhn]

* Adding “clu.exporting.Exporter” to “clu.repl.columnize” [Alexander Böhn]

* Added a stub clu/__main__.py file (all it does now is print the version) [Alexander Böhn]

* Added a 'clu-boilerplate' console script entry point ... which echoes out the (mercifully very short) boilerplate you     need to use CLU in a new Python module. [Alexander Böhn]

* Added the Exporter stuff to “clu.testing.utils” [Alexander Böhn]

* Added a “temporaryname” fixture-factory function to “clu.testing” [Alexander Böhn]

* Added a stupid little version-string script. [Alexander Böhn]

* Added an actual export to the ExporterBase subclass test. [Alexander Böhn]

* Added a __class_getitem__ method to “clu.exporting.Registry” ... and amended the relevant test accordingly. [Alexander Böhn]

* Added builtin exemplars to REPL env. [Alexander Böhn]

* Added “wheel” to the install requirements. [Alexander Böhn]

* Added “show-consts.py” and “show-modules.py” to the tox run ... I did this on a lark, to see if it would work and planning to     revert it immediately – but it is actually really good to have     these all print out, particularly in the PyPy environment (and     perhaps others to come) which are not as readily inspectable.     So these stay in. Yes!! [Alexander Böhn]

* Added pytest markers back in to tox.ini – ... I AM PLEASED TO ANNOUNCE TOX RUNS AND EVERYTHING PASSES! Except     a bunch of Windows tests that get skipped. BUT OTHERWISE!!!! [Alexander Böhn]

* Added “scripts/show-modules.py” showing module-name nondeterminism ... it doesn’t really show all the modules, per se: it iterates     over all of them but at the moment it only displays the results     in which the results from the two calls “pickle.whichmodule(…)”     and “clu.naming.determine_module(…)” are dissimilar. ... also I re-used the same ANSI formatting stuff as I used in the     “show-consts.py” script (and they weren’t all that fleshed out,     designwise, at any rate) so this thing could use some work. [Alexander Böhn]

* Adding submodule in “tests” for Exporter secondary-package setup. [Alexander Böhn]

* Added a “zict.LRU” buffer atop the ANSI code lookup caches. [Alexander Böhn]

* Added tests for “clu.naming.dotpath_to_prefix(…)” [Alexander Böhn]

* Added argument checking to “clu.naming.dotpath_to_prefix(…)” [Alexander Böhn]

* Added φ to represent the name of a Partial lambda-type ... which, you may ask, what the fuck does that mean? Allow me to     explain: I had originally used a hack (by way of subclassing)     to allow the Partial types returned from “apply_to(…)” to be     given names and repr-string that matched lambda-type functions     – that is to say, functions created with the “lambda” keyword –     and in doing so, they’d all be treated the same as lambda-types     by the “clu.exporting” mechanisms. This was handy because, as     it turned out, “apply_to(…)” Partials were just as useful as     typical lambda-type predicates, in like a whooole lot of the     kinds of situations we get ourselves into, programmatically,     here in the salt-mines of CLU coding. ... The problem arose just now, which while checking out some other     recent (but unrelated) updates to the Partial-type structure,     I saw that Partial instances retained a value for “__module__”     that matched where the Partial class was defined (that is to     say, “clu.predicates”) rather than wherever that specific     Partial had been instantiated. ... I did not like that. This was due, of course, to the fact that     lambda-types are created with a keyword, whereas Partial-types     are just dumb ol’ instances, and these things obey different     internal Python laws. ... To fix it, the Exporter again came to the rescue. This patch is     mainly: 	a) The addition of the constant φ to represent the default 	   name of the Partial-type – known as the “phi-type” here- 	   after – and all the necessary support for a constant of 	   this sort (it gets referenced in some GREEK_STUFF dict 	   somewhere, etc etc). 	b) The embellishment of the Exporter’s “export” method to 	   support the φ constant and the phi-type idea – which 	   incedentally results in the “__lambda_name__” attribute 	   actually being useful now, as it retains the naming 	   information germane to what the thing originally was: 	   lambda-type (“<lambda>”) or phi-type (“<Partial>”). 	c) The necessary tweaks to related functions to consider 	   all of this (like e.g. the clu.typology predicate called 	   “islambda(…)” considers both λ and φ when checking the 	   value of “__lambda_name__”) 	d) Finally, and most crucially, the addition of logic – 	   again in the Exporter – to alter the attribute value of 	   “__module__” to the correct value whenever it encounters 	   a phi-type in need of name-adjustment. This is doubly 	   interesting (if you asked me) as it is the first use 	   of the “dotpath” attribute the Exporter now sets, as a 	   result of that recent edit wherein all Exporters are now 	   initialized as “Exporter(path=__file__)” – the “path” 	   value is used to compute the dotted module path, and lo, 	   IT SEEMS TO WORK!!!!!!!!!!!!!!! Yeah dogg. [Alexander Böhn]

* Adding the new Directory subclasses to the REPL environment. [Alexander Böhn]

* Added two more Directory shortcut-subclasses in “clu.fs.filesystem” [Alexander Böhn]

* Added “predicate_none(…)” to clu.predicates using “negate(…)” ... also added tests for same and for the recently-added predicate     “clu.typology.differentlength(…)” [Alexander Böhn]

* Added “differentlength” to clu.predicates ... this predicate isn’t a simple “negate(…)” of “samelength(…)” –     it checks that its arguments are iterable in the same way as     “samelength(…)” – so we define it here preemptively because of     the fact that its negation is nontrivial. [Alexander Böhn]

* Added scripts/show-consts.py – a prettyprinter for clu.constants ... It’s adapted from the ad-hoc little inline const prettyprinter,     “clu.constants.consts.print_all()” with a bunch of my own ANSI     formatting sludge on top ... At this point it looks childish, but not too far off the final     mark – it’s a weird medium in which to design, can I just say? ... Yeah like I would say 72-74% done, maybe ... Just go ahead, straight up `python scripts/show-consts.py` to     execute it… you (meaning anyone besides me) might have to do     some freaky PYTHONPATH shit first; I am virtualenv-ing all of     this stuff right now but I’ll try and make these sort of things     work OK, as like a example-code thing, an “Intro to CLU” type     of deal, maybe. [Alexander Böhn]

* Added and filled a fixture graveyard at tests/obsolete_fixtures.py ... contains my spruced-up versions of the pytest-datadir fixture     code, like for future reference of someshit I guess. [Alexander Böhn]

* Added a test for “resolve(…)” from clu.predicates. [Alexander Böhn]

* Added in instance checks for “metaclass(…)” tests. [Alexander Böhn]

* Added “iscallable(…)” and “iscallablelist(…)” to clu.typology ... and in so doing also tweaked “isfunction(…)” to return False for     class types – all of which are callable – and any arbitrary     instances of class types in posession of a `__call__(…)` method     …the identification of which is now the domain of the brand-new     “iscallable(…)” predicate. NOTE that this means “iscallable(…)”     is VERRRRY DIFFERENT from the builtin “callable(…)” predicate,     the likes of which is very eager call its operands callable if     that is in any way vaguely the case. [Alexander Böhn]

* Adding to the “callable_types” typelist in clu.typology. [Alexander Böhn]

* Added a test for the collator-based accessors. [Alexander Böhn]

* Added “metaclass(…)” predicate and collator-based accessors ... all are found in clu.predicates; ... `metaclass(thing)` will retrieve either a) type(type(thing),     		       	    	     	    b) type(thing), or 					    c) thing,     depending on whether “thing” is a metaclass, a class, or an     instance. ... There are three new accessors: “attrs(…)”, “pyattrs(…)” and     “items(…)”. These are all based on the new “collator(…)” apply-     style basis function, which works like the “accessor(…)” and     “searcher(…)” functions to apply one simple “getattr(…)”-type     function to a thing, using a list of 1+ attribute or item names     to compose its result. Unlike the other functions, which return     the first viable result from the application list that gets     returned, “collator(…)”-based accessors accumulate all results     into an ordered tuple for return. WHICH MEANS: these accessors     work like so: [Alexander Böhn]

  class YoDogg(object):

  	     yo = "Yo dogg,"
  	     dogg = "I heard you like"
  	     iheard = "irritating recursion"

  	assert attrs(YoDogg, 'yo', 'dogg') == ("Yo Dogg,",
  					       "I heard you like")
  	assert attrs(YoDogg, 'dogg', 'yo') == ("I heard you like",
  	       		     	     	       "Yo Dogg,")
  	assert attrs(YoDogg, 'yo', 'wtf') == ("Yo Dogg,",)
  	assert attrs(YoDogg, 'wtf', 'hax') == None

  ... I mean and you know the drill by now, “pyattrs(…)” is the same
      shit but for __python__ __reserved__ __names__, and “items(…)”
      of course is for getting items, like out of dicts and whatnot.

* Added some superfluous asserts on the numpy import. [Alexander Böhn]

* Added numpy import-or-skip to ensure the “array_types” assertion ... since 'MaskedArray' is hardcoded into the assertion, the test     would theoretically fail if numpy was unavailable, since the     typelist wouldn’t have been populated with any numpy types in     the init phase of the clu.typology module; I know *I* can’t     freakin imagine a world without numpy but that doesn’t mean     there isn’t such a place somewhere, assuredly; hence this lil’     tweak right here, for the people who live in that spiritually-     impovershed theoretical numpy-less flummoxing drugery, yes. [Alexander Böhn]

* Added “fields” and `stringify(…)`-based repr to clu.keyvalue. [Alexander Böhn]

* Added an “update(…)” dict-like method to the exporter. [Alexander Böhn]

* Added test checking the sum of three exporter instances. [Alexander Böhn]

* Added text fixture to provide long “Lorem Ipsum”-style texts; ... wrote a new key-value-store test using the Lorem Ipsum fixture; ... switched one of the filesystem tests to use our wrapped version     of NamedTemporaryFile and in doing so, caught triaged and fixed     an actual bug in that code -- which I believe is how this whole     thing is supposed to work in the first place, right? Right. ... a few assorted touchups to the filesystem module have also made     it in there, I do believe. [Alexander Böhn]

* Added “dict_types” to clu.typology ... fully clarified a few imports from clu.constants.polyfills too. [Alexander Böhn]

* Added custom-bool method example in predicate builtin helper tests. [Alexander Böhn]

* Added another set of exemplary assertions to the helper tests. [Alexander Böhn]

* Added `allof(…)`/`anyof(æ)`/`noneof(≠)` variadic helper functions ... they’re in clu.predicates – their presence helps to clarify     just why the fuck `tuplize(…)`/`listify(≠)` etc are there like     to begin with: they’re all variadics instead of single-argument     functions whose operand(s) must be iterable. Yes! [Alexander Böhn]

* Added `hasattr(¬)` negations: `noattr(…)` and `nopyattr(…)` [Alexander Böhn]

* Added “isenum(…)” pre-checks to the new enum dict-examining predicates. [Alexander Böhn]

* Added “negate(¬) function for negating boolean predicates. [Alexander Böhn]

* Added more Python versions to tox.ini. [Alexander Böhn]

* Added more fixtures and keyvalue tweaks ... Practical upshot is that the first test is done and runs. [Alexander Böhn]

* Added “version” and “update(…)” to the keyvalue API. [Alexander Böhn]

* Added PyPy compatibility check in clu.predicates.Partial.__init__(…) [Alexander Böhn]

* Adding XDG_RUNTIME_DIR to the list of verboten XDG env names. [Alexander Böhn]

* Added more tests for module functions in clu.fs.filesystem ... specifically: `ensure_path_is_valud(…)`, `write_to_path(…)`,     `which(…)`, `back_tick(…)` (in its simplest mode of operation),     and `rm_rf(…)`. [Alexander Böhn]

* Added `isXXXXXlist(…)` predicates to clu.typology ... this consists of two moving parts:     a) Added an `issequence(…)` predicate to clu.typology        ... this uses “collections.abc.Sequence” to check a given        	   thing’s sequence-ness     b) Added `isXXXXXXlist(…)` predicates, each composed as such:        isXXXXXXlist = lambda thinglist: issequence(thinglist) and        		             	    predicate_all(*thinglist) [Alexander Böhn]

  ... docstrings courtesy clu.exporting.Exporter

* Added/edited some apply_to(…)-related docstrings. [Alexander Böhn]

* Added try/except around dict-ification in Exporter.__init__(…) [Alexander Böhn]

* Added some method docstrings in clu.exporting.Exporter. [Alexander Böhn]

* Added “default” keyword args for accessor/searchers ... as in those from clu.predicates; tests were updated accordingly. [Alexander Böhn]

* Added tests for enum aliasing ... added an AliasingEnum subclass of Enum that makes use of the     AliasingEnumMeta metaclass (largely for conveniences’ sake). [Alexander Böhn]

* Added __init__.py to scripts. [Alexander Böhn]

* Added memberless Enum subclass to `isenum(…)` tests. [Alexander Böhn]

* Added tests for `isenum(…)` and `enumchoices(…)` ... and with that, I do believe we are approaching 100% coverage     for the clu.predicates module, fuck yes. [Alexander Böhn]

* Added tests for `clu.predicates.apply_to(…)` ... also fixed a bug in the `iscontainer(…)` predicate (one of the     internal-usage `apply_to(…)` preds) that was particularly prone     to being triggered by operations on typelists (q.v. source code     for clu.typology module supra.) as any iterable non-normative     •type• would return True from the predicate, causing the logic     of the function to attempt to iterate the type, which of course     that would fail in like nearly almost all cases (enum types of     course being the notable exception). So now `iscontainer(…)`     checks for `not isclasstype(…)`, as do several other predicates     that were doing things like manually inspecting __mro__ or some     shit like that; everything is more consistent and nicer-looking     now, yes. ... Also, most of the apply_to tests straight-up copy-paste-use the     typelist stuff from clu.typology (Ibid.) [Alexander Böhn]

* Added `isnormative(…)` and `iscontainer(…)` predicates ... these are, like, refinements of `isiterable(…)` which matches     string-ish and bytes-ish types, which sometimes you don’t want;     so `isnormative(…)` matches all those string/bytes sorts of     things, while `iscontainer(–)` is just a logical combination     that does `isiterable(…) and not `isnormative(…)`. ... there are tests now for all the “apply_to(…)”-based logical     predicate stuff e.g. `predicate_{all,any,and,or,xor}(…)` and     also tests for `uncallable(…)`, `isexpandable(…)`, and those     two new ones `isnormative(…)` and `iscontainer(…)`. Fuck yeah. [Alexander Böhn]

* Added tests for all the `getpyattr(…)` and related accessors. [Alexander Böhn]

* Added NOp tests for clu.predicates. [Alexander Böhn]

* Added tests for `isiterable(…)` and `ismergeable(…)` ... also made the version stuff consistent in its import-ness ... and tweaked a few consts in clu.constants. [Alexander Böhn]

* Added predicate-logic functions and lambdas. [Alexander Böhn]

* Adding a few lines to .gitignore. [Alexander Böhn]

* Added support for alias() in Pythons lacking __set_name__ [Alexander Böhn]

* Added a Makefile to do project-related tasks. [Alexander Böhn]

* Added tons of project-related meta-documents ... You know, stuff like: * .editorconfig * .landscape.yml * .travis.yml * appveyor.yml * setup.cfg * conftest.py * COPYING.md * MANIFEST.in ... and a few new legalese morsels in LICENSE.txt. [Alexander Böhn]

* Added tox.ini. [Alexander Böhn]

* Added note about the project name. [Alexander Böhn]

* Added some new constants; predicates in use in filesystem.py. [Alexander Böhn]

* Added filesystem, appdirs, and keyvalue modules ... plus some miscellaneous support functions for same. [Alexander Böhn]

* Added dicts, exporting, naming, sanitzer etc. [Alexander Böhn]

* Added header boilerplate to version.py. [Alexander Böhn]

* Added a bunch of basic project stuff ... .gitignore, .bumpversion.cfg; ... ABOUT.md, README.md, CODE_OF_CONDUCT.md ... __init__.py files in clu/ and test/ ... __version__.py and semantic-versioning code in version.py ... basic setup.py boilerplate. [Alexander Böhn]

### Minutiae

* Minutiae. [Alexander Böhn]

* Minutiae’s minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae in “clu.importing” inline test typecheck. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae in the “show-modules.py” script. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

* Minutiae II. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

### Other

* Bump version: 0.7.2 → 0.8.0. [Alexander Böhn]

* Clarified the  docstrings. [Alexander Böhn]

* Further KeyMap optimizations, this time in `FrozenNested.submap(…)` … which that implementation had always bugged me as it was pretty   pathological – no longer to we have to iterate the whole KeyMap   instance to slice out a submap. … the tradeoff is, we do iterate the whole KeyMap in order to test   via short-circuit whether or not the namespace(s) provided to   `FrozenNested.submap(…)` are valid, and return an empty dict if   they are not; fortunately tho now since the various `flatten()`   and `nestify()` implementations default to returning immutable   (“frozen”) instances, `namespace()` calls are cached by default. … So yeah I am pretty happy with that. [Alexander Böhn]

* Optimized nestification in `clu.config.keymap.{FrozenFlat,Flat}` … Facilitating this meant the addition of a `flatwalk(…)` function   that walks a flattened namespaced dictionary and expands the   embedded namespaces accordingly. [Alexander Böhn]

* Optimized loops in `clu.config.abc.NamespaceWalker.flatten(…)` … that function defaults to returning a FrozenFlat instance now,   instead of a mutable Flat … assignment to the output instance happens in a single dictionary   comprehension instead of a loop that triggers namespace packing   and unpacking … Yeah! [Alexander Böhn]

* Simplified the `clu.config.abc.KeyMap.clear(…)` implementation … which now it depends on a call to the underlying `submap(…)` [Alexander Böhn]

* Test update in leu of that last `clu.importing.ModuleAlias` update. [Alexander Böhn]

* Using `tuplize(…)` in some `clu.importing.ModuleAlias` methods … this prevents None values from sneaking in there. [Alexander Böhn]

* Avoiding a gratuitous list comprehension in `clu.config.keymapview` … which was used in the default `__len__(…)` implementation in the   base abstract class. Now we use `clu.typology.iterlen(…)` on a   generator expression which we all know is way betterer. [Alexander Böhn]

* Fixed a long-standing problem with `clu.predicates.slots_for(¬)` … the issue was that if a class at some point defined a single slot   with the (completely valid) syntax `__slots__ = 'string_name'`,   the output from `slots_for(¬)` would have iterated that string   resulting in something like `('yo', 'd', 'o', 'g', 'g')` instead   of the expected `('yo', 'dogg')`. … we deal with this by introducing a `clu.predicates.normalize(…)`   function that uses `clu.predicates.isnormative(…)` to selectively   tuplize strings while passing other iterables through without   fucking with them. [Alexander Böhn]

* Construct `clu.config.keymap.Nested` instances from iterables is GO … just needed a single additional `dict(…)` call in the constructor … so, like, you can create instances of all KeyMap types found in   `clu.config.keymap` concrete definition package the same way you   can create ordinary dicts – iterables yielding `key, value` pairs   will do the trick. [Alexander Böhn]

* No longer are defaultdicts necessary in `clu.config.keymap.Nested` … the source of the bug was one line of code in which I had tried   to be clever – frequently the downfall of many a programmer – and   the fix was to just expand it into two freaking lines already,   which made it more legible. … This allowed for the removal of the “DefaultTree(…)” function,   which I disliked. This should speed things up, too. Yes! [Alexander Böhn]

* Optimized `__contains__` and `__getitem__` in config.keymap.Nested … fucking FINALLY. This should be more appropriately described as   “de-pathologized” rather than “optimized”. … Also updated the tests that depended on an earlier repr fix. [Alexander Böhn]

* Clarified the `clu.config.abc.KeyMap.popitem()` docstring text. [Alexander Böhn]

* Finally implemented `clu.config.abc.KeyMap.popitem()` … which what took me so long? Seems to work deterministically   enough on both the Flat and Nested keymap implementations. [Alexander Böhn]

* Spelling totally counts. [Alexander Böhn]

* Fixed that bug in Python there. [Alexander Böhn]

* Re-enabled long-dormant inline `clu.importing.base` tests. [Alexander Böhn]

* Updated `clu.typology` with the new `Typespace` type. [Alexander Böhn]

* Fixed `clu.typespace` compatibility and added `@inline.runif(…)` … to wit: *) The `clu.typespace.types` pseudo-module is now an instance of    `clu.typespace.namespace.Typespace` which is a descendent of    `clu.typespace.namespace.Namespace` and has typespace-specific    stuff in it.    +) MEANING: if you do `types.ModuleType` (which is something       present in Python’s `types` module) it looks up the right       thing, as does `types.Module` – which was the point of CLU’s       `types` in the first place    +) The on-the-fly sub-namespace stuff is cleaner, I believe    +) The inline tests in `clu.typespace` have been fixed up *) Speaking of tests: when decorating inline test functions you    can now conditionally run things, by using `@inline.runif(…)`    with a boolean value. Examples and inline documentation of this    are included *) Fuck yes! [Alexander Böhn]

* The new `Directory.subdirectories(¬)` method uses a regex filter … previously it had used a suffix-specific filter, which employed   `clu.fs.misc.suffix_searcher(…)` which made kind of very little   sense as directories rarely have file-suffix-y suffixes by which   one might wish to filter them. [Alexander Böhn]

* Slightly more lexically precise there. [Alexander Böhn]

* My word, the stuff in `clu.stdio` is incomplete. [Alexander Böhn]

* Using f-strings as docstrings is bad. I stopped doing it. [Alexander Böhn]

* Made `clu.testing.utils.format_environment(…)` handle empties. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Fixed flaw in comparing IDs. [Alexander Böhn]

* Clu.fs.filesystem.Directory.walkback() yields lists of strings … whereas originally it was handing back lists of directory entry   objects, which I don’t think can just be used in a string context   without e.g. “os.fspath(…)”-ing them first, erm. [Alexander Böhn]

* Few things are as satisfying as swapping `return` with `yield from` [Alexander Böhn]

* Trimmed an intermediate iterator. [Alexander Böhn]

* Rewrote `Directory.walkback(…)` to use itertools.groupby(…) … The other version was using an `if`/`else` branch inside a `for`   loop inside a `while True` loop, which that just rubbed me the   wrong way, basically. This is less irritating, personally. [Alexander Böhn]

* New `Directory.walkback(…)` function was terminating early … So I fixed that. [Alexander Böhn]

* Including the banner figlet command, for reference. [Alexander Böhn]

* Future-resistance for the repl banners … not quite future-proofing. SHAMELESS PLUG: I figlet-ed banners   up to Python 3.11 because that’s the version that will contain   my patch!! Yaaayyyyyy!!!! [Alexander Böhn]

* CONSISTENCY!!! [Alexander Böhn]

* Removed gratuitous “tuplize(…)” calls … these were found in “__slots__” assignments in assorted class   definitions. Removing these calls allowed trimming of imports   from “clu.predicates”. … there are also a few changes to the nox/pytest configurations,   allowing for tests to run instead of collapsing into a heap of   inscrutable error messages. [Alexander Böhn]

* PyYAJL bindings appear unwilling to build. [Alexander Böhn]

* Further punctiliousness in error-supressing defaults in `exporting.py` [Alexander Böhn]

  … to wit: we use a dummy object, which could never be what either
  of these functions is looking for.

* Recomposed a sentence in a comment to be aesthetically better. [Alexander Böhn]

* Commented out a problematic numpy dtype conversion. [Alexander Böhn]

  … doing `numpy.dtype(numpy.floating)` issues a warning, and you only
    have to tell me not to do a thing once, dogg

* Forgot to remove distutils-related import. WHOOPS. [Alexander Böhn]

* Changed zero to False in “itermodule(…)” getattr() call default. [Alexander Böhn]

* Rewrote clu.fs.filesystem.which(…) and fixed other peoples’ bugs. [Alexander Böhn]

  * … the `which(…)` rewrite removes the dependency on a distutils
    function, “find_executable(…)”, and thus distutils itself. The
    new stuff uses CLU internals and is, as noted in the code, both
    faster and betterer.

  * … and as for other peoples’ bugs: the functions `itermodule(…)`
    and `itermoduleids(…)` in “clu.exporting” would – more frequently
    than you might think – throw weird, un-track-downable errors
    when iterating some third-party module that did “clever” things
    upon being imported (that is, when its module code was executed)
    and the result was inappropriate exceptions being thrown with
    no indication as to what and where the problem was to be found.
    The quick/cheap solution, herein, was to alter these functions’
    `getattr(…)` calls to include a default value – `False` in the
    case of `itermodule(…)` and zero for `itermoduleids(…)` – which
    seems to supress a bunch of the issues I was having, at least
    on my systems. This tests out OK for me, but we’ll keep an eye
    on it for side effects. Yes.

* This requirements file just makes Dependabot lose its mind. [Alexander Böhn]

* Fixed ambiguously failing git-tags test. [Alexander Böhn]

* Dependabot update. [Alexander Böhn]

* Bump version: 0.7.1 → 0.7.2. [Alexander Böhn]

* Switching over to bump2version ... as it appears the original “bumpversion” has committed infocide. [Alexander Böhn]

* Including “clu.importing” top-level module in coverage report. [Alexander Böhn]

* Restructured “clu.importing” into a subpackage ... as that module was getting a bit ungainly. Thus far, we have     split off the ProxyModule stuff, and juggled the inline tests     accordingly; most notably, the “initialize_types(…)” call for     CLU’s “Module” type is in “clu/importing/__init__.py”. After     sorting out all the imports, this proved to not fuck things     up – SO FAR. We shall see. [Alexander Böhn]

* Not-quite-redundant env-value defaulting in “clu.repl.columnize” [Alexander Böhn]

* Bump version: 0.7.0 → 0.7.1. [Alexander Böhn]

* Fix for the “dict resized during iteration” occasional puke ... which that’s a problem whilst importing some other people’s     package modules, occasionally – NOT a CLU issue, mind you –     that OK yeah, for more complainey exposition regarding this     crapola, see the inline programmer notes in “clu/exporting.py” [Alexander Böhn]

* EVEN MORE coverage nitpicks for “clu.dispatch” ... 100% coverage or bust. [Alexander Böhn]

* More coverage nitpicks for “clu.dispatch” [Alexander Böhn]

* Inline test-function coverage for “clu.dispatch” [Alexander Böhn]

* Some coverage gap-filling for “clu.dicts” [Alexander Böhn]

* Coverage minutiae for “clu.extending” [Alexander Böhn]

* Slight refactor – and coverage minutiae – for “clu.extending” [Alexander Böhn]

* Test coverage for various methods in “clu.constants.enums” [Alexander Böhn]

* Enabled respecializing (via subscript) a “clu.importing.ModuleAlias” [Alexander Böhn]

* Some coverage minutiae for “clu.importing” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* That should be the very last uncovered line in “clu.config.env” [Alexander Böhn]

* Coverage minutiae for “clu.config.ns” and “clu.config.env” [Alexander Böhn]

* Dead-code removal and coverage minutiae. [Alexander Böhn]

* Dealing with inherited hashability for mutable keymap types ... there is now a “clu.abstract.Unhashable” type, which explicitly     removes any “__hash__(…)” methods and intercedes appropriately     in “__subclasshook__(…)” – such that checking the subclass or     instance á la “isinstance(instance, clu.abstract.Unhashable)”     works correctly most of the time     - it won’t work if “collections.abc.Hashable” is an explicit       subtype in the MRO of a type in question, and     - implicit (aka structural) subtype checks against this new       Unhashable type won’t work for vanilla “abc.ABC” descendants       because all of them include a “__hash__(…)” method apparently       (which is a slot method inherited from a C-API PyType, it       would seem) ... there are real inline tests in “clu.config.ns” that actually go     and execute a small Java program to list all of the available     Java “system properties” – which are basically dot-separated     namespaced keys already, conveniently ... “clu.config.abc.FlatOrderedSet._from_iterable(…)” implements     the necessary call to make FlatOrderedSet work out-of-the-box     with the “collections.abc.Set” API ... there are tests for the new “clu.abstract.Unhashable” stuff in     the pytest suite. [Alexander Böhn]

* Pragma-no-cover-ing the “pytest_sessionfinish(…)” exithandle-assigner. [Alexander Böhn]

* Removed “nondeterministic” test function annotation. [Alexander Böhn]

* Sorted out inline-tests-versus-__main__ controversy ... specifically, “clu.typespace” and “clu.api” are packages whose     “__init__.py” files define inline tests – that is all well and     good, those tests run as normative during iterative testing     while coding (like e.g. ⌘-R in TextMate et al.) but then for     nox and codecov runs, they need a stub ”__main__.py” file to     import and run the inline test function. AND THAT’S ALL these     “__main__.py” files should aspire to ever do, okay? Tough break     kid, better luck next time ... also: coverage fixes (because it is always fucking wonky and     counterintuitive, behaviorwise, phhheh) ... and: the ‘Click’ package has been bumped up to the big time:     it is now a bona-fide install requirement. Huzzah! [Alexander Böhn]

* Actual inline tests running in “clu.api” skeleton. [Alexander Böhn]

* Skeleton of Click-based “clu.api” nested-command-module scheme. [Alexander Böhn]

* Inline tests for “clu.csv”; plus some spring cleaning ... as in, got rid of Makefile rules and scripts that weren’t doing     me any favors ... all marginally-useful old scripts live in “clu/scripts/legacy”     which is wildcard-excluded from coverage. [Alexander Böhn]

* Bump version: 0.6.9 → 0.7.0. [Alexander Böhn]

* Testing and CI config updates. [Alexander Böhn]

* Full coverage for “clu.constants.consts” (albiet with pragmas) [Alexander Böhn]

* Full coverage for “clu.predicates” in the pytest suite. [Alexander Böhn]

* Tweak to “clu.version.git_version” speeds things up ... and should nudge coverage to 100% [Alexander Böhn]

* Near-100% test-coverage for “clu.repl.modules” [Alexander Böhn]

* Lots of miscellany ... to wit: 1. Eschewing “clu.predicates.typeof(…)” for plain “type(…)” in the    “clu.extending” function-dispatch type registry 2. This, due to a specific None-check “clu.predicates.typeof(…)”    now contains 3. “clu.importing.ModuleAlias” is now a Callable (per ABC ancestry)    and is completely and totally test-covered 4. “clu.importing.ModuleAlias” uses “clu.typology.subclasscheck(…)”    instead of “issubclass(…)” (which is a shitty function and, I am    now rembering, problematic enough to have spurred me to write    the original “clu.typology.subclasscheck(…)” way back when 5. None-check in “clu.naming.suffix(…)” 6. No-argument check in “clu.naming.dotpath_join(…)” 7. Loads of explicit checks for “clu.naming” helpers including the    venerated “dotpath_join(…)”, “dotpath_split(…)”, and “suffix(…)” [Alexander Böhn]

* EVEN MORE “clu.compilation.compiledb” updates. [Alexander Böhn]

* More “clu.compilation.compiledb” overhauls and rearrangement. [Alexander Böhn]

* Sprucing up tests things in some of “clu.config” [Alexander Böhn]

* We’re just now able to instance “clu.compilation.CDBJsonFile” again ... it needs a great deal of work – but it does now cleanly inherit     from “clu.fs.abc.BaseFSName”! That seriously serendipitously     kind of worked out w/r/t how the existing implementation was,     like, such a good fit for it [a BaseFSName ancestor]. Yes! [Alexander Böhn]

* The services of `readme_renderer` are no longer required ... we’ve decided to go in a different direction, clean out your     desk and go see HR on the way out, fuckface. [Alexander Böhn]

* Allowing the test-project-specific “.tm_properties” file into Git. [Alexander Böhn]

* Started a testsuite for the “clu.all” module. [Alexander Böhn]

* Makefile version-bump rules use “git-pushex” ensuring coverage runs. [Alexander Böhn]

* Tests for some constituent “clu.importing” parts *) “clu.importing.PolymerType” and “clu.importing.PerApp” *) “clu.importing.Registry.for_qualname(…)” *) “clu.importing.ModuleAlias” – through “templated” ModuleBase    			       	 subtype inspection *) “clu.importing.installed_appnames(…)” *) “clu.importing.initialize_new_types(…)” and its sister function,    “clu.importing.initialize_module(…)” – these are un-exported and    					  private, reserved only for 					  internal use… ah but such 					  things are in need of a 					  good test-suite-ing, much 					  as any others *) Expanded import-hook resolution assertions and verifications *) Cache-integrity verification – there are a shitzillion levels    of caching in play throughout the import-hook stuff; fortunately    it all seems to be harmoniously working, at the time of writing *) Dead-code haircuts all around *) Minutiae adjustments in “clu.importing” – whitespace, etc *) The “clu.importing” inline tests were brought up to parity with    the pytest suites, on an as-needed basis. [Alexander Böhn]

* Coverage setting tweaks, and attribution notes for “git-pushex” [Alexander Böhn]

* Only calculating the branch in “git-pushex” if necessary. [Alexander Böhn]

* Removed no-op script from post-push hook actions. [Alexander Böhn]

* Trimmed dead code and installed coverage post-push hook. [Alexander Böhn]

* Basic pre- and post-push Git hook-script infrastructure in place. [Alexander Böhn]

* Setting up Autohook for git-hook script dispatching ... Q.v. https://github.com/nkantar/Autohook supra. [Alexander Böhn]

* Sprinkling lots of “pragma: no cover” directives hither and thither. [Alexander Böhn]

* Coverage for “clu.repl.columnize” inline demo function. [Alexander Böhn]

* More code-coverage settings updates. [Alexander Böhn]

* Inline test for legacy “clu.repl.ansi.ansidoc(…)” function ... née “old_ansidoc(…)” [Alexander Böhn]

* Bump version: 0.6.8 → 0.6.9. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Removed hardcoded absolute paths from “test_repr.py” ... using “consts.BASEPATH” instead – easy-peasy, lemon-squeezy. [Alexander Böhn]

* Switching “clu.repl.ansi.ansidoc(…)” to use the new DocFormat class ... which this brilliant new hotness type is both composed from and     descended from various “clu.abstract.Formatter” types, defined     for the most part in “clu.repl.ansi” (a module that oooooof, if     ever any module needed to get split up into smaller, and more     bite-sized chunks, this one is it) ... using the “clu.repl.ansi.DocFormat” type to furnish “ansidoc(…)”     will be faster, more expandable, more controllable, sexier,     smarter, better-looking, and generally a better all-around deal     than the one-off corner-case-ridden function it replaces. [Alexander Böhn]

* Enabled previously failing assert in “columnize(…)” tests. [Alexander Böhn]

* Ported the original “pycolumnize” testsuite over ... Q.v. https://git.io/JvFuu supra. ... the orig used unittest and mock so there was some significant     editing done ... two assertions are currently commented out. [Alexander Böhn]

* Match “clu.scripts.repl.star_export(…)” test critera to the function. [Alexander Böhn]

* Minor “.coveragerc” update. [Alexander Böhn]

* Updates to codecov configuration, and tweaks in “clu.importing” [Alexander Böhn]

* Skip the manifest check when running nox outside of a Git repo. [Alexander Böhn]

* Noxfile docstring tweak. [Alexander Böhn]

* Some updates and streaminling to “clu.scripts.repl” [Alexander Böhn]

* MISCELLANEOUS/SUNDRY * Fix in “clu.importing” inline test import statement; * “clu.abstract.BasePath” uses “os.fspath(…)”   ... meaning the class-kwarg “basepath” accepts “os.PathLike”       instances as well as strings and bytes (and None, I guess)   ... note to self: subclass “clu.abstract.ValueDescriptor” and       make a “PathDescriptor” that knows about path stuff * Very minor adjustment to dev requirememts. [Alexander Böhn]

* Notes and docstrings for the new stuff in “clu.importing” ... as in: the new “__init_subclass__(…)” methods of “FinderBase”     and “LoaderBase”; the equivalent logic in “ModuleBase”; many     other miscellaneous related assorted sundries as well ... also the “clu.importing.ModuleAlias” class has been kitted out     similar to “clu.importing.ArgumentSink”, like with a bunch of     ABC ancestors, hashability, in/eqality operators, and other     fancy stuff. [Alexander Böhn]

* All crucial subclass logic transplanted from “initialize_types(…)” ... so: “clu.importing.FinderBase” and “clu.importing.LoaderBase”     have “__init_subclass__(…)” methods that take care of assigning     e.g. loader class and instance references to subclasses that     require them – which frankly this should have been where this     stuff was done from day one, but ah oh well ... “clu.importing.LoaderBase” has a subclass cache (in “linkages”)     and a per-subclass instance cache, modeled after the mechanism     used by “clu.exporting.ExporterBase”; all those aforementioned     “__init_subclass__(…)” methods lean on this new registry setup     in some way; ... this assignment logic was also added/moved into ModuleBase’s     existing “__init_subclass__(…)” method ... all the “dynamic subtype” interstitial class declarations in     the “initialize_types(…)” and related/subordinate functions     are just ‘pass’ statements     • related logic in the “dynamic” subtype creation stuff one       currently finds in “clu.application” was also axed ... all this shit was double-checked six ways from Sunday – all the     tests run OK; a new inline diagnostic added to “clu.importing”     dumps the contents of the new loader caches; etc etc ad nauseum ... oh yeah one more thing, “clu.abstract.AppName” searches the MRO     for an appname if its subtype is initialized without specifying     one (or if it’s None) in the same manner of fashion employed by     “clu.importing.ModuleBase” in its “__init_subclass__(…)” method. [Alexander Böhn]

* Fixed resize-during-iteration heisenbug in “Loader.__repr__(…)” [Alexander Böhn]

* Marking the “PYTHON_BIN” const as a path. [Alexander Böhn]

* Whitespace aesthetics. [Alexander Böhn]

* Filter out Nones when listing appspaces. [Alexander Böhn]

* Trimmed obsolete code and notes. [Alexander Böhn]

* Very minor docstring nitpick. [Alexander Böhn]

* “Class.fields” attributes are additively heritable within “clu.fs” ... to wit: if you have a filesystem class, one that inherits from     “clu.fs.abc.BaseFSName”, and you use a “fields” attribute on     that class, it will behave like e.g. the “__slots__” special     attribute behaves: you assign tuples of strings to it, and when     utilized behind-the-scenes, “clu.predicates.ancestral_union(…)”     is employed to always look at the union of all “fields” tuples     across the class tower in question. Phew. ... I may move this mechanism into “clu.abstract” – but that may     require more dunder-name abuse, project-wide, which that’s a     thing I am actually actively trying to avoid, these days. Hey,     a guy can exhibit personal growth, no? [Alexander Böhn]

* Disabling symlinking to “clu.fs.filesystem.TemporaryName” instances. [Alexander Böhn]

* Programmer note about the super/subclass attribute-delete thing. [Alexander Böhn]

* Ignore errors when attempting to delete a subclass attribute ... this bug caught courtesy of the TMI project, ha. [Alexander Böhn]

* Bump version: 0.6.7 → 0.6.8. [Alexander Böhn]

* “clu.importing.ProxyModule” is now a “generic template type” ... to wit, you don’t simply inherit from ProxyModule – you do it     like this: [Alexander Böhn]

  class MyProxy(ProxyModule[Module]):
  	    # …etc

  .... where the “Module” type parameter is something you got from
       calling “clu.importing.initialize_types(…)”, as in:

           Module, Finder, Loader = initialize_types(APPNAME)

  ... which why? Why would anyone do that? Because this way, the
      definition of ProxyModule can exist in “clu.importing” in a
      totally concrete way – independent of you the CLU user and
      whatever and however you might choose to define your own apps’
      specific ModuleBase types. You can then import, “specialize”
      and use “clu.importing.ProxyModule” with ease, and we don’t
      have to add more crapola to the PolymerType registry or the
      type-initialization system or any of that other stuff.

  ... Furthermore, we can proceed to use this strategem for future
      generic class-module types – or perhaps, if need be, generic
      module finders or loaders – for a totally forward-compatible
      class-module typology that isn’t reliant on subclassing things
      (which that is one of CLU’s blemishes, the fact that currently
      its users are asked to arbitrarily subclass a lot of shit). As
      they say on Mandalore, this is the way.

  ... And if I may add a personal note here – I am fucking shocked
      and amazed that this whole “generic template type” trick is
      something that actually works – and that it did so on more or
      less the first serious go-around. It is totally both a wicked
      abuse of the “typing” modules’ new reserved dunder-methods,
      but also a total sweet embrace of same. Seriously I cannot
      believe this shit at all dogg, yeah!

* Spelling fix. [Alexander Böhn]

* “clu.fs.abc.BaseFSName” is no longer an AbstractContextManager ... it turns out that this one abstract ancestor did not really     much matter – we just made “clu.fs.filesystem.Directory” and     “clu.fs.filesystem.TemporaryName” inherit individually from     the AbstractContextManager ABC; we only had to add a one-line     “__enter__(…)” method to TemporaryName and that was that ... thus opening the door to mixing BaseFSName in with classes that     descend from working context-manager types; see the immediately     preceding commit regarding a TemporaryFileWrapper subclass that     mixes in BaseFSName – implementations of BaseFSName mixin types     can be pleasantly minimal, needing only “__init__(…)”, their     “name(…)” properties, and “to_string(…)” in many cases (and we     can maybe get rid of the requirement for the latter, methinks) [Alexander Böhn]

* Experimental “fs.abc.TemporaryFileWrapper” / “BaseFSName” subclass ... only exists for now in an inline test function, which runs OK ... the trick was making the “name” ABC property writeable in the     implementation, incidentally ... need to unclobber __enter__ and __exit__ though, most likely ... to set this up we moved “clu.fs.filesystem.temporary(…)” over     to “clu.fs.misc”; one unit test was likewise moved as well. [Alexander Böhn]

* Fixing “arrowheads” in extracted signatures with a regex ... which is surprisingly effective and not thing of now having     two problems, actually, evidently, yeah. [Alexander Böhn]

* Had to name something “inline” inside “clu.typespace.test()” ... as that’s how the nox inline-test collector spots such modules. [Alexander Böhn]

* Moved the “clu.typespace” inline tests to a “__main__.py” file ... The reason for this is: the setup we’re using with `nox` to     detect and run all the inline tests constructs commands of the     form: [Alexander Böhn]

  $ python -m clu.module.name

  ... using the “clu.exporting.path_to_dotpath(…)” function to change
      a modules’ file path into the dotted module name that’s used in
      that command there.† The problem, then, is “path_to_dotpath(…)”
      special-cases “__init__.py” and “__main__.py” files, converting
      paths that terminate in these filenames into the name of the
      enclosing module, e.g. “clu/config/__init__.py” will get turned
      into just “clu.config”. In 99.9999% of cases, this is what you
      want. But what I just found out is: doing the `python -m` thing
      with a dotpath that resolves to a package – that is to say, a
      directory – tries to load and execute a “__main__.py” file from
      that directory, *NOT* an “__init__.py” file. There is even some
      kind of specialized error message your Python executable will
      spit back at you if you try to do `python -m package.dotpath`
      when a “__main__.py” file isn’t found therein.
  ... SO ANYWAY. tl;dr there is now a “clu/typespace/__main__.py” file
      that contains the “inline” tests that were formerly inlined in
      the “clu/typespace/__init__.py”, and the latter does a wacky
      little import do-si-do in its “if __name__ == "__main__"” bit to
      pull in and run those tests. Which, notably, aren’t “inline” any
      longer. What to call them, “out of line”? “offline”? “ingrown”?
      I am open to suggestions.
  ... And so yeah while the current setup works, as far it goes with
      both running nox and ⌘-R’ing the “__init__.py” file in TextMate
      it would not at all be too forward to call this arrangement a
      ridiculous Rube Goldberg nonsensical misdirection. So maybe I
      will change this shit at some point, or maybe I will leave it
      be. We shall see doggie, indeed yes.

  † – that’s an oversimplification – while “path_to_dotpath(…)” is at
      the heart of this transformation, it actually involves a bunch
      of moving parts; those who are curious should have a look at
      these parts of CLU for the deets:

          * “clu.fs.filesystem.Directory.importables(…)”, a method
  	  which itself relies on:
  	* the “suffix_searcher(…)” and “re_excluder(…)” functions,
  	  found in “clu.fs.misc”;
  	* “clu.exporting.path_to_dotpath(…)”, as mentioned – this
  	  function is used sparingly, but everywhere it is used is
  	  like some super-crucial shit;
  	* everything in “clu.all”: “import_all_modules(…)”, its
  	  sister function “import_clu_modules()”, and the function
  	  whose heuristics sniff out inline tests – appropriately
  	  named “inline_tests(…)”
  	* the nox configuration file, “noxfile.py”, which you’ll
  	  find in the project root, q.v. https://git.io/JvSpx sub.

* Paramatrized a bunch of handy functions ... including: *) ‘compare_module_lookups_for_all_things(…)’ in     	       	  “clu.repl.modules”, 	       *) ‘prepare_types_ns(…)’ and ‘modulize(…)’ in 	       	  “clu.typespace” ... did a thorough overhaul of the aforementiomed “modulize(…)”,     which doing so fixed a few long-standing subtle bugs ... also reduced the use of __file__ within “prepare_types_ns(…)”     and the module-level code that calls it ... added inline tests to “clu.typespace”, verifying “modulize(…)”     and “prepare_types_ns(…)”, like to the hilt ... minor tweaks and updates made to “clu.repl.modules.ModuleMap” [Alexander Böhn]

* Conditionally suffix the “HOSTNAME” const string. [Alexander Böhn]

* Hoisted all of the “types” namespace init-code out of module level ... to wit: that involved taking a bunch of imperative directives     out of the “clu.typespace” modules’ ‘__init__.py’ file and then     sticking them back in there wrapped in a function that gets     called once, at module level, to assign its return value to the     “types” namespace. ... this lets the imports, some of which are quite fragile with     circularity concerns, get thrown into the function’s execution     block, and thus isolated ... nevertheless there were a lot of tweaks that had to be made     following this change, as a lot of my code did the sloppy and     expedient thing of importing a thing or two, here and there,     from “clu.typespace” instead of wherever the fuck the thing     came from in the first place… that is one thing about CLU and     all of its module exporters – how you can’t have a some thing     “Thing” and export it from two places, e.g. “clu.things.Thing”     *or* “clu.dst.thingamabobs.abc.Thing” is okay but not *both*. ... see yeah if you *were* to export “Thing” from both places,     calls like `moduleof(Thing)` and its ilk would end up being     nondeterministic. ... okay so like a photon passing a black hole, this commit note     has veered off on quite a serious fucking tangent. But I do     see now that my module look-up stuff (as seen when one executes     `python -m clu`) should find any such duplicates – even when     implicit, like if “clu.things.Thing” is only exported the once     but is imported from elsewhere in some other spot – and flag     the fuck out of them in the reddest of ANSI red text ... so are we cowabunga on this? yes, we’re cowabunga. [Alexander Böhn]

* Hoisted all of the “types” namespace init-code out of module level ... to wit: that involved taking a bunch of imperative directives     out of the “clu.typespace” modules’ ‘__init__.py’ file and then     sticking them back in there wrapped in a function that gets     called once, at module level, to assign its return value to the     “types” namespace. ... this lets the imports, some of which are quite fragile with     circularity concerns, get thrown into the function’s execution     block, and thus isolated ... nevertheless there were a lot of tweaks that had to be made     following this change, as a lot of my code did the sloppy and     expedient thing of importing a thing or two, here and there,     from “clu.typespace” instead of wherever the fuck the thing     came from in the first place… that is one thing about CLU and     all of its module exporters – how you can’t have a some thing     “Thing” and export it from two places, e.g. “clu.things.Thing”     *or* “clu.dst.thingamabobs.abc.Thing” is okay but not *both*. ... see yeah if you *were* to export “Thing” from both places,     calls like `moduleof(Thing)` and its ilk would end up being     nondeterministic. ... okay so like a photon passing a black hole, this commit note     has veered off on quite a serious fucking tangent. But I do     see now that my module look-up stuff (as seen when one executes     `python -m clu`) should find any such duplicates – even when     implicit, like if “clu.things.Thing” is only exported the once     but is imported from elsewhere in some other spot – and flag     the fuck out of them in the reddest of ANSI red text ... so are we cowabunga on this? yes, we’re cowabunga. [Alexander Böhn]

* Trimmed dead code and juggled a few imports. [Alexander Böhn]

* Rearranged and annotated the module-export-list prettyprinter ... aka “python -m clu” ... this also involved some refinements to the const-lister,     the predicate string-sorters, the module-mapper, and a bunch     of consts that were, like, way past a healthy retirement age ... lots of programmer notes, plus gratuitous whitespace-nudgery,     import-re-namification, vertical code-text liney-up-manship,     and all kinds of general clinical evidence and indications     of what Nichael Bluth calls “The O.C. disorder” ... in a nutshell. Yes! [Alexander Böhn]

* Gratuitous whitespace. [Alexander Böhn]

* Whitespace and thing-names. [Alexander Böhn]

* Bump version: 0.6.6 → 0.6.7. [Alexander Böhn]

* Paths in “consts” are now instances of “pathlib.Path” ... instead of interned strings ... it took surprisingly little effort – almost none, actually – to     support this change throughout the rest of CLU… I am kind of     waiting for the other-shoe untested-codepath giant error-message     supernova to occur right in my face, as a result of this; let     that be known, and but so, I go forth! [Alexander Böhn]

* The const-module ANSI display now uses “clu.repl.modules.ModuleMap” ... and myrdiad other formatting strategem. [Alexander Böhn]

* Very minor tweak to the “clu.exporting.ExporterBase” repr logic. [Alexander Böhn]

* Only import “pickle” in “clu.naming” when necessary. [Alexander Böhn]

* Expanded the in/equality ops in “clu.config.abc.FlatOrderedSet” [Alexander Böhn]

* Storing and preserving predicates in “clu.config.abc.FlatOrderedSet” [Alexander Böhn]

* More sundry and assorted repr-scaping. [Alexander Böhn]

* Fancy indexing now works for “clu.config.abc.FlatOrderedSet” ... also there’s a “clu.config.abc”-specific unit-test suite, now. [Alexander Böhn]

* Un-redundified the “clu.config.abc.FlatOrderedSet” repr output. [Alexander Böhn]

* Updates to “clu.abstract.ReprWrapper”, “clu.dicts.ChainMap” etc etc ... “clu.abstract.ReprWrapper” correctly uses stuff from “clu.repr”     which up until now it had been duplicating some logic here and     there ... “clu.config.abc.FlatOrderedSet” and “clu.dicts.ChainMap” both     now implement an “is_a(…)” class method, for doing internal-use     instance checking properly in subclasses and structurally-alike     similar types ... other misc. simplification and tweaks to “clu.dicts.ChainMap” ... programmer notes added to “clu.dicts.ChainRepr” ... fix for a bug when repr-izing a “clu.exporting.ExporterBase”     subclass instance created without a “path” attribute (which is     rarely used but in fact a legal use of the things) ... some minor updates to the “clu.dicts” testsuite. [Alexander Böhn]

* You say tomato, I say to-MAAAAH-to, like real snooty. [Alexander Böhn]

* Subtle tweak in the “clu.repl.ansi.DocFormat” renderer ... namely, passing a formatter internally as such, and not as a     “color” – preventing an additional parsing step ... also in this commit: the use of an abstract method to prevent     the exporter registry from accidentally being instanced. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* All instances of “clu.abstract.Format” are callable ... the default implementation forwards the callable call to the     instances’ “render(…)” method ... also, “clu.predicates.slots_for(…)” now uses an LRU cache. [Alexander Böhn]

* Updating the (irritatingly manual) “clu.abstract” list of exports. [Alexander Böhn]

* Exporting the “clu.repl.ansi” keyword-arg helper function. [Alexander Böhn]

* Abstracted the common textwrap.TextWrapper args in “clu.repl.ansi” [Alexander Böhn]

* Removing some non-ANSI-specific testing code. [Alexander Böhn]

* Test data fixture-ization. [Alexander Böhn]

* Got rid of superfluous one-off const import in “clu.abstract” [Alexander Böhn]

* Start of “clu.repl.ansi” reorganization efforts • Moved CacheDescriptor and a related lambda to “clu.abstract” • Made “clu.repl.ansi.DocFormat” a variable-arity callable to match   the existing “clu.repl.ansi.ansidoc(…)” signature and behavior • Exporting the “clu.repl.ansi.ANSIFormatBase” namedtuple type. [Alexander Böhn]

* Some docstring and programmer-notes tweakage in “clu.fs.abc” [Alexander Böhn]

* Trying out a new “explain(…)” function for runtile REPL introspection. [Alexander Böhn]

* NOW I HAVE TWO PROBLEMS. [Alexander Böhn]

* Parity between the old “ansidoc(…)” function and everything new ... q.v. the inline tests for pudding-style proof. [Alexander Böhn]

* Some exports and miscellaneous codescaping. [Alexander Böhn]

* Redid all the ANSI and terminal formatting stuff with OOP ... so don’t NO ONE accuse me of not being object-oriented enough     for anything, ever. [Alexander Böhn]

* Fixed columnar justification in CLU module display. [Alexander Böhn]

* Tons of revisions to “clu.repl.columnize” ... including! • things in “clu.abstract” supporting new formatters     	       … with unit tests!     	       • streamlined and non-nonsensical width-estimation 	       • elimination of some inappropriate lambdas 	       • new, improved, generally sexier docstrings 	       • the more tangled-up and illegible bits of internal 	         code have been untangled and, at least, legiblized     	       • a general revision of all of the keyword-argument- 	         related crapola that had been previously occupying 		 “clu.repl.columnize” up until now, including total 		 normalization of all of the naming 	       • a better inline “demo(…)” function that will, if 	         given a chance, respect the width of the terminal ... on the whole, it’s something I am relatively unashamed to have     as a part of CLU right now, rather than a hastily-retrofitted     copypasta hackjob, ported from something penned originally by     an obvious Python-hating Rubyist (clearly evidenced by their     anti-significant-whitespace fantods manifested as a plague of     “pass” statements demarking each block-dedent, excuse me?…)     and adapted without style, elegance, or forward-thinkingness     by me when I did not feel like writing such a function, dogg. [Alexander Böhn]

* Moved “modeflags(…)” to “clu.fs.misc” ... plus of course the requisite adjustments to tests and etcetera. [Alexander Böhn]

* Abstract-base-class-ified “clu.fs.TemporaryName” and “clu.fs.Directory” [Alexander Böhn]

* “clu.fs.filesystem.rm_rf(…)” raises if you feed it a mountpoint. [Alexander Böhn]

* Pervasive, dogged, ineffable use of explicit exception chaining. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* An LRU cache seriously speeds up repeat calls in “clu.repl.modules” ... the inline-test running time went from a couple of seconds down     to like 1/100th of that – I try not to gratuitously cache or     otherwise memoize functions but sometimes it’s just idiotic not     to do so, doggie ... this commit also has the remains of an attempt to twaddle with     what turned out to be one of the overly-sensitive codepaths in     “clu.importing” which this, the twaddling, did not work in the     end. The embellishment of a few lines of inline-test code in     “clu.application” was from sorting out the non-working-osity     of same. Yep. [Alexander Böhn]

* Removed the “appdirs” dev requirement. [Alexander Böhn]

* Made “Pillow” an explicit dev requirement. [Alexander Böhn]

* Made “python-dateutil” an explicit dev requirement. [Alexander Böhn]

* Moved the Figlet banners into “clu.constants.data” which makes more sense. [Alexander Böhn]

* Another mere period in but one more docstring. [Alexander Böhn]

* A mere period in but a docstring. [Alexander Böhn]

* Only retarget bound methods for renaming just the once. [Alexander Böhn]

* Another day, another Unicode codepoint with which to amuse myself. [Alexander Böhn]

* Removed confusing “+” signs from formatting regexes. [Alexander Böhn]

* OCD-ish update/tweak to “clu.predicates.wrap_value(…).__doc__” [Alexander Böhn]

* Bump version: 0.6.5 → 0.6.6. [Alexander Böhn]

* The “humanize” package no longer exposes “timedelta” [Alexander Böhn]

* Dead code harvest pt. II. [Alexander Böhn]

* Dead code harvest. [Alexander Böhn]

* Bump version: 0.6.4 → 0.6.5. [Alexander Böhn]

* Links in the “boilerplate.py” README.md. [Alexander Böhn]

  For some reason, hithertofore undefined

* Include README.md explaining “boilerplate.py” code. [Alexander Böhn]

* Significant refactor of the “ExporterBase.export(…)” rename logic ... this is the first significant update to this logic – which oh     by the way is kinda one of CLU’s most-executed and crucial-est     bits of logic by like a long shot – in I have no fucking idea     how long or how many commits it’s been more specifically than     just “A FUCKING LOT” ... The main piece is that function-renaming – which used to only     apply to lambdas and phi-type partials – has been expanded such     that we try it on basically *everything*. If you are callable,     and you have a “__name__” attribute, we will absolutely attempt     to rechristen you in the fullest (as in writing __name__ and     editing __qualname__, “non-destructively” assigning a value for     __lambda_name__ that is backwards-compatible with every single     random snippet that nooks at __lambda_name__, and selectively     resetting __module__ for phi-type instances. ... Note how that last. [Alexander Böhn]

* Trimmed dead code and refined the newer geegaws a bit ... updated the “star-import” module list in “clu.scripts.repl” ... moved some stuff here, some there – those chairs on the upper     deck of the Titanic aren’t getting any *more* polished all by     themselves after all. [Alexander Böhn]

* Refactored the re-usable stuff in the module-exports report script ... said re-usables are in the new “clu.repl.modules”… er… module;     consisting mainly of the one gratuitously long-named function,     “compare_module_lookups_for_all_things(…)” – which is also, I     should mention, now accepting varargs – some named tuples,     a handful of utility lambdas and other such thingees. ... there is also a “clu.repl.modules.ModuleMap” class which wraps     a module instance and offers its (non-dunder-named) innards     up via the “collections.abc.Mapping” interface. I wrote this     class and then promptly immediately forgot why I had first     endeavored to do so. And so yeah now it’s there. OK. ... moved a few common code tidbits into “clu.repl.ansi” from the     module-exports report script and the constant-value reporter. ... as a result those respective “__main__.py” script files are     like 90% slimmer, generally not redundant (as opposed to before,     when they were redundant) and not as tempting to describe as     a pile of code-spaghettified hot garbage as they have been in     the past. [Alexander Böhn]

* Assuaging the GitHub vulnerobotic japery. [Alexander Böhn]

* All types of lovely and fantastic miscellany ... “clu.constants.polyfills” no longer depends on anything from     “clu.constants.consts” (in fact the latter will now attempt a     guarded import from the former, because we can) ... The new boolean constant “clu.constants.consts.NUMPY” is True     if you can import numpy from within the Python environment in     which CLU is operating ... “clu.mathematics” doesn’t export anything when it has to mock     the numpy module (which it will do if that aforementioned const     value is False) ... New “noxfile.py” logic attempts to install numpy when it looks     like it’ll need to test code that conditionally leverages it ... Running Nox using Make rules will generate a JSON report of how     everything worked out, by default ... “clu.repl.ansi.ANSIFormat” now employs a pretty conservative     instance-caching scheme – hard references, keyed on hashed enum     values, queries follow the same exhaustive normalization we’ve     been using all along before calling up to “super().__new__(…)”     – that seems to work all nice and transparent like ... Other assorted frippery, devil-may-care flim-flam, and sundry     jocund elements of imaginative fancy. [Alexander Böhn]

* The “Format” class is now “clu.abstract.Format” ... right now it just has the one “render(…)” abstract method, but     the journey of 1,000 premature optimizations starts with but a     single such method, no? [Alexander Böhn]

* Tweak to “clu.naming.duplicate(…)” [Alexander Böhn]

* Tweak to “clu.exporting.ExporterBase.inner_repr()” ... trims repr strings down by shortening “path” using “basepath”     and “os.path.relpath(…)” [Alexander Böhn]

* Using interim variable instead of global lookup. [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* Killed unnecessary shebang. [Alexander Böhn]

* Many ANSI scripting updates and pile-on enhancements. [Alexander Böhn]

* Optimization of common codepath in “Directory.subdirectory(…)” [Alexander Böhn]

* Replaced “uniquify(…)” with set logic in “Directory.importables(…)” [Alexander Böhn]

* HAAAACK. [Alexander Böhn]

* Repackaging the standard streams into a namespace. [Alexander Böhn]

* Using the new “clu.stdio.TermSize” structure in “clu.testing.pytest” [Alexander Böhn]

* Started a new top-level module “clu.stdio” [Alexander Böhn]

* Throwing in a terminal-based coverage report Makefile rule. [Alexander Böhn]

* Fleshing out the coverage configuration stuff ... added a .coveragerc config file ... amended .gitignore with new incoming coverage report outputs ... fixed a long-standing bug that was keeping the output from     “clu.repl.ansi.print_ansi_centered(…)” from using the proper     terminal-width value when called during a pytest run – this     had been evident when the delete-temps @exithandle printed its     output – by revising the way we get the terminal width in a     few places throuought the codebase; q.v.:     * http://bit.ly/py-term-size sub. and     * https://stackoverflow.com/a/3010495/298171 sub. ... tweaked the nox session definition for code-coverage runs – it     now piggybacks on the pytest setup ... and so on and so forth. [Alexander Böhn]

* Base requirements aren’t necessary to run “codecov” [Alexander Böhn]

* Setting things up with codecov.io. [Alexander Böhn]

* Propagate errors from “star_export(…)” and “module_export(…)” ... instead of silently swallowing them on REPL startup. [Alexander Böhn]

* Updated the development requirements. [Alexander Böhn]

* Supress load errors from instakit when CLU versions are mismatched. [Alexander Böhn]

* Makefile minutiae. [Alexander Böhn]

* Utilizing “enum._is_sunder(…)” (aka “ismifflin(…)”) in clu.predicates ... also added a new predicate “ispublic(…)” – which is true for a     string that is not “ispyname(…)” and not “ismifflin(…)” – which     in “clu.scripts.repl.star_export(…)” keeps inadvertant leakage     of module internals into the global namespace from happening. [Alexander Böhn]

* Made “clu.typespace.namespace.NamespaceRepr” compatible with stdlib ... by which I mean, the stdlib type “types.SimpleNamespace” works     the same as our own “SimpleNamespace” type w/r/t the relevant     repr functions and methods. [Alexander Böhn]

* Ensure class-modules aren’t created in circumstances when unwarranted. [Alexander Böhn]

* Fix the import of “clu.typespace.types” in “clu.scripts.repl” [Alexander Böhn]

* Automatic width adjust in module-export display script. [Alexander Böhn]

* Festooned the license text with all the latest Unicodery and doodadishness. [Alexander Böhn]

* Tied up a few doc-stringy loose ends. [Alexander Böhn]

* Excised all traces of “TemporaryFileWrapper” from “clu.fs.filesystem” ... as it seems to be getting on splendidly over in “clu.fs.abc” [Alexander Böhn]

* Relocated our “TemporaryFileWrapper” to the “clu.fs.abc” module. [Alexander Böhn]

* Removed TypeLocker remnants from “clu.fs.filesystem” [Alexander Böhn]

* Starting a “clu.fs.abc” module, for filesystem-centric base classes ... the TypeLocker metaclass has already been relocated therein. [Alexander Böhn]

* Trimmed dead bpython-determination method code. [Alexander Böhn]

* Neatened up the module star-exporting process in “repl.py” ... like e.g., don’t copy module dunder-attributes even when they’ve     been explicitly exported from a module… stuff like that. [Alexander Böhn]

* Programmer notes throughout “repl.py” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Polished “repl.py” enough to replace the CLU per-REPL scripts ... which the latter of which, the per-REPL scripts, have been     depreciated and put in a “legacy” subdirectory in “clu.scripts”     where I might look at them in the future from time to time to     remember the follies of my youth. [Alexander Böhn]

* Streamlined type-repr logic for “clu.importing.MetaRegistry” types. [Alexander Böhn]

* Relaxed type-checking in “clu.version” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Bump version: 0.6.3 → 0.6.4. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Storing PyPI classifiers in an external file. [Alexander Böhn]

* Some resuffling of consts. [Alexander Böhn]

* Revised requirements and “repl-bpython.py” script. [Alexander Böhn]

* Winnowing dev requirements, pt. II. [Alexander Böhn]

* Winnowing dev requirements. [Alexander Böhn]

* The “clu.abstract.Prefix” class is now “clu.abstract.BasePath” ... and all that goes with that. [Alexander Böhn]

* Compartmentalize imports. [Alexander Böhn]

* Revise programmer notes for “clu.application.AppBase.__init_subclass_(…)” [Alexander Böhn]

* Make DEFAULT_APPSPACE act like a real default. [Alexander Böhn]

* Consistency in naming. [Alexander Böhn]

* Whooooops. [Alexander Böhn]

* Idempotency for the “AppBase.initialize_*()” functions. [Alexander Böhn]

* More foundational work on “clu.application” [Alexander Böhn]

* Unceremoniously throwing in some .ipynb scratch. [Alexander Böhn]

* Exporting the few code-fronds to be found in “clu.application” [Alexander Böhn]

* Cleaned up “application.AppBase” a bit; added another inline test. [Alexander Böhn]

* Planting a seedling into which “clu.application” can maybe grow. [Alexander Böhn]

* Tweaked CLU import in noxfile.py. [Alexander Böhn]

* Shortened inline-test-gathering function name. [Alexander Böhn]

* Allow arbitrary test-function names in “clu.all.clu_inline_tests(…)” [Alexander Böhn]

* The module docstring in “clu.repl.banners” was waaay freakin old. [Alexander Böhn]

  ... a nearly-untouched artifact of my original “replenv.py” script†
      in fact – which itself presaged “replutilities.py”‡, which was
      the primogenitor for CLU’s exporter function, its predicate and
      typology libraries, and a bunch of other stuff that no one on
      Earth but I would ever want to recall. Yes!

  † http://bit.ly/replenv-py
  ‡ http://bit.ly/replutilities-py

* Passing an output-stream “file” argument along in “clu.repl.banners” ... defaults to the results of the module-level “attr(…)” call in     “clu.repl.ansi” [Alexander Böhn]

* Only calculate the fractional “SEPARATOR_WIDTH” value once. [Alexander Böhn]

* Overhauled a bunch of “clu.repl.ansi” and “clu.repl.banners” ... honed the “clu.repl.ansi.paragraphize(…)” function used in the     “ansidoc(…)” utility – it now recognizes bulleted paragraphs     and inline code samples (provided the latter are prefixed with     the typical “>>> ” or similar) ... the pattern-matching for the aforementioned formatting tricks,     it should be mentioned, use “clu.fs.misc.re_matcher(…)” which     has nothing that intrinsically tethers it to file-path employ ... edited a bunch of real-world docstrings in use throughout the     “clu.exporting” and “clu.importing” modules to leverage these     capabilities ... spruced up the code in “clu.repl.banners” to be less janky and     overall more befitting of the year 2020 ... added some convenience lambdas and module-level constants in     “clu.repl.ansi” that should allow the basic ansi-print stuff     to work in various REPLs (i.e. not just bpython) [Alexander Böhn]

* Made “filesystem.Directory” inherit from “clu.abstract.ReprWrapper” [Alexander Böhn]

* Correction within programmer note. [Alexander Böhn]

* Inspect likely names first. [Alexander Böhn]

* Pre-emptively adding “co_freevars” to the __code__ inspect list. [Alexander Böhn]

* Apparently you have to check “co_cellvars” sometimes too. [Alexander Böhn]

* Bump version: 0.6.2 → 0.6.3. [Alexander Böhn]

* Bumped testing numpy minimum version. [Alexander Böhn]

* Removed redundant PyYAML requirement. [Alexander Böhn]

* Touched up “requirements/dev.txt” as well. [Alexander Böhn]

* Bumped up a bunch of minimum versions for the install requirements. [Alexander Böhn]

* Removing assorted unnecessary stuff from the keymap implementations. [Alexander Böhn]

* The big s/PROJECT_NAME/APPNAME/g changeover. [Alexander Böhn]

* Formally added “consts.APPNAME” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Filled in two irritatingly missing “clu.repr” tests. [Alexander Böhn]

* Short-circuit return for file-list calls on nonexistant directories. [Alexander Böhn]

* Using the “consts” fixture in leu of manual import in “test_repr.py” [Alexander Böhn]

* Removed gratuitous “tuple()” calls in “test_keyvalue.py” [Alexander Böhn]

* Converted the “Directory.ls(…)” function to use a “re_matcher()” ... whereas before a one-off regex was in play. [Alexander Böhn]

* Explanatory comment note. [Alexander Böhn]

* Un-hard-coded the suffix list in the “suffix_searcher(…)” test ... by adding a “clu.fs.filesystem.Directory.suffixes(…)” method! [Alexander Böhn]

* Using “Directory.suffix_histogram(…)” in “suffix_searcher(…)” test. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Cleaned up and legible-ized “fs.filesystem.Directory.__len__()” [Alexander Böhn]

* Cleaned up and legible-ized the “fs.filesystem.Directory” iterators ... using “with” clauses and proper flow control. [Alexander Böhn]

* Updated “clu.version” tests ... got rid of one-off brittle module-level code ... added tests for “clu.version.git_version” functions ... ensured tests respectfully utilize the “cluversion” fixture. [Alexander Böhn]

* Importing “countfiles(…)” globally in “test_fs_filesystem.py” ... as it was used in, like, every other test function. [Alexander Böhn]

* Testing the entirety of a renamed “__qualname__” ... in “test_renaming.py” [Alexander Böhn]

* A (somewhat overdue) unit test for “Directory.suffix_histogram(…)” ... our 200th unit test! [Alexander Böhn]

* Simplified “clu.testing.utils.InlineTester.add_function(…)” [Alexander Böhn]

* Updated the requirements ... specifically dealing with the “pout” package. [Alexander Böhn]

* Adapting another gem of a snippet I found in PyPy ... q.v http://bit.ly/lazy-borg-modulespace – ... I am not immediately sure how I am going to use this one,     but getting rid of that hacky little “sys.modules” tuplizer     lambda would be nice. [Alexander Böhn]

* Trimmed dead code and reconciled a redundant Greek import. [Alexander Böhn]

* Bringing all treatments of “__qualname__” values up to snuff ... as in, no longer do we just alias it to “__name__” when we’re     renaming or resetting things – we specifically seek to preserve     the parts of “__qualname__” dotpath-ish strings with namespace-     specific information, while altering only the sections relevant     to whatever it is we are doing (i.e. renaming, or whatever). ... likewise, in functions like “determine_name(…)”, in the event     (however unlikely) that the code branches to the consideration     of a “__qualname__” value, we deterministically cleave off only     the bit we care about using “str.rpartition(…)” and slicing ... there are one or two extremely corner-iffic cases where some     still-existing “__qualname__” negligence could possibly, under     thoroughly bizarre and freakish circumstances, transpire – but     I have marked them shits as TODO and will assuredly find time     to procrastinate from whatever I should actually be doing in     the near-to-middling future and address these, toot sweet. ... in conclusion: thank you for using CLU, doggie, yeah!~ [Alexander Böhn]

* Swapped the return values from “clu.naming.qualified_name_tuple(…)” ... thus matching the order of those returned by “dotpath_split(…)”     in the same module. [Alexander Böhn]

* Removed empty inline tests from “clu.testing.utils” [Alexander Böhn]

* Got rid of the async coroutine inline-test code in “clu.dispatch” ... as much as I loved it. [Alexander Böhn]

* Nixed unnecessary shebang. [Alexander Böhn]

* Fixed file perms. [Alexander Böhn]

* No longer using “collections.OrderedDict” in “clu.version” [Alexander Böhn]

* Enhanced cache-stats diagnostics. [Alexander Böhn]

* Trying to fix an off-by-one error in one of the inline diagnostics. [Alexander Böhn]

* Using EXPORTER_NAME throughout “clu.importing” [Alexander Böhn]

* Fixed file perms. [Alexander Böhn]

* CLU-module exporter detection is now less hardcoded and janky. [Alexander Böhn]

* Made a bunch of constant usage more explicitly obvious. [Alexander Böhn]

* Widened the criteria used by Nox to select inline-test modules ... this means inspecting multiple lists of names on a putative     test-function’s “__code__” object property. [Alexander Böhn]

* Ensure “suffix” function isn’t clobbered in “clu.naming” module namespace. [Alexander Böhn]

* Moved the “repr-delimiter” character constant to “clu.constants.consts” [Alexander Böhn]

* Docstring minutiae. [Alexander Böhn]

* Slowly modernizing the “clu.fs.appdirectories” inline tests. [Alexander Böhn]

* Another “clu.config.proxy” nitpick bugfix. [Alexander Böhn]

* Fixed a few random bugs in “clu.config.proxy” ... argument-passing and naming consistency issues, mostly. [Alexander Böhn]

* Disabling unused code in some paramatrized “appdirectories” tests. [Alexander Böhn]

* Myriad updates to the enums used by “clu.fs.appdirectories” [Alexander Böhn]

* Un-redundified and parametrized the “clu.fs.appdirectories” testsuite ... trimmed a lot of dead and/or repeated code ... fine-tuned inline fixtures and parameters ... added a “cluversion” fixture to the pytest plugin that provides an     instance of “clu.version.VersionInfo” for the CLU app’s current     “semver” – semantic version – number ... added tests for “clu.fs.appdirectories.clu_appdirs(…)” that are     parametrized on the “System” enum value ... reformatted the fixture/argument test function signatures to     match my crippling OCD ... added a new Make rule to show the pytest configuration details     (via `pytest --setup-plan --trace-config`) syntax-highlighted     in ANSI color (via the ineffable Pygments) [Alexander Böhn]

* Updated the “clu.fs.appdirectories” tests to use fixtures ... rather than constant values stored in the test class. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Tweaking “norecursedirs” pytest INI-option. [Alexander Böhn]

* Explicitly setting some environment variables in “noxfile.py” [Alexander Böhn]

* Requiring numpy during tox runs. [Alexander Böhn]

* Even better docstrings and hook function names. [Alexander Böhn]

* Documented the “delete_temps” INI option CLU’s pytest plugin adds. [Alexander Böhn]

* Revised a bunch of variable names in “pytest_addoption(…)” [Alexander Böhn]

* Forgot to F that string. [Alexander Böhn]

* Deduplication in the pytest plugin configuration setup stuff. [Alexander Böhn]

* The “delete-temps” CLI option has a correponding INI file value. [Alexander Böhn]

* Decorated the custom hook in “conftest.py” [Alexander Böhn]

* Let’s be type-safe. [Alexander Böhn]

* Setting the CLU-specific pytest options in “conftest.py” ... using “Config.addinivalue_line(…)” in the “pytest_configure”     hook function. [Alexander Böhn]

* Bump version: 0.6.1 → 0.6.2. [Alexander Böhn]

* Moved pytest-specific settings to a “pytest.ini” file. [Alexander Böhn]

* Stopping on first Nox error. [Alexander Böhn]

* Using nox in “test-all” Makefile rule. [Alexander Böhn]

* Bump version: 0.6.0 → 0.6.1. [Alexander Böhn]

* Accelerated “clu.fs.filesystem.Directory.suffix_histogram(…)” ... by using “collections.Counter.update(…)” in the “os.walk(…)”     generator loop – instead of manually incrementing per-suffix     counter values. [Alexander Böhn]

* Moved “clu_inline_tests()” from “noxfile.py” to the “clu.all” module ... as it was already generic w/r/t Nox and is potentially useful. [Alexander Böhn]

* The noxfile is now parametrized to within an inch of its life ... also numpy is no longer a hard requirement (!) ... aaaand nox runs as speedily as I can imagine is possible. [Alexander Böhn]

* Lots of tox/nox/requirements minutiae. [Alexander Böhn]

* Further broke down and parametrized the Nox setup. [Alexander Böhn]

* Made the manifest-checking a separate Nox task. [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* Catching “ImportError” in “clu.testing.hooks” ... otherwise pytest would be a shadow hard-requirement for running     all of CLU. [Alexander Böhn]

* Made “clu.typology.iterlen(…)” attempt to delegate to “len(¬)” first. [Alexander Böhn]

* Updated “scripts/repl-bpython.py” ... to match structural changes to the “clu.compilation” module. [Alexander Böhn]

* This is really kind of fucking stupid. [Alexander Böhn]

* Import order matters. [Alexander Böhn]

* Removed dead (but not forgotten) code. [Alexander Böhn]

* OK so there was a “string.center(…)” method THIS WHOLE TIME!!! Wow. [Alexander Böhn]

* Make my file. [Alexander Böhn]

* Slight rearrangement of inline-test autodiscovery. [Alexander Böhn]

* Less ponderous KeyError message from “clu.predicates.try_items(…)” [Alexander Böhn]

* Bump version: 0.5.15 → 0.6.0. [Alexander Böhn]

* Ah yes, what it once was. [Alexander Böhn]

* Fixed phantom-environment-variable bug in “clu.dicts.ChainMap” [Alexander Böhn]

* Made the inline-test Nox run command slightly more legible. [Alexander Böhn]

* Docstring minutiae. [Alexander Böhn]

* Notes and minutiae in inline-test Nox session task. [Alexander Böhn]

* Running all inline test suites automatically via Nox ... !!!!!!!!!!!!!!!!!!! [Alexander Böhn]

* Setting up Nox. [Alexander Böhn]

* The inline-tester is more popular than the hacked “pout” module. [Alexander Böhn]

* The exit handle set by pytest’s finalizer hook now returns a boolean ... as it should have, per the “clu.dispatch” modules’ expectations,     apparently… ooof. [Alexander Böhn]

* Edited the «TODO» note on the “which(…)”/“back_tick(…)” test. [Alexander Böhn]

* Made the “which(…)”/“back_tick(…)” binary list plausibly portable. [Alexander Böhn]

* Abstracted all the “flags” business in “clu.fs.filesystem” [Alexander Böhn]

* Disambiguated the logic in “clu.fs.filesystem.rm_rf(…)” [Alexander Böhn]

* We really don’t support Python 3.5 or 3.6. [Alexander Böhn]

* Bump version: 0.5.14 → 0.5.15. [Alexander Böhn]

* Don’t declare known dunder names as slots under PyPy. [Alexander Böhn]

* Bump version: 0.5.13 → 0.5.14. [Alexander Böhn]

* Sorted out directory-excludes for documentation. [Alexander Böhn]

* Bump version: 0.5.12 → 0.5.13. [Alexander Böhn]

* Bump version: 0.5.11 → 0.5.12. [Alexander Böhn]

* Requiring a minimal “pout” [Alexander Böhn]

* Bump version: 0.5.10 → 0.5.11. [Alexander Böhn]

* Updating, slash juggling, requirements. [Alexander Böhn]

* Bump version: 0.5.9 → 0.5.10. [Alexander Böhn]

* Simplifying “super(…)” calls in “clu.config” [Alexander Böhn]

* Removed unused “iterchain(…)” from “clu.repr” [Alexander Böhn]

* Minor tweaks to “clu.dicts.ChainMap.from{keys,items}(…)” [Alexander Böhn]

* Caching the return from “clu.predicates.newtype(…)” ... this isn’t perfect, as it pretty much necessitates that any     attributes – as in, any values for the class-body namespace –     be passed as “clu.typespace.SimpleNamespace” dictionaries, or     something else hashable (that happens to be, like, the only     convenient hashable “frozen dictionary” type lying around my     heirarchy RN)… I don’t hate this, as using a “Namespace”-y type     kind of works for this purpose, despite the supurfluousness…     in any case we’ll see. ... like, I may move “newtype(…)” out of “clu.predicates” entirely     as it is outgrowing its original one-liner convenience lambda,     for seriously. [Alexander Böhn]

* “clu.predicates.newtype(…)” uses a bespoke default base “ObjectType” ... this distinguishes types that are created with this function ... “clu.predicates.ObjectType” inherits from ‘object’ and adds     nothing except one more bump in its inheritance-chain road; ... again, a few minimal additions to the predicates testsuite were     necessary – but thankfully not a biggie. [Alexander Böhn]

* Removed intermediate package imports from “clu.compilation” [Alexander Böhn]

* Completely and punctilliously rewrote “clu.predicates.newtype(…)” ... to be, like, a real thing ... updated the relevant test (which didn’t need much reworking) [Alexander Böhn]

* Importing inline test fixtures in “clu.config.proxy” [Alexander Böhn]

* Killed some dead code. [Alexander Böhn]

* Split the environment-variable keymaps off into “clu.config.env” [Alexander Böhn]

* Whooooops. [Alexander Böhn]

* «python -funroll-loops» [Alexander Böhn]

* Lotsa generator use throughout “clu.shelving.redat.RedisConf” [Alexander Böhn]

* Further simplified inline-test function dispatch ... got rid of “newline” keyword argument. [Alexander Böhn]

* Toggle test function verbosity based on output mode. [Alexander Böhn]

* The beginnings of JSON reporting output for the inline tester. [Alexander Böhn]

* Bump version: 0.5.8 → 0.5.9. [Alexander Böhn]

* Maintaining legacy make targets for the consts and modules scripts. [Alexander Böhn]

* Removing gratuitous exec-perm bits. [Alexander Böhn]

* Symlinked the old script locations to their new module-main source. [Alexander Böhn]

* Now the “show-modules.py” script is the clu.__main__ module code ... and OK in that last commit, pretend I typed “show-consts.py”,     OK?? Same diff. ... OK so yeah you can execute the show-modules brouhahah by doing: [Alexander Böhn]

  % python -m clu

  ... and I am not married to having this script action there, and
      might move it; I can sense a giant OCD reorganization-bender
      may be in my immediate future, so we shall see

* Made the “show-modules.py” script the module-main of “clu.constants” ... as in, instead of running it by typing: [Alexander Böhn]

  % PYTHONPATH="." python ./clu/scripts/show-modules.py

  ... you just be like:

      % python -m clu.constants

  ... which we can all agree is sooooo much better-looking, yes?!?

* Excluding documentation from MANIFEST.in. [Alexander Böhn]

* Setting up Sphinx documentation. [Alexander Böhn]

* Removed “chain/iterchain” references from “clu.config.keymap{view}” [Alexander Böhn]

* Removed unused “collections.abc” reference from “clu.config.keymap” [Alexander Böhn]

* Consolidated imports. [Alexander Böhn]

* Removed unused “@abstractmethod” reference from “clu.config.keymap” [Alexander Böhn]

* And just for good measure: s/nsutils/ns/g. [Alexander Böhn]

* The big s/defg/keymap/g has landed. [Alexander Böhn]

* Programmer notes. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Relocated the old “clu.config” env API to “clu.config.base” ... this is, like, a temporary situation – so everything from the     original “NamespacedMutableMapping”-related “clu.config” fiasco     can more or less live in this “base” module – keeping the tests     working, and the few annyoingly dependent other parts of the     system from having a flying shit attack ... and then so right now “clu.config.env” is actually empty, but     *now* we can start to migrate everything to the all-new and     improved “KeyMap”-based shit, which until recently was entirely     confined in “clu.config.defg” but now includes:     * clu.config.abc     * clu.config.defg     * clu.config.env COMING SOON!!     * clu.config.keymapview     * clu.config.nsutils     * clu.config.proxy ... yeah! Fuck yeah my doggie, indeed. [Alexander Böhn]

* Bump version: 0.5.7 → 0.5.8. [Alexander Böhn]

* Continuing the Great DEFG Split-Up… ... successfully moved FrozenKeyMap, KeyMap, NamespaceWalker, and     related base classes to “clu.config.abc” ... global-find-and-replace updated all the references to same ... tossed the NamespacedMutableMapping ABC into “clu.config.base”     for the time being, and global-find-and-replaced its references ... juggled and re-juggled all the relevant imports ... updated the ‘repl-bpython.py’ script ... other related nonsense. [Alexander Böhn]

* Moved the environment-access function API to “clu.config.nsutils” [Alexander Böhn]

* Commencing the Great DEFG Split-Up ... so far the KeyMap view classes and the namespace utility funcs     have been excised from “clu.config.defg” and installed in their     own modules:     * “clu.config.keymapview” and     * “clu.config.nsutils”, respectively ... also the NAMESPACE_SEP and ENVIRON_SEP constants were formally     lodged into “clu.constants.consts” ... much consolidation of imports was done – but everything works,     all unit and inline tests run green with this new layout (!) [Alexander Böhn]

* Ported some inline tests to the main pytest testsuite ... mainly from “clu.dicts” and “clu.typespace.namespace” – in fact     there is a new testsuite just for namespace-related shizzatch ... some updates to “clu.dicts” and “clu.importing” as well:     … specifically, the start of pickling hooks for class-modules     … aaaand an expansion of “clu.dicts.asdict(…)” [Alexander Böhn]

* Total nitpick. [Alexander Böhn]

* Trifiling minutiae. [Alexander Böhn]

* Trying to figure out the safest way to generate this stuff. [Alexander Böhn]

* Simplified the “clu.importing.modules_for_appname(…)” logic. [Alexander Böhn]

* Converting even more tuple-returners to generators. [Alexander Böhn]

* Using “short repr” mode in “clu.repr.strfield(…)” where applicable. [Alexander Böhn]

* Updated several methods in “clu.exporting” *) “clu.exporting.Registry.all_appnames()” is now a generator, *) “clu.exporting.ExporterBase.modulenames()” is now a generator, *) “clu.exporting.ExporterBase.modules()” is now vastly simplified,    having been rewritten as a single-line dictionary comprehension. [Alexander Böhn]

  ... there was one update that had to be made in “show-modules.py”,
      to account for the “modulenames()” generator-ness, also.

* Hedge against exhaustion in “clu.exporting.ExporterBase.modules()” [Alexander Böhn]

* Made “clu.exporting.ExporterBase.modulenames()” into a generator. [Alexander Böhn]

* Made “clu.exporting.itermodule{ids}(…)” into generator functions. [Alexander Böhn]

* Removed pointless “sorted(…)” call in “clu.exporting.itermodule(…)” [Alexander Böhn]

* Made “clu.predicates.uniquify(…)” into a generator ... rather than something that just happens to return a tuple. [Alexander Böhn]

* Made “clu.fs.filesystem.Directory” into a “clu.abstract.Cloneable” [Alexander Böhn]

* Moved STRINGPAIR and WHITESPACE to “clu.constants.consts” ... they were repeated components of custom reprlib subclasses. [Alexander Böhn]

* Couple of legibility-oriented line breaks in “clu.dicts” [Alexander Böhn]

* Inline test confirms custom-repr commutativity for ChainMap types ... like, “clu.dicts.ChainMap” reprs as “collections.ChainMap” does     when using the custom “reprlib” subclass in “clu.dicts” [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* Got rid of redundant inline tests in “clu.dicts” [Alexander Böhn]

* Ignore errors for earlier versions of the “pout” module. [Alexander Böhn]

* What we’re on about. [Alexander Böhn]

* TURN THAT SHIT OFF. [Alexander Böhn]

* Bump version: 0.5.6 → 0.5.7. [Alexander Böhn]

* CHANGES DEEMED TO HAVE BEEN LOGGED. [Alexander Böhn]

* Parity-check ‘twixt “clu.dicts.ChainMap” and “collections.ChainMap” ... surprisingly, without any extracurricular coaxing on my part,     “__eq__(…)” works butter-smooth between both types, as does     constructing a CLU ChainMap from a standard-library instance     (although the opposite path remains unhiked for now, gah) [Alexander Böhn]

* OK this really isn’t bad, for a quick ‘n’ dirty bespoke-repr jalopy ... It needs it some special-casin’ kinda love but hey, it looks     reasonably legible and non-shitty pretty much right out of the     gates. What gates? The gates, I dunno. It was behind some gates     and now those gates are open, dogg, I have no idea actually OK?     OK anyway. [Alexander Böhn]

* Plugged in the faster “clu.dicts.merge*()” functions as warranted. [Alexander Böhn]

* Got rid of all the ineffective method reimplementations. [Alexander Böhn]

* Appears the “try_items(…)” predicate handily beats “item_search(…)” ... THE MORE YOU KNOW™ [Alexander Böhn]

* Tried a different “__len__()” implementation: it’s exactly the same ... speedwise at least. It’s more explicit, but also uglier (if you     were to ask me, which you most certainly did not, but hey –     c’est la guerre, no?) [Alexander Böhn]

* Made the inline testsuite for “clu.dicts” into a real actual thing ... and the verdict is, “clu.dicts.ChainMap.flatten()” is horribly     inefficient but everything else is totally rad doggie. [Alexander Böhn]

* Bump version: 0.5.5 → 0.5.6. [Alexander Böhn]

* Spicing up the bpython REPL with more datastructure samples ... pre-made and ready-to-eat!! [Alexander Böhn]

* Miniscule change in “clu.exporting” allows method docstring mutation ... !!! ... also, there are a bunch of docstring mutations in the namespace     module ... aaaaaand the removal of that wack and horrible hacked-up     “isnamespace(…)” predicate from “clu.predicates” – there is a     real, non-hacky version in “clu.typespace.namespace” from here     on out, ok? OK!! [Alexander Böhn]

* Docstring edits in “clu.importing” [Alexander Böhn]

* Dropped gratuitous “list(…)” from “Directory.importables(…)” innards. [Alexander Böhn]

* Changelog requirements include install requirements. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Fixed SimpleNamespace.__dir__(…)” and “SimpleNamespace.__repr__(…)” ... wbich were apparently broken?… WHOOOOOPS. [Alexander Böhn]

* Clarified the in-use syntax of our intermediate dataclass decorator. [Alexander Böhn]

* ModuleSpec instances are no longer considered packages by default. [Alexander Böhn]

* Fixing the report-format sizing… YET ONCE AGAIN. [Alexander Böhn]

* Gratuitous further simplification. [Alexander Böhn]

* Using the “clu.testing.utils.InlineTester” fixture dictionary ... instead of hardcoding, fuck yeah dogg. [Alexander Böhn]

* Slight performance gain made via pass-through-ing of some methods ... specifically the “keys(…)”, “items(…)” and “values(…)” methods;     this is likely due to those having fallen back to the default     implementations prior to the explicit pass-through, which meant     that “clu.config.defg.Nested” proxies were using the classes     for key/items/values views that did not take advantage of any     of the “NamespaceWalker” machinery. [Alexander Böhn]

* Changed the internal weakref field name from “keymap” to “referent” ... which the former was both weirdly syntactically repetetive and     amiguously confusing; the latter says what it actually is and     isn’t the name of any other things already in use in general. [Alexander Böhn]

* Got rid of reasonable-looking but completely stupid clone() impl ... which would have created a weakref to a temporary, essentially ... UGH. [Alexander Böhn]

* Fixed generated docstrings on returned test functions ... FYI, docstrings with format components are, like, undefined     behavior it looks like…?! [Alexander Böhn]

* Docstrings ‘n’ notes for the proxy-related inline metafunctions. [Alexander Böhn]

* Slightly less class-level clutter. [Alexander Böhn]

* Actually using the class method I just added. [Alexander Böhn]

* Truly a miniscule rearrangement of things. [Alexander Böhn]

* Many more inline tests for “clu.config.proxy” types. [Alexander Böhn]

* Made the “ExporterBase” use its instance registry as a cache ... so, like, “ExporterBase.__new__(…)” returns existing instances     for dotpaths matching the invocation arguments. [Alexander Böhn]

* Minute updates to the bpython REPL script. [Alexander Böhn]

* I can’t believe I forgot to inherit Proxy from View, uggggh. [Alexander Böhn]

* Reverted the use of newer “KeyMap” classes in “FileBase” ancestors ... this was causing base-class layout conflicts when “__weakref__”     slot members were added to the abstract bases at the root of     the KeyMap class tower. I left the KeyMap imports in, commented     out – when I get rid of all the old namespaced-mapping shit     in favor of the all-new hottness this will be such a non-issue     you will forget having even read this commit note, doggie, yeah. [Alexander Böhn]

* Moved “__weakref__” slot declaration down to “FrozenKeyMapBase” [Alexander Böhn]

* Initial inline tests for “KeyMapView” and “KeyMapProxy” [Alexander Böhn]

* You know, sometimes, resource allocation *is* initialization. [Alexander Böhn]

* Minor cleanup in “clu.testing.utils” [Alexander Böhn]

* Minor renames in “clu.testing.utils” [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* I ❤️ fstrings. [Alexander Böhn]

* Updated the “clu.testing.utils.InlineTester” docstring ... now the code sample illustrates returning POSIX status values. [Alexander Böhn]

* Changelog and git-ignore tweaks. [Alexander Böhn]

* Bump version: 0.5.4 → 0.5.5. [Alexander Böhn]

* Integrating “gitchangelog” and taking it for a trial run. [Alexander Böhn]

* A fine Commit #1,000 as any: preservation of namespace insert-order ... happy order-of-magnitude-aversary, my dear CLU, and salud! [Alexander Böhn]

* Inline tests return POSIX exit status values and call “sys.exit(…)” ... also there is a command that copies the CLU boilerplate starter     code right to YOUR CLIPBOARD!!!! Huzzah. [Alexander Böhn]

* First draft of “KeyMapView” and “KeyMapProxy” ... which those are ‘FrozenKeyMap’ and ‘KeyMap’ types, respectively,     that wrap weakrefs to actual KeyMap instances and forward method     calls to those instances down from the public API. ... includes a decorator “@selfcheck” that tests the Truthiness of     the ‘self’ instance before the actual method invocation and     raises a ‘ValueError’ for any and all unworthy instance values. ... tests and all that other hoohah to follow, after I veg out     with the cats and some kombucha and watch me some YouTube. [Alexander Böhn]

* Generators beat constructed lists. [Alexander Böhn]

* Bump version: 0.5.3 → 0.5.4. [Alexander Böhn]

* How many commits are just, however circuitously, pushing whitespace? [Alexander Böhn]

* Inline fixture is inline-fixture’d. [Alexander Böhn]

* Trying to figure out if inline-testing instance methods is worth it. [Alexander Böhn]

* Fold my case. [Alexander Böhn]

* Using str.casefold() instead of str.lower() for comparison. [Alexander Böhn]

* Fixed a few assertions. [Alexander Böhn]

* Cleaned up the “clu.importing” inline testsuite a bit. [Alexander Böhn]

* Environment-var diagnostic printout function and fixture decorator ... among other additions to “clu.testing.utils.InlineTester” ... fixtures are memoized with “functools.lru_cache(…)” and stored     in a dict in the “@inline” instance; maybe I will add automatic     cache-warming as a precheck function, and/or a report on cache     usage as a diagnostic… WHO KNOWS REALLY. [Alexander Böhn]

* Inline test harness support for preflight and diagnostic functions ... So, like, you can decorate things like so: [Alexander Böhn]

  @inline.precheck
      def preflight_function():
      	# …

      @inline.diagnostic
      def post_execution_function():
      	# …

  ... Functions decorated per the former will each run exactly once,
      before the main test run; those decorated as per the latter
      will each run exactly once, after the main test run.
  ... There are examples of these in a bunch of my inline test suites
      for you to peruse
  ... There was some internal abstraction and consolidation that
      happened in “clu.testing.utils.InlineTester” to support all of
      this – all good and fairly legible changes, I should say; the
      new things have docstrings and stuff. Yes!

* Computing lambda qualified name in lambda-repr test. [Alexander Böhn]

* Cleaned up some testing stuff, both inline and out. [Alexander Böhn]

* Proper index-labeling and ordering for inline test functions. [Alexander Böhn]

* Using the “flatdict()” fixture-ish function in KeyMap inline tests ... also killed some dead code in “clu.testing.utils” [Alexander Böhn]

* WTF HAX. [Alexander Böhn]

* Fixed a regression with hacky “isnamespace(…)” from “clu.predicates” [Alexander Böhn]

* Explicit > Implicit. [Alexander Böhn]

* Don’t trigger “__missing__(…)” during “ChainModuleMap” item access. [Alexander Böhn]

* Even more repr-related refactors. [Alexander Böhn]

* Miscellaneous repr-related tweaks and updates. [Alexander Böhn]

* I just worked really really hard… on fixing “Namespace.__repr__(…)” ... I mean “SimpleNamespace” had this copypasta from SO, and the     ancestor “Namespace” used this super-janky thing that, like,     called “pprint.pformat(…)” on the instance ‘__dict__’ and then     opaquely regexed the results of that for some reason – ... sooooo I switched them to use “clu.abstract.ReprWrapper” and     everything started exploding with outlandish infinite-recursion     error supernovae; ... so I started playing around with “reprlib” – ... I first tried applying “@recursive_repr(…)” to “ReprWrapper”     methods, which didn’t really help – ... I did a lot of fucking around and to make a long story short,     there is now a “reprlib.Repr” subclass with recursion-friendly     methods sitting in “clu.typespace.namespace” – ... There was way more recursion than just that tho: I battled     recursive imports, recursive stringification, recursive fuckall     and who the fuck knows… all really my own sloppy fault, I mean     I haven’t updated “clu.typespace” in millenia, it feels like ... and THEN at the end of it all, when things worked, I spent     even MORE time tweaking the stupid string-formatting for like     an hour, making it JUUUUUUST RIIIIIIGHT ... blech! Fuck yes. [Alexander Böhn]

* Oh yeah… explicit is soooo much better than implicit – and thus. [Alexander Böhn]

* ¡IMPLICIT RECURSIVE NAMESPACES! [Alexander Böhn]

* Futzed with inline-test names, naming, and name-display. [Alexander Böhn]

* “clu.importing.PolymerType.add_module(…)” checks existing appspaces ... raises a ‘NameError’ should you attempt to add a module with     an appspace that already exists. [Alexander Böhn]

* Allowing “clu.importing.ProxyModule” to target other ProxyModules ... when a ProxyModule is encountered while processing the list of     targets, its existing contents are extracted, flattened out,     and merged into the governing proxy’s internal ChainModuleMap. [Alexander Böhn]

* Extremely minor test docstring tweak. [Alexander Böhn]

* Docstring updates for “ProxyModule” and “ChainModuleMap” ... the callable/‘__missing__(…)’ stuff has had the shit documented     out of it. [Alexander Böhn]

* “clu.importing.ProxyModule” knows about module ‘__getattr__(…)’ ... and “MappingType.__missing__(…)” too, and callables in general. [Alexander Böhn]

* Bump version: 0.5.2 → 0.5.3. [Alexander Böhn]

* Ensuring no duplication occurs when initializing ProxyModules ... also, it seems I misunderstood the use of the “module” param     accepted by “collections.namedtuple”… erm. [Alexander Böhn]

* As much as I appreciate this inadvertant neologism my OCD disallows it. [Alexander Böhn]

* Tailored non-logorrheic type-reprs for class-modules and friends ... also added a whole shitton of exemplary docstrings and assorted     programmer notes ... and tweaked the exception-handling messaging in “ProxyModule”’s     ‘__getattr__(¬)’ logic ... and added the first new beginning of a “clu.application” module     (which right now is just copypasta from “clu.importing” that’ll     get deleted in short order – but it’s something, which you will     not is not nothing, is it not not?? [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* “typing.Mapping[…]” is more general than “typing.Dict[…]” [Alexander Böhn]

* Reordered the dataclass & the mapping, reflecting definition order. [Alexander Böhn]

* Shortcutting the @dataclass decorator in the name of legibility. [Alexander Böhn]

* Deduplicated the efforts between “initialize_{new_types,module}(…)” [Alexander Böhn]

* Fixed it! [Alexander Böhn]

* Go by the name you’ve been given, not just the one you’re called. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* I should have done this a loooong time ago – ... that is to say: added a per-appname class registry for all the     Finders, Loaders, individually-appspace’d Module subtypes…     all that shit in “clu.importing” basically. [Alexander Böhn]

* Storing the app-named “Loader” class in its companion “Finder” [Alexander Böhn]

* Extremely minor/subtle logic nitpick in “Environ.__exit__(…)” [Alexander Böhn]

* Compensated for Falsey argument behavior. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Reverting unnecessary confusing complexification. [Alexander Böhn]

* WHOOOOOPS. [Alexander Böhn]

* Allow non-None but Falsey “environment” args in Nested’s constructor. [Alexander Böhn]

* Split inline testing data into two ‘pseudo-fixture’ functions. [Alexander Böhn]

* Narrowing the scope of the semantic-version regex. [Alexander Böhn]

* Git version inline tests now check Git output against CLU version. [Alexander Böhn]

* Find path to Git binary on “clu.version.git_version” module load. [Alexander Böhn]

* Amended the ProxyModule unit test by one assertion. [Alexander Böhn]

* Sequester the “targets” ProxyModule attribute rather than deleting. [Alexander Böhn]

* Neatened up some of ProxyModule’s parts: docstrings, init stuff, &c ... fleshed out an inline test or two in “clu.importing” as well. [Alexander Böhn]

* Renamed a related test function. [Alexander Böhn]

* Context-managed environment access for mutable “Environ” instances. [Alexander Böhn]

* Docstring labeling for inline KeyMap tests. [Alexander Böhn]

* Better test-function lexical grouping. [Alexander Böhn]

* Traded gratuitous test prints for generally real-er testing code. [Alexander Böhn]

* Out with pointless varargs, in with docstrings ... also in with DefaultDicts by, erm, default in the Nested types ... and also, in with key checking for mutable Nested type deletes ... and also other stuff. [Alexander Böhn]

* More inline-test formatting minutiae and speedups. [Alexander Böhn]

* Nitpicks on inline test output formatting. [Alexander Böhn]

* Copied ‘clu/__main__.py’ to ‘clu/version/__main__.py’ ... in anticipation of, you know, putting something real up in the     package-level main file, doggie. [Alexander Böhn]

* Minor logic shortcut in new “FrozenNested.submap(…)” method ... in no way was implementing this the panacea of O(1)-ness I had     assumed it’d be when I started, baaaah. [Alexander Böhn]

* Packed string compare beats iterative namespace chunk compare. [Alexander Böhn]

* Ooops – forgot to actually change directories. [Alexander Böhn]

* Ensure that “git_version_tags(…)” uses the project base directory. [Alexander Böhn]

* Bump version: 0.5.1 → 0.5.2. [Alexander Böhn]

* Updated “clu-version” to output a Git version tag, if present. [Alexander Böhn]

* Propagated the docstrings. [Alexander Böhn]

* Some revisions and streamlining to “clu.fs.filesystem.back_tick(…)” ... the verenable function had a few implicit shortcomings: only     lists and tuples were valid as non-string command arguments;     bytes-mode output decoding was being handled by some specious     logic of mine, instead of by just using the “text” argument to     the “subprocess.Popen” constructor; “shlex.split(…)” was called     in “non-posix mode”, whatever the fuck that means; assorted     other messiness also abounded. [Alexander Böhn]

* Tuneups to inline test information-printouts ... first off, a “verbose” kwarg flag keeps the decorator wrapper     function from wasting time printing out information that is     just going to get consumed by the stdout-redirector used during     all run cycles after the first one; ... but then secondly, we retrieve the test functions’ docstring,     and call the first stripped line of that docstring the “title”,     and we stick that in the header printed for each test function.     No use of this datum elsewhere (for the moment). [Alexander Böhn]

* Fast environment-specific “__contains__(…)” and “__getitem__(…)” ... key-prefix conversion is much much faster than “walk(…)” over     the whole backend data source, doggie. [Alexander Böhn]

* Brought a filesystem test over to “clu.testing.utils” as an inline ... to ensure we’re testing “clu.testing.utils.countfiles” in the     inline test suite. [Alexander Böhn]

* Rewrote the “NamespaceWalkerViewBase.__len__()” implementation ... to use “clu.typology.iterlen(…)” and a generator expression,     rather than for-looping with an index variable (how gouche!) [Alexander Böhn]

* Further adventures in mature optimization ... this time it’s a corresponding “NamespaceWalkerKeysView” type,     and a new intermediate abstract sub-base for all the new view     types that provides a less näive “__len__()” method. [Alexander Böhn]

* Docstring for the internal “startswith_ns(…)” helper function. [Alexander Böhn]

* Sometimes, you want seperate “__new__(…)” and “__init__(…)” funcs. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Exporting the “clu.config.defg.envwalk(…)” helper function. [Alexander Böhn]

* Gratuitous logic simplification in inline-testing’s inline tests. [Alexander Böhn]

* Updating the primary “@inline” docstring. [Alexander Böhn]

* Revised the @inline test decorator mechanism ... to wit: it is now implemented as a class that is instanced     automatically via module ‘__getattr__(…)’ each time it is     requested for import ... this makes managing the stopwatch instances and the decorated     functions, as instance attributes, way way easier ... plus it eliminates the need for the clunky “vars()” argument     to all the “inline.test()” calls ... a few other revisions were made during these changes (most     notably the elimination of the “collection phase” in the main     stopwatch report – but that was kind of stupid anyway) [Alexander Böhn]

* Bump version: 0.5.0 → 0.5.1. [Alexander Böhn]

* Actual inline tests for @inline and friends. [Alexander Böhn]

* More inane dev-ish comments. [Alexander Böhn]

* Const-correct Craving. [Alexander Böhn]

* Developer-facing comments about what the fuck is going on. [Alexander Böhn]

* Fixed time reporting for one-off execution of @inline tests. [Alexander Böhn]

* Killed a lot of dead code. [Alexander Böhn]

* Integrated ‘dbx-stopwatch’ with the inline test framework ... including a custom report-formatting function, as theirs is     awful (and not like this one is much better but the need is     there, and it’s something, OK?) ... inline tests auto-collect and run via local-variable mapping     hook ”inline.test(«vars», [runcount])” ... a number of inline test suites were converted over to the new     auto-collection API ... tweaked the requirements accordingly (N.B. this still needs     some winnowing) [Alexander Böhn]

* Reorganized the “clu.config” testsuite ... moved all KeyMap-related tests to their own test class. [Alexander Böhn]

* Enabling last inline test. [Alexander Böhn]

* Nitpickery. [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* Docstrings and miscellany. [Alexander Böhn]

* Pure, unfiltered minutiae. [Alexander Böhn]

* Total minutiae. [Alexander Böhn]

* Being explicit about the class we’re using in the KeyMap env tests. [Alexander Böhn]

* Initial tests with new KeyMap-based environment access are GO. [Alexander Böhn]

* Simplifying some internal string-only comparisons. [Alexander Böhn]

* The very first of passing test runs WITH the new KeyMaps installed! ... getting to green on this involved finding and fixing a big-ish     bug in the “compare_ns(…)” helper, which we use in implementing     “Nested.__contains__(…)” and “Nested.__getitem__(…)” – dropping     in “itertools.zip_longest(…)” therein in leu of a “zip(…)” call     was the fortunately simple fix, once the flaw was discovered. ... We are using the new KeyMap classes in “clu.config.filebase”     and all of the format definition modules e.g. ‘tomlfile’ &c. ... We were able to explicitly swap KeyMap ancestors in on at least     one test – ‘test_nested_and_flat(¬)’ – wholesale with no issues     (after squashing the big-ish bug of course). ... So yeah, here’s to many more! 🥂 [Alexander Böhn]

* Updated the REPL scripts for the new “clu.config” hot shit. [Alexander Böhn]

* Allowing keyword updates in “Flat” and “Nested” constructors. [Alexander Böhn]

* Gratuitous recursion added to “KeyMap.update(…)” [Alexander Böhn]

* One less import is one more fuck-yes in the pot ... you know, the fuck-yes pot. We all have one, somewhere. [Alexander Böhn]

* Another slight name disambiguation. [Alexander Böhn]

* Rewrote it again with a set comprehension. [Alexander Böhn]

* Rewrote “FrozenKeyMap.namespaces()” to suck a lot less. [Alexander Böhn]

* Faster still for the logic of “get_ns(…)” [Alexander Böhn]

* Another gratuitous function rename. [Alexander Böhn]

* Like I said. [Alexander Böhn]

* Since we aren’t worried about interstitial sequences anymore… ... we won’t need to expand iterable keys during namespace packing,     like duh. [Alexander Böhn]

* Got rid of any naming ambiguity regarding keys, nskeys, and such. [Alexander Böhn]

* Minor simplification in “get_ns(…)” logic. [Alexander Böhn]

* Simplified the logic behind “FrozenNested.namespaces()” [Alexander Böhn]

* Same slight simplification in “FrozenKeyMap.submap(…)” logic. [Alexander Böhn]

* Slight simplification of the “KeyMap.clear(…)” logic. [Alexander Böhn]

* Simplified “KeyMap.pop(…)” logic. [Alexander Böhn]

* Moving disabled code. [Alexander Böhn]

* Disabling (for now) sequence expansion in nested trees. [Alexander Böhn]

* More professionalism. [Alexander Böhn]

* Making “FrozenNested.mapwalk()” look professional. [Alexander Böhn]

* Un-abstracting the “KeyMap.__reversed__(…)” method. [Alexander Böhn]

* “__contains__(…)” and “__iter__(…)” are abstract methods of “KeyMapViewBase” [Alexander Böhn]

* More flat/nested conversion test coverage. [Alexander Böhn]

* Testing roundtrip flatten-to-nestify and nestify-to-flatten. [Alexander Böhn]

* Removed sequence literals from nested sample data. [Alexander Böhn]

* The “mapwalk(…)” function includes sequence indexes. [Alexander Böhn]

* Compatibility stuff across the board for the new KeyMap API. [Alexander Böhn]

* Aaaaand BUNCHA DOCSTRINGS ... say it like Eddie Izzard saying “BUNCHA FLOWERS” in that bit     that he did. [Alexander Böhn]

* Reworded that nota-benne. [Alexander Böhn]

* Bespoke namespace iterator function for “Nested” [Alexander Böhn]

* OK so the immutable namespacey rewrite of “clu.config.Nested” works. [Alexander Böhn]

* Logic notes for new REPL script. [Alexander Böhn]

* Inline test is the inliniest, testiest ever before seen. [Alexander Böhn]

* I give up, the KeyMap class tower is now ‘clu.abstract.Slotted’ ... like if this is a problem down the line doggie just stick in a     ‘__dict__’ slot somewhere and everything’ll be A-OK, guaranteed. [Alexander Böhn]

* Moved “namespaces(…)” method up into ‘FrozenKeyMap’ [Alexander Böhn]

* I got your module exports, right over here within my pants. [Alexander Böhn]

* Well fuck – that actually worked pretty much the first time ... happy birthday to me, I guess, rite?? For reals dogg December     the Fifth is my real actual birthday, so thank you, me, for     conforming to the Me Coding Guidelines. [Alexander Böhn]

* And so commenceth the Great Re-Naming Of The Things. [Alexander Böhn]

* Trimmed disabled unprefixed-key-related code alternatives. [Alexander Böhn]

* Keyword API accomodations for retrieving views of unprefixed keys. [Alexander Böhn]

* Re-enabling “Flat.nestify(…)” [Alexander Böhn]

* Map-Walker™ [Alexander Böhn]

* Redoing the foundations of “clu.config.abc.NamespacedMutableMapping” [Alexander Böhn]

* Also made “clu.config.fieldtypes.__getattr__(…)” quiet down. [Alexander Böhn]

* The “qualified_name(…)” and “qualified_import(…)” fns are quieter ... they were, like, unnecessarily chatty there for a long while. [Alexander Böhn]

* Remove insecure Django requirement. [Alexander Böhn]

* Further fleshing out REPL script. [Alexander Böhn]

* Getting started on new REPL environment script. [Alexander Böhn]

* Tweaked a method name in “clu.dicts.ChainMap” ... specifically it is now “mapcontaining” instead of “mapcontains” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* One other spot where our ChainMaps and their ChainMaps may meet. [Alexander Böhn]

* Our ChainMap will take our ChainMaps and their ChainMaps too. [Alexander Böhn]

* Made “clu.naming.qualified_import(…)” work with just module names ... versus qualified-thing-names, which was what specifically it     was expecting previously. [Alexander Böhn]

* I like “delattr(…)” more than “del «…»” [Alexander Böhn]

* WHOOOOPS. [Alexander Böhn]

* Setting importlib-metadata requirement in stone. [Alexander Böhn]

* Minor bpython REPL script update. [Alexander Böhn]

* HAAAAAACK ... until I summon the werewithall to do some kind of stem/leaf     type of analysis or property or whatever the fuck – this total     hackjob bullshit will do (and it actually is kind of totally     effective for like the near-forseeable future actually, yeah) [Alexander Böhn]

* Iterchaining those “dir(…)” lists ahead-of-time ... Minimum waaaaaaaaaaage »¡HIYAAA!« [SFX: whip-crack] [Alexander Böhn]

* True paranoia ... I just remembered I read somewhere that “__init__(…)” methods     are not guaranteed to run only once, and might run a couple of     times just for shits ‘n’ giggles. [Alexander Böhn]

* Plugging yet another microsecond-in-diameter hole. [Alexander Böhn]

* Storing “__dir__(…)” results for ProxyModule’s “__dir__(…)” impl ... Also, I like ‘delattr(…)’ more than ‘del «thing»’ – the latter     of which looks way too nondeterministic by association and also     more problematically loosey-goosey like in general. [Alexander Böhn]

* Explicit, I am told, brings more general joy than (say) implicit ... I dunno whether premature optimization is better or more joyful     or nicer or what-have-you than other kinds of optimization but     you are getting those in this diff too whether you like it     or not, doggie, OK? OK. [Alexander Böhn]

* Fixed possible race condition in “ProxyModule.__getattr__(…)” ... “ProxyModule._executed” could be True for like one or maybe two     frames of interpreter execution during which the initialization     mapping list “ProxyModule.target_dicts” still existed, which     could short-circuit attribute-access for like half a frame more     after calling for the deletion of the list – this is probably     minute enough to qualify this diff as “premature optimization”     – or “obsessive-compulsive flow control”, either-or – but I do     not care as it is far more satisfying to have unfucked it than     it’d be to leave it sitting there all fucked and such. [Alexander Böhn]

* Culling ‘sys.modules’ on “clu.importing.Registry.unregister(…)” ... fucking finally. [Alexander Böhn]

* Got rid of the ‘SubModule(…)’ class-module context-manager – ... it was waaaay more trouble than it was worth ... also stopped merging proxied modules’ exporters into the proxy     module’s exporter – this was wreaking havoc with “nameof(…)”     and “moduleof(…)” search-component mechanisms; ... INSTEAD we are simply leaving proxy-module exporters to work     as they would normally – like e.g. on stuff explicitly defined     therein – and using an overridden “ProxyModule.__dir__(…)” to     get the job done. [Alexander Böhn]

* Module-importing “clu.constants.consts” instead of cherry-picking. [Alexander Böhn]

* Bump version: 0.4.10 → 0.5.0. [Alexander Böhn]

* Made “clu.importint.ProxyModule” a real thing ... with tests (both inline and unitary), docstrings and notes,     differentiated support functions and classes… YOU NAME IT ... !!!!!!!!!!!!!!!!!! FUCK YES !!!!!!!!!!!!!!!!!!! [Alexander Böhn]

* Further notations, errata, and error-message minutiae. [Alexander Böhn]

* Bespoke (aka hack-tastic) one-off proxy-module typename reporting. [Alexander Böhn]

* De-redundifying proxy-module “__getattr__(…)” error handling. [Alexander Böhn]

* Position one arg for module name, keyword-only arg for docstring. [Alexander Böhn]

* Docstring for experimental proxy-module “__init__(…)” call. [Alexander Böhn]

* Uncluttering proxy module namespace via function inlining. [Alexander Böhn]

* Trimming class-module instance methods in “__execute__()” [Alexander Böhn]

* Trimming intermediate target lists from proxy module internals. [Alexander Böhn]

* Threw in an additional assert in old test, just to be safe. [Alexander Böhn]

* Updated “clu.typology” assertion regarding “clu.extending” ancestry. [Alexander Böhn]

* Experimental class-based module-wrapper proxy thing in tests ... the meat of this currently resides in “test_importing.py”,     q.v. test function ‘test_module_dict_proxy_idea’ supra. for     the module-class proxy reference implementation, a working     example subclass and example code that does not fail to run ... basically it’s a ChainMap for module attributes (like literally     as this implementation uses “clu.dicts.ChainMap” internally) ... also internally, the sub-sub-sub-sub-metaclass base for all     class-based modules inherits from “clu.extending.Extensible” –     which that type itself inherits from “clu.abstract.NonSlotted”     instead of plain ol’ ‘type’ ... the implementation classes for the “clu.extending.doubledutch”     decorator – “DoubleDutchRegistry” and “DoubleDutchFunction” –     now leverage a number of CLU- and standard-library-based ABCs. [Alexander Böhn]

* The “clumods” pytest fixture now depends on the “consts” fixture. [Alexander Böhn]

* Session-scoping the “greektext” pytest fixture. [Alexander Böhn]

* Moreso deployment of the new “consts” pytest fixture. [Alexander Böhn]

* Updated comment note on module inclusion criterion. [Alexander Böhn]

* Import shuffle. [Alexander Böhn]

* Killed trailing whitespace. [Alexander Böhn]

* Generalized and centralized import-all-modules logic ... created a new module “clu.all”, containing two functions:     • “import_all_modules(basepath, appname)”       → Imports all modules, both file-based and class-based, from       	the app «appname» within the package rooted at «basepath»     • “import_clu_modules()”       → Imports all CLU-specific modules – a convenience call for         “import_all_modules(consts.BASEPATH, consts.PROJECT_NAME)” ... the “clu.testing.pytest.clumods” fixture now simply delegates     to a call to “clu.all.import_clu_modules()” ... the clu-module-importing function in ye olde “show-modules.py”     script has been replaced with “clu.all.import_all_modules(…)” ... no specific tests have been added because this shit is already     super-100%-plus covered by existing test code, doggie. [Alexander Böhn]

* Re-instating “rm_rf(…)” usage in pytest plugin’s exit handle. [Alexander Böhn]

* Using “shutil.rmtree(…)” in “clu.fs.filesystem.rm_rf(…)” ... instead of all of my tortured bespoke logic that apparently did     not quite work right. [Alexander Böhn]

* Noting possible one-liner for “installed_appnames()” impl. [Alexander Böhn]

* Bump version: 0.4.9 → 0.4.10. [Alexander Böhn]

* Updated/refactored some of “clu.fs.pypath” ... “pypath.append_path(…)” has been renamed “pypath.add_path(…)”,     and it now accepts a keyword-only argument ‘prepend=True’ to,     y’know, prepend its payload to ‘sys.path’ instead of appending. ... “pypath.remove_invalid_paths()” calls ‘site.removeduppaths()’     before doing anything to ‘sys.path’ ... There’s a new convenience function “pypath.enhance(…)” which     is basically sugar for calling “remove_invalid_paths()” ahead     of calling “add_path(…)” – which as already noted now also     includes a call to ‘site.removeduppaths()’ ... the REPL script imports “clu.fs.pypath” as a module, instead     of picking through its exported functions ... many tests make use of new “clu.fs.pypath.enhance(…)” function. [Alexander Böhn]

* Moved the “pytester” requirement into the CLU pytest plugin proper. [Alexander Böhn]

* Testing and pytest support for “clu.dispatch” ... new “clu.constants.consts” item ‘USER’, value of the current     users’ username ... rework of “clu.fs.filesystem.rm_rf(…)” logic ... The “clu.testing.pytest” plugin now implements a pytest hook     function “pytest_sessionfinish(…)”, which in turn conditionally     binds an exit handler – using “clu.dispatch.exithandle” – that     deletes any stray pytest temporary-file artifacts left over     upon interpreter shutdown     … namely, anything in the directory $TMPDIR/pytest-of-$USER –       which stubbornly would not remove itself and (according to       the policy of pytest’s code for this, apparently) just keeps       accumulating piles of cruft every time ‘pytest’ was executed ... All in aid, really, of the one new test, in “test_dispatch.py”,     which makes use of the “pytester” built-in pytest plugin to     cleanly test exit handlers; see the source of same for details. [Alexander Böhn]

* Updated the bpython REPL script for the ‘dispatch’ update. [Alexander Böhn]

* Moved “clu.shelving.dispatch” down to “clu.dispatch” ... as it is clearly bigger than just the nascent ‘shelving’ module. [Alexander Böhn]

* Made “clu.fs.filesystem.TemporaryFileWrapper” an explicit Iterable ... as in, it inherits from ‘collections.abc.Iterable’ ... also added 'pytester' to the test plugins loaded in conftest.py. [Alexander Böhn]

* Bump version: 0.4.8 → 0.4.9. [Alexander Böhn]

* Split off async parts of “clu.abstract.ManagedContext” ... into “clu.abstract.AsyncManagedContext” [duh] ... also added tests for the former. [Alexander Böhn]

* Exclude async methods on lower pythons from “clu.abstract.ManagedContext” [Alexander Böhn]

* Re-enabling test for qualified naming of constants. [Alexander Böhn]

* Elected to use context-managed exporting in “clu.exporting” itself. [Alexander Böhn]

* Trimmed and tweaked “clu.exporting” generally – ... moved “clu.exporting.rename” to “clu.naming” where arguably it     has always belonged ... removed nearly all method-level imports in “clu.exporting” in     favor of module-level; so far, so good ... made a couple minor tweaks to “clu.exporting.ExporterBase”, of     which the most notable is that “clu.exporting.ExporterBase” is     now a context manager; doing: [Alexander Böhn]

  exporter = Exporter(path=__file__)

  	with exporter as export:

  	     @export
  	     def yodogg():
  	     	 ...

      … now works, and makes a certain amount of sense

* Removed old “Python 3”-specific REPL module. [Alexander Böhn]

* Removed old Bash REPL stub. [Alexander Böhn]

* Fixed docstring *again* pt. II. [Alexander Böhn]

* Fixed docstring *again* [Alexander Böhn]

* Use current if “importables(…)” called with Falsy subdirectory. [Alexander Böhn]

* Docstring minutiae. [Alexander Böhn]

* REPL script updates. [Alexander Böhn]

* Bump version: 0.4.7 → 0.4.8. [Alexander Böhn]

* Typographic eratta en extremis. [Alexander Böhn]

* Bump version: 0.4.6 → 0.4.7. [Alexander Böhn]

* Bump version: 0.4.5 → 0.4.6. [Alexander Böhn]

* SIG-WINCH!!!!! [Alexander Böhn]

* Logging format config manscaping. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Tweaking shutdown logic. [Alexander Böhn]

* Minor tweak to zipfile artifact save logic. [Alexander Böhn]

* Even more “clu.shelving.dispatch” minutiae. [Alexander Böhn]

* Exit handle functions execute properly from signal handlers. [Alexander Böhn]

* More tweaks to async signal-handler demo code. [Alexander Böhn]

* Bump version: 0.4.4 → 0.4.5. [Alexander Böhn]

* Some minutiae in “clu.shelving.dispatch.test(…)” [Alexander Böhn]

* Rounded out “clu.shelving.dispatch” innards. [Alexander Böhn]

* No longer reversing the sequence in “functional_and.__call__(…)” [Alexander Böhn]

* Moved a bunch of stuff around. [Alexander Böhn]

* Many updates to “clu.shelving” and friends ... support for exit-handler functions in “clu.shelving.dispatch”,     wherein multiple functions can be registered through the new     “@exithandler” decorator, and ordered execution is guaranteed     even if the process ends abruptly due to like e.g. SIGKILL or     what have you ... exemplary exit-handler definitions are now in use within the     “clu.shelving.redat” and “clu.app.redprocess” modules ... a new abstract type “clu.abstract.ManagedContext” fills in the     special async and synchronous context-manager methods, based on     “setup(…)” and “teardown(…)” function calls. [Alexander Böhn]

* CHAIN CHAIN CHAAAIIIN – CHAAAIN THE FOOOO-OOOL. [Alexander Böhn]

* Only checking the CLU app’s registered class-based modules. [Alexander Böhn]

* CLU-project module tests properly consider class-based modules. [Alexander Böhn]

* Fixed Redis class-module inline test. [Alexander Böhn]

* Managing Redis subprocess with a class-based module. [Alexander Böhn]

* More Redis-handle decoupling. [Alexander Böhn]

* Initially decoupling “redat.RedisConf” from “redat.RedRun” [Alexander Böhn]

* Sleeping in the proper place during Redis server process startup. [Alexander Böhn]

* De-duplicating “multidict” requirement. [Alexander Böhn]

* Clarified a few things in “clu.config.filebase” [Alexander Böhn]

* Bump version: 0.4.3 → 0.4.4. [Alexander Böhn]

* Fixed “RedRun.__repr__(…)” when the configuration is inactive. [Alexander Böhn]

* Escaping a raw regex string. [Alexander Böhn]

* Fixed variable-shadow name bug in “clu.fs.misc” [Alexander Böhn]

* Fixed bug when calling “clu.fs.misc.re_excluder(…)” with no args. [Alexander Böhn]

* Getting rid of polyfill “walk(…)” and “scandir(…)” [Alexander Böhn]

* Minor touchups to “clu.fs.filesystem.back_tick(…)” [Alexander Böhn]

* Using @itervariadic with “clu.fs.misc.re_excluder(…)” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Argument length check in “clu.fs.misc.re_excluder(…)” [Alexander Böhn]

* Abstracted the “exclude” bit from two “clu.fs.filesystem” methods ... namely: “clu.fs.filesystem.Directory.importables(…)” and its     cousin, “clu.fs.filesystem.Directory.suffix_histogram(…)”, and     stowed the logic of said bit in a function in “clu.fs.misc”. [Alexander Böhn]

* Git-ignoring Redis artifacts. [Alexander Böhn]

* Bump version: 0.4.2 → 0.4.3. [Alexander Böhn]

* I keep thinking I fixed “clu.repl.ansi.print_ansi_centered(¬)…” ... and then it turns out there is yet another corner-case causing     it to be off by one or two filler characters in some situation     or another – likely one brought about by the last “fix” – but     I really do think I’ve nailed it this time, famous last words,     OK we shall see now won’t we doggie yeah. [Alexander Böhn]

* Much much miscellany -» Added “clu.fs.misc.extension(…)” and “clu.naming.suffix(¬)”,    both of which return the extension (née “suffix”) from a file’s    path – one is a lambda and the other is a function with a few    more options. Both of these were deployed around and about the    codebase at large -» Fixed a bug in “clu.importing.ModuleBase.__dir__()” that made    itself known when ‘dir(…)’-ing “ModuleBase” subclass instances    suffering from a lack of integral “clu.exporting.ExporterBase”    properties; this pertained to “clu.predicates.union(…)” – which    I am now starting to think is silly – and the fix was ro redo    the implementation with “itertools.chain(…)” and a ‘frozenset’. -» Generally rejuggled the third-party imports in “clu.naming” and    tidied up a few things in there while also adding in functions    dealing with file suffixes, as aforementioned -» Removed the debug grace from “clu.testing.utils.__getattr__(…)” -» Fixed the “clu.typespace.types.__package__” property and tidied    the imports in the “clu.typespace” packages’ “__init__.py” file -» Only requiring Pillow in non-PyPy envs when running `tox` due    to PyPy remaining obstinately stupid about compiling it therein -» Additional tox-related OCD-ish tweaks and additional morsels. [Alexander Böhn]

* Trimmed outdated imports from “repl-bpython.py” [Alexander Böhn]

* Migrated “clu.extensible” inline tests to the testsuite. [Alexander Böhn]

* Trimming “clu.constants.polyfills” [Alexander Böhn]

* Removing old “clu.constants.terminalsize” hacks. [Alexander Böhn]

* Docstring tweak. [Alexander Böhn]

* Some import/export touchups ... the master exporter class-registry dictionary now uses weakrefs ... the filesystem root is now programmatically determined ... gratuitous super-call in “FinderBase.invalidate_caches()” has     been removed. [Alexander Böhn]

* Got rid of MODNAMES once and for all ... FUCK YES. [Alexander Böhn]

* Finally we can eschew “clu.constants.data.MODNAMES”!… ... in favor of an actual programmatically-generated list of the     project’s importable file-based submodules ... the current method “clu.fs.filesystem.Directory.importables(…)”     is pretty comprehensive, for something hacked together quickly     and out of frustration ... TODOs of course are: *) split that lambda off into some kind of     reusable exclude-list shit in “clu.fs.misc”, and add some tests     and sensible defaults and yadda-yadda; *) check to see if this     has any value outside of this particular application; and other     such shit ... YES!!! YES DOGG THIS WAS ON MY PERSONAL SHIT-LIST FOR A WHILE     NOW SO I CAN START THE DAY HAPPY OKAY?? [Alexander Böhn]

* Bump version: 0.4.1 → 0.4.2. [Alexander Böhn]

* Properly set “_executed” flag on modules lacking an “__execute__()” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Importing “clu.abstract” wholesale rather than piecemeal ... in both “clu.exporting” and “clu.importing” [Alexander Böhn]

* Removed unnecessary callable check in “clu.exporting.determine_name(…)” [Alexander Böhn]

* Getting “lru_cache” in “clu.exporting” directly from ‘functools’ [Alexander Böhn]

* One-character typo fix. [Alexander Böhn]

* Bump version: 0.4.0 → 0.4.1. [Alexander Böhn]

* Less precision is OK with me in this case. [Alexander Böhn]

* Fleshing out “clu.repr” tests and details. [Alexander Böhn]

* Simplified decorator usage in “clu.fs.misc” [Alexander Böhn]

* Tweaked “suffix_searcher(…)” test to explicitly check None operands. [Alexander Böhn]

* Another premature optimization in the testsuite. [Alexander Böhn]

* Further pairing down gratuitous filesystem work in some tests. [Alexander Böhn]

* Rolled the “clu.fs.misc.samesize(…)” test into its precedent. [Alexander Böhn]

* Fleshing out “clu.fs.misc” tests to check file-size functions. [Alexander Böhn]

* Avoiding gratuitous file-copy operations in some tests. [Alexander Böhn]

* Expand the “filesize(…)” test to check nonexistant file attributes. [Alexander Böhn]

* Allow “clu.exporting.determine_name(…)” to work on all wrappers – ... not just function-types (as defined with “def” or lambdas) but     any callable types with a callable “__wrapped__” attribute. [Alexander Böhn]

* Ugh. [Alexander Böhn]

* Some of these tests are kind of circuitous. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* More “clu.abstract” unit tests – some adapted from existing tests. [Alexander Böhn]

* Test suites for metaclasses in “clu.abstract” [Alexander Böhn]

* Ported two “clu.importing” inline tests to the testsuite ... specifically it’s the two tests that exercize the code for the     “clu.importing.SubModule” utility. [Alexander Böhn]

* All kinds of new tests. [Alexander Böhn]

* Moved “MappingViewRepr” to “clu.abstract” and documented it. [Alexander Böhn]

* Importing “clu.abstract” wholesale and not piecemeal in “clu.dicts” [Alexander Böhn]

* Updated some docstring references to “Slotted” and “Prefix” [Alexander Böhn]

* The “Prefix” metaclass has been moved to “clu.abstract” [Alexander Böhn]

* Using “clu.abstract” classes in “clu.dicts” [Alexander Böhn]

* Moved “wrap_value(…)”, “hoist(…)” and friends to “clu.predicates” ... also trying to trim some of the gratuitous no-op lambdas. [Alexander Böhn]

* Fleshed out some sensible-default base classes in “clu.abstract” ... like there is now an intermediate ancestor of the verenable     “clu.abstract.ValueDescriptor” class called “Descriptor” that     makes use of “clu.abstract.SlottedRepr” ... which that class, “SlottedWrapper” is itself derived from the     “clu.abstract.ReprWrapper” class and uses ‘__slots__’ values     across its inheritence chain to build its instances’ reprs     through a call to “clu.repr.strfields(…)” (q.v. the latest few     patches supra.) [Alexander Böhn]

* Moving “stringify(…)” and friends from “clu.fs.misc” to “clu.repr” ... made the change across the entire project ... still have to deal with a couple of dingleberries remaining in     the “fs.misc” module – namely “wrap_value(…)”, “hoist(…)” etc. [Alexander Böhn]

* Refactored “clu.fs.misc.stringify(…)” ... it now consists of a sub-function, “strfields(…)” – and the     internal type-switch repr helper is just called “strfield(…)”. ... this will allow it to be used with the nascent abstract type,     “clu.abstract.ReprWrapper” ... also added new predicates:     • “reverse(ƒ)” » returns a lambda that returns “reversed(ƒ)”     • “rmro(cls)” » is basically “reverse(mro)”     • “ancestral(atx, cls)” » like “attr_across(atx, *rmro(cls))”     • “ancestral_union(atx, cls)” » basically this is an alias for       “uniquify(chain.from_iterable(ancestral(…)))” [Alexander Böhn]

* “clu.testing.utils.countfiles(…)” can take strings, “pathlib.Path”¬ ... or anything that is “os.fspath(¬)”-able (whereas previously it     called “target.walk()” on its primary argument, limiting its     use to “clu.fs.filesystem.Directory” instances, pretty much) [Alexander Böhn]

* Simplified that “clu.fs.filesystem.TemporaryName.write(…)” call ... using a call to “TemporaryName.parent()” ... also added None checks to “Directory.{copy_all,flatten}(…)” [Alexander Böhn]

* Swapped a manual read of a “__doc__” attr for “inspect.getdoc(…)” ... also removed a call to “ensure_path_is_valid(…)” within the     “clu.fs.filesystem” module, in favor of custom logic allowing     for idempotency (as as it was, the existing logic would fail     to write if a file existed, which why?) [Alexander Böhn]

* Changing all references to “Slotted” and the like to “clu.abstract” ... the “Slotted” metaclass and the “ValueDescriptor” read-only     property class have been relocated to “clu.abstract”; ... The export machinery was removed from “clu.abstract” – enabling     the types from that module to be used by “clu.exporting” itself ... “doctrim(…)” was also removed from “clu.exporting” – we are now     using ‘importlib.cleandoc(…)’ generally in its stead ... other assorted updates to grease the wheels of this particular     iota of progress were in fact made to shit in general, doggie. [Alexander Böhn]

* Lambda-ifying the “@cache” decorator in “clu.exporting” [Alexander Böhn]

* Using “inspect.getdoc(…)” instead of manually retrieving ‘__doc__’ [Alexander Böhn]

* Docstring manipulation fixes and touchups. [Alexander Böhn]

* Type checks in “clu.importing.SubModule.__init__(…)” [Alexander Böhn]

* Invalidating module-finder caches when unregistering a class-module. [Alexander Böhn]

* You really just can’t reuse class-module names now can you. [Alexander Böhn]

* Made “clu.importing.cache” a properly reusable decorator ... with – you guessed it dogg – a lambda-expression OH YOU KNOW ME     BY NOW OKAY. [Alexander Böhn]

* Caching with “functools.lru_cache(…)” in “create_module(…)” [Alexander Böhn]

* Relocated the “clu.importing.LoaderBase.module_repr(…)” logic ... it is now in “clu.importing.Package.__repr__(…)”, which is the     place in which it should be, considering the fact that that     “module_repr(…)” abstract method was actually depreciated at     some point during the massive amount of “importlib” API churn,     at which I mercifully came in at the very tail end when I wrote     all of this shit here doggie. [Alexander Böhn]

* Ensure module.qualname uses module.name (not ModuleClass.name) [Alexander Böhn]

* Per-app Finder subclasses are added based on installed appnames ... as opposed to previously, wherein it was depending on identity     hashes of class objects, which was fundamentally flawed as each     call to “initialize_types(…)” would always install a new Finder     subclass regardless of the appname used. [Alexander Böhn]

* Killed dead code. [Alexander Böhn]

* Simplified “clu.importing.SubModule” using new class properties. [Alexander Böhn]

* Made class-module properties name/prefix/qualname work on classes ... by moving the property methods to the MetaModule metaclass, and     then proxying property methods on the class – those that work     on the instances – to class property access ... this was in aid of furnishing an “iter_modules(…)” class method     on “clu.importing.FinderBase” which as the docstring notes is     a quote-unquote non-standard API used by the “pkgutil” module ... other support shit for “iter_modules(…)” includes a function     “clu.importing.modules_for_appname(…)” which that does pretty     much what you think it does. [Alexander Böhn]

* Ensure class-moduyles’ exporter type is properly named. [Alexander Böhn]

* Testing deferred export of a class-module attribute. [Alexander Böhn]

* Silence the GitHub security alert for Pillow. [Alexander Böhn]

* Timing and pretty-print decorator for inline test functions ... available now in “clu.testing.utils” as “@inline” ... usage example in the docstring, plus it’s been added to a bunch     of existing inline test functions. [Alexander Böhn]

* Testing module-level registry functions inline. [Alexander Böhn]

* Clarified now-module-level class-module registry functions. [Alexander Böhn]

* Moved “all_appnames()” and “all_modules()” into module-level ... and out of “clu.importing.MetaRegistry” where formerly they     were @staticmethods ... this is in an attempt to unclutter the starting namespace of     newly defined class-modules. [Alexander Böhn]

* Minor docstring manscaping. [Alexander Böhn]

* Bump version: 0.3.9 → 0.4.0. [Alexander Böhn]

* Clarified “appname” parameters ... and, may I just say: I am really, really happy with the whole     class-based module implementation that’s in “clu.importing”.     If I can just say. Yes! [Alexander Böhn]

* Docstrings, tests, nitpicks, consolidations, and such. [Alexander Böhn]

* Integrated clu.exporting with clu.importing! ... to wit: class-module subclasses get built-in Exporter instances     tied to their appname/appspace/name dotpath; ... said subclasses have a custom “@export” decorator injected into     their namespace, so like when you’re doing, like: [Alexander Böhn]

  class YoDogg(Module):

  	    @export
              def iheard(self, wat):
  	        return f"I heard {wat}"

  	    @export
  	    def youlike(self, wat):
  	        return f"that you like {wat}"

      a) the “export” thingy has been predefined for that specific
         class namespace that you are working in, in that case, and
      b) you don’t need to manually import an ExporterBase subclass,
         instantiate it, and call its “decorator()” method before
         using “export” as long as it is used *only within that class
         block*
  ... still – awesome, tho, yes? I think yes.

* Directly using “collections.abc” in “clu.typespace.namespace” [Alexander Böhn]

* Bump version: 0.3.8 → 0.3.9. [Alexander Böhn]

* Caching module specs in “clu.importing” ... this works across all “clu.importing.FinderBase” subclasses –     meaning for all defined appnames – short-circuting spec lookups     within “sys.meta_path” to the first “FinderBase” subclass when     the spec in question is in the cache. TAKE THAT, LATENCY. [Alexander Böhn]

* Killed gratuitous “chain()” in “clu.importing.ModuleBase.__dir__(…)” [Alexander Böhn]

* Clarified the “clu.importing.Package” docstring. [Alexander Böhn]

* Only split spec.name if it’s registered. [Alexander Böhn]

* Removed unused class-keyword argument check. [Alexander Böhn]

* Sorting registered appnames in “clu.importing” [Alexander Böhn]

* Removed read/write access code in “clu.importing.Registry” [Alexander Böhn]

* Disabled read/write access to the “clu.importing.Registry” data ... commented out, for now. [Alexander Böhn]

* Un-un-fixed inline test in “clu.importing” [Alexander Böhn]

* Nixed a bit of dead code. [Alexander Böhn]

* Class modules work with more than one appname ... for future generations: the bug was in the one comparison being     done in “clu.importing.FinderBase.find_spec(…)”, FYI. [Alexander Böhn]

* Mostly fixed “clu.importing.LoaderBase.module_repr(…)” [Alexander Böhn]

* A docstring for “clu.importing.Package” [Alexander Böhn]

* Class modules also inherit from “clu.importing.Package” [Alexander Böhn]

* Actually let’s do it this way instead. [Alexander Böhn]

* Ensure intermediate module instances are packages ... as in, they have a “__path__” attribute containing a list. [Alexander Böhn]

* Docstring for “clu.importing.initialize_types(…)” [Alexander Böhn]

* Testing importing a member function of a class-module. [Alexander Böhn]

* Ensure DO_NOT_INCLUDEs aren’t included in “dir(module)” [Alexander Böhn]

* Basics of “clu.importing” – class-based modules. [Alexander Böhn]

* Miscellaneous predicates I wrote in the middle of the fucking night. [Alexander Böhn]

* Inserted module-local versions of a few lambdas into “exporting” ... in the name of breaking dependency cycles that these static     type-checkers can’t reason their way around. [Alexander Böhn]

* Makefile and type-check setup tweaks. [Alexander Böhn]

* Gearing up for some basic type-checking. [Alexander Böhn]

* Catch SyntaxError as well as ImportError in “clu.constants.polyfills” [Alexander Böhn]

* Ensure the fake “lru_cache(¬)” uses a __wrapped__ attribute. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Re-implemented “clu.predicates.finditem[s?]” ... now using `searcher(…)/collator(…)` instead of `apply_to(…)` [Alexander Böhn]

* Dispatch functions in “clu.extending” can all have the same name ... fucking finally. [Alexander Böhn]

* Major tuneups in “clu.extending” including annotation support! ... also the “clu.extending.DoubleDutchRegistry” classes’ “cache”     attribute is now a real actual LRU cache (courtesy zict) and     not just a copy of the dict it was supposedly caching ... also expanded renaming support in “clu.exporting” and added a     related test or two. [Alexander Böhn]

* Full coverage for “clu.extending” in module inline tests. [Alexander Böhn]

* Updates for “clu.typology” metaclass support in “repl-bpython.py” [Alexander Böhn]

* Many additions to “clu.typology” including metaclass support ... predicates for checking metaclasses and dealing with metatype     and ABC lists ... tests for these new additions ... refinements in “clu.extending” including new greek letters! ... miscellaneous updates in accordance with this awesome new shit. [Alexander Böhn]

* OMEGA MARKS THE END (by which I mean, the “pair(…)” tests run OK!!! [Alexander Böhn]

* Changes “clu.predicates.pyname(…)” to match “determine_name(…)” ... q.v. the previous commit note supra. w/r/t the “__qualname__”     and “__name__” attributes. [Alexander Böhn]

* Exporter instances and subclasses can now be unregistered ... with tests for both that, and the new “__wrapped__”-function     awareness logic ... in doing this we had to subtlely but fundamentally alter the     logic within the verenable “clu.exporting.determine_name(…)”     function – it now privileges “__name__” over “__qualname__”     while going about its business. Tests seem to suggest this     hasn’t perturbed anything, but that function is at the heart     of the export system and so I wanted to make a note of the     change here. [Alexander Böhn]

* A list comprehension should be faster than a “list(genexp)” ... right?… [Alexander Böhn]

* Since @export handles __wrapped__ we can drop these manual exports ... also there is now a flag to make any function decorated with     @itervariadic not iterate variadically, on like a case-by-case     basis. [Alexander Böhn]

* Many rather significant updates: 1) The exporter will follow a “__wrapped__” attribute on a function    to determine its name 2) Added “clu.predicates.itervariadic(…)”, a decorator to allow a    function accepting (•args) to, when called with one iterable    argument, to expand the iterable into “•args” when appropriate    … “where appropriate” meaning it won’t do this by default on    string/bytes/file-path-like arguments. 3) Updated the “__iter__()” methods of a bunch of things across the    project to use “yield from” whenever possible, and to generally    be less circuitous 4) Speaking of “__wrapped__”, that attribute is now set by at least    one of my functional tools (I know “clu.fs.misc.wrap_value(…)”    will do it but I forget the other one or two I updated RN). 5) Made some miscellaneous refinements in “clu.extending”. 6) The rest is A SURPRISE (because I forgot already – see the diff    my fellow nerds, yes!) [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Exporting Ω(a, b) as an alias for “clu.extending.pair(…)” [Alexander Böhn]

* The inlineiest and the testiest inline tests for “clu.extending” ... also another use of module “__getattr__(…)” – this time, it’s     to initiate the… runtime adjuistment… of the testing utility     module “pout” (which was writing all its shit to `sys.stderr`     which in TextMate is this mass of godawful red text, plus I     prefer `sys.stdout` for capturing and other shit, etc etc ok     yeah OK). [Alexander Böhn]

* A little early Chanukkah present from RPython – ... check this crazy shit out; originally from here: https://bitbucket.org/pypy/pypy/src/default/rpython/tool/pairtype.py. [Alexander Böhn]

* Commenting in, commenting out. [Alexander Böhn]

* Formally requiring “pout” (for now) [Alexander Böhn]

* Ported most of the ChainMap unit tests to an inline function ... for introspectability. Strangely enough they don’t assert-fail     in that context. I am beginning to worry that I have gone and     done something very, very stupid somewhere in that testsuite… [Alexander Böhn]

* Tests of all sorts for “clu.dicts.ChainMap” [Alexander Böhn]

* I did a ChainMap. [Alexander Böhn]

* More ABC-reshuffling. [Alexander Böhn]

* Moved “clu.config.abc.ReprWrapper” around in the inheritance chain. [Alexander Böhn]

* Well pypy3 is •trying• to run the testsuite in tox. [Alexander Böhn]

* Bump version: 0.3.7 → 0.3.8. [Alexander Böhn]

* Manual version adjust. [Alexander Böhn]

* Manual version adjust. [Alexander Böhn]

* Bump version: 0.3.6 → 0.3.7. [Alexander Böhn]

* Bump version: 0.3.5 → 0.3.6. [Alexander Böhn]

* Tweaked conditional-deepcopy logic ... now it uses “getattr(…)” which readers of the CLU source – if     any exist besides myself – will note that I love that shit. [Alexander Böhn]

* Conditional deep-copying in “FlatOrderedSet”’s “clone(…)” logic. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* The “clu.config.abc.Clonable.clone(…)” method takes a “memo” param ... two birds with one abstract method, dogg. [Alexander Böhn]

* Allowing __slots__ to percolate through select class stacks. [Alexander Böhn]

* Implemented better ReprWrapper and Cloneable ABCs. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Using “clu.predicates.item_search(…)” in “clu.dicts.merge_two(…)” ... also we’re using “clu.fs.misc.typename_hexid(…)” around some of     the “clu.config” `__repr__` implementations; ... aaaaaand there are one or two new predicates in “clu.typology”. [Alexander Böhn]

* Very corner-cased OCD-y adjustment to “clu.predicates.slots_for(…)” [Alexander Böhn]

* Checking for `__mro__` internally instead of using “isclasstype(…)” [Alexander Böhn]

* AND THERE WAS MUCH NEGATION OF BOOLEAN PREDICATES. [Alexander Böhn]

* Using “clu.fs.misc.differentfile(…)” in “clu.fs.filesystem” [Alexander Böhn]

* One more teeny little refactoring in “clu.fs.misc.u8bytes(…)” [Alexander Böhn]

* Another micro-refactor in “clu.fs.misc.u8bytes(…)” [Alexander Böhn]

* Slight refactoring in “clu.fs.misc.u8bytes(…)” [Alexander Böhn]

* Rewrote and sort-of optimized “clu.fs.misc.stringify(…)” ... also did some more nitpickery with the “clu.config” ABCs and     added more miscellany in general within “clu.fs.misc” as does     befit its name. [Alexander Böhn]

* The tox settings had somehow become awry, so I un-awrized them. [Alexander Böhn]

* Bump version: 0.3.4 → 0.3.5. [Alexander Böhn]

* Moved config’s abstract bases into a new “clu.config.abc” module ... and all the myriad changes that go along with such. [Alexander Böhn]

* Some assorted housekeeping minutiae. [Alexander Böhn]

* EVERYBODY CHILL. [Alexander Böhn]

* Fixed that irritating off-by-one bug in “print_ansi_centered(…)” [Alexander Böhn]

* Easing iteration in “clu.exporting” ... using “yield from”, and ... removing gratuitous tuple-conversions. [Alexander Böhn]

* Removed wack function “predicates_for_types(…)” ... so uncivilized. [Alexander Böhn]

* Using “yield from” in “clu.exporting.ExporterBase” [Alexander Böhn]

* Using “yield from” in “clu.config.fieldtypes” [Alexander Böhn]

* Package-scoping the “clumods” fixture. [Alexander Böhn]

* Restoring entire `os.environ` mapping in “environment” test fixture. [Alexander Böhn]

* Removed empty test. [Alexander Böhn]

* Fixed “clu.config.filebase.FileBase” so file paths override searches ... previously, even specifying an explicit file path would not end     up overriding the file path search, had the file path search     found anything. [Alexander Böhn]

* “clu.fs.filesystem.Directory” is now reverse-iterable. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Further premature optimization. [Alexander Böhn]

* Hashed out gratuitous asserts in hot loop. [Alexander Böhn]

* Ensure sequence item keys are found in the directory instance. [Alexander Böhn]

* Iterating a “clu.fs.Directory” instance returns strings ... whereas before, it was returning raw DirEntry object instances,     as emitted by “os.scandir(…)” – this has been corrected. [Alexander Böhn]

* The OrderedMappingViews in “clu.dicts” implement “collections.abc.Sequence” ... and they are now well-tested. [Alexander Böhn]

* Removed “__call__(…)” stub from “clu.fs.filesystem.Directory” [Alexander Böhn]

* Trimmed dead code in “clu.fs.filesystem” [Alexander Böhn]

* Renaming the “clu.dicts” testsuite module. [Alexander Böhn]

* Fixed “len(Directory(…))” which had been infinitely recursing ... also added some useful items/keys/values-views implementations     in “clu.dicts” [Alexander Böhn]

* Starting on “clu.fs.sourcetree” module ... q.v. *.srctree files from the Cython test suite. [Alexander Böhn]

* I kind of hate “__setattr__(…)” and “__getattr__(…)” in every way. [Alexander Böhn]

* Almost there with namespaced field attribute access. [Alexander Böhn]

* Trimmed a bunch of dead code ... also wrote a docstring summarizing the “clu.naming” primary API. [Alexander Böhn]

* Halfway to namespaced field access as dotted attributes. [Alexander Böhn]

* Fixed a docstring copypasta typo. [Alexander Böhn]

* Getting rid of CLU-specific inline-test-ish code in “clu.config.filebase” [Alexander Böhn]

* Ensure sys.path entries pointing to files aren’t made into Directories. [Alexander Böhn]

* Clarified the parent module of “remove_invalid_paths(…)” [Alexander Böhn]

* Changing the PyYAML requirememt to tox-only ... also got rid of some unnecessary DepreciationWarning supressors. [Alexander Böhn]

* Bump version: 0.3.3 → 0.3.4. [Alexander Böhn]

* Requiring PyYAML. [Alexander Böhn]

* Bump version: 0.3.2 → 0.3.3. [Alexander Böhn]

* Including TOML files in MANIFEST.in. [Alexander Böhn]

* Bump version: 0.3.1 → 0.3.2. [Alexander Böhn]

* Bugfixes in “clu.config” – ... better None-checks in “clu.config.env” ... force-stringify arg in “clu.confiig.settings.Schema.nestify(…)” ... check type before length in “clu.config.fieldtypes.StringField” ... many updates and tweaks to the “clu.fs.appdirectories” module ... testing package EnvBase subclasses and custom schema classes     in “test_config.py” ... miscellaneous changes to support all of the above shit. [Alexander Böhn]

* A large miscellany-roundup push, featuring: ... correct-er (i.e. more like the builtin) “update(…)” method’s     logic, w/r/t iterable arguments; ... correct-er (i.e. not inconsistent) argument passing/checking in     several of the “clu.config.fieldtypes.fields”; ... updates to “clu.config.filebase.FileName” allowing config files     to optionally be located and used from “sys.path” directories ... fixes to the aforementioned “clu.config.filebase.FileName” to     decouple it from CLU’s app name – config files should all now     defer to the “clu.config.filebase.FileBase” respective subclass     name information, across the board; ... Lots of docstring tweaks, corrections, and OCD-ish updates; ... The initialization logic of “clu.config.settings.Schema” now     takes place in “__new__(…)” rather than “__init__(…)” – this     lets subclassers forego calling up to the superclass if they     define an “__init__(…)” and clearly separates the concerns; ... Some minor nitpicky updates to the way that the aforementioned     “clu.config.settings.Schema” stringification methods work; ... Calling “clu.config.settings.Schema.validate()” returns True     if all goes well… this may or may not be gratuitous as it’ll     never return False – if validation goes awry at any point the     call to “validate()” raises a ValidationError; ... The possible “replaceable endings” in “clu.exporting” are     as automatically-generated as possible, and more comprehensive     like in general; and finally ... the exporter tests now correctly locate, import, and examine     the “yodogg” testing module’s exporter subclasses. [Alexander Böhn]

* WHOOOOPS. [Alexander Böhn]

* Fixing “clu.config.fieldtypes.TupleField” [Alexander Böhn]

* Removed “default” params from NamespacedFieldManager methods. [Alexander Böhn]

* Trimmed a whoooooole lot of dead code. [Alexander Böhn]

* Fixed container field types ... it wasn’t a pretty fix – it involves manually calling a field’s     “__set_name__(…)” method – but it works. Blech! [Alexander Böhn]

* Moved file-format-related config stuff into “clu.config.formats” [Alexander Böhn]

* I feel docstring, oh so docstring – [Alexander Böhn]

* Docstrings for “clu.config.settings.Schema” [Alexander Böhn]

* Dead code trim, simplifications, greater helpfulness in exceptions… [Alexander Böhn]

* These tests, they are a-pass-in’ [Alexander Böhn]

* Beginnigs of __repr__ logic for “clu.config.base.{Flat,Nested}” ... also fixes ensuring “clu.dicts.merge_two(…)” will actually work. [Alexander Böhn]

* More wide-ranging updates to the “clu.config” machinery ... Added a “clone()” method! ... Fixed “clu.dicts.merge_two(…)” to be properly generic, and thus     support these new mapping types! ... cleaned the dead code out of “clu.config.tomlfile”! ... AND MORE!!!! [Alexander Böhn]

* Had to rename “clu.config.toml” as “clu.config.tomlfile” ... to avoid confusing `import` – like it was somehow doing py2-ish     implict relative imports, “import toml” from within the file     that defined “clu.config.toml” would yield “clu.config.toml” –     what the fuuuuuuuuuuuck? So I changed it. [Alexander Böhn]

* Many updates to “clu.config” … ... docstrings abound! ... fixes for the “clu.config.base.Flat.{keys,values}(…)” methods! ... “Flat.nestify(…)” and “Nested.flatten(…)” allow reformatting     namespaced-dictionary data losslessly between internal formats! ... Expanded the “find_file(…)” method and moved it and its many     helper class-methods from “clu.config.filebase.FileBase” up to     “clu.config.filebase.FileName” – the key difference being that     the latter is a mixin class and can be reused outside of the     FileBase implementation(s)! ... Most of the intermediate file-finding-related methods can take     either additional or overriding parameters which will be great     for testing!! ... other miscellaneous shit I am sure!!! [Alexander Böhn]

* Self-test introspection for the “clu.config.toml” module. [Alexander Böhn]

* Getting ever-closer – adding “clu.config.toml” [Alexander Böhn]

* Continuing apace on “clu.config.filebase” [Alexander Böhn]

* Fleshing out “clu.config.base”; staring on “clu.config.filebase” [Alexander Böhn]

* Start of the “clu.config” module. [Alexander Böhn]

* Moved a few enum-alias-related predicates into “clu.typology” [Alexander Böhn]

* First stab at slash-operators for Directory filesystem types. [Alexander Böhn]

* Trying to get the PyPy testenv to actually use PyPy, like it used to. [Alexander Böhn]

* Bump version: 0.3.0 → 0.3.1. [Alexander Böhn]

* Some tox.ini adjustments. [Alexander Böhn]

* Raising when calling “flatten(…)” on a nonexistant Directory. [Alexander Böhn]

* Confirming the new script directory location in the testsuite. [Alexander Böhn]

* Tweaks to the new display capacities of the “show-modules.py” script. [Alexander Böhn]

* Removed unused import. [Alexander Böhn]

* The “show-modules.py” script actually shows all the modules. [Alexander Böhn]

* Vendoring in a “columnize” implementation ... courtesy https://github.com/rocky/pycolumnize. [Alexander Böhn]

* Updating the hardcoded module list. [Alexander Böhn]

* Bump version: 0.2.10 → 0.3.0. [Alexander Böhn]

* Test for “clu.fs.filesystem.script_path(…)” no longer xfails. [Alexander Böhn]

* Bump version: 0.2.9 → 0.2.10. [Alexander Böhn]

* Moved “scripts” directory into the CLU module base proper. [Alexander Böhn]

* F-strings in “clu/__init__.py. [Alexander Böhn]

* Bump version: 0.2.8 → 0.2.9. [Alexander Böhn]

* Stubbing out migration methods in “clu.keyvalue.CLUInterface” [Alexander Böhn]

* Enabled versioning by default in “clu.keyvalue.interface” [Alexander Böhn]

* Installing CSV-related lambdas from an earlier CLU iteration. [Alexander Böhn]

* Commented out hardcoded length-check lines in exporter tests. [Alexander Böhn]

* “weakref.WeakValueDictionary” is the new “collections.OrderedDict” ... as far as the “clu.fs.filesystem.TypeLocker” internal registry     is concerned at least doggie. [Alexander Böhn]

* Revised the “clu.fs.filesystem.TypeLocker” registry metaclass ... got rid of the “__prepare__(…)” method that just returned an     `OrderedDict` – it’s 2019 and our Python 3.7 dicts are more     ordered than `OrderedDict` (and also less janky in the repr). ... Properly assign “__name__” and “__qualname__” – and also our     own “__lambda_name__” – to each lazy-static “directory(…)”     method that TypeLocker creates, using the same semantics and     logic as “clu.exporting.ExporterBase.export(…)” ... Updated docstrings and nota-benne comments therein ... Also threw in some filesystem-module tests updates and other     assorted miscellany. [Alexander Böhn]

* Renamed “suffix(…)” to “re_suffix(…)” to clarify things. [Alexander Böhn]

* Assorted touchups in “clu.exporting” ... to wit:     a) made ValueDescriptor a proper data descriptor (if read-only)     b) made both “__class_getitem__(…)” calls throw the same sorts        of exceptions if they are passed the wrong shit     c) added a proxied “clu.exporting.ExporterBase.items()” method     d) something else nifty that I can’t remember just now, oh well. [Alexander Böhn]

* Reshuffle ... WHOOOOOOOOOOOPS. [Alexander Böhn]

* Including “.pyc” files in package index suffixes. [Alexander Böhn]

* Module-file suffixes for “path_to_dotpath(…)” come from “importlib” [Alexander Böhn]

* Stacking exports atop lru_cache decorators in “clu.fs.misc” [Alexander Böhn]

* Lowercasing all suffixes before comparison. [Alexander Böhn]

* Limiting function cache size on regex match/search functions. [Alexander Böhn]

* Caching “clu.fs.misc.re_{matcher,searcher}” functions ... using default-value “functools.lru_cache(…)” RN. [Alexander Böhn]

* Nitpick on the variable name inside the returned lambda ... within “clu.fs.misc.re_{matcher,searcher}” – it has, up to this     point, been `searching_for`, which is wrong as this variable     contains the string that itself is being searched; truncating     the name to `searching` satisfies my OCD in this case (read it     and you’ll see if you find this summary confusing, tensewise). [Alexander Böhn]

* Un-exporting two module constants in “clu.repl.banners” [Alexander Böhn]

* Un-exporting two module constants in “clu.enums” [Alexander Böhn]

* Un-exporting two module constants in “clu.fs.filesystem” ... get that comparison failure rate down doggie. [Alexander Böhn]

* Generalizing “clu.fs.misc.suffix_searcher(…)” [Alexander Böhn]

* Using “clu.fs.misc.gethomedir()” in “AppDirs” tests. [Alexander Böhn]

* Using new export “clu.fs.misc.gethomedir()” in the filesystem code. [Alexander Böhn]

* Nota benne. [Alexander Böhn]

* Moved one-off “gethomedir()” lambda to “clu.fs.misc” ... and exported it from there with a docstring and everything. [Alexander Böhn]

* Refactored the “clu.fs.filesystem.rm_rf(…)” test with “countfiles(…)” [Alexander Böhn]

* Passing through “parent” in the “temporaryname” fixture factory. [Alexander Böhn]

* Error-checking in “clu.fs.filesystem.TemporaryName.filesize(…)” [Alexander Böhn]

* Test fixture manscaping. [Alexander Böhn]

* One more “pth” → “path” changeover. [Alexander Böhn]

* Starting to normalize the argument names in “clu.fs.filesystem” ... tests still pass, so far…¬ [Alexander Böhn]

* Prevent leakage from the “clu.fs.filesystem.TypeLocker” metalclass ... specifically, all classes for which TypeLocker was their meta     – we still need a good word for that – would receive a “types”     attribute that was a reference to an OrderedDict full of all     of those classes, as kept internally by TypeLocker for its own     housekeeping purposes. That was a downside of its use, as this     attribute was kind of hanging out in the open, using a fairly     common name with no underscore-prefixing (something I kind of     loathe, personally, but that’s me) or other indication of what     it was or what it was for or how shit could break if it were     to be improperly fucked with. ... This solves the problem by overshadowing the “types” attribute     with a read-only “clu.exporting.ValueDescriptor” instance on     all generated classes. [Alexander Böhn]

* Bump version: 0.2.7 → 0.2.8. [Alexander Böhn]

* Rewrote “ls(…)” and “ls_la(…)” from “clu.fs.filesystem.Directory” ... to use the new less-cumbersomely-verbose modes of dealing with     “clu.fs.misc.suffix_searcher(…)” [Alexander Böhn]

* Rewrote a lot of “clu.fs.filesystem.Directory.flatten(…)” ... as well as rewrites in “clu.fs.misc.suffix_searcher(…)” and     “clu.testing.utils.countfiles(…)” – the latter of which now     also takes a “suffix” argument to only count files matching     a specific suffix, like duh ... expanded the “flatten(…)” method tests to cover all the new     combos of using the suffix-related arguments and double-checked     the output of everything and whatnot ... ALSO FIXED MANY BUUUUUUUGGS. [Alexander Böhn]

* Exporter checks in “clu.testing.pytest.clumods” and “show-modules.py” ... beforehand, there was a hardcoded list of “CLU modules” in a     static tuple in “clu.constants.data” which really was a list     of modules in CLU that used the “clu.exporting.Exporter” class     to export their shit. ... now there still is; the difference is that that tuple can now     contain any valid module in CLU and the two places where the     tuple gets iterated also check to see if the module they’re     exporting contains an exporter – if it doesn’t, whatever that     bit of code returns won’t contain said module ... clearly this is a janky system but we currently need it to     test that the Exporter registration system works in the first     place; it could get pared down to like only being used in one     or two instances, I feel like. [Alexander Böhn]

* Changed “followlinks=True” in “Directory.walk(…)” arguments ... plus some random updates and minutiae in “clu.fs.filesystem”     and “clu.testing.utils” [Alexander Böhn]

* Confirming the counts of the flattened directory contents ... using a “countfiles(…)” function, which in itself isn’t really     any type of anything – but its existence did necessitate the     creation of a new “clu.testing.utils” module. [Alexander Böhn]

* Bump version: 0.2.6 → 0.2.7. [Alexander Böhn]

* I think it’s irritating how .jpg and .jpeg are valid JPEG suffixes. [Alexander Böhn]

* Bump version: 0.2.5 → 0.2.6. [Alexander Böhn]

* We now have a “Directory.flatten(…)” instance method ... plus a working test stub, plus helper methods (one of which let     us rewrite some of “Directory.zip_archive(…)” to omit inlining     the “relparent(…)” lambda). I wrote all of this up at the bar     while standing up and drinking whiskey talking intermittently     to other patrons so I am calling this effort NOT BAD AT ALL. [Alexander Böhn]

* Makefile rules for running pytest and tox ... I mean, it’s cool and all that the pytest fixture stuff is now     a “plugin” module, with a setuptools endpoint and shit, instead     of just a conftest.py file (which was working just fine by the     way) but pytest, while a nice program and all, completely loses     its fucking shit completely under certain conditions – one of     which is, if somewhere or somehow during its utterly Byzantine     loading/discovery/setup/config phase it is told to load one of     these “plugin” modules more more than exactly once, it crashes     like a fucking trainwreck and spews out what has to literally     be the largest and most illegible traceback I have ever seen     (and I worked with JSP and Servlets 1.0 in the fucking late     1990s). ... Anyway. So pytest isn’t all that bad aside from one or two of     these occasional supernova-class exception belches every so     often – once I sifted through the wreckage for the offending     file I found the answer reading the pytest code, which was     completely decent: legible, full of well-written comments     and docstrings; aside from the plague of leading underscores     that infects a lot of Pythonilinguists I thought it was great.     So yeah I read it, figured out the fix (which itself wasn’t     anything too nasty or circuitous) and that’s that. ... So yeah that’s the reason for this long-winded commit note:     it’s so easy to talk shit about code and be like MOTHERFUCKER     WHAT IN THE NAME OF LOVECRAFTIAN TWAT IS THIS AWFULNESS, WHO     EVEN THINKS LIKE THAT and soforth; but so it’s necessary to     point out when shit is not bad, and especially when shit is     in fact somehow good. So yeah GOOD ON YOU, PYTEST, YOU GET     A COOKIE!!! Indeed. [Alexander Böhn]

* The “clu.fs.filesystem.script_path()” function is poorly behaved ... particularly in normal sdist installs. Its test code has been     branded with the shameful and dreaded X-FAIL for the moment. [Alexander Böhn]

* Bump version: 0.2.4 → 0.2.5. [Alexander Böhn]

* Getting rid of root-level conftest.py, in favor of “clu.testing” [Alexander Böhn]

* A docstring! A docstring for this function straight away!!! ... if you say it in like a King Arthur voice it’s kinda funny. [Alexander Böhn]

* This is evidently how console-script endpoints should work. [Alexander Böhn]

* Bump version: 0.2.3 → 0.2.4. [Alexander Böhn]

* Made the stupid little version-string script a setuptools entrypoint. [Alexander Böhn]

* Bump version: 0.2.2 → 0.2.3. [Alexander Böhn]

* Moving the pytest fixtures that use CLU formally into the project. [Alexander Böhn]

* Bump version: 0.2.1 → 0.2.2. [Alexander Böhn]

* Fixed unlabeled keyword arg “default” in “slots_for(…)” internals. [Alexander Böhn]

* Tweaked and wrote tests for “clu.predicates.slots_for(…)” [Alexander Böhn]

* New accessors in “clu.predicates” using “inspect.getattr_static(…)” ... Which that function, “getattr_static(…)” retrieves attributes     from things without setting off any of the “__getattr__(…)” or     “__getattribute__(…)” logic insanity; this means that calling     it (or any of my new and improved accessors based on it!!) will     get you, like, e.g. a descriptor instance instead of to whatever     the call to that instances’ “__get__(…)” method would’ve lead. ... So the new predicate attribute getter function things are all     named “stattr(…)”, “stattrs(…)” – just like the versions sans     the “st” prefixes (which it’s “st” for “static”, get it??) only     the underlying calls use “getattr_static(…)” instead of calling     “resolve(…)”… which calls “or_none(…)” which calls “getattr(…)”     which calls a bajillion descriptor/class-dict/instance-dict/mro     thingamabobs about whose inner workings I am always a bit hazy. ... SO YEAH ENJOY. Also I wrote tests for these, plus I simplified     “getitem(…)” and also gave “clu.exporting.ValueDescriptor” a     real “__repr__(…)” function for some reason. Yup. [Alexander Böhn]

* Bump version: 0.2.0 → 0.2.1. [Alexander Böhn]

* Made the “clu.typespace.namespace.SimpleNamespace” type “hashable” [Alexander Böhn]

* Bump version: 0.1.9 → 0.2.0. [Alexander Böhn]

* Clarified the “clu.naming.moduleof(…)” docstring. [Alexander Böhn]

* Ensured “determine_module(…)” will return any specified default value. [Alexander Böhn]

* Clarified the “clu.naming.nameof(…)” docstring. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Bump version: 0.1.8 → 0.1.9. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Made “clu.naming.{name,module}of(…)” truly universal ... to wit: they now search over the space of *all* registered     instances of *all* registered subclasses of the base class     “clu.exporting.ExporterBase” ... the logic is this:     1) First, try the instances’ attributes (either “__qualname__”        or “__name__”, or either “__module__” or “__package__”,        depending on what we’re doing).     2) Failing that, look up the name with each “ExporterBase”        subclass in the registry, using ‘ExporterSubclass.nameof(…)’        or ‘ExporterSubclass.moduleof(…)’, depending.     3) If the instance isn’t found in any registered subclasses’        instance registry, try searching the system-wide module        space using “clu.exporting.search_for_{name,module}(…)”     4) For module searches only, try one last search using the        “pickle.whichmodule(…)” function before giving up. ... and you know, all tests pass – so fuck yes! [Alexander Böhn]

* Loading the “{attr,pyattr,item}_across(…)” predicates in the REPL. [Alexander Böhn]

* Fixed prefix in “yodogg” embedded test package. [Alexander Böhn]

* Filtering out class-registry function names in “ExporterBase.__dir__(…)” [Alexander Böhn]

* A little DRY in “clu.exporting” [Alexander Böhn]

* Object-identity comparisons in registered items work in tests. [Alexander Böhn]

* Some cheeky-ass motherfucking shit here. [Alexander Böhn]

* Made “path” a first-class keyword arg of “clu.exporting.ExportBase” [Alexander Böhn]

* Fixed a bug in “clu.fs.pypath.remove_paths(…)” and added some stuff ... namely “clu.fs.pypath.remove_invalid_paths(…)”, which removes     anything in “sys.path” that doesn’t point anywhere; ... also added a module-private function “mutate_syspath(…)” used     in both “remove_paths(…)” and “remove_invalid_paths(…)” to     change the “sys.path” list in-place without randomly reordering     it at the time. ... the new function is imported into the REPL environment and also     called before the interactive interpreter starts, ensuring that     the REPL environments’ “sys.path” is not bullshit in any way. [Alexander Böhn]

* Using “clu.naming.nameof(…)” instead of “clu.exporting.determine_name(…)” ... in “clu.typespace.namespace” [Alexander Böhn]

* One more assert in the ExporterBase subclass test. [Alexander Böhn]

* Extraordinarily minor tweak to docstring. [Alexander Böhn]

* Tweaked custom-subclass Exporter test. [Alexander Böhn]

* Simplified class-keyword logic in “ExporterBase” metaclasses. [Alexander Böhn]

* Avoiding namespace clash with “appnames” method and module-level set instance. [Alexander Böhn]

* Generalized “clu.exporting.PrefixDescriptor” as “ValueDescriptor” [Alexander Böhn]

* Class registry for ExporterBase derived types added. [Alexander Böhn]

* Split up ExportBase’s metaclass into “Slotted” and “Prefix” [Alexander Böhn]

* OCD-ish tweak to “clu.exporting.Prefix.__new__(…)” [Alexander Böhn]

* Moved PrefixDescriptor definition out of Prefix.__new__(…) [Alexander Böhn]

* Say that the new class will be slotted in the “__new__” docstring. [Alexander Böhn]

* Rewrote the “basepath” stuff in “clu.exporting.Exporter” ... using metaclasses. Now users of CLU can use the exporting stuff     by creating a trivial subclass of “clu.exporting.ExporterBase”     like so: [Alexander Böhn]

  class MyExporter(clu.exporting.ExporterBase,
  			 prefix="/my/prefix"):
  	    pass

      … so easy, like taking candy from a baby (but far less cruel
      and sadistic). Yes!

* ALWAYS DOUBLE-CHECK YOUR PROJECT-WIDE FIND-AND-REPLACE RESULTS ... there can be bogus side-effects that are silly at best (like     this one) and devastating at worst – I am sure each and every     one of you knows personally what I am talking about exactly.     Yep. [Alexander Böhn]

* Renamed all those “thingname_xxx(…)” functions in “clu.exporting” ... also refined “clu.naming.{nameof,moduleof}” – coronating them     as the new top-level user-facing interface to finding out what     the fuck are the names for shit. Use of “determine_name(…)” was     getting a bit creaky – that function was originally written as     module-private, for use in the Exporter internals; now, it can     basically keep that role (with a few reasonable exceptions) and     “nameof(…)” and “moduleof(…)” can take over everywhere outside     of the CLU exporting and name-discovery module internal code. ... Yes! [Alexander Böhn]

* “nameof(…)” is a real func instead of a “determine_name(…)” wrapper ... this involved:     a) Moving *all* the module-search stuff out of “clu.naming” and        into “clu.exporting”;     b) Implementing module-search functions within exported modules        as “Exporter.nameof(…)” and “Exporter.moduleof(…)” – using        the generic “thingname(…)” function brought over from the        “clu.naming” module;     c) Rewiring “clu.naming.nameof(…)”, and its now-irritatingly        incongruently-named cousin “clu.naming.determine_module(…)”        to 1) first attempt attribute access, falling back on 2)        the new “Exporter” class methods before 3) resorting to        “determine_name(…)” or “thingname_search_by_id(…)” (which,        at that point, will basically both do the same system-wide        module search) – with “determine_module(…)” additionally        trying to delegate out to “pickle.whichmodule(…)” before        giving up entirely;     d) Splitting dotpath elements in “nameof(…)” in case the        final result ends up being an unwieldy qualified name     e) Updating all the imports and exports and et cetera. [Alexander Böhn]

* More relativity. [Alexander Böhn]

* Relative-izing “path_to_dotpath(…)” to keep it non-CLU-specific. [Alexander Böhn]

* Fixed typo in requirements/dev.txt. [Alexander Böhn]

* Fleshed out the “dev” requirements. [Alexander Böhn]

* Removed irritating Makefile rule to clean up after pytest ... having already dealt with this with fixtures. [Alexander Böhn]

* Cleaned up tox.ini. [Alexander Böhn]

* Bump version: 0.1.7 → 0.1.8. [Alexander Böhn]

* Split off testing requirements into tox.txt. [Alexander Böhn]

* Requiring docopt in requirements/install.txt. [Alexander Böhn]

* I HATE VIRTUALENVS. [Alexander Böhn]

* Tweaking the REPL boostrap script. [Alexander Böhn]

* Shuffled imports in module naming test. [Alexander Böhn]

* Resolved double-export situation with SimpleNamespace and Namespace. [Alexander Böhn]

* Laid down a few pytest markers. [Alexander Böhn]

* Removed “Nondeterminism(…)” exception toss in naming test. [Alexander Böhn]

* Removing the last vestiges of the old xfail constants naming test. [Alexander Böhn]

* EXECUTIVE CALL: you have to import from “clu.constants” subpackages ... MEANING: you can’t do this shit anymore: [Alexander Böhn]

  from clu.constants import DEBUG, FilesystemError

  ... RATHER: you have to specify the subpackage:

      	from clu.constants.consts import DEBUG
  	from clu.constants.exceptions import FilesystemError

  ... if that is annoying well TOO BAD. The source of a certain kind
      of nondeterminism in like e.g. “clu.naming.determine_module(…)”
      was the fact that these constants (it was always the constants,
      as they never have “__module__” or “__package__” properties)
      could be found by functions like “thingname_search_by_id(…)” in
      TWO SEPARATE AND DISTINCT PLACES. The nondeterminism comes from
      that, plus the fact that the module-load order (and thus, the
      natural-sort order of “sys.modules”) is itself nondeterministic
      fundamentally.

* Reshuffled the stuff in conftest.py. [Alexander Böhn]

* Moved list of XDG environment variables into “clu.constants.data” [Alexander Böhn]

* Repaired and updated the “determine_module(…)” test. [Alexander Böhn]

* It looks like this may solve the “xfail” naming test issue… [Alexander Böhn]

* Normalized the arguments for “clu.naming.nameof(…)” [Alexander Böhn]

* Class methods on “clu.exporting.Exporter” to retrieve modules ... So there are two new class methods:     1) Exporter.modulenames() → returns a list of the names of the        Exporter instances in the registry – whose names are those        of the module in which they’re ensconced; e.g. 'clu.enums',        'clu.fs.filesystem', etc.     2) Exporter.modules() → returns a dict keyed with the names        from “Exporter.modulenames()” and populated with the actual        modules these dotted paths indicate; this is done internally        with “importlib.import_module(…)”. [Alexander Böhn]

* Converted an outlying ‘%’-style format string to an f-string. [Alexander Böhn]

* Exporting “clu.repl.ansi.evict_announcer(…)” in all the right places. [Alexander Böhn]

* Bump version: 0.1.6 → 0.1.7. [Alexander Böhn]

* Tests for “clu.exporting.Exporter” instance registry. [Alexander Böhn]

* If a module wasn’t using the Exporter just then, it is now. [Alexander Böhn]

* Instance registry for all “clu.exporting.Exporter” objects. [Alexander Böhn]

* REPL script updates. [Alexander Böhn]

* Combined “path_to_dotpath(…)” and “dotpath_to_prefix(…)” ... and what do we get? why, “path_to_prefix(…)” of course, you     doofus goober! ... threw in some quick addenda to the “dotpath_to_prefix(…)” test     function to test this new shortcut. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* F-STRINGS!!! F-STRINGS!!!!!!!!! F-STRINGS!!!!!!!!!!!!!! [Alexander Böhn]

* Rewrote “clu.predicates.getitem(…)” to not use a ‘get()’ function ... now it sticks to basic “__getitem__(…)” and “__contains__(…)”     calls, which are fine ... also: started generally replacing the string-interpolate ‘%’     operator with f-strings (yay!!!!!) [Alexander Böhn]

* That empty-string default to “getattr(…)” was bugging me ... in “clu.exporting.Exporter.export(…)”, so I changed it up. [Alexander Böhn]

* Streamlining in the “clu.exporting.Exporter” initializer. [Alexander Böhn]

* Realigning “clu.exporting.Exporter” logic. [Alexander Böhn]

* Allow easy access to a Partial’s function and predicate arguments ... that is, “clu.predicates.Partial”, our custom module-local     subclass of “functools.partial” that we use with “apply_to(…)” ... this “Partial” class is only ever returned from “apply_to(…)”;     as such, we can kit it out for that purpose – as in this case,     where we’ve added some properties for accessing the “function”     and “predicate” arguments that were used to initialize this     Partial instance. [Alexander Böhn]

* Ensure that copy operations in “clu.fs.filesystem” return booleans. [Alexander Böhn]

* Further simplifying the sequence predicates of “clu.typology” ... instead of manually checking the sequence argument in a lambda     definition, we make all of the simple sequence predicates the     partial-application result of “predicate_all(predicate)” which     basically delegates the sequence argument handling to the     “apply_to(…)” internals, which are like way more considerate     than any ad-hoc stuff could possibly manage to be ... still, also added “isxtypelist(…)” intermediate (even though     there was only one sequence-predicate corner-case that used a     call to “istypelist(…)” rather than “issequence(…)” and that     has since been redefined using the “predicate_all(…)” trick     mentioned above, it’s helpful to look at if you’re thinking     about doing something of that sort ... Yeah! Basically. [Alexander Böhn]

* Using an intermediate predicate to simplify the sequence predicates ... that are found in “clu.typology” ... added a “xlist(predicate, thinglist)” lambda, which basically     is a shortcut for: [Alexander Böhn]

  issequence(thinglist) and predicate_all(predicate, thinglist)

      … which was getting to be a boilerplate-y repetetive refrain in
      all of those “clu.typology” sequence predicates
  ... used this new intermediate in “clu.mathematics” just basically
      to like kick the tires and soforth

* Simplified “lambda_repr(…)” definition in clu.predicates ... the “pyname(…)” shortcut lambda had been defined, like, a mere     eleven LoC north of the offending definition… how embarrasing. [Alexander Böhn]

* Simplified the “predicate_none” test predicate. [Alexander Böhn]

* Importing “operator” in reply-bpython.py. [Alexander Böhn]

* Updated “clu.typology” testsuite function name. [Alexander Böhn]

* Fixed test function name, which was wrong, and needed fixing. [Alexander Böhn]

* Updated some filesystem tests to use the “temporarydir” fixture. [Alexander Böhn]

* Moved the huge greek-text dict to new module “clu.constants.data” ... Which OK yeah I know “data” is a lame-ass name for a module or     anything like that – technically they *all* contain data so it     is not that descriptive – but I wanted a catch-all junk-drawer     module, and so. Yes! [Alexander Böhn]

* Removed dangling import. [Alexander Böhn]

* Trying package scope for the “dirname” fixture ... the latest pytest docs call package-scope “experimental” – so     that’s what this is: like that time you drunkenly made out with     your sophomore-year roommate and then never really talked about     it afterward for like twenty years, I am “experimenting”. [Alexander Böhn]

* Split the “datadir” fixture into two fixtures, one module-scoped ... this way a) you can just get the "test/data" path wrapped in     a Directory instance, if you like, and b) that part of all the     fixture code only runs once per module, which that in theory     might be vaguely faster, one day. [Alexander Böhn]

* Sometimes you have to just do it yourself to do it right ... I mean, no offense to the pytest-datadir author(s), or to the     people behind pytest itself – but what the fuck, the datadir     plugin has, you know, ONE JOB: mirror a data directory for use     at test-function scope. And I mean, it was technically doing     that job – but that’s all it was doing; its usage was causing     copies of the mirrored directory contents to unceremoniously     pile up in a $TMPDIR subfolder (hithertofore unknown to me)     called “pytest-of-fish” (because that’s my local username, OK,     “fish”)… like one copy every time the fucking testsuite ran.     There are like a nontrivial stash of test images in there right     now (and that is just like off the bat, it would only have gone     up) and I was only using the fixture in like ONE fucking test,     imagine had I been more zealous. ... So OK whatever, like I am sure all the other pytest programmers     and plugin developers all have gigantic SANs and redundant SSDs     in the biggest and storage-capacity-est laptops money can buy,     or someshit – I do not, and after dealing with multitudinous     secret stashes like e.g. “.pytest_cache” and “.tox” and others,     I was not expecting this last heap of data to show up where it     did, grow with reckless abandon until “rm -rf”-ed, without any     further explanation. ... So! I looked at the fucking plugin and it was like 20 lines of     code, in three fixture functions. I copypasta’ed it into clu’s     “conftest.py” file, commented it (which like expanded its LoC     count by at least 2.5x) and then wrote a new fixture that did     what the original code was supposed to do – only a) correctly,     b) using my own filesystem abstractions, which are fairly more     featureful in a bunch of ways than “pathlib.Path” or othershit     … «BRAGGGGG» yes erm ok – but and then c) using `yield` and     managed context and assertions, because who the fuck wrote this     original shit anyway?? I am sorry guys but your thing had ONE     FUCKING JOB and while it technically did do this (like, without     shooting uncaught exceptions everywhere or trashing my files,     I guess) IT SUCKED. My shit rules, because it works, it’s     legible, it’s commented and be-docstring’d and on GitHub – any     one can use it of course – and it doesn’t have the ridiculous     overblown sense of purpose to be like a whole plugin package     and shit. YOURE JUST ANOTHER PART OF ME!! oh wait I shouldn’t     be quoting that guy these days, how uncouth, sorry about that. [Alexander Böhn]

* Replaced “allof(…)” helper with “and” operator expressions ... the problem with using “allof(…)” within functional-style     compositions is that it does not short-circuit, so you can’t     really use it in situations like: [Alexander Böhn]

  yodogg = lambda a, b: allof(isiterable(a),
  				    isiterable(b),
  				    set(a).issuperset(set(b)))

      … which that looks like it might work, but if either “a” or “b”
      is actually not iterable – that is to say, one of the first two
      predicates being fed to “allof(…)” evaluates to False – then
      the last expression throws a TypeError at the point where it
      attempts to initialize a `set` with something non-iterable.

      … This lambda should be rewritten like this:

          yodogg = lambda a, b: isiterable(a) and \
  	       	 	      isiterable(b) and \
  			      set(a).issuperset(set(b))

      … Notice how all it takes is a backslash and some indentation
      here and there, and no one has to gripe about “waaaah Python
      lambdas’re only one line, whyyyyyy” or such shit. Yeah so the
      2nd form of the lambda works if you call “yodogg(None, None)” –
      that is, assuming returing False from such a call is within the
      definition of “works”. Frankly if you *want* exceptions (which
      generally I don’t, for normal operations) that is one case in
      which lambdas will definitely not assuage your issues, as you
      can’t really backslash your way through try/except blocks, I
      don’t think. Yep.
  ... Also in this commit: some miscellaneous import-juggling

* Minor simplification in the clu.exporting.Exporter constructor. [Alexander Böhn]

* Whitespace OCD. [Alexander Böhn]

* Simplified some of the collator tests’ assertions. [Alexander Böhn]

* Renamed “collator” to “acquirer” and rewrote “collator” ... as always this is all found in clu.predicates, my favorite     module these days ... “collator” better refered to the operation that got all of the     occurrences of something* across all of a list of things (as it     is now), rather than the operation to get each occurrence of     many somethings from a single thing (which is what “acquirer”     now does); I like these names better as they are more apropos,     what do you think? [Alexander Böhn]

* Got rid of “unicode” usage in clu.predicates. [Alexander Böhn]

* Exporting some oddly un-exported typelists from clu.typology. [Alexander Böhn]

* Test for “isunique(…)” and “samelength(…)” of clu.typology. [Alexander Böhn]

* I dunno dogg it just reads better this way I think. [Alexander Böhn]

* Rewrote “isunique(¬)” and added “samelength(¬)” in clu.typology. [Alexander Böhn]

* Import ordering OCD. [Alexander Böhn]

* Expanded “apply_to(…)” test to include exception-raising. [Alexander Böhn]

* Amended test function name. [Alexander Böhn]

* Tests for “subclasscheck(…)” and sundry callable-related predicates ... all from clu.typology, in the new typology test suite. [Alexander Böhn]

* Formatting and whitespace. [Alexander Böhn]

* Removed unnecessary call to “maketypelist(…)” in “subclasscheck(…)” ... that would be in clu.typology – in the function definition that     is arguably the backbone of that whole module, actually. [Alexander Böhn]

* Finally, started a testcase suite for clu.typology. [Alexander Böhn]

* Trepidaciously starting to use “functools.wraps(…)” in “negate(…)” ... I can’t seem to get it to NOT update the function signature,     as is displayed in e.g. bpython above the display of inline     __doc__ strings …!? [Alexander Böhn]

* Expanded classtype predicates test to cover “metaclass(…)” [Alexander Böhn]

* Fixed a docstring that was showing the wrong arity. [Alexander Böhn]

* Made “isfunction(…)” – née “ΛΛ(…)” – not use “callable(…)” [Alexander Böhn]

* Using an empty tuple as the collator’s default return value. [Alexander Böhn]

* Exporting “collator(…)” from clu.predicates. [Alexander Böhn]

* Using new collation accessor to build typelists in clu.typology. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Fixed SUNDER and DUNDER in clu.enums. [Alexander Böhn]

  Whoooooooooops

* Updated an old source notation in clu.typology. [Alexander Böhn]

* Swiped dotpath-attribute resolution function snipped from stdlib ... AND IT JUST WORKS. Tests just pass, everything is just fine.     HOW IS THAT POSSIBLE… I am suspicious of course but if that     were to be that, how awesome would that be??? Here’s the orig: [Alexander Böhn]

  https://docs.python.org/3/library/operator.html#operator.attrgetter

  ... YEAH!!!

* Bump version: 0.1.5 → 0.1.6. [Alexander Böhn]

* All sorts of new numpy-related shizziach. [Alexander Böhn]

* Clu.repl.ansi.ansidoc(…) is now variadic ... call it with all the things, feel free ... or just use it with `pythonpy`: [Alexander Böhn]

  py 'clu.repl.ansi.ansidoc(clu.exporting.Exporter.export, clu.predicates.negate)' | less -R

  ... it’s THAT EASY.

* Using multiple format directives in ANSI “color” arguments. [Alexander Böhn]

* Trying to wrangle an “ansidoc(thing)” function ... which that putatively will do exactly what you think it will     do, which is display docstrings for things in ANSI colors –     LIKE HUU-DOYYY as Liz Lemon would put it during L.U.N.C.H. [Alexander Böhn]

* Made one of the numpy asserts more legibly attractive. [Alexander Böhn]

* Tests for sigma aliases: both “σ” and “Σ” from clu.mathematics. [Alexander Böhn]

* N.B. my love for Greek symbology is due to math and not frats. [Alexander Böhn]

* If we’re conditionally getting things, it needs to look good. [Alexander Böhn]

* Went mad with Greek math aliases, like a little, just a bit. [Alexander Böhn]

* How do you write this line and not think of that Family Guy guy ... the one who says that thing. [Alexander Böhn]

* Another day, another Makefile rule to clean up some shit somewhere. [Alexander Böhn]

* Reverted `__bytes__(…)` method changes in clu.fs.filesystem ... using “self.to_string()” would have had those methods return     bytes-ified object repr strings, which we don’t actually want     that, we want the fucking filesystem path in bytes-ized form. [Alexander Böhn]

* Removed some redundant `stringify(…)` calls in clu.fs.filesystem. [Alexander Böhn]

* Tidied up the imports in clu.repl.ansi. [Alexander Böhn]

* Check for “source” keyword in class kwargs before deleting it. [Alexander Böhn]

* This is the second time I’ve misplaced an “encoding” keyword arg ... specifically when inlining a bytes() or str() conversion – for     some reason I keep passing the encoding argument into the call     enclosing the conversion-op construction, instead of, you know,     where it’s the fuck supposed to be. GAH. [Alexander Böhn]

* Corrected some ⌘ C-⌘ V kind of docstring mistakes. [Alexander Böhn]

* Spaces to tabs, when it comes to Makefiles. [Alexander Böhn]

* Fencing the Enum import in clu.predicates. [Alexander Böhn]

* Always None-initialized Exporter.dotpath if a path wasn’t passed. [Alexander Böhn]

* Wishful thinking. [Alexander Böhn]

* Exporters now accept a “path” kwarg for specifying their __file__ [Alexander Böhn]

* Isolating imports in clu.naming. [Alexander Böhn]

* Trimming and compartmentalizing clu.exporting imports ... AGAIN I KNOW. [Alexander Böhn]

* Fully clarified the imports in clu.exporting. [Alexander Böhn]

* Going from pickle.whichmodule(…) to my own module-determiner ... which if we do this, it makes the one test marked as “xfail” in     `test_naming.py` into a Heisenbug; that test now comes back as     an “xpass” over 50% of the time, for some reason – but it still     fails enough not to warrant unmarking it. Huh. [Alexander Böhn]

* Amended real-world exporter-combo tests to examine keysets. [Alexander Böhn]

* Renamed the module-level unnamed lambdas in the exporter test ... so as not to shadow or overwrite or otherwise fuck with things     that had the same names, but had been defined local to their     respective test methods in other places. [Alexander Böhn]

* Fixed the unnamed-lambda test in `test_exporting.py` ... in a hacky way I confess – I had to move the lambda definitions     out of the test-case method and up to the module-level for the     “thingname_search(…)” function to work on them. [Alexander Böhn]

* Travis tweak. [Alexander Böhn]

* MTV’s Make My File. [Alexander Böhn]

* Using “clu.fs.misc.stringify(…)” in “clu.fs.appdirectories.AppDirs” ... added some trivial sanity-check type lines in the test suite. [Alexander Böhn]

* Looking at the return value of Directory.zip_archive(…) in the test. [Alexander Böhn]

* Trimmed some dead code. [Alexander Böhn]

* Finally, a clu.fs.filesystem test for Zipfile archiving. [Alexander Böhn]

* Bump version: 0.1.4 → 0.1.5. [Alexander Böhn]

* Fixed a bug in clu.fs.filesystem.Directory.zip_archive(…) ... the bug was actually in clu.fs.filesystem.TemporaryName.copy(…)     which I had blindly refactored at some point in the somewhat     recent past; anyway, I’m going to add a proper test which is     why this commit also includes a gratuitous bunch of JPG and PNG     binaries as “test data”, erm. [Alexander Böhn]

* We no longer have to delete things from modules ... lest anyone forget, that’s why we wrote all that exporter stuff. [Alexander Böhn]

* Moved “scandir” and “walk” imports to clu.constants.polyfills. [Alexander Böhn]

* Changed all my “graceful_issubclass(…)” refs to `subclasscheck(…)` ... it’s better-looking, less confusing, terse-er and an all-around     improvement. Don’t you think? [Alexander Böhn]

* Using the clu.exporter machinery in clu.fs.{filesystem,misc} [Alexander Böhn]

* If we bring back clades, we’ll redo all this stuff. [Alexander Böhn]

* Made `clu.predicates.Partial.__init__(…)` not use an explicit check ... specifically it was testing “if PYPY” to decide whether to pass     its variadic arguments up the `super(…)` call-chain; now, it     just tries to pass, repeating the call without the variadics if     anything gets raised. Because you know what that is? ITS MORE     PYTHONIC, MOTHERFUCKERS, THAT IS WHAT THAT IS. [Alexander Böhn]

* More Makefile tweaks. [Alexander Böhn]

* Made the Makefile look slightly less like drunken spider footprints ... there is actually a “make test” target after all these years;     there are separate rules to purge build and test artifacts (the     latter of which have been piling up it would seem); some things     make sense now to do before other things, blah blah ITS ANOTHER     MAKEFILE COMMIT OKAY? You know EXACTLY what it is and YOU DON’T     GIVE A FUUUUUUCK. Who can blame you? I’ll let you know when the     diff is something of consequence in a language you like, okay     my doggie? Fuck yes. [Alexander Böhn]

* Keeping Makefile tasks from wreaking mayhem with native extensions ... one rule, written for a Cython-based project, was going through     and unceremoniously purging everything that had an *.so suffix,     which in this case was not so much Cython artifacts as it was     all the helpfully compiled bits of installed modules like oh     you know NUMPY and all its friends dogg what the fuck! OK so     fixed. Whooooooops. [Alexander Böhn]

* Bump version: 0.1.3 → 0.1.4. [Alexander Böhn]

* The clu.compilation.macros module had lost its ever-crucial TOKEN! ... It also had docstrings on one class but not the other, for some     stupid reason – I evened that shit up and fixed it. [Alexander Böhn]

* Using the emoji-riddled inline code as the actual `negate(…)` docs. [Alexander Böhn]

* No longer defining the ANSI metaclass’ CacheDescriptor inline. [Alexander Böhn]

* MIGHT AS WELL FACE IT YOURE ADDICTED TO __slots__ ATTRIBUTES. [Alexander Böhn]

* ANSI string-lookup caches now count their hits and misses. [Alexander Böhn]

* For some reason the “typing” module plays unnicely. [Alexander Böhn]

  ... with virtualenvs. Like it being installed makes nearly every
      attempt to start a Python program crash all over itself somewhere
      deep on some import from `typing`. Whatevs, I’m over it, go
      fuck yourself, typing module you fucking douche

* Moving development-environment REPL scriptlets into the codebase… [Alexander Böhn]

* Fleshed out clu.repl.ansi.ANSIFormat a bit ... meaning I stole a few of the best bits from VersionInfo (which     is also a NamedTuple ancestor) and adapted them, particularly     for construction ... tried to figure out WTF is with bpython and printing ANSI and     got rather much nowhere ... All of the ANSI-enmeta’d enums – or OK pal what is •your• cool     word for “classes that employt the indicated classtype as their     metaclass” – now cache their “Type.for_name('string')” lookups,     which were potentially doing linear scans of both internal dict     sets (`__members__` *and* `__aliases__` motherfucker) and while     I personally never experienced slow performance or behavior on     this operation, the fact that it could have concievably been     pathologically there sometime in the far-off future led me to     choose this issue as my PREMATURE OPTIMIZATION OF THE WEEK!!!! [Alexander Böhn]

* Bump version: 0.1.2 → 0.1.3. [Alexander Böhn]

* Only using Python versions currently available locally in tox.ini. [Alexander Böhn]

* Docstring spit-and-polish in the clu.sanitize module. [Alexander Böhn]

* DOCSTRINGS!! DOCSTRINGS!!!!!!! DOCSTRINGS!!!!!!!!!!!!!!!!!!! [Alexander Böhn]

* Spiffed up the `negate(…)` docstring ... since yeah OK I confess, this function is basically like my     new kitten right now, in terms of my feelings. [Alexander Böhn]

* Fixed a whoooooole lot of unreasonable docstrings in clu.predicates. [Alexander Böhn]

* Truly gratuitous callability checks in `attr(…)` accessor test. [Alexander Böhn]

* Bringing the negated `hasattr(…)` shortcuts into the testsuite. [Alexander Böhn]

* Used `negate(function)` to build `noattrs(…)` and `nopyattrs(…)` ... which those are shortcut `hasattr(…)` function shortcuts. [Alexander Böhn]

* WHOOOOPS ... forgot to pass on those predicate arguments now didn’t I there. [Alexander Böhn]

* Moved clu.repl.enums to clu.enums (deserving as it is of the top level) [Alexander Böhn]

* Got rid of the TOXENV stuff completely from Travis’ config. [Alexander Böhn]

* Updated the Travis CI config’s TOXENV matrix thing. [Alexander Böhn]

* Pointing tox.ini’s [deps] at the proper requirements file. [Alexander Böhn]

* Fully qualifying all non-relative imports with “clu.xxxxx…” [Alexander Böhn]

* Making “tox” run. [Alexander Böhn]

* Not recursing into the venv root. [Alexander Böhn]

* Better docstrings for some clu.repl.ansi functions. [Alexander Böhn]

* Moving the “environment” pytest fixture function to conftest.py. [Alexander Böhn]

* Warnings are fired off when setting up AppDirs with certain values ... to wit: “appauthor”, “roaming” and “multipath” are Windows-only     options; we now warn if one tries to make use of them while on     a non-Windows platform ... also refactored some of the AppDirs-based key-value ancestor     type stuff. [Alexander Böhn]

* Fixed and added tests for clu.fs.script_path(…) [Alexander Böhn]

* Got rid of legacy Cython helpers in setup.py. [Alexander Böhn]

* Rehashing the keyvalue module. [Alexander Böhn]

* Removed “defaults” kwarg from ANSIFormatBase NamedTuple declaration ... this greased the wheels for PyPy compatibility, and it turns     out to be totally unnecessary anyway, because the defaulting is     taken care of in the subclass. [Alexander Böhn]

* N.B. “psutil” IS NOT OF OR IN THE STANDARD LIBRARY, DOGG. [Alexander Böhn]

* Removed “defaults” kwarg from ANSIFormatBase NamedTuple declaration ... this greased the wheels for PyPy compatibility, and it turns     out to be totally unnecessary anyway, because the defaulting is     taken care of in the subclass. [Alexander Böhn]

* MANIFEST.in includes only .py files from the tests/ directory. [Alexander Böhn]

* Noodled around with the project Makefile, pt. II. [Alexander Böhn]

* Noodled around with the project Makefile. [Alexander Böhn]

* Bump version: 0.1.1 → 0.1.2. [Alexander Böhn]

* Amended clu.predicates accessor lambdas with call signatures. [Alexander Böhn]

* Corrected clu.predicates.pyname(…) docstring. [Alexander Böhn]

* Properly module-exporting some of the clu.repl.enum stuff. [Alexander Böhn]

* Trimmed inline assert from clu.repl.ansi. [Alexander Böhn]

* Using clu.exporting in clu.repl.ansi. [Alexander Böhn]

* Trimmed inline assert from clu.repl.banners. [Alexander Böhn]

* Using clu.exporting in clu.repl.banners. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Trimmed inline assert from clu.repl.enums. [Alexander Böhn]

* Using clu.exporting in clu.repl.enums. [Alexander Böhn]

* Getting System enum from fully-qualified module path. [Alexander Böhn]

* Got rid of crappy old unused memoization tools in clu.fs.msic. [Alexander Böhn]

* Tests (and tweaks) for clu.fs.filesystem.temporary(…) [Alexander Böhn]

* Pruned unused SYSTEM import from test_fs_appdirectories.py. [Alexander Böhn]

* Removed clu.fs.appdirectories inline test from clu.keyvalue. [Alexander Böhn]

* Put in stubbed Win32 clu.fs.appdirectories tests ... each of which ensures it gets skipped by immediately making a     call to “pytest.importorskip(…)” with some win32 interop module     as the operand. [Alexander Böhn]

* Checking type of convenience Directory properties. [Alexander Böhn]

* Proper tests for clu.fs.appdirectories (adapted from inline tests) ... THE GOOD NEWS: there’s a full test suite for the aforementioned     clu.fs.appdirectories – namely the AppDirs class from same –     that uses a py.test “fixture” to keep XDG_WHATEVS variables out     of the picture; all systems except System.WIN32 get their test     coverage; tests are properly parameterized for the user who is     running them (i.e. it’ll work for someone who isn’t me) ... THE BAD NEWS: under some conditions – notably when running with     py.test – the “self.system is System.DARWIN” (&c.) comparisons     within the clu.fs.appdirectories module were failing, as the     System enum looked like it came from a different place, module,     or package (pick your fave) and so I had to implement a fucking     `__eq__(…)` method in clu.constants.enums.System and change all     the comparisons from “is” to “==” to get this shit to work –     which kind-of totally defeats one of the great advantages of a     fucking enum (namely that its instance members are singletons     automatically and can be compared with “is”). ... THE UGLY NEWS: the same problem that affected the enums seems     to also affect the use of clu.version.VersionInfo – so I had     to stringify both sides in all the comparisons between those in     all of the test methods, which we can all agree, that’s fucking     ugly as shit, right? I mean it works and it’s legible and the     functionality is being properly tested, yes, but AT WHAT COST. [Alexander Böhn]

* Trimmed inline assert from clu.sanitizer. [Alexander Böhn]

* Using clu.exporting in clu.sanitizer. [Alexander Böhn]

* Trimmed inline assert from clu.dicts. [Alexander Böhn]

* Using clu.exporting in clu.dicts. [Alexander Böhn]

* Test for in-place clu.exporting.Exporter add operator. [Alexander Böhn]

* Made clu.exporting.Exporter add-able and in-place-add-able ... updated tests accordingly ... stole logic from clu.typespace.namespace.Namespace. [Alexander Böhn]

* Renamed clu.predicates.partial_ex to clu.predicates.Partial. [Alexander Böhn]

* Juggled imports in clu.keyvalue relevant to inline test. [Alexander Böhn]

* Re-enabled the Exporter in clu.keyvalue. [Alexander Böhn]

* Exporting “lambda_repr(…)” from clu.predicates. [Alexander Böhn]

* Partials created by clu.predicates.apply_to(æ…) are repr-equivalent ... meaning: they don’t use the `functools.partial.__repr__()` like     as-is off-the-shelf; `apply_to(…)` now uses a custom subclass     of `functools.partial` overriding the `__repr__()` method and     adding `__name__` and `__qualname__` attributes – such that all     these partial objects look like lambda instances (at least as     far as `clu.exporting.Exporter.export(…)` is concerned). ... This is in the category of “Circuitous and arguably stupid yet     strangely satisfying hacks” – as it allows the exporter to     rename `apply_to(…)` partials just as it does with lambdas,     sans too much extra tweaking. We’ll see when the other shoe     drops and it turns out that this change breaks everything in     sight, okay. [Alexander Böhn]

* Socked away my lambda.__repr__–equivalent. [Alexander Böhn]

* Using clu.exporting in clu.mathematics. [Alexander Böhn]

* Further clu.predicates trimming. [Alexander Böhn]

* Trimmed inline assert from clu.predicates. [Alexander Böhn]

* Using the clu.exporter in clu.predicates. [Alexander Böhn]

* Trimmed inline assert from clu.typology. [Alexander Böhn]

* Using the clu.exporting.Exporter in clu.typology. [Alexander Böhn]

* Starter tests for clu.exporting ... which have already revealed some module-level-related problems     with `thingname_search(…)` and friends ... also using clu.exporting.Exporter in clu.naming. [Alexander Böhn]

* Basic exporter working as clu.exporting.Exporter. [Alexander Böhn]

* Renamed instances of clu.version.VersionInfo to version_info ... because calling them “version” was causing a shadow situation     to occur with the module clu.version. [Alexander Böhn]

* Trimming specious code from clu.exporting. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Niced up a few docstrings in clu.predicates. [Alexander Böhn]

* Corrected `enumchoices(…)` docstring. [Alexander Böhn]

* Rewrote clu.mathematics ... since it was just the one “clamp(…)” function, this was less     crazy than you might think; it was still a complete overhaul     tho, involving the generic-ization of “clamp(…)” and a new     `isdtype(…)` predicate ... added tests for clu.mathematics as well ... tweaked the clu.naming tests to fail less and be less stupid ... tweaked some clu.typology innards too. [Alexander Böhn]

* Cleaned up some imports and moved `pytuple(…)` to clu.predicates. [Alexander Böhn]

* Many changes, most notably in the clu.naming tests ... those are now employing pytest’s “XFAIL” marker more reasonably ... in conjunction with all that, rather than use `pytest.xfail(…)`     we’re still intercepting AssertionErrors when things’ll likely     go sideways, but instead we’re raising a new custom exception     subclass `clu.constants.exceptions.Nondeterminism` – because     a bunch of these on-again, off-again failures seem to stem from     e.g. the ordering of “sys.modules” and whatnot – and that shit     is fucking nondeterministic as fuck ... did some more real beyond-basic cleanup in clu.exporter – not     that you’d know (although the module will compile and import     correctly, so there’s that) ... juggled some things between clu.naming and clu.predicates –     largely with the goal of reducing dependencies; I think I’ve     almost managed to decouple these two modules but for a few     imports here and there (which is a big schmeal). ... AND MANY MOOOORRREE. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Rewrote `clu.typology.graceful_issubclass(…)` using `predicate_any(…)` ... which OK, fuck, phew: that function – while, ah, functional –     had one of the messiest, ugliest, inscrutablest implementations     it has ever been my displeasure to produce. I think I got hung     up on having a signature that •looked• like `issubclass(…)` or     `isinstance(…)` as much as possible; it had too much try/except     shit in its flow control… blah blah blah. Now it looks awesome     (albiet probably still inscrutable at first glance to some) but     it’s clean as shit and uses my favorite new shit: `apply_to(…)`     and its favorite child, `predicate_any(…)`. They make doing     these weird pseudo-functional generator-expression mashups a     true fucking pleasure. Yes! [Alexander Böhn]

* Trying to import numpy in clu.constants.polyfills. [Alexander Böhn]

* Consolidated the custom exception and warning subclasses ... they all now live in clu.constants.exceptions. [Alexander Böhn]

* Expanded the enum alias class’ `member_for_value(…)` method. [Alexander Böhn]

* Made the enum alias class slightly less redundant. [Alexander Böhn]

* Minor additions and tweaks to the enum alias tests. [Alexander Böhn]

* Made clu.repl.enums.alias a __slots__ class. [Alexander Böhn]

* Warnings for when a dotpath contains dashes. [Alexander Böhn]

* The `path_to_dotpath(…)` function was exported from the wrong place ... now it’s not, because I fixed it. [Alexander Böhn]

* Tweaked ever-so-slightly the print_all() thing in consts.py. [Alexander Böhn]

* Removed gratuitous module-level imports in predicate tests. [Alexander Böhn]

* Bringing back λ the ultimate. [Alexander Böhn]

* Nixed unnecessary “os.path.basename()” in clu.naming. [Alexander Böhn]

* Defined a constant BASEPATH, specifying the root directory ... I mean, we need this – you can see that we need this, n’est cé     pas? Right? ... also now there is an inline module `__name__ == "__main__"`     sort of dealie in clu.constants.consts that prints out all of     the constant variables defined therein. Not an inline test –     I swear I’m not going back to those – but a handy debugging     thinamadoo, basically. [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Marked string as raw in clu/version/read_version.py. [Alexander Böhn]

* Removed old project egg-info directory name. [Alexander Böhn]

* Tweak fix to Makefile. [Alexander Böhn]

* Uncrustified and updated setup.py. [Alexander Böhn]

* Tweaked project name. [Alexander Böhn]

* Fixed unmarked raw string in regex. [Alexander Böhn]

* Tweak to .gitignore. [Alexander Böhn]

* Bump version: 0.1.0 → 0.1.1. [Alexander Böhn]

* Updated .bumpversion.cfg ... thanks to read_version.py I no longer have to update a bajillion     backup __version__ strings, and so. [Alexander Böhn]

* Rearranging the deck chairs on the Titanic pt. LVII. [Alexander Böhn]

* Just found out that enums are “expandable” – ... as in, you can be like `tuplize(*EnumSubclass)` to get back a     tuple containing all of the members of EnumSubclass, in order,     with no problem. I restructured `apply_to(¬)` and the predicate    `isexpandable(…)` accordingly. Side note, really – what makes     things quote-unquote expandable, really? Why can I be all like     “*EnumSubclass” but not “*generator_expression” ?? Help me dogg     you’re my only hope. [Alexander Böhn]

* Asserting that \enum members are not enums. [Alexander Böhn]

* Tests added for those good ol’ utility helpers ... I am talking of course about `tuplize(…)`, `uniquify(…)`, and     `listify(…)`, the three of whom have been with us for like ever     it feels like. [Alexander Böhn]

* More tests and more predicate overhauls! ... new predicates: `haslength(…)` checks for a “__len__” attr;    `uncallable(…)` sees if a thing isn’t callable; `thing_has(…)`,    `class_has(…)`, `isslotted(…)`, `isdictish(…)`, `isslotdicty(¬)`     and others were completely rewritten to actually work – the     first two of those now use the also-rewritten and extremely     generally useful new `apply_to(…)` function; `isexpandable(…)`     checks a thing against a list of types to see if you can do    `*thing` to expand it – I don’t know the language lawyer rules     for “asterisking” or tuple-expansion or whatever the fuck it     is actually called so this may change; tests for `haslength(…)`     and the “{thing/class}_has” and slot/dict predicates have been     added and, erm, tested; `predicate_nop(…)` was moved out of     clu.typology and into clu.predicates; some other NOp thingees     and internal-use doohickeys were added and probably other shit     as well (I always forget exactly what when I am editing these     commit notes, bah). Yes! [Alexander Böhn]

* Using pytest.xfail() where nondeterminism might happen. [Alexander Böhn]

* Fixed some corner-cases in typology ... thanks, nacent test suite!! [Alexander Böhn]

* Migrated clu.naming tests from replutilities. [Alexander Böhn]

* Migrated dict/namespace merge tests from replutilities. [Alexander Böhn]

* Migrated predicates tests from replutilities. [Alexander Böhn]

* Migrated clu.version inline tests. [Alexander Böhn]

* Trimmed dead code from filesystem tests. [Alexander Böhn]

* Migrated clu.fs.filesystem inline tests. [Alexander Böhn]

* Finished writing that docstring. [Alexander Böhn]

* Fixed enum aliases. [Alexander Böhn]

* Typelist function tune-up ... and and overdue __all__/__dir__ set for the clu.typology module. [Alexander Böhn]

* Moved the enums from clu.fs.appdirectories to clu.constants.enums. [Alexander Böhn]

* Moved aliasing enum stuff from clu.constants to clu.repl. [Alexander Böhn]

* Remove gratuitous OS check in clu.fs.NamedTemporaryFile. [Alexander Böhn]

* It’s probably overkill to fork() before umask()-ing ... but frankly the race condition inherent in trying to get the     process’ current umask without perturbing the value is fucking     stupid, it is exactly dumb shit like that that inflames my OCD     and keeps me from telling everyone I know about how great the     fucking POSIX API is (which really that is not a joke, I really     actually generally like it except for warts like this one). [Alexander Böhn]

* Peppering in __all__ and __dir__ joyously and mirthfully ... also you wouldn’t know it but between this commit and the last     one I completely replumbed all the .envrc and .direnvrc shit     on my entire computer – apparently “loading” a source file in     the direnv world (which up until recently I thought was a nice     world that was good to live in) does *not* export bash aliases,     functions, or anything else up to a certain point. ... So I hacked around that – but that was fine, no problem, a     complete and total breeze compared to this bizarre bullshit     nonsensical PYTHONPATH-related REPL freakout I was having prior     to all that. I ended up using the `virtualenv --verbose --clear`     command, which if you didn’t know, that second option flag is     literally described like e.g. “blow away the entire virtualenv     and start over from scratch” or something like that – after     doing that and then blindly monkeying around with PATH-y stuff     a while afterwards, I got my shit to work… that shit in this     case would be the “replenv” stuff, upon which the whole CLU     project is literally based. Blech. Anyway you can’t see any     of that, because why would I check that nonsense into source     control?? It’s not as if I am about to absently save right over     all that irritatingly hard work and break it all again, only to     find myself in a sea of inscrutable nonfunctionality, sans the     ol’ reliable `git bisect` or anything else, hah. Yeah! [Alexander Böhn]

* Sorted out a ton of stuff w/r/t modes and permissions. [Alexander Böhn]

* Git-ignoring .tm_properties. [Alexander Böhn]

* ANSI text printing works on the command line. [Alexander Böhn]

* Fixed CSDIL enum’s __index__(…) method. [Alexander Böhn]

* ANSI metaclass name-lookup method now considers aliases. [Alexander Böhn]

* ZERO-COST ENUM MEMBER ALIASING, MOTHERFUCKERS. [Alexander Böhn]

* Tweaks in the ansi and typespace modules. [Alexander Böhn]

* Further OCD-ish CSDIL cleanup. [Alexander Böhn]

* Combined those two CSIDL dicts into an Enum ... also wrote a basic launchd plist generator for xdg-runtime.py. [Alexander Böhn]

* Fleshing out xdg-runtime.py. [Alexander Böhn]

* Cleaned up xdg-runtime.py script. [Alexander Böhn]

* S/typing/typology/g. [Alexander Böhn]

* So many many things. [Alexander Böhn]

* Vendoring in the excellent “read_version” – ... by one John Thorvald Wodder II (if that really is his name –     I mean who cares dogg this code is tight but really that sounds     more like a component of some kind of Winklevoss joke than an     actual human name) who published it herein: [Alexander Böhn]

  • https://github.com/jwodder/read_version

* Ported over the “keyvalue” updates from Homage ... specifically the changes that make it play nice with the whole     “appdirectories” all-singing all-dancing crapola – namely these     commits: [Alexander Böhn]

  • https://git.io/fjVvR – “appdirs” → “appdirectories”
  	• https://git.io/fjVvE – subsequent “keyvalue” refactoring

  ... indeeed dogg it’s not like it’s breakthrough lambda-calculus or
      a new kind of JIT thing or any of that, but you know, 50% of
      programming is coming up with names for shit; the other 50%
      is figuring out the names other people came up with for their
      shit; the fun stuff (matrix math, type-algebra, prematurely
      optimizing things, doing algorithms, generally trying new shit
      of any sort) are momentary rounding errors found ephemerally on
      serendipitous occasions somewhere betwen those two time-suck
      categories of what it is, doggie.

* Tweaked Makefile and rebased the travis config. [Alexander Böhn]

* A few tweaks to clu.fs.filesystem. [Alexander Böhn]

* Minor tweak to short project description. [Alexander Böhn]

* Fleshed out ABOUT.md and README.md. [Alexander Böhn]

* Snipped a dead code line. [Alexander Böhn]

* Fixes for clu.version.VersionInfo. [Alexander Böhn]


