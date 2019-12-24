# Changelog


## 0.5.4-4+gb9aebd8 [SNAPSHOT]

### Other

* A fine Commit #1,000 as any: preservation of namespace insert-order ... happy order-of-magnitude-aversary, my dear CLU, and salud! [Alexander Böhn]

* Inline tests return POSIX exit status values and call “sys.exit(…)” ... also there is a command that copies the CLU boilerplate starter     code right to YOUR CLIPBOARD!!!! Huzzah. [Alexander Böhn]

* First draft of “KeyMapView” and “KeyMapProxy” ... which those are ‘FrozenKeyMap’ and ‘KeyMap’ types, respectively,     that wrap weakrefs to actual KeyMap instances and forward method     calls to those instances down from the public API. ... includes a decorator “@selfcheck” that tests the Truthiness of     the ‘self’ instance before the actual method invocation and     raises a ‘ValueError’ for any and all unworthy instance values. ... tests and all that other hoohah to follow, after I veg out     with the cats and some kombucha and watch me some YouTube. [Alexander Böhn]

* Generators beat constructed lists. [Alexander Böhn]


## v0.5.4 (2019-12-24)

### Add

* Added a “shortrepr(…)” method to show namespace info, sans newlines ... also added the “show-consts.py” and “show-modules.py” script     invocations to the Makefile. [Alexander Böhn]

* Added a “clu.importing.PerApp.appspaces()” convenience function ... does precisely what you think it does. [Alexander Böhn]

* Added inline test for “clu.importing.ProxyModule” fallbacks. [Alexander Böhn]

* Addressing automated GitHub security alert. [Alexander Böhn]

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.5.3 (2019-12-17)

### Add

* Additional sanity-check in “Environ.__exit__(…)” [Alexander Böhn]

* Added wildcard «‽» to the semantic-version regex “build” field. [Alexander Böhn]

* Additional testing to ensure that “FrozenEnv” is frozen. [Alexander Böhn]

* Added API to directly access the backing environment dictionary. [Alexander Böhn]

* Added proper error-handling when calling Git commands. [Alexander Böhn]

* Added “version” make target. [Alexander Böhn]

### Other

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


## v0.5.2 (2019-12-15)

### Add

* Added a “clu.version.git_version” module and trivial functions ... simple shit to get the git tag version ... unlike the other stuff under “clu.version” which are pretty     much entirely self-contained, “clu.version.git_version” uses     standard CLU stuff (e.g. the Exporter, the inline test harness,     et cetera) so WE’LL JUST SEE HOW THIS GOES NOW WON’T WE. [Alexander Böhn]

* Added ‘ValuesView’ and ‘ItemsView’ tailored for “NamespaceWalker” ... which these types each implement much faster, less circuitous     versions of the “__contains__(…)” and “__iter__()” methods,     utilizing the “walk()” method of their associated mappings ... the necessity for these was no gamble or – oddly enough in my     personal case – wasn’t premature. No! I saw the need for speed     reflected in the timing reports coming from my own new outfit     for running inline tests – see all those recent changes to the     “clu.testing.utils” module, specifically regarding “@inline”     and friends. Yes!!!!! [Alexander Böhn]

* Added “iterlen(…)” to put an end to like e.g. “len(tuple(¬))” ... pretty much a straight-up ⌘-c ⌘-v from the “more-itertools”     source – namely their function “ilen(…)” [Alexander Böhn]

* Added a bunch of ancestors to “clu.testing.utils.@inline” [Alexander Böhn]

* Added “@inline” decorator to bpython REPL script. [Alexander Böhn]

* Added note about executing test functions multiple times. [Alexander Böhn]

### Other

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

* Minutiae. [Alexander Böhn]

* Revised the @inline test decorator mechanism ... to wit: it is now implemented as a class that is instanced     automatically via module ‘__getattr__(…)’ each time it is     requested for import ... this makes managing the stopwatch instances and the decorated     functions, as instance attributes, way way easier ... plus it eliminates the need for the clunky “vars()” argument     to all the “inline.test()” calls ... a few other revisions were made during these changes (most     notably the elimination of the “collection phase” in the main     stopwatch report – but that was kind of stupid anyway) [Alexander Böhn]


## v0.5.1 (2019-12-10)

### Add

* Added baseline environment-variable-access function API ... also differentiated the testing of the “old-style” Flat and     Nested classes, versus the new shit. [Alexander Böhn]

* Added a “FrozenNested.mapwalk()” method, delegates to “mapwalk(…)” [Alexander Böhn]

* Added namespaced “KeyMap.pop(…)” and “KeyMap.clear(…)” [Alexander Böhn]

* Added a test illustrating “try_items(…)” particular behavior ... w/r/t DefaultDict factories and “getitem(…)” [Alexander Böhn]

### Other

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


## v0.5.0 (2019-11-27)

### Add

* Added a “consts” fixture to the pytest plugin. [Alexander Böhn]

### Other

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


## v0.4.10 (2019-11-27)

### Other

* Bump version: 0.4.9 → 0.4.10. [Alexander Böhn]

* Updated/refactored some of “clu.fs.pypath” ... “pypath.append_path(…)” has been renamed “pypath.add_path(…)”,     and it now accepts a keyword-only argument ‘prepend=True’ to,     y’know, prepend its payload to ‘sys.path’ instead of appending. ... “pypath.remove_invalid_paths()” calls ‘site.removeduppaths()’     before doing anything to ‘sys.path’ ... There’s a new convenience function “pypath.enhance(…)” which     is basically sugar for calling “remove_invalid_paths()” ahead     of calling “add_path(…)” – which as already noted now also     includes a call to ‘site.removeduppaths()’ ... the REPL script imports “clu.fs.pypath” as a module, instead     of picking through its exported functions ... many tests make use of new “clu.fs.pypath.enhance(…)” function. [Alexander Böhn]

* Moved the “pytester” requirement into the CLU pytest plugin proper. [Alexander Böhn]

* Testing and pytest support for “clu.dispatch” ... new “clu.constants.consts” item ‘USER’, value of the current     users’ username ... rework of “clu.fs.filesystem.rm_rf(…)” logic ... The “clu.testing.pytest” plugin now implements a pytest hook     function “pytest_sessionfinish(…)”, which in turn conditionally     binds an exit handler – using “clu.dispatch.exithandle” – that     deletes any stray pytest temporary-file artifacts left over     upon interpreter shutdown     … namely, anything in the directory $TMPDIR/pytest-of-$USER –       which stubbornly would not remove itself and (according to       the policy of pytest’s code for this, apparently) just keeps       accumulating piles of cruft every time ‘pytest’ was executed ... All in aid, really, of the one new test, in “test_dispatch.py”,     which makes use of the “pytester” built-in pytest plugin to     cleanly test exit handlers; see the source of same for details. [Alexander Böhn]

* Updated the bpython REPL script for the ‘dispatch’ update. [Alexander Böhn]

* Moved “clu.shelving.dispatch” down to “clu.dispatch” ... as it is clearly bigger than just the nascent ‘shelving’ module. [Alexander Böhn]

* Made “clu.fs.filesystem.TemporaryFileWrapper” an explicit Iterable ... as in, it inherits from ‘collections.abc.Iterable’ ... also added 'pytester' to the test plugins loaded in conftest.py. [Alexander Böhn]


## v0.4.9 (2019-11-26)

### Add

* Added ‘has_appname’ to “clu.exporting.ExporterBase.__dir__(…)”’s filter. [Alexander Böhn]

### Other

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


## v0.4.8 (2019-11-22)

### Other

* Bump version: 0.4.7 → 0.4.8. [Alexander Böhn]

* Typographic eratta en extremis. [Alexander Böhn]


## v0.4.7 (2019-11-22)

### Other

* Bump version: 0.4.6 → 0.4.7. [Alexander Böhn]


## v0.4.6 (2019-11-22)

### Add

* Added a “clu.shelving.dispatch.shutdown(…)” function ... like “clu.shelving.dispatch.trigger(…)” but with an actual call     to ‘sys.exit(¬)’ at the end ... also more bells & whistles to “clu.shelving.redat.RedisConf”     have been grafted on, somehow. [Alexander Böhn]

* Added a bunch of async shit I don’t quite understand. [Alexander Böhn]

### Other

* Bump version: 0.4.5 → 0.4.6. [Alexander Böhn]

* SIG-WINCH!!!!! [Alexander Böhn]

* Logging format config manscaping. [Alexander Böhn]

* Trimmed dead code. [Alexander Böhn]

* Tweaking shutdown logic. [Alexander Böhn]

* Minor tweak to zipfile artifact save logic. [Alexander Böhn]

* Even more “clu.shelving.dispatch” minutiae. [Alexander Böhn]

* Exit handle functions execute properly from signal handlers. [Alexander Böhn]

* More tweaks to async signal-handler demo code. [Alexander Böhn]


## v0.4.5 (2019-11-22)

### Other

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


## v0.4.4 (2019-11-21)

### Add

* Adding default Redis config file. [Alexander Böhn]

* Added a few diagnostic lines to the Redis inline test. [Alexander Böhn]

* Added some gratuitous asserts to the Redis inline test. [Alexander Böhn]

* Adding the Exporter to “clu.shelving.redat” [Alexander Böhn]

* Adding a “shelving” module and initial Redis process-handler. [Alexander Böhn]

### Other

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


## v0.4.3 (2019-11-14)

### Add

* Adding conftest.py to MANIFEST.in. [Alexander Böhn]

* Adding one-liner “conftest.py” to load the pytest plugin module ... this re-enables running pytest just as ‘pytest’ – instead of     having to be all like ‘python -m pytest -p clu.testing.pytest’     via make each and every time. [Alexander Böhn]

### Other

* Bump version: 0.4.2 → 0.4.3. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

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


## v0.4.2 (2019-11-08)

### Add

* Added “issingleton(…)” and “issingletonlist(…)” to “clu.typology” ... plus we’re using the former now in “clu.repr.strfield(…)” which     is cleaner than what it was doing before (which was dirtier) [Alexander Böhn]

### Other

* Bump version: 0.4.1 → 0.4.2. [Alexander Böhn]

* Properly set “_executed” flag on modules lacking an “__execute__()” [Alexander Böhn]

* Whitespace. [Alexander Böhn]

* Importing “clu.abstract” wholesale rather than piecemeal ... in both “clu.exporting” and “clu.importing” [Alexander Böhn]

* Removed unnecessary callable check in “clu.exporting.determine_name(…)” [Alexander Böhn]

* Getting “lru_cache” in “clu.exporting” directly from ‘functools’ [Alexander Böhn]

* One-character typo fix. [Alexander Böhn]


## v0.4.1 (2019-11-07)

### Add

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

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.4.0 (2019-10-22)

### Add

* Added method “clu.exporting.Registry.has_appname(…)” [Alexander Böhn]

### Other

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


## v0.3.9 (2019-10-22)

### Add

* Added docstring note about “__slots__” to ModuleBase. [Alexander Böhn]

* Added a nota benne about the instance/class name. [Alexander Böhn]

* Adding “clu.abstract” ABCs module and class-module tests. [Alexander Böhn]

* Added “array.ArrayType” to the typespace as “types.Array” [Alexander Böhn]

### Other

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


## v0.3.8 (2019-09-16)

### Other

* Bump version: 0.3.7 → 0.3.8. [Alexander Böhn]

* Manual version adjust. [Alexander Böhn]

* Manual version adjust. [Alexander Böhn]


## v0.3.7 (2019-09-16)

### Other

* Bump version: 0.3.6 → 0.3.7. [Alexander Böhn]


## v0.3.6 (2019-09-16)

### Other

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


## v0.3.5 (2019-09-13)

### Add

* Added “__getstate__(…)” and “__setstate__(…)” to “clu.config.base” ... specifically, the “clu.config.base.NamespacedMutableMapping”     subclasses “Flat” and “Nested” [Alexander Böhn]

### Other

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


## v0.3.4 (2019-09-03)

### Other

* Bump version: 0.3.3 → 0.3.4. [Alexander Böhn]

* Requiring PyYAML. [Alexander Böhn]


## v0.3.3 (2019-09-03)

### Other

* Bump version: 0.3.2 → 0.3.3. [Alexander Böhn]

* Including TOML files in MANIFEST.in. [Alexander Böhn]


## v0.3.2 (2019-09-03)

### Add

* Added new field types and spruced up the existing ones ... also began adding the new configuration schema stuff to the     demo “yodogg” project found in tests/. [Alexander Böhn]

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.3.1 (2019-08-16)

### Add

* Adding “clu.constants.enums” to the hardcoded module list. [Alexander Böhn]

* Adding “clu.exporting.Exporter” to “clu.repl.columnize” [Alexander Böhn]

### Other

* Bump version: 0.3.0 → 0.3.1. [Alexander Böhn]

* Some tox.ini adjustments. [Alexander Böhn]

* Raising when calling “flatten(…)” on a nonexistant Directory. [Alexander Böhn]

* Minutiae in the “show-modules.py” script. [Alexander Böhn]

* Confirming the new script directory location in the testsuite. [Alexander Böhn]

* Tweaks to the new display capacities of the “show-modules.py” script. [Alexander Böhn]

* Removed unused import. [Alexander Böhn]

* The “show-modules.py” script actually shows all the modules. [Alexander Böhn]

* Vendoring in a “columnize” implementation ... courtesy https://github.com/rocky/pycolumnize. [Alexander Böhn]

* Updating the hardcoded module list. [Alexander Böhn]


## v0.3.0 (2019-08-15)

### Other

* Bump version: 0.2.10 → 0.3.0. [Alexander Böhn]

* Test for “clu.fs.filesystem.script_path(…)” no longer xfails. [Alexander Böhn]


## v0.2.10 (2019-08-15)

### Add

* Added a stub clu/__main__.py file (all it does now is print the version) [Alexander Böhn]

### Other

* Bump version: 0.2.9 → 0.2.10. [Alexander Böhn]

* Moved “scripts” directory into the CLU module base proper. [Alexander Böhn]

* F-strings in “clu/__init__.py. [Alexander Böhn]


## v0.2.9 (2019-08-15)

### Add

* Added a 'clu-boilerplate' console script entry point ... which echoes out the (mercifully very short) boilerplate you     need to use CLU in a new Python module. [Alexander Böhn]

* Added the Exporter stuff to “clu.testing.utils” [Alexander Böhn]

* Added a “temporaryname” fixture-factory function to “clu.testing” [Alexander Böhn]

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.2.8 (2019-08-12)

### Other

* Bump version: 0.2.7 → 0.2.8. [Alexander Böhn]

* Rewrote “ls(…)” and “ls_la(…)” from “clu.fs.filesystem.Directory” ... to use the new less-cumbersomely-verbose modes of dealing with     “clu.fs.misc.suffix_searcher(…)” [Alexander Böhn]

* Rewrote a lot of “clu.fs.filesystem.Directory.flatten(…)” ... as well as rewrites in “clu.fs.misc.suffix_searcher(…)” and     “clu.testing.utils.countfiles(…)” – the latter of which now     also takes a “suffix” argument to only count files matching     a specific suffix, like duh ... expanded the “flatten(…)” method tests to cover all the new     combos of using the suffix-related arguments and double-checked     the output of everything and whatnot ... ALSO FIXED MANY BUUUUUUUGGS. [Alexander Böhn]

* Exporter checks in “clu.testing.pytest.clumods” and “show-modules.py” ... beforehand, there was a hardcoded list of “CLU modules” in a     static tuple in “clu.constants.data” which really was a list     of modules in CLU that used the “clu.exporting.Exporter” class     to export their shit. ... now there still is; the difference is that that tuple can now     contain any valid module in CLU and the two places where the     tuple gets iterated also check to see if the module they’re     exporting contains an exporter – if it doesn’t, whatever that     bit of code returns won’t contain said module ... clearly this is a janky system but we currently need it to     test that the Exporter registration system works in the first     place; it could get pared down to like only being used in one     or two instances, I feel like. [Alexander Böhn]

* Changed “followlinks=True” in “Directory.walk(…)” arguments ... plus some random updates and minutiae in “clu.fs.filesystem”     and “clu.testing.utils” [Alexander Böhn]

* Confirming the counts of the flattened directory contents ... using a “countfiles(…)” function, which in itself isn’t really     any type of anything – but its existence did necessitate the     creation of a new “clu.testing.utils” module. [Alexander Böhn]


## v0.2.7 (2019-08-09)

### Other

* Bump version: 0.2.6 → 0.2.7. [Alexander Böhn]

* I think it’s irritating how .jpg and .jpeg are valid JPEG suffixes. [Alexander Böhn]


## v0.2.6 (2019-08-09)

### Other

* Bump version: 0.2.5 → 0.2.6. [Alexander Böhn]

* We now have a “Directory.flatten(…)” instance method ... plus a working test stub, plus helper methods (one of which let     us rewrite some of “Directory.zip_archive(…)” to omit inlining     the “relparent(…)” lambda). I wrote all of this up at the bar     while standing up and drinking whiskey talking intermittently     to other patrons so I am calling this effort NOT BAD AT ALL. [Alexander Böhn]

* Makefile rules for running pytest and tox ... I mean, it’s cool and all that the pytest fixture stuff is now     a “plugin” module, with a setuptools endpoint and shit, instead     of just a conftest.py file (which was working just fine by the     way) but pytest, while a nice program and all, completely loses     its fucking shit completely under certain conditions – one of     which is, if somewhere or somehow during its utterly Byzantine     loading/discovery/setup/config phase it is told to load one of     these “plugin” modules more more than exactly once, it crashes     like a fucking trainwreck and spews out what has to literally     be the largest and most illegible traceback I have ever seen     (and I worked with JSP and Servlets 1.0 in the fucking late     1990s). ... Anyway. So pytest isn’t all that bad aside from one or two of     these occasional supernova-class exception belches every so     often – once I sifted through the wreckage for the offending     file I found the answer reading the pytest code, which was     completely decent: legible, full of well-written comments     and docstrings; aside from the plague of leading underscores     that infects a lot of Pythonilinguists I thought it was great.     So yeah I read it, figured out the fix (which itself wasn’t     anything too nasty or circuitous) and that’s that. ... So yeah that’s the reason for this long-winded commit note:     it’s so easy to talk shit about code and be like MOTHERFUCKER     WHAT IN THE NAME OF LOVECRAFTIAN TWAT IS THIS AWFULNESS, WHO     EVEN THINKS LIKE THAT and soforth; but so it’s necessary to     point out when shit is not bad, and especially when shit is     in fact somehow good. So yeah GOOD ON YOU, PYTEST, YOU GET     A COOKIE!!! Indeed. [Alexander Böhn]

* The “clu.fs.filesystem.script_path()” function is poorly behaved ... particularly in normal sdist installs. Its test code has been     branded with the shameful and dreaded X-FAIL for the moment. [Alexander Böhn]


## v0.2.5 (2019-08-07)

### Other

* Bump version: 0.2.4 → 0.2.5. [Alexander Böhn]

* Getting rid of root-level conftest.py, in favor of “clu.testing” [Alexander Böhn]

* A docstring! A docstring for this function straight away!!! ... if you say it in like a King Arthur voice it’s kinda funny. [Alexander Böhn]

* This is evidently how console-script endpoints should work. [Alexander Böhn]


## v0.2.4 (2019-08-07)

### Add

* Added a stupid little version-string script. [Alexander Böhn]

### Other

* Bump version: 0.2.3 → 0.2.4. [Alexander Böhn]

* Made the stupid little version-string script a setuptools entrypoint. [Alexander Böhn]


## v0.2.3 (2019-08-07)

### Other

* Bump version: 0.2.2 → 0.2.3. [Alexander Böhn]

* Moving the pytest fixtures that use CLU formally into the project. [Alexander Böhn]


## v0.2.2 (2019-08-07)

### Other

* Bump version: 0.2.1 → 0.2.2. [Alexander Böhn]

* Fixed unlabeled keyword arg “default” in “slots_for(…)” internals. [Alexander Böhn]

* Tweaked and wrote tests for “clu.predicates.slots_for(…)” [Alexander Böhn]

* New accessors in “clu.predicates” using “inspect.getattr_static(…)” ... Which that function, “getattr_static(…)” retrieves attributes     from things without setting off any of the “__getattr__(…)” or     “__getattribute__(…)” logic insanity; this means that calling     it (or any of my new and improved accessors based on it!!) will     get you, like, e.g. a descriptor instance instead of to whatever     the call to that instances’ “__get__(…)” method would’ve lead. ... So the new predicate attribute getter function things are all     named “stattr(…)”, “stattrs(…)” – just like the versions sans     the “st” prefixes (which it’s “st” for “static”, get it??) only     the underlying calls use “getattr_static(…)” instead of calling     “resolve(…)”… which calls “or_none(…)” which calls “getattr(…)”     which calls a bajillion descriptor/class-dict/instance-dict/mro     thingamabobs about whose inner workings I am always a bit hazy. ... SO YEAH ENJOY. Also I wrote tests for these, plus I simplified     “getitem(…)” and also gave “clu.exporting.ValueDescriptor” a     real “__repr__(…)” function for some reason. Yup. [Alexander Böhn]


## v0.2.1 (2019-08-01)

### Other

* Bump version: 0.2.0 → 0.2.1. [Alexander Böhn]

* Made the “clu.typespace.namespace.SimpleNamespace” type “hashable” [Alexander Böhn]


## v0.2.0 (2019-08-01)

### Other

* Bump version: 0.1.9 → 0.2.0. [Alexander Böhn]

* Clarified the “clu.naming.moduleof(…)” docstring. [Alexander Böhn]

* Ensured “determine_module(…)” will return any specified default value. [Alexander Böhn]

* Clarified the “clu.naming.nameof(…)” docstring. [Alexander Böhn]

* Whitespace. [Alexander Böhn]


## v0.1.9 (2019-07-27)

### Add

* Added an actual export to the ExporterBase subclass test. [Alexander Böhn]

* Added a __class_getitem__ method to “clu.exporting.Registry” ... and amended the relevant test accordingly. [Alexander Böhn]

* Added builtin exemplars to REPL env. [Alexander Böhn]

* Added “wheel” to the install requirements. [Alexander Böhn]

* Added “show-consts.py” and “show-modules.py” to the tox run ... I did this on a lark, to see if it would work and planning to     revert it immediately – but it is actually really good to have     these all print out, particularly in the PyPy environment (and     perhaps others to come) which are not as readily inspectable.     So these stay in. Yes!! [Alexander Böhn]

* Added pytest markers back in to tox.ini – ... I AM PLEASED TO ANNOUNCE TOX RUNS AND EVERYTHING PASSES! Except     a bunch of Windows tests that get skipped. BUT OTHERWISE!!!! [Alexander Böhn]

### Other

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


## v0.1.8 (2019-07-23)

### Add

* Added “scripts/show-modules.py” showing module-name nondeterminism ... it doesn’t really show all the modules, per se: it iterates     over all of them but at the moment it only displays the results     in which the results from the two calls “pickle.whichmodule(…)”     and “clu.naming.determine_module(…)” are dissimilar. ... also I re-used the same ANSI formatting stuff as I used in the     “show-consts.py” script (and they weren’t all that fleshed out,     designwise, at any rate) so this thing could use some work. [Alexander Böhn]

* Adding submodule in “tests” for Exporter secondary-package setup. [Alexander Böhn]

* Added a “zict.LRU” buffer atop the ANSI code lookup caches. [Alexander Böhn]

### Other

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


## v0.1.7 (2019-07-23)

### Add

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

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.1.6 (2019-07-16)

### Add

* Added some superfluous asserts on the numpy import. [Alexander Böhn]

* Added numpy import-or-skip to ensure the “array_types” assertion ... since 'MaskedArray' is hardcoded into the assertion, the test     would theoretically fail if numpy was unavailable, since the     typelist wouldn’t have been populated with any numpy types in     the init phase of the clu.typology module; I know *I* can’t     freakin imagine a world without numpy but that doesn’t mean     there isn’t such a place somewhere, assuredly; hence this lil’     tweak right here, for the people who live in that spiritually-     impovershed theoretical numpy-less flummoxing drugery, yes. [Alexander Böhn]

* Added “fields” and `stringify(…)`-based repr to clu.keyvalue. [Alexander Böhn]

* Added an “update(…)” dict-like method to the exporter. [Alexander Böhn]

* Added test checking the sum of three exporter instances. [Alexander Böhn]

### Other

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


## v0.1.5 (2019-07-15)

### Add

* Added text fixture to provide long “Lorem Ipsum”-style texts; ... wrote a new key-value-store test using the Lorem Ipsum fixture; ... switched one of the filesystem tests to use our wrapped version     of NamedTemporaryFile and in doing so, caught triaged and fixed     an actual bug in that code -- which I believe is how this whole     thing is supposed to work in the first place, right? Right. ... a few assorted touchups to the filesystem module have also made     it in there, I do believe. [Alexander Böhn]

### Other

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


## v0.1.4 (2019-07-09)

### Add

* Added “dict_types” to clu.typology ... fully clarified a few imports from clu.constants.polyfills too. [Alexander Böhn]

### Other

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


## v0.1.3 (2019-07-09)

### Add

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

### Other

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


## v0.1.2 (2019-07-02)

### Add

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

### Other

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

* Minutiae. [Alexander Böhn]

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


## v0.1.1 (2019-06-26)

### Add

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

### Other

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

* Minutiae II. [Alexander Böhn]

* Sorted out a ton of stuff w/r/t modes and permissions. [Alexander Böhn]

* Git-ignoring .tm_properties. [Alexander Böhn]

* ANSI text printing works on the command line. [Alexander Böhn]

* Fixed CSDIL enum’s __index__(…) method. [Alexander Böhn]

* ANSI metaclass name-lookup method now considers aliases. [Alexander Böhn]

* Minutiae. [Alexander Böhn]

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


