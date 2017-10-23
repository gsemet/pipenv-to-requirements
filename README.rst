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

Generate `requirements[-dev].txt` from `Pipfile` (using `pipenv`)

* Free software: MIT
* Documentation: https://pipenv-to-requirements.readthedocs.org/en/latest/
* Source: https://github.com/Stibbons/pipenv-to-requirements


Usage
-----

Just before building source/binary/wheel package of your python module, just execute:

To generated frozen dependencies:

    pipenv run pipenv_to_requirements -f

For not frozen dependencies:

    pipenv run pipenv_to_requirements


Contributing
------------

Create your development environment with

    .. code-block:: bash

        $ make dev

Execute unit tests:

    .. code-block:: bash

        $ make test

Build source package:

    Use it for most package without low level system dependencies.

    .. code-block:: bash

        $ make sdist

Code Style Checks:

    .. code-block:: bash

        $ make check

Code formatter:

    .. code-block:: bash

        $ make style

Create a release:

    .. code-block:: bash

        git tag 1.2.3
        make push

    On successful travis build on the Tag branch, your Pypi package will be updated automatically.
