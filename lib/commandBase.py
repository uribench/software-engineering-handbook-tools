from docopt import docopt


class CommandBase:
    """Base class for the sub-commands of the 'handbook' command"""

    def __init__(self, command_args, global_args, version=None):
        """
        Initialize the command.

        command_args (dict of {str: value}): arguments of the command
        global_args (dict of {str: value}): arguments of the program
        version (str): version of the subclass (i.e., concrete command)
        """

        # parse the combined arguments from command's 'docstring' and passed command_args 
        self.args = docopt(self.__doc__, version=version, argv=command_args)
        self.global_args = global_args

    def execute(self):
        """Execute the command."""
        raise NotImplementedError
