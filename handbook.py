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

Commands:
{}
"""

from docopt import docopt
from docopt import DocoptExit
import sys
import pkgutil

__version__ = '0.1.2'

def main():
    """"""
    commands = loadCommands('commands')
    usage = appendCommandsAndSummariesToUsage(__doc__, commands)

    args = docopt(usage, version=__version__, options_first=True)

    command_name = args.pop('<command>')
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}
    global_args = args

    try:
        command_class = getattr(commands[command_name], command_name.capitalize())
    except AttributeError:
        print('Error: Unknown command')
        raise DocoptExit()

    command = command_class(command_args, global_args)

    command.execute()

def appendCommandsAndSummariesToUsage(usage, commands):
    commandsAndSummaries = ''
    for name, module in commands.items():
        command_class = getattr(module, name.capitalize())
        command = command_class()
        summary = command.summaryDescrition()
        commandsAndSummaries += '    {}\t{}\n'.format(name, summary)
        del command

    return usage.format(commandsAndSummaries)

def loadCommands(dirname):
    """"""
    commands = {}
    for finder, name, ispkg in pkgutil.iter_modules([dirname]):
        if name not in sys.modules:
            module = finder.find_module(name).load_module(name)
            commands.update({name: module})

    return commands

if __name__ == '__main__':
    main()