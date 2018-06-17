from lib.commandBase import CommandBase
from lib.scanConfigNavigationTree import ScanConfigNavigationTree

__version__ = '0.5.0'

class Toc(CommandBase):
    """
    Compose a TOC of the Handbook navigation tree from configuration.

    Usage:
      toc [options] [FILE]

    Arguments:
      FILE  destination TOC filename

    Options:
      -h --help             show this help message and exit
      -v, --version         show the version and exit
      --toc-path=PATH       TOC file path relative to site root
                            [default: .]
      --links-root=PATH     TOC file links root relative to site root 
                            [default: /Handbook/]
      -d --depth=LEVEL      max depth of the generated TOC tree [default: 8]
      --start-index=INDEX   start index of the TOC items [default: 1]
      --no-item-prefix      do not include item prefix for the TOC items
      --no-index            do not include index numbers for the TOC items
      --no-item-link        do not include links for the TOC items
      --header              include HTML header for the TOC file
    """

    def __init__(self, command_args={}, global_args={}):
        """"""
        super().__init__(command_args, global_args, version=__version__)

    def execute(self):
        """Entry point for the execution of this sub-command."""
        self.processArgs()
        self.scanTree = ScanConfigNavigationTree(self.siteRoot, self.verbose)
        self.scanTree.scan(self.nodePerformer)

    def processArgs(self):
        """Process global_args and command_args."""

        self.siteRoot = self.global_args['--root']
        self.verbose = self.global_args['--verbose']
        print('global_args: {}'.format(self.global_args))
        print('args: {}'.format(self.args))

    def nodePerformer(self, rootPath, rootName, rootOptions, rootChildrenNodes):
        """"""
        pass
