import os
import sys
import yaml
import re

class ScanConfigNavigationTree:
    """
    Scan the configuration navigation tree.

    An external performer is executed for each visited node.
    """

    def __init__(self, siteRoot, verbose=False):
        """"""
        self.siteRoot = siteRoot
        self.verbose = verbose

        # one or more YAML navigation configuration files
        self.navigationPath = 'config/navigation/'
        # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
        self.rootConfigFile = 'root.yml'

    def scan(self, nodePerformer):
        """Entry point for the scan of the configuration navigation tree"""

        self.nodePerformer = nodePerformer
        rootConfigFullFileName = os.path.join(self.siteRoot, *[self.navigationPath, self.rootConfigFile])

        if not os.path.exists(rootConfigFullFileName):
            print('Error: root config file <{}> does not exist'.format(rootConfigFullFileName))
            sys.exit()

        try:
            with open(rootConfigFullFileName, 'r') as fp:
                navigationTree = yaml.load(fp)
                self.scanTree(self.siteRoot, navigationTree)
        except IOError as e:
            print('Error: operation failed: {}'.format(e.strerror))

    def parseNode(self, node):
        """
        Parse a navigation node string and returns its parts.

        Args:
            node (str): A navigation node including a directory name (Human readable string),
                followed by optional space-separated arguments as tags, each with the 
                following syntax: @<key>[=<value>]

        Returns:
            str, str: nodeName, nodeTags
        """

        nodeName, nodeTags = self.splitNodeNameAndTags(node)
        nodeOptions = self.getNodeOptions(nodeTags, nodeName)

        return nodeName, nodeOptions

    def scanTree(self, path, tree):
        """
        Scan the provided navigation tree recursively.

        Args:
            path (str): location for the root directory for the root node of the provided tree.
            tree (dict of {str: str} or str): nested data structure representing the navigation  
                tree from path onward.
                For more information and examples see: config/navigation/README.md
        """

        rootNode, rootChildrenTrees = self.getRootNodeAndChildrenTrees(tree)
        rootChildrenNodes = self.forestToRootNodes(rootChildrenTrees)
        rootName, rootOptions = self.parseNode(rootNode)

        # bail out if the tree root is marked as a 'stub' with the 'stop' tag
        if rootOptions['stop']:
            return

        rootPath = os.path.join(path, rootName)
        self.nodePerformer(rootPath, rootName, rootOptions, rootChildrenNodes)

        # continue building the navigation tree recursively
        for childTree in rootChildrenTrees:
            self.scanTree(rootPath, childTree)

    def getHandbookName(self, tree):
        """"""
        rootNode, rootChildrenTrees = self.getRootNodeAndChildrenTrees(tree)
        nodeName, nodeTags = self.splitNodeNameAndTags(rootNode)

        return nodeName

    def getRootNodeAndChildrenTrees(self, tree):
        """"""
        if type(tree) is dict:
            # tree here is a one-item dictionary representing a 'non-leaf directory' (having children):
            #   - the 'key' is a string (root name followed by optional arguments)
            #   - the 'value' is a list of root's children trees
            rootNode, rootChildrenTrees = list(tree.items())[0]
        else:
            # tree here is a string representing a 'leaf directory' (having no children):
            #   - root name followed by optional arguments
            rootNode = tree
            rootChildrenTrees = []

        return rootNode, rootChildrenTrees

    def forestToRootNodes(self, forest):
        """Return the root nodes of all the trees in forest."""

        rootNodes = []
        for tree in forest:
            if type(tree) is dict:
                rootNodes.append(list(tree.keys())[0])
            else:
                rootNodes.append(tree)

        # root node is root name followed by optional arguments
        return rootNodes

    def forestToRootNames(self, forest):
        """Return the root names of all the trees in forest."""

        rootNodes = self.forestToRootNodes(forest)

        rootNames = []
        for node in rootNodes:
            nodeName, nodeTags = self.splitNodeNameAndTags(node)
            rootNames.append(nodeName)

        return rootNames

    def splitNodeNameAndTags(self, node):
        """"""
        r = re.compile(r'^(?P<name>[^@]+)(?P<tags>.*)$')
        m = r.match(node)
        nodeName = m.group('name').strip()
        nodeTags = m.group('tags').strip().split(' ')

        return nodeName, nodeTags

    def getNodeOptions(self, tags, name):
        """"""
        # parse explicit arguments
        validKeys = ['id', 'include', 'stop']
        nodeOptions = {}
        r = re.compile(r'@(?P<k>[a-z]+)=?(?P<v>.*)')
        for tag in tags:
            m = r.match(tag)
            if m is None:
                continue
            if m.group('k') in validKeys:
                nodeOptions.update({m.group('k') : m.group('v')})
            else:
                print('Error: Unknown argument: {}'.format(m.group('k')))
                sys.exit()
        
        # set defaults
        nodeOptions['stop'] = True if 'stop' in nodeOptions else False
        if 'id' not in nodeOptions or nodeOptions['id'] == '':
            nodeOptions['id'] = self.nodeNameToNodeID(name)
        if 'include' in nodeOptions and nodeOptions['include'] == '':
            nodeOptions['include'] = self.nodeNameToNodeID(name)

        return nodeOptions

    def nodeNameToNodeID(self, nodeName):
        """"""
        # remove invalid characters
        validCharsRegEx = r'[^\w\-. ()]+'
        r = re.compile(validCharsRegEx)
        name = r.sub('', nodeName)

        # additional formatting
        name = re.sub(' ', '-', name)
        name = re.sub('-+', '-', name)
        id = name.lower()

        return id

