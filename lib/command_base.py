"""
Base class for sub-commands of the 'handbook' command.
"""

import os
import sys
from docopt import docopt

class CommandBase:
    """Base class for the sub-commands of the 'handbook' command"""

    def __init__(self, command_args=None, global_args=None, version=None):
        """
        Initialize the command.

        command_args (dict of {str: value}): arguments of the command
        global_args (dict of {str: value}): arguments of the program
        version (str): version of the subclass (i.e., concrete command)
        """

        # set default values for global_args and command_args
        if command_args is None:
            command_args = {}

        if global_args is None:
            global_args = {}

        self.global_args = global_args
        self.verbose = self.global_args['--verbose']
        self.site_root = self.global_args['--root']

        if self.site_root is None:
            self._set_default_site_root('HANDBOOK_ROOT')

        # parse the combined arguments from command's 'docstring' and passed command_args
        self.args = docopt(self.__doc__, version=version, argv=command_args)

    def execute(self):
        """Execute the command"""
        raise NotImplementedError

    @classmethod
    def summary_description(cls):
        """Return a short description of the concrete command"""
        summary = 'No summary description was provided'
        for line in cls.__doc__.splitlines():
            summary = line.strip()
            if summary:
                break

        return summary

    def _set_default_site_root(self, environ_variable):
        if environ_variable in os.environ:
            self.site_root = os.environ[environ_variable]
        else:
            print('Error: Handbook root is unknown:')
            print('  Set the {} environment variable, or'.format(environ_variable))
            print('  provide value for the --root option in the command line.')
            print('  Run handbook.py -h for more details on the Environment.')
            sys.exit()

