from docopt import docopt


class CommandBase:
    """Base class for the sub-commands of the 'handbook' command"""

    def __init__(self, command_args, global_args, version=None):
        """
        Initialize the command

        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """

        # parse the combined arguments from own docstring and passed command_args 
        self.args = docopt(self.__doc__, version=version, argv=command_args)
        self.global_args = global_args

    def execute(self):
        """Execute the command"""
        raise NotImplementedError
