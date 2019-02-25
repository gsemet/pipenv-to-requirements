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

dev: mk-venv
	pipenv install --dev
	pipenv run pip install -e .

dev-ci: mk-venv
	pipenv install --dev --deploy
	pipenv run pip install -e .

dev-py2: mk-venv
	pipenv install --dev --two
	pipenv run pip install -e .

mk-venv:
	rm -rf .venv
	mkdir -p .venv

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
	pipenv run pytest -v $(MODULE)

test-v:
	pipenv run pytest -vs $(MODULE)

test-verbose:
	pipenv run pytest -s $(MODULE)

test-coverage:
	pipenv run py.test -v --cov $(MODULE) --cov-report term-missing

dists: requirements sdist wheels

requirements:
	pipenv run pipenv_to_requirements

release: requirements

sdist: requirements
	pipenv run python setup.py sdist

bdist: requirements
	pipenv run python setup.py bdist

wheels: requirements
	pipenv run python setup.py bdist_wheel

pypi-publish: clean-dist build release
	pipenv run twine upload --repository-url=https://upload.pypi.org/legacy/ dist/*.whl dist/*.gz

update:
	pipenv update --clear

githook: style

push: githook
	@git push origin --tags

clean: clean-dist
	pipenv --rm
	rm -rf .venv

clean-dist:
	rm -rf dist/

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
ut: test
