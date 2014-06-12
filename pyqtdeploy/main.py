#!/usr/bin/env python3

# Copyright (c) 2014, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import argparse
import os
import sys


# The entry point for the setuptools generated wrapper.
def main():
    # Parse the command line.
    parser = argparse.ArgumentParser()

    parser.add_argument('action',
            help="the action to perform, otherwise the GUI is started",
            nargs='?', metavar="build|configure|show-packages")
    parser.add_argument('--output',
            help="the name of the output file (configure) or directory (build)",
            metavar="OUTPUT")
    parser.add_argument('--package', help="the package name (configure)",
            metavar="PACKAGE")
    parser.add_argument('--project', help="the project file (build)",
            metavar="FILE")
    parser.add_argument('--target', help="the target platform (configure)",
            metavar="TARGET")
    parser.add_argument('--quiet', help="disable progress messages (build)",
            action='store_true')
    parser.add_argument('--verbose',
            help="enable verbose progress messages (build)",
            action='store_true')

    args = parser.parse_args()

    # Handle the specific actions.
    if args.action == 'build':
        rc = build(args)
    elif args.action == 'configure':
        rc = configure(args)
    elif args.action == 'show-packages':
        rc = show_packages(args)
    else:
        rc = gui(args)

    return rc


def gui(args):
    """ Start the GUI. """

    # Interpret any action as a project file.
    if args.action is not None:
        project_file = args.action
    elif args.project is not None:
        project_file = args.project
    else:
        project_file = None

    from PyQt5.QtWidgets import QApplication

    from . import Project, ProjectGUI

    app = QApplication(sys.argv, applicationName='pyqtdeploy',
                organizationDomain='riverbankcomputing.com',
                organizationName='Riverbank Computing')

    if project_file is None:
        project = Project()
    else:
        project = ProjectGUI.load(project_file)
        if project is None:
            return 1

    gui = ProjectGUI(project)
    gui.show()

    return app.exec()


def build(args):
    """ Perform the build action. """

    if args.project is None:
        missing_argument('--project')
        return 2

    from . import Builder, Project, UserException

    try:
        builder = Builder(Project.load(args.project))
        builder.quiet = args.quiet
        builder.verbose = args.verbose
        builder.build(args.output)
    except UserException as e:
        handle_exception(e)
        return 1

    return 0


def configure(args):
    """ Perform the configure action. """

    if args.package is None:
        missing_argument('--package')
        return 2

    from . import configure_package, UserException

    try:
        configure_package(args.package, args.target, args.output)
    except UserException as e:
        handle_exception(e)
        return 1

    return 0


def show_packages(args):
    """ Perform the show-packages action. """

    from . import show_packages, UserException

    try:
        show_packages()
    except UserException as e:
        handle_exception(e)
        return 1

    return 0


def missing_argument(name):
    """ Tell the user about a missing argument. """

    # Mimic the argparse message.
    print(
            "{0}: error: the following arguments are required: {1}".format(
                    os.path.basename(sys.argv[0]), name),
            file=sys.stderr)


def handle_exception(e):
    """ Tell the user about an exception. """

    print("{0}: {1}".format(os.path.basename(sys.argv[0]), e.text),
            file=sys.stderr)
