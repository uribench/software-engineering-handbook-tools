from lib.commandBase import CommandBase
from lib.scanConfigNavigationTree import ScanConfigNavigationTree

__version__ = '0.0.0'

class Validate(CommandBase):
    """
    Validate the integrity of the Handbook.

    Usage:
      validate [options]

    Options:
      -h --help             show this help message and exit
      -v, --version         show the version and exit
    """

    def __init__(self, command_args={}, global_args={}):
        """"""
        super().__init__(command_args, global_args, version=__version__)

    def execute(self):
        """Entry point for the execution of this sub-command."""
        print('\'validate\' command not implemented yet!')
        # self.processArgs()
        # self.scanTree = ScanConfigNavigationTree(self.siteRoot, self.verbose)
        # self.scanTree.scan(self.nodePerformer)

    def processArgs(self):
        """Process global_args and command_args."""

        self.siteRoot = self.global_args['--root']
        self.verbose = self.global_args['--verbose']

    def nodePerformer(self, rootPath, rootName, rootOptions, rootChildrenNodes):
        """"""
        pass
