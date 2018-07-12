"""
Base class for sub-commands of the 'handbook' command.
"""

import os
import sys
from docopt import docopt
from handbook_tools.lib.handbook_validation import HandbookValidation

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

        # parse the combined arguments from command's 'docstring'
        # and passed command_args
        self.args = docopt(self.__doc__, version=version, argv=command_args)

        # process global_args
        self.verbose = global_args['--verbose']
        self.site_root = self._set_site_root(global_args['--root'])

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

    def _set_site_root(self, root_option):
        """"""
        site_root = root_option
        environ_variable = 'HANDBOOK_ROOT'

        if site_root is None:
            if environ_variable in os.environ:
                site_root = os.environ[environ_variable]
            else:
                site_root = '.'

        site_root = site_root.rstrip('/')
        self._validate_site_root_or_exit(site_root)

        return site_root

    @staticmethod
    def _validate_site_root_or_exit(site_root):
        """"""
        error_message = """Handbook root is invalid. Specify a valid location using
                           --root option or HANDBOOK_ROOT environment variable"""

        HandbookValidation.fail_on_nonexisting_filesystem(site_root, error_message)

    def _init_output_file(self, output_filename):
        """"""
        if output_filename is None:
            output_file = sys.stdout
        else:
            output_full_filename = os.path.join(self.site_root, output_filename)
            error_message = 'Output file already exists'
            HandbookValidation.fail_on_existing_path(output_full_filename, error_message)

            output_file = open(output_full_filename, 'a')

        return output_file
