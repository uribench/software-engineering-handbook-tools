#!/usr/bin/env python3

"""
Dispatcher for commands to build and maintain the Software Engineering Handbook.

Usage:
  handbook.py [options] <command> [<args>...]
  handbook.py (-h|--help)
  handbook.py (-v|--version)

Options:
  -h, --help        show this help message and exit
  -v, --version     show the version and exit
  --verbose         print warning messages
  --root=PATH       site root

Commands:
{commands}

Examples:
  handbook.py -h
  handbook.py some-command -h
  handbook.py some-command --version
  handbook.py some-command
  handbook.py --root=tests/fixtures/site some-command

Environment:
  The location of the root of the Software Engineering HandbookWhen is determined
  using the following process:
    If no value is provided for the '--root' option, then the value of $HANDBOOK_ROOT
    environment variable is used when such exists. Otherwise the program terminates and
    the user is notified accordingly.
  Set the $HANDBOOK_ROOT environment variable based on the structure of your file system.
  By default, this repository uses 'direnv' configuration file (.envrc) with:
    export HANDBOOK_ROOT=../software-engineering-handbook
"""

import sys
import pkgutil
from docopt import docopt
from docopt import DocoptExit

__version__ = '0.2.2'

def main():
    """Program entry point"""
    commands = _load_commands('commands')
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
    args = docopt(usage, version=__version__, options_first=True)

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
