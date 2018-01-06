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

Generate ``requirements[-dev].txt`` from ``Pipfile`` (using ``pipenv``).

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

- `ReadTheDocs <https://github.com/rtfd/readthedocs.org/issues/3181>`_
- `Pyup <https://github.com/pyupio/pyup/issues/197>`_
- ``pip install`` (if you install a package with ``pip`` that does not have a ``requirements.txt``,
  its dependencies won't be installed, even if you use ``Pipfile``)


Usage
-----

Just before building source/binary/wheel package of your python module, only of the following
commands:

- To generate requirements files (ie, dependencies are described eventually by range):

    .. code-block:: bash

        pipenv run pipenv_to_requirements

- To generate frozen requirements (ie, all dependencies have their version frozen):

    .. code-block:: bash

        pipenv run pipenv_to_requirements -f

It will generate ``requirements.txt`` and, if applicable, ``requirements-dev.txt``, in the current
directory.

ReadTheDocs
-----------

Simply commit these files in your tree so that readthedocs, and ensure they are synchronized each
time you change your ``Pipfile``. Do not forget to ask ReadTheDocs to use ``requirements-dev.txt``
when building the documentation.

Contributing
------------

Create your development environment with

.. code-block:: bash

    $ make dev

Execute unit tests:

.. code-block:: bash

    $ make test

Code formatter:

.. code-block:: bash

    $ make style

Code Style Checks:

.. code-block:: bash

    $ make check
