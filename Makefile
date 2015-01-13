.PHONY: clean lint test testall coverage release sdist

help:
	@echo "clean - remove build and Python artifacts"
	@echo "lint - run flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 tinyblog
	flake8 tests

test:
	python setup.py test

testall:
	tox

coverage:
	coverage run --source tinyblog setup.py test
	coverage report -m

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	ls -l dist
