import os
import sys
from urllib.request import pathname2url
from lib.commandBase import CommandBase
from lib.scanConfigNavigationTree import ScanConfigNavigationTree

__version__ = '0.5.1'

class Toc(CommandBase):
    """
    Compose a TOC of the Handbook from configuration.

    Usage:
      toc [options]

    Options:
      -h, --help            show this help message and exit
      -v, --version         show the version and exit
      -o, --output=FILE     specify output TOC file relative to site root
      -d, --depth=LEVEL     max depth of the generated TOC tree [default: 8]
      --no-stop             ignore 'stop' tags to scan the entire tree
      --no-prefix           do not include item prefix for the TOC items
      --no-index            do not include index numbers for the TOC items
      --no-link             do not include links for the TOC items
      --header              include HTML header for the TOC file

    Examples:
      handbook.py toc
      handbook.py toc -h
      handbook.py toc --version
      handbook.py toc -d 3
      handbook.py toc --depth=3 --no-index
      handbook.py toc --d 2 --no-index --no-link -o TOC2.md
    """

    def __init__(self, command_args={}, global_args={}):
        """"""
        super().__init__(command_args, global_args, version=__version__)
        # kill bullets of unordered list (not supported by GitHub)
        self.tocHeader = '<style>ul { list-style-type: none; }</style>\n\n'
        self.tocTitle = '# Table of Contents\n\n'
        self.markdownUL = '-'

    def execute(self):
        """Entry point for the execution of this sub-command."""
        self.processArgs()
        self.tocFile = self.initOutputFile()
        self.depth = 0
        self.index = []
        self.scanTree = ScanConfigNavigationTree(self.siteRoot, self.verbose, self.noStop)
        self.scanTree.scan(self.nodePerformer)
        self.tocFile.close()

    def processArgs(self):
        """Process global_args and command_args."""
        self.siteRoot = self.global_args['--root']
        self.verbose = self.global_args['--verbose']
        self.outputFile = self.args['--output']
        self.maxDepth = int(self.args['--depth'])
        self.noStop = self.args['--no-stop']
        self.includePrefix = not self.args['--no-prefix']
        self.includeIndex = not self.args['--no-index']
        self.includeLink = not self.args['--no-link']
        self.includeTocHeader = self.args['--header']

    def initOutputFile(self):
        """"""
        if self.outputFile is not None:
            tocFullFileName = os.path.join(self.siteRoot, self.outputFile)
            if os.path.exists(tocFullFileName):
                print('Error: TOC file already exists: {}'.format(tocFullFileName))
                sys.exit()

            fo = open(tocFullFileName, 'a')
        else:
            fo = sys.stdout

        try:
            if self.includeTocHeader:
                fo.write(self.tocHeader)
            fo.write(self.tocTitle)
        except IOError as e:
            print('Error: Operation failed: {}'.format(e.strerror))

        return fo

    def nodePerformer(self, rootPath, rootOptions, rootChildrenNodes):
        """"""
        name = os.path.basename(rootPath)
        link = rootPath.replace(self.siteRoot, '')
        self.updateIndexCounter(link)

        # skip handbook root and too deep TOC items 
        if self.depth > 1 and (self.depth - 1) <= self.maxDepth:
            self.tocFile.write(self.formatTOC(name, link))

    def updateIndexCounter(self, link):
        """"""
        depth = len(link.split(os.sep)) - 1
        if depth > len(self.index):
            self.index += [1]
        if depth <= self.depth:
            self.index[depth-1] += 1
            self.index = self.index[:depth]
        self.depth = depth

    def formatTOC(self, name, link):
        """"""
        # compose indent string
        indent = ' ' * 2 * (self.depth - 2)
        # compose optional item prefix string
        prefix = ''
        if self.includePrefix:
            prefix = self.markdownUL + ' '
        # compose optional index string
        indexString = ''
        if self.includeIndex:
            indexString = '.'.join(str(e) for e in self.index[1:self.depth])
            indexString += ' '
        # compose item string with optional link
        tocItem = name
        if self.includeLink:
            linkURL = pathname2url(link)
            tocItem = '[' + name + '](' + linkURL + ')'

        return '{}{}{}{}\n'.format(indent, prefix, indexString, tocItem)
