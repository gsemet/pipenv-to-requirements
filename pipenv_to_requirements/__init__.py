# -*- coding: utf-8 -*-

import argparse
import logging
import sys

# pylint: disable=wrong-import-position
from pipenv.project import Project

logging.basicConfig(level=logging.INFO)

# pylint: disable=undefined-variable
if sys.version_info < (3, 0):

    def isstr(astring):
        return isinstance(astring, basestring)
else:

    def isstr(astring):
        return isinstance(astring, str)


# pylint: enable=undefined-variable

# pylint: enable=wrong-import-position


def clean_version(pkg_name, pkg_info):
    if isstr(pkg_info):
        if pkg_info.strip() == "*":
            return pkg_name
        return "{}{}".format(pkg_name, pkg_info)
    if not pkg_info:
        return pkg_name
    version = pkg_info.get("version", "").strip()
    editable = pkg_info.get("editable", False)
    markers = pkg_info["markers"].strip() if pkg_info.get("markers") else ""
    extras = pkg_info.get("extras", [])
    subdir = pkg_info.get("subdirectory", [])
    git = pkg_info.get("git", "").strip()
    path = pkg_info.get("path", "").strip()
    ref = pkg_info.get("ref", "").strip()
    rstr = ""
    if not editable:
        rstr += pkg_name

    if extras:
        rstr += "[{}]".format(', '.join([s.strip() for s in extras]))

    if not editable:
        if version and version != "*":
            rstr += version.strip()
    elif git:
        ref = "@" + ref if ref else ref
        rstr = "-e git+" + git + ref + "#egg=" + pkg_name
        if subdir:
            rstr += '&subdirectory=' + subdir
    else:
        rstr = "-e " + path
    if markers:
        rstr += " ; " + markers
    return rstr


def parse_pip_file(pipfile, section):
    return [clean_version(n, i) for n, i in pipfile.get(section, {}).items()]


def parse_args():
    parser = argparse.ArgumentParser(description='Generate requirements*.txt matching Pipfile*')
    parser.add_argument('-o',
                        '--output',
                        help=('Generate only the main packages to a different file, '
                              'instead of requirements.txt'))
    parser.add_argument('-d',
                        '--dev-output',
                        help=('Generate only dev packages to a different file, '
                              'instead of requirements-dev.txt'))
    parser.add_argument('-f',
                        '--freeze',
                        action="store_true",
                        help='Generate requirements*.txt with frozen versions')

    parser.add_argument('-q',
                        '--quiet',
                        action="store_true",
                        help="Run silently without outputting logs")

    args = parser.parse_args()
    return args


def get_logger(is_quiet):
    logger = logging.getLogger(__name__)
    if is_quiet:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.INFO)
    return logger


def main():

    args = parse_args()

    logger = get_logger(args.quiet)

    if args.freeze:
        pipfile = Project().lockfile_content
    else:
        # pylint: disable=protected-access
        pipfile = Project()._lockfile
        # pylint: enable=protected-access
        if callable(pipfile):
            pipfile = pipfile()

    def_req = parse_pip_file(pipfile, 'default')
    dev_req = parse_pip_file(pipfile, "develop")

    intro = [
        "################################################################################",
        "# This requirements file has been automatically generated from `Pipfile` with",
        '# `pipenv-to-requirements`', '#', '#',
        '# This has been done to maintain backward compatibility with tools and services',
        '# that do not support `Pipfile` yet.', '#',
        "# Do NOT edit it directly, use `pipenv install [-d]` to modify `Pipfile` and",
        "# `Pipfile.lock` and then regenerate `requirements*.txt`.",
        "################################################################################", ""
    ]

    if def_req:
        if args.output:
            requirement_txt = args.output
        elif args.dev_output:
            # if -d without -o, do not generate packages, for compatibility sake
            requirement_txt = None
        else:
            requirement_txt = "requirements.txt"
        if requirement_txt:
            with open(requirement_txt, "w") as f:
                f.write("\n".join(intro + sorted(def_req)) + "\n")
            logger.info("generated: %s", requirement_txt)

    if dev_req:
        if args.dev_output:
            requirement_txt = args.dev_output
        elif args.output:
            # if -o without -d, do not generate dev packages, for compatibility sake
            requirement_txt = None
        else:
            requirement_txt = "requirements-dev.txt"
        if requirement_txt:
            with open(requirement_txt, "w") as f:
                f.write("\n".join(intro + sorted(dev_req)) + "\n")
            logger.info("generated: %s", requirement_txt)
