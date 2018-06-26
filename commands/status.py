import os
import sys
from lib.commandBase import CommandBase
from lib.scanDirectoryTree import ScanDirectoryTree

__version__ = '0.0.2'

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
        self.reportTitle = '# Status Report\n'

    def execute(self):
        """Entry point for the execution of this sub-command."""
        self.processArgs()
        self.report = self.initOutputFile()
        self.scanTree = ScanDirectoryTree(self.siteRoot)
        taskQueue = [{'title': 'Metadata Files', 'rootPath': self.metadataPath},
                     {'title': 'Guides Files', 'rootPath': self.guidesPath},
                     {'title': 'Topics Files', 'rootPath': self.topicsPath}]
        self.title = ''
        self.authoredFilesCount = 0
        for task in taskQueue:
            rootPath = os.path.join(self.siteRoot, task['rootPath'])
            self.scanTree.scan(rootPath, task['title'], self.nodePerformer)
        self.report.write('\n\n  **Total Authored Files Count: {}**'. \
                          format(self.authoredFilesCount))
        self.report.close()

    def processArgs(self):
        """Process global_args and command_args."""
        self.siteRoot = self.global_args['--root']
        self.outputFile = self.args['--output']

    def initOutputFile(self):
        """"""
        if self.outputFile is not None:
            reportFullFileName = os.path.join(self.siteRoot, self.outputFile)
            if os.path.exists(reportFullFileName):
                print('Error: Report file already exists: {}'.format(reportFullFileName))
                sys.exit()

            fo = open(reportFullFileName, 'a')
        else:
            fo = sys.stdout

        try:
            fo.write(self.reportTitle)
        except IOError as e:
            print('Error: Operation failed: {}'.format(e.strerror))

        return fo

    def nodePerformer(self, path, title, fileList):
        """"""
        fileList = self.filterFiles(path, fileList)
        shortPath = path.replace(self.siteRoot, '')
        try:
            if title != self.title:
                self.report.write('\n## {}\n\n'.format(title))
                self.title = title
            for file in fileList:
                filePath = os.path.join(shortPath, file)
                self.report.write('  - {}  \n'.format(filePath))
                self.authoredFilesCount += 1
        except IOError as e:
            print('Error: Operation failed: {}'.format(e.strerror))

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
