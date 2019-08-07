
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
	find . -name \*.pyc -print -delete

clean-cython:
	find $(PROJECT_NAME)/ -name \*.so -print -delete

clean-build-artifacts:
	rm -rf build dist python_$(PROJECT_NAME).egg-info

clean-test-artifacts: clean-pyc
	rm -rf ../.pytest_cache ../.hypothesis .pytest_cache .hypothesis .tox

cython:
	python setup.py build_ext --inplace

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

twine-upload: cython sdist wheel
	twine upload -s dist/*

bump:
	bumpversion --verbose patch

bigbump:
	bumpversion --verbose minor

check: clean-test-artifacts
	check-manifest -v
	python setup.py check -m -s
	travis lint .travis.yml

pytest:
	python -m pytest -p clu.testing.pytest

tox:
	tox

test: check pytest

test-all: check tox

.PHONY: clean distclean rebuild
.PHONY: dist upload bigupload
.PHONY: clean-pyc clean-cython
.PHONY: clean-build-artifacts clean-test-artifacts clean-pytest-artifacts

.PHONY: cython sdist wheel twine-upload bump bigbump

.PHONY: check pytest tox test test-all

