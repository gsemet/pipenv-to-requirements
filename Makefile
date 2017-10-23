.PHONY: build

MODULE:=pipenv-to-requirements

all: dev style checks build dists test-unit

dev:
	@pipenv install --dev --skip-lock

style: isort autopep8 yapf

isort:
	@pipenv run isort -y

autopep8:
	@pipenv run autopep8 --in-place --recursive setup.py $(MODULE)

yapf:
	@pipenv run yapf --style .yapf --recursive -i $(MODULE)

checks: flake8 pylint

flake8:
	@pipenv run python setup.py flake8

pylint:
	@pipenv run pylint --rcfile=.pylintrc --output-format=colorized $(MODULE)

build: dists

shell:
	@pipenv shell

test-unit:
	@pipenv run pytest $(MODULE)

test-coverage:
	pipenv run py.test -v --cov $(MODULE) --cov-report term-missing

dists: sdist bdist wheels

sdist:
	@pipenv run python setup.py sdist

bdist:
	@pipenv run python setup.py bdist

wheels:
	@pipenv run python setup.py bdist_wheel

pypi-publish: build
	@pipenv run python setup.py upload -r pypi

update:
	@pipenv update

githook: style

push: githook
	@git push origin --tags

# aliases to gracefully handle typos on poor dev's terminal
check: checks
devel: dev
develop: dev
dist: dists
install: install-system
pypi: pypi-publish
styles: style
test: test-unit
unittest: test-unit
wheel: wheels
