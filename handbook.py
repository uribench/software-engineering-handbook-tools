#!/usr/bin/env python3
"""
Dispatcher for commands to build and maintain the Software Engineering Handbook

Usage:
    handbook [options] <command> [<args>...]

Options:
    -h, --help      show this help message and exit
    -v, --version   show the version and exit
    --verbose       print warning messages
    --root=PATH     site root [default: ../software-engineering-handbook] 

The subcommands are:
    build           builds the handbook navigation (directories and navigation files)
    toc             generates a table of contents
    verify          verifies various aspects of the handbook
"""

from docopt import docopt
from docopt import DocoptExit

import commands

__version__ = '0.1.0'


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__, options_first=True)

    command_name = args.pop('<command>').capitalize()
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}
    global_args = args

    try:
        command_class = getattr(commands, command_name)
    except AttributeError:
        print('Error: Unknown command')
        raise DocoptExit()

    # global parameters not exposed as program arguments
    global_params = {
        # one or more YAML navigation configuration files
        'navigationPath': 'config/navigation/',
        # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
        'rootConfigFile': 'root.yml',
        # optional YAML files with custom content for the index.md files
        'metadataPath': 'config/metadata/'
    }

    command = command_class(command_args, global_args, global_params)

    command.execute()
