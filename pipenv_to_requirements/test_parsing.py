# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

import pipenv_to_requirements
# pylint: disable=import-error
import pipfile

# pylint: enable=import-error

VECTORS_FOLDER = os.path.join(os.path.dirname(__file__), "vectors")


class TestParsing(object):
    @staticmethod
    def load_requirements(name):
        with open(os.path.join(VECTORS_FOLDER, name)) as f:
            return [l.strip() for l in f.readlines()]

    @staticmethod
    def load_vector_pipfile(name):
        pipfile_location = os.path.join(VECTORS_FOLDER, name)
        pfile = pipfile.load(pipfile_location)
        pipfile_json = json.loads(pfile.lock())
        return pipfile_json

    def test_normal(self):
        pipfile_json = self.load_vector_pipfile("Pipfile.normal")

        requirements = pipenv_to_requirements.parse_pip_file(pipfile_json, "default")
        requirements_dev = pipenv_to_requirements.parse_pip_file(pipfile_json, "develop")

        expected_requirements = self.load_requirements("Pipfile.normal.requirements.txt")
        assert sorted(requirements) == sorted(expected_requirements)

        expected_requirements_dev = self.load_requirements("Pipfile.normal.requirements-dev.txt")
        assert sorted(requirements_dev) == sorted(expected_requirements_dev)

    def test_editable(self):
        pipfile_json = self.load_vector_pipfile("Pipfile.editable")

        requirements = pipenv_to_requirements.parse_pip_file(pipfile_json, "default")
        requirements_dev = pipenv_to_requirements.parse_pip_file(pipfile_json, "develop")

        expected_requirements = self.load_requirements("Pipfile.editable.requirements.txt")
        assert sorted(requirements) == sorted(expected_requirements)

        expected_requirements_dev = self.load_requirements("Pipfile.editable.requirements-dev.txt")
        assert sorted(requirements_dev) == sorted(expected_requirements_dev)

    def test_markers(self):
        pipfile_json = self.load_vector_pipfile("Pipfile.markers")

        requirements = pipenv_to_requirements.parse_pip_file(pipfile_json, "default")
        requirements_dev = pipenv_to_requirements.parse_pip_file(pipfile_json, "develop")

        expected_requirements = self.load_requirements("Pipfile.markers.requirements.txt")
        assert sorted(requirements) == sorted(expected_requirements)

        print(requirements_dev)
        expected_requirements_dev = self.load_requirements("Pipfile.markers.requirements-dev.txt")
        assert sorted(requirements_dev) == sorted(expected_requirements_dev)
