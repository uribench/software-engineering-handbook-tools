#!/usr/bin/env python3

"""
Dispatcher for commands to build and maintain the Software Engineering Handbook.

Usage:
  handbook [options] <command> [<args>...]
  handbook (-h|--help)
  handbook (--version)

Options:
  -h, --help        Show this help message and exit
  --version         Show the version and exit
  --verbose         Print warning messages
  --root=PATH       Site root. When not provided, current directory will be used.
                    May also be specified using HANDBOOK_ROOT environment variable.

Commands:
{commands}

Examples:
  handbook -h
  handbook some-command -h
  handbook some-command --version
  handbook some-command
  handbook --root=tests/fixtures/site some-command

Environment Variables:
  HANDBOOK_ROOT     Optionally set this variable to define the handbook root
"""

import os
import sys
import pkgutil
from docopt import docopt
from docopt import DocoptExit
from handbook_tools import __version__ as VERSION

def main():
    """Program entry point"""
    this_dir = os.path.abspath(os.path.dirname(__file__))
    commands = _load_commands(os.path.join(this_dir, 'commands'))
    command_name, command_args, global_args = _process_args(commands)

    try:
        command_class = getattr(commands[command_name], command_name.capitalize())
    except AttributeError:
        print('Error: Unknown command')
        raise DocoptExit()

    command = command_class(command_args, global_args)
    command.execute()

def _load_commands(dirname):
    """"""
    commands = {}
    for finder, name, _ in pkgutil.iter_modules([dirname]):
        if name not in sys.modules:
            module = finder.find_module(name).load_module(name)
            commands.update({name: module})

    return commands

def _process_args(commands):
    """"""
    usage = _append_commands_and_summaries_to_usage(__doc__, commands)
    args = docopt(usage, version=VERSION, options_first=True)

    command_name = args.pop('<command>')
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}
    # after removing the command_name and command_args,
    # what is left is considered global_args
    global_args = args

    return command_name, command_args, global_args

def _append_commands_and_summaries_to_usage(usage, commands):
    """"""
    sorted_commands = sorted(commands.items())
    style_fore_green = '\x1b[0;32m'
    style_reset_all = '\x1b[0m'
    commands_and_summaries = ''
    for name, module in sorted_commands:
        command_class = getattr(module, name.capitalize())
        # do not instantiate the class. use its class method directly.
        summary = command_class.summary_description()
        commands_and_summaries += \
            '  {}{: <18}{}{}\n'.format(style_fore_green, name, style_reset_all, summary)

    return usage.format(commands=commands_and_summaries)

if __name__ == '__main__':
    main()
