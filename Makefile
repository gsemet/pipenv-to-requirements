.PHONY: build

MODULE:=pipenv_to_requirements

all: ensure-pip dev style checks dists test

ensure-pip:
	pip install --user --upgrade pipenv pip
	pip --version
	pipenv --version

ensure-pip-ci:
	pip install --upgrade pipenv pip
	pip --version
	pipenv --version

dev:
	pipenv install --dev
	pipenv run pip install -e .

dev-ci:
	pipenv install --dev --skip-lock
	pipenv run pip install -e .

dev-py2:
	pipenv install --dev --two
	pipenv run pip install -e .

style: isort autopep8 yapf

isort:
	pipenv run isort -y

autopep8:
	pipenv run autopep8 --in-place --recursive setup.py $(MODULE)

yapf:
	pipenv run yapf --style .yapf --recursive -i $(MODULE)

checks: flake8 pylint

flake8:
	pipenv run python setup.py flake8

pylint:
	pipenv run pylint --rcfile=.pylintrc --output-format=colorized $(MODULE)

sc: style checks
sct: style checks test

build: dists

test:
	pipenv run pytest $(MODULE)

test-verbose:
	pipenv run pytest -s $(MODULE)

test-coverage:
	pipenv run py.test -v --cov $(MODULE) --cov-report term-missing

dists: requirements sdist bdist wheels

requirements:
	pipenv run pipenv_to_requirements

release: requirements

sdist: requirements
	pipenv run python setup.py sdist

bdist: requirements
	pipenv run python setup.py bdist

wheels: requirements
	pipenv run python setup.py bdist_wheel

pypi-publish: build release
	pipenv run python setup.py upload -r pypi

update:
	pipenv update

githook: style

push: githook
	@git push origin --tags

clean:
	pipenv --rm

prepare-release: requirements

# aliases to gracefully handle typos on poor dev's terminal
check: checks
devel: dev
develop: dev
dist: dists
install: install-system
pypi: pypi-publish
styles: style
wheel: wheels
