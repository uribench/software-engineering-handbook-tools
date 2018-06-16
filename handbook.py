#!/usr/bin/env python3

"""
Dispatcher for commands to build and maintain the Software Engineering Handbook.

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

def main():
    """"""
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

    command = command_class(command_args, global_args)

    command.execute()

if __name__ == '__main__':
    main()