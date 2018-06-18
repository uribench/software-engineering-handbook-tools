import os
from lib.commandBase import CommandBase
from lib.scanDirectoryTree import ScanDirectoryTree

__version__ = '0.0.1'

class Status(CommandBase):
    """
    Generates various status reports about the Handbook.

    Usage:
      status [options]

    Options:
      -h, --help            show this help message and exit
      -v, --version         show the version and exit
      -o, --output=FILE     specify output report file relative to site root

    Examples:
      handbook.py status
      handbook.py status -h
      handbook.py status --version
      handbook.py status -o report.md
    """

    def __init__(self, command_args={}, global_args={}):
        """"""
        super().__init__(command_args, global_args, version=__version__)
        # optional authored metadata YAML files for the navigation files
        self.metadataPath = 'config/metadata/'
        # optional authored guide files
        self.guidesPath = 'Guides/'
        # optional authored topic files
        self.topicsPath = 'Topics/'
        # file extensions to look for
        self.whiteList = ['.md', '.yml']
        # file names to ignore
        self.blackList = []

    def execute(self):
        """Entry point for the execution of this sub-command."""
        self.processArgs()
        rootPath = os.path.join(self.siteRoot, self.guidesPath)
        self.scanTree = ScanDirectoryTree(self.siteRoot)
        self.scanTree.scan(rootPath, self.nodePerformer)

    def processArgs(self):
        """Process global_args and command_args."""

        self.siteRoot = self.global_args['--root']
        self.outputFile = self.args['--output']

    def nodePerformer(self, path, fileList):
        """"""
        print('Files before filtering: {}'.format(fileList))
        fileList = self.filterFiles(path, fileList)
        print('Files after filtering: {}'.format(fileList))

    def filterFiles(self, path, fileList):
        """"""
        ignoreList = []
        for fileName in fileList:
            filePath = os.path.join(path, fileName)
            if not os.path.isdir(filePath):
                extension = os.path.splitext(fileName)[1]
                if extension not in self.whiteList:
                    ignoreList.append(fileName)
            else:
                    ignoreList.append(fileName)

        return list(set(fileList) - set(ignoreList + self.blackList))
