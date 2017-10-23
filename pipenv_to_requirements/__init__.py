# -*- coding: utf-8 -*-

import sys
from pipenv.project import Project


def formatPipenvEntryForRequirements(pkg_name, pkg_info):
    return "{name}{version}".format(
        name=pkg_name,
        version=pkg_info.get("version", "").strip(),
    )


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
        pipfile = Project()._lockfile

    # Create pip-compatible dependency list
    pipfile = Project().lockfile_content
    def_req = [
        formatPipenvEntryForRequirements(n, i) for n, i in pipfile.get("default", {}).items()
    ]
    dev_req = [
        formatPipenvEntryForRequirements(n, i) for n, i in pipfile.get("develop", {}).items()
    ]

    intro = [
        "################################################################################",
        "# This requirements files has been automatically generated from `Pipfile.lock`",
        '# with `pipenv-to-requirements`', '#',
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
