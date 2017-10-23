======================
pipenv-to-requirements
======================

.. image:: https://travis-ci.org/Stibbons/pipenv-to-requirements.svg?branch=master
    :target: https://travis-ci.org/Stibbons/pipenv-to-requirements
.. image:: https://badge.fury.io/py/pipenv-to-requirements.svg
   :target: https://pypi.python.org/pypi/pipenv-to-requirements/
   :alt: Pypi package
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

Generate ``requirements[-dev].txt`` from ``Pipfile`` (using ``pipenv``)

* Free software: MIT
* Documentation: https://pipenv-to-requirements.readthedocs.org/en/latest/
* Source: https://github.com/Stibbons/pipenv-to-requirements

Rational
--------

``Pipfile`` and its sibling ``Pipfile.lock`` are clearly superior tools defining clear dependencies
or a package. ``Pipfile`` is to be maintained by the package's developer while ``Pipfile.lock``
represent a clear image of what is currently installed on the current system, guarantying full
reproductibility of the setup. See more information about `Pipfile format here
<https://github.com/pypa/pipfile>`_. Most of the time, ``Pipfile.lock`` should be ignored (ie, not
tracked in your git) for packages published on Pypi.

`pipenv <https://github.com/kennethreitz/pipenv>`_ is a great tool to maintain ``Pipfile``, but
developers might be stuck with backward compatibility issues for tools and services that still use
`requirements.txt` and does not know how to handle ``Pipfile`` or ``Pipfile.lock`` yet.
For examples:

- ReadTheDocs
- Pyup


Usage
-----

Just before building source/binary/wheel package of your python module, just execute:

To generated frozen dependencies:

    pipenv run pipenv_to_requirements -f

For not frozen dependencies:

    pipenv run pipenv_to_requirements

It will generate `requirements.txt` and, if applicable, `requirements-dev.txt` in the current
directory.

Contributing
------------

Create your development environment with

    .. code-block:: bash

        $ make dev

Execute unit tests:

    .. code-block:: bash

        $ make test

Build source, binary and wheels packages:

    .. code-block:: bash

        $ make dist

Code Style Checks:

    .. code-block:: bash

        $ make check

Code formatter:

    .. code-block:: bash

        $ make style

Create a release:

    .. code-block:: bash

        make requirements
        git tag 1.2.3
        make push

On successful travis build on the Tag branch, your Pypi package will be updated automatically.
