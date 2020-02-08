
PROJECT_NAME = clu

clean: clean-cython clean-build-artifacts clean-pyc

distclean: clean-cython clean-test-artifacts clean-build-artifacts

rebuild: clean-build-artifacts cython

dist: twine-upload

upload: clean-build-artifacts bump dist
	git push

bigupload: clean-build-artifacts bigbump dist
	git push

clean-pyc:
	find $(PROJECT_BASE) -name \*.pyc -print -delete

clean-cython:
	find $(PROJECT_BASE) -name \*.so -print -delete

clean-build-artifacts:
	rm -rf build dist python_$(PROJECT_NAME).egg-info

clean-test-artifacts: clean-pyc
	rm -rf  $(PROJECT_ROOT)/.pytest_cache \
			$(PROJECT_ROOT)/.hypothesis \
			$(PROJECT_BASE)/.pytest_cache \
			$(PROJECT_BASE)/.hypothesis \
			$(PROJECT_BASE)/.nox \
			$(PROJECT_BASE)/.tox

clean-type-caches:
	rm -rf $(PROJECT_VENV)/var/cache/mypy_cache
	rm -rf $(PROJECT_VENV)/var/cache/pytype

cython:
	python setup.py build_ext --inplace

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

twine-upload: cython sdist wheel
	twine upload -s $(PROJECT_BASE)/dist/*

bump:
	bumpversion --verbose patch

bigbump:
	bumpversion --verbose minor

check: clean-test-artifacts
	check-manifest -v
	python setup.py check -m -s
	travis lint .travis.yml

mypy:
	mypy --config-file mypy.ini

pytype:
	pytype --config pytype.cfg --verbosity=2

pytest:
	python -m pytest -p clu.testing.pytest

tox:
	tox

nox:
	nox

renox: clean-test-artifacts
	nox

test: check pytest

test-all: check nox

# python -m pytest --setup-plan --trace-config | pygmentize -l eiffel -O "style=monokai"
# python -m pytest --setup-plan --trace-config | pygmentize -l cry -O "style=vim"
# python -m pytest --setup-plan --trace-config | pygmentize -l aconf -O "style=vim"
# python -m pytest --setup-plan --trace-config | pygmentize -l hs -O "style=friendly"

test-configuration:
	python -m pytest --setup-plan --trace-config | pygmentize -l clean -O "style=vim"

version:
	python -m clu.version

consts-old:
	DEBUG=1 PYTHONPATH="." $(PROJECT_BASE)/clu/scripts/show-consts.py

modules-old:
	DEBUG=1 PYTHONPATH="." $(PROJECT_BASE)/clu/scripts/show-modules.py

consts:
	python -m clu.constants

modules:
	python -m clu

remove-changelog:
	rm -f CHANGELOG.md

changelog: remove-changelog
	gitchangelog > CHANGELOG.md

repl:
	python -m bpython --config=$(PROJECT_ROOT)/.config/bpython/config.py3 \
			-i $(PROJECT_BASE)/clu/scripts/repl.py

ipy:
	python -m IPython --autoindent --pylab --colors=LightBG \
			--config=$(PROJECT_ROOT)/.config/ipython/config3.py \
			-i $(PROJECT_BASE)/clu/scripts/repl.py

ptpy:
	python -m ptpython -i $(PROJECT_BASE)/clu/scripts/repl.py

# this loads the system IPython, not the virtualenv:
ptipy:
	ptipython -i $(PROJECT_BASE)/clu/scripts/repl.py

.PHONY: clean distclean rebuild
.PHONY: dist upload bigupload
.PHONY: clean-pyc clean-cython
.PHONY: clean-build-artifacts clean-test-artifacts clean-pytest-artifacts

.PHONY: cython sdist wheel twine-upload bump bigbump

.PHONY: check pytest tox nox renox
.PHONY: test test-all

.PHONY: version consts-old modules-old consts modules
.PHONY: repl ipy ptpy ptipy