
PROJECT_NAME = clu
CLU_REPL_SCRIPT = $(PROJECT_BASE)/$(PROJECT_NAME)/scripts/repl.py

clean: clean-cython clean-build-artifacts clean-pyc

distclean: clean-cython clean-test-artifacts clean-build-artifacts

rebuild: clean-build-artifacts cython

upload: clean-build-artifacts changelog bump twine-upload
	git push

bigupload: clean-build-artifacts changelog bigbump twine-upload
	git push

clean-pyc:
	find $(PROJECT_BASE) -name \*.pyc -print -delete

clean-cython:
	find $(PROJECT_BASE) -name \*.so -print -delete

clean-build-artifacts:
	rm -rf build dist python_$(PROJECT_NAME).egg-info

clean-test-artifacts:
	rm -rf  $(PROJECT_ROOT)/.pytest_cache $(PROJECT_BASE)/.pytest_cache $(PROJECT_BASE)/.nox

clean-type-caches:
	rm -rf $(PROJECT_VENV)/var/cache/mypy_cache
	rm -rf $(PROJECT_VENV)/var/cache/pytype

cython:
	python -m setup build_ext --inplace

sdist:
	python -m build

wheel:
	python -m build -w

twine-upload: sdist
	twine upload -s $(PROJECT_BASE)/dist/*

bump:
	bump-my-version bump patch --verbose

bigbump:
	bump-my-version bump minor --verbose

check: clean-test-artifacts
	check-manifest -v
	travis lint .travis.yml

mypy:
	mypy --config-file mypy.ini

pytype:
	pytype --config pytype.cfg --verbosity=2

pytest:
	python -m pytest -p clu.testing.pytest

nox:
	nox --report $(PROJECT_BASE)/.noxresults.json

renox: clean-test-artifacts nox

test: check pytest

test-all: check nox

test-configuration:
	python -m pytest --setup-plan --trace-config | pygmentize -l clean -O "style=vim"

version:
	python -m clu.version

consts:
	python -m clu.constants

modules:
	python -m clu

remove-changelog:
	rm -f CHANGELOG.md

changelog: remove-changelog
	gitchangelog > CHANGELOG.md
	git addremove .
	git commit -m "[make] Changelog updated @ $(shell git rev-parse --short HEAD)"

repl:
	python -m bpython --config=$(PROJECT_ROOT)/.config/bpython/config.py3 -i $(CLU_REPL_SCRIPT)

ipy:
	python -m IPython --autoindent --pylab --colors=LightBG --config=$(PROJECT_ROOT)/.config/ipython/config3.py -i $(CLU_REPL_SCRIPT)

ptpy:
	python -m ptpython -i $(CLU_REPL_SCRIPT)

# this loads the system IPython, not the virtualenv:
ptipy:
	ptipython -i $(CLU_REPL_SCRIPT)

coverage:
	python -m pytest -p pytest_cov --cov=$(PROJECT_NAME) tests/

.PHONY: clean distclean rebuild
.PHONY: upload bigupload
.PHONY: clean-pyc clean-cython
.PHONY: clean-build-artifacts clean-test-artifacts clean-pytest-artifacts

.PHONY: cython sdist wheel twine-upload bump bigbump

.PHONY: check pytest nox renox
.PHONY: test test-all

.PHONY: version consts-old modules-old consts modules
.PHONY: repl ipy ptpy ptipy