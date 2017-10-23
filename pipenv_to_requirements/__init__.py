# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from pipenv.project import Project


def clean_version(pkg_name, version):
    if not version:
        return pkg_name
    if isinstance(version, str):
        if version.strip() == "*":
            return pkg_name
        return "{}{}".format(pkg_name, version)
    if 'editable' in version:
        return "-e ."


def formatPipenvEntryForRequirements(pkg_name, pkg_info):
    return clean_version(pkg_name, pkg_info["version"].strip()
                         if "version" in pkg_info else pkg_info)


def parse_pip_file(pipfile, section):
    return [formatPipenvEntryForRequirements(n, i) for n, i in pipfile.get(section, {}).items()]


def main():

    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage: ")
        print("  pipenv-to-requirements [-f|--freeze]")
        print()
        print("Options:")
        print("  -f --freeze    Generate requirements*.txt with frozen dependencies")
        sys.exit(0)

    if "-f" in sys.argv or "--freeze" in sys.argv:
        pipfile = Project().lockfile_content
    else:
        # pylint: disable=protected-access
        pipfile = Project()._lockfile
        # pylint: enable=protected-access

    def_req = parse_pip_file(pipfile, "default")
    dev_req = parse_pip_file(pipfile, "develop")

    # Create pip-compatible dependency list
    def_req = [
        formatPipenvEntryForRequirements(n, i) for n, i in pipfile.get("default", {}).items()
    ]
    dev_req = [
        formatPipenvEntryForRequirements(n, i) for n, i in pipfile.get("develop", {}).items()
    ]

    intro = [
        "################################################################################",
        "# This requirements files has been automatically generated from `Pipfile` with",
        '# `pipenv-to-requirements`', '#', '#'
        '# This has been done to maintain backward compatibility with tools and services',
        '# that does not support `Pipfile` yet.', '#'
        "# Do NOT edit it directly, use `pipenv install [-d]` to modify `Pipfile` and",
        "# `Pipfile.lock`",
        "################################################################################", ""
    ]

    if def_req:
        with open("requirements.txt", "w") as f:
            f.write("\n".join(intro + sorted(def_req)))
        print("generated: requirements.txt")

    if dev_req:
        with open("requirements-dev.txt", "w") as f:
            f.write("\n".join(intro + sorted(dev_req)))
        print("generated: requirements-dev.txt")
