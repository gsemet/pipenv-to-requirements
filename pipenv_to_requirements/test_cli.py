from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest

from pipenv_to_requirements import main

# pylint: disable=redefined-outer-name, unused-argument


@pytest.fixture
def fake_pipenv(mocker):
    fake_pipenv_project = mocker.patch("pipenv_to_requirements.Project")
    fake_pipenv_project2 = mocker.Mock()
    fake_pipenv_project2._lockfile = fake_pipenv_project2.lockfile_content = {
        "develop": {
            "dev-n1": "v1",
            "dev-n2": "v2"
        },
        "default": {
            "def-n1": "v1",
            "def-n2": "v2"
        }
    }
    fake_pipenv_project.return_value = fake_pipenv_project2
    mocker.patch("pipenv_to_requirements.parse_pip_file")


def test_no_opt(fake_pipenv, mocker, fs):
    fake_args = mocker.Mock("fake_args")
    fake_args.output = None
    fake_args.dev_output = None
    fake_args.freeze = None
    mocker.patch("pipenv_to_requirements.parse_args", return_value=fake_args)

    main()
    assert os.path.exists('requirements.txt')
    assert os.path.exists('requirements-dev.txt')


def test_opt_output(fake_pipenv, mocker, fs):
    fake_args = mocker.Mock("fake_args")
    fake_args.output = "requirements-custom.txt"
    fake_args.dev_output = None
    fake_args.freeze = None
    mocker.patch("pipenv_to_requirements.parse_args", return_value=fake_args)

    main()
    assert os.path.exists('requirements-custom.txt')
    assert not os.path.exists('requirements-dev.txt')


def test_opt_dev_output(fake_pipenv, mocker, fs):
    fake_args = mocker.Mock("fake_args")
    fake_args.output = None
    fake_args.dev_output = "requirements-dev-custom.txt"
    fake_args.freeze = None
    mocker.patch("pipenv_to_requirements.parse_args", return_value=fake_args)

    main()
    assert not os.path.exists('requirements.txt')
    assert os.path.exists('requirements-dev-custom.txt')


def test_opt_dev_output_freeze(fake_pipenv, mocker, fs):
    fake_args = mocker.Mock("fake_args")
    fake_args.output = None
    fake_args.dev_output = "requirements-dev-custom.txt"
    fake_args.freeze = True
    mocker.patch("pipenv_to_requirements.parse_args", return_value=fake_args)

    main()
    assert not os.path.exists('requirements.txt')
    assert os.path.exists('requirements-dev-custom.txt')


def test_opt_output_and_dev_output(fake_pipenv, mocker, fs):
    fake_args = mocker.Mock("fake_args")
    fake_args.output = "requirements-custom.txt"
    fake_args.dev_output = "requirements-dev-custom.txt"
    fake_args.freeze = None
    mocker.patch("pipenv_to_requirements.parse_args", return_value=fake_args)

    main()
    assert os.path.exists('requirements-custom.txt')
    assert os.path.exists('requirements-dev-custom.txt')
