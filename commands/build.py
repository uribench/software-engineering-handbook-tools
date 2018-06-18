import os
import sys
import yaml
from urllib.request import pathname2url
from jinja2 import Template
from lib.commandBase import CommandBase
from lib.scanConfigNavigationTree import ScanConfigNavigationTree

__version__ = '1.0.0'

class Build(CommandBase):
    """
    Build the Handbook navigation tree from configuration.

    Usage:
      build [options]

    Options:
      -h, --help        show this help message and exit
      -v, --version     show the version and exit

    Examples:
      handbook.py build
      handbook.py build -h
      handbook.py build --version
    """

    def __init__(self, command_args={}, global_args={}):
        """"""
        super().__init__(command_args, global_args, version=__version__)

        # navigation file name (auto-generated)
        self.navigationFileName = 'index.md'
        # optional YAML files with custom content for the navigation files
        self.metadataPath = 'config/metadata/'
        # path to template files
        self.templatesPath = 'config/templates/'
        # Jinja2 template file for the navigation files
        self.navigationFileTemplate = 'navigation-file-template.j2'

    def execute(self):
        """Entry point for the execution of this sub-command."""
        self.processArgs()
        self.scanTree = ScanConfigNavigationTree(self.siteRoot, self.verbose)
        self.scanTree.scan(self.nodePerformer)

    def processArgs(self):
        """Process global_args and command_args."""
        self.siteRoot = self.global_args['--root']
        self.verbose = self.global_args['--verbose']

    def nodePerformer(self, rootPath, rootOptions, rootChildrenNodes):
        """"""
        rootName = os.path.basename(rootPath)
        self.createRootDir(rootPath)
        self.createIndexFile(rootPath, rootOptions, rootName, rootChildrenNodes)

    def createRootDir(self, path):
        """"""
        if os.path.exists(path):
            print('Error: target directory already exists: {}'.format(path))
            sys.exit()

        os.mkdir(path)

    def createIndexFile(self, path, options, title, childrenNodes):
        """"""
        template = self.loadTemplate(self.templatesPath, self.navigationFileTemplate)
        metadataFileName = options['id'] + '.yml'
        metadataFullFileName = os.path.join(self.siteRoot, *[self.metadataPath, metadataFileName])

        intro = []
        rawGuides = []
        rawTopics = []

        if os.path.exists(metadataFullFileName):
            metadata = self.loadMetadata(metadataFullFileName)
            intro = metadata.get('intro', [])
            rawGuides = metadata.get('guides', [])
            rawTopics = metadata.get('topics', [])

        contents = self.formatContents(path, childrenNodes)
        guides = self.formatMetadataListItems('/Guides', rawGuides)
        topics = self.formatMetadataListItems('/Topics', rawTopics)

        indexFileContents = template.render(title=title, intro=intro, contents=contents, guides=guides, topics=topics)
        self.writeIndexFile(path, indexFileContents)

    def loadTemplate(self, templatePath, templateName):
        """"""
        try:
            templateFullFileName = os.path.join(self.siteRoot, *[templatePath, templateName])
            with open(templateFullFileName) as templateFile:
                return Template(templateFile.read())
        except IOError as e:
            print('Error: operation failed: {}'.format(e.strerror))

    def loadMetadata(self, filename):
        """"""
        try:
            with open(filename, 'r') as fp:
                metadata = yaml.load(fp)
        except IOError as e:
            print('Error: operation failed: {}'.format(e.strerror))

        return metadata

    def formatContents(self, path, childrenNodes):
        """"""
        contents = []
        for childNode in childrenNodes:
            childName, childOptions = self.scanTree.parseNode(childNode)
            if not childOptions['stop']:
                path = path.replace(self.siteRoot, '')
                link = os.path.join(path, childNode)
                item = self.formatMarkdownLinkedItem(childNode, link)
            else:
                item = childName
                
            contents.append(item)

        return contents

    def formatMetadataListItems(self, path, rawItems):
        """"""
        items = []
        for item in rawItems:
            itemText = os.path.basename(item)
            link = os.path.join(path,item)
            formatedItem = self.formatMarkdownLinkedItem(itemText, link)
            items.append(formatedItem)

        return items

    def formatMarkdownLinkedItem(self, item, link):
        """"""
        linkURL = pathname2url(link)
        item = '[{}]({})'.format(item, linkURL)

        return item

    def writeIndexFile(self, path, content):
        """"""
        indexFullFileName = os.path.join(path, self.navigationFileName)
        try:
            with open(indexFullFileName, 'a') as fo:
                fo.write(content)
        except IOError as e:
            print('Error: Operation failed: {}'.format(e.strerror))
