#!/usr/bin/env python3

"""Create the Handbook navigation (directories and README files) from configuration

Usage:
  createHandbook.py [options]

Options:
  -h --help             show this help message and exit
  -v --verbose          print warning messages
  --root=PATH           site root [default: ../software-engineering-handbook] 
"""

import os
import sys
import yaml
import re
from docopt import docopt
from urllib.request import pathname2url
from jinja2 import Template

navigationPath = 'config/navigation/'   # one or more YAML navigation configuration files
rootConfigFile = 'root.yml'         # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
metadataPath = 'config/metadata/'   # optional YAML files with custom content for the index.md files
metadataFileExtension = '.yml'
templatesPath = 'config/templates/'
indexTemplate = 'index-template.j2'

def buildTree(path, tree):
    """
    Builds the navigation tree recursively, based on the provided tree

    :param path: points to the location where the 'root directory' will be created for the provided 
        tree.
    :type path: string
    :param tree: nested data structure representing the navigation tree from path onward.
        For more information and examples see: config/navigation/README.md
    :type tree: dictionary or string
    """

    rootNode, rootChildrenTrees = getRootNodeAndChildrenTrees(tree)
    rootChildrenNodes = forestToRootNodes(rootChildrenTrees)
    rootName, rootOptions = parseNode(rootNode)

    # bail out if the tree root is marked as a 'stub' with the 'stop' tag
    if rootOptions['stop']:
        return

    rootPath = os.path.join(path, rootName)
    createRootDir(rootPath)
    createIndexFile(rootPath, rootOptions, rootName, rootChildrenNodes)

    # continue building the navigation tree recursively
    for childTree in rootChildrenTrees:
        buildTree(rootPath, childTree)

def getRootNodeAndChildrenTrees(tree):

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

def getHandbookName(tree):
    rootNode, rootChildrenTrees = getRootNodeAndChildrenTrees(tree)
    nodeName, nodeTags = splitNodeNameAndTags(rootNode)

    return nodeName

def forestToRootNodes(forest):
    """Returns the root nodes of all the trees in forest"""

    rootNodes = []
    for tree in forest:
        if type(tree) is dict:
            rootNodes.append(list(tree.keys())[0])
        else:
            rootNodes.append(tree)

    # root node is root name followed by optional arguments
    return rootNodes

def forestToRootNames(forest):
    """Returns the root names of all the trees in forest"""

    rootNodes = forestToRootNodes(forest)

    rootNames = []
    for node in rootNodes:
        nodeName, nodeTags = splitNodeNameAndTags(node)
        rootNames.append(nodeName)

    return rootNames

def parseNode(node):
    """
    Parses a navigation node string and returns its parts

    :param node: A navigation node including a directory name ('Humanized' style) followed by 
        optional space separated arguments as tags, each with the following syntax: @<key>[=<value>]
    :type node: String
    :return: nodeName, nodeTags
    :rtype: string, string
    """

    nodeName, nodeTags = splitNodeNameAndTags(node)
    nodeOptions = getNodeOptions(nodeTags, nodeName)

    return nodeName, nodeOptions

def splitNodeNameAndTags(node):
    r = re.compile(r'^(?P<name>[^@]+)(?P<tags>.*)$')
    m = r.match(node)
    nodeName = m.group('name').strip()
    nodeTags = m.group('tags').strip().split(' ')

    return nodeName, nodeTags

def getNodeOptions(tags, name):
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
        nodeOptions['id'] = nodeNameToNodeID(name)
    if 'include' in nodeOptions and nodeOptions['include'] == '':
        nodeOptions['include'] = nodeNameToNodeID(name)

    return nodeOptions

def nodeNameToNodeID(nodeName):
    # remove invalid characters
    validCharsRegEx = r'[^\w\-. ()]+'
    r = re.compile(validCharsRegEx)
    name = r.sub('', nodeName)

    # additional formatting
    name = re.sub(' ', '-', name)
    name = re.sub('-+', '-', name)
    id = name.lower()

    return id

def createRootDir(path):
    if os.path.exists(path):
        print('Error: target directory already exists: {}'.format(path))
        sys.exit()

    os.mkdir(path)

def createIndexFile(path, options, title, childrenNodes):
    template = loadTemplate(templatesPath, indexTemplate)
    metadataFileName = options['id'] + metadataFileExtension
    metadataFullFileName = os.path.join(siteRoot, *[metadataPath, metadataFileName])

    intro = []
    rawGuides = []
    rawTopics = []

    if os.path.exists(metadataFullFileName):
        metadata = loadMetadata(metadataFullFileName)
        intro = metadata.get('intro', [])
        rawGuides = metadata.get('guides', [])
        rawTopics = metadata.get('topics', [])

    contents = formatContents(path, childrenNodes)
    guides = formatMetadataListItems('/Guides', rawGuides)
    topics = formatMetadataListItems('/Topics', rawTopics)

    indexFileContents = template.render(title=title, intro=intro, contents=contents, guides=guides, topics=topics)
    writeIndexFile(path, indexFileContents)

def loadTemplate(templatePath, templateName):
    try:
        templateFullFileName = os.path.join(siteRoot, *[templatePath, templateName])
        with open(templateFullFileName) as templateFile:
            return Template(templateFile.read())
    except IOError as e:
        print('Error: operation failed: {}'.format(e.strerror))

def loadMetadata(filename):
    try:
        with open(filename, 'r') as fp:
            metadata = yaml.load(fp)
    except IOError as e:
        print('Error: operation failed: {}'.format(e.strerror))

    return metadata

def formatContents(path, childrenNodes):
    contents = []
    for childNode in childrenNodes:
        childName, childOptions = parseNode(childNode)
        if not childOptions['stop']:
            path = path.replace(siteRoot, '')
            link = os.path.join(path, childNode)
            item = formatMarkdownLinkedItem(childNode, link)
        else:
            item = childName
            
        contents.append(item)

    return contents

def formatMetadataListItems(path, rawItems):
    items = []
    for item in rawItems:
        itemText = os.path.basename(item)
        link = os.path.join(path,item)
        formatedItem = formatMarkdownLinkedItem(itemText, link)
        items.append(formatedItem)

    return items

def formatMarkdownLinkedItem(item, link):
    linkURL = pathname2url(link)
    item = '[{}]({})'.format(item, linkURL)

    return item

def writeIndexFile(path, content):
    indexFullFileName = os.path.join(path, 'index.md')
    try:
        with open(indexFullFileName, 'a') as fo:
            fo.write(content)
    except IOError as e:
        print('Error: Operation failed: {}'.format(e.strerror))

def processArgs():
    global verbose, siteRoot

    args = docopt(__doc__)
    verbose = args['--verbose']
    siteRoot = args['--root']

def main():
    global handbookPath

    rootConfigFullFileName = os.path.join(siteRoot, *[navigationPath, rootConfigFile])

    if not os.path.exists(rootConfigFullFileName):
        print('Error: root config file <{}> does not exist'.format(rootConfigFullFileName))
        sys.exit()

    try:
        with open(rootConfigFullFileName, 'r') as fp:
            navigationTree = yaml.load(fp)
            handbookPath = getHandbookName(navigationTree) + '/'
            buildTree(siteRoot, navigationTree)
    except IOError as e:
        print('Error: operation failed: {}'.format(e.strerror))

if __name__ == '__main__':
    processArgs()
    main()