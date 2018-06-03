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
from urllib.request import pathname2url
from docopt import docopt


handbookPath = 'Handbook/'          # head of the handbook (relative to site root)
configPath = 'config/navigation/'   # one or more YAML navigation configuration files
rootConfigFile = 'root.yml'         # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
metadataPath = 'config/metadata/'   # optional YAML files with custom content for the README.md files
metadataCustomFilePrefix = '@'
metadataFileExtension = '.yml'

def createNextLevel(path, nextLevels):
    """"""
    if type(nextLevels) is not list:
        print('Error: expected list, received {} instead: {}'.format(type(nextLevels), nextLevels))
        sys.exit()

    for topLevel in nextLevels:
        if type(topLevel) is dict:
            # topLevel is a one-item dictionary representing a 'Non-leaf directory' (having children)
            navigationNode = list(topLevel.keys())[0]
            navigationNodeNextLevels = list(topLevel.values())[0]
            children = nextLevelsToChildren(navigationNodeNextLevels)

            dirPath = createCurrentLevel(path, navigationNode, children)
            createNextLevel(dirPath, navigationNodeNextLevels)
        else:
            # topLevel is a string representing a 'leaf directory' (having no children)
            createCurrentLevel(path, topLevel)

def createCurrentLevel(path, navigationNode, children=None):
    dirName, metadataFileName = parseNavigationNode(navigationNode)
    dirPath = os.path.join(path, dirName)
    createDir(dirPath)
    createIndexFile(dirPath, dirName, children, metadataFileName)

    return dirPath

def parseNavigationNode(node):
    nodeParts = node.split(metadataCustomFilePrefix)
    # remove trailing and leading spaces while preserving internal spaces
    dirName = nodeParts[0].strip()
    if len(nodeParts) == 1:
        metadataFileName = dirName
    elif len(nodeParts) == 2:
        metadataFileName = nodeParts[1].strip()
    else:
        print('Error: navigation node syntax error: {}'.format(node))
        sys.exit()

    metadataFileName = formatFileName(metadataFileName)
    metadataFileName += metadataFileExtension

    return dirName, metadataFileName

def formatFileName(fileName):
    validCharsRegEx = r'[^\w\-. ()]+'
    # compile the regular expression
    r = re.compile(validCharsRegEx)
    # remove invalid characters
    fileName = r.sub('', fileName)
    # additional formatting
    fileName = re.sub(' ', '_', fileName)
    fileName = fileName.lower()

    return fileName

def nextLevelsToChildren(nextLevels):
    children = []
    for child in nextLevels:
        if type(child) is dict:
            children.append(list(child.keys())[0])
        else:
            children.append(child)

    return children

def createDir(path):
    if os.path.exists(path):
        print('Error: at least one of the target directories already exists: {}'.format(path))
        sys.exit()

    os.mkdir(path)

def createIndexFile(path, parentDirName, siblingDirNames, metadataFileName):
    print('Index File:')
    print('\t path: {}'.format(path))
    print('\t parentDirName: {}'.format(parentDirName))
    print('\t siblingDirNames: {}'.format(siblingDirNames))
    print('\t metadataFileName: {}'.format(metadataFileName))

    metadataFullFileName = os.path.join(siteRoot, *[metadataPath, metadataFileName])
    if os.path.exists(metadataFullFileName):
        createCustomIndexFile(path, parentDirName, siblingDirNames, metadataFullFileName)
    else:
        createDefaultIndexFile(path, parentDirName, siblingDirNames)

def createCustomIndexFile(path, parentDirName, siblingDirNames, metadataFullFileName):
    pass

def createDefaultIndexFile(path, parentDirName, siblingDirNames):
    pass

def processArgs():
    global verbose, siteRoot

    args = docopt(__doc__)
    # print(args)

    verbose = args['--verbose']
    siteRoot = args['--root']

def main():
    rootConfigFullFileName = os.path.join(siteRoot, *[configPath, rootConfigFile])

    if not os.path.exists(rootConfigFullFileName):
        print('Error: root config file <{}> does not exist'.format(rootConfigFullFileName))
        sys.exit()


    try:
        with open(rootConfigFullFileName, 'r') as fp:
            navigation = yaml.load(fp)
            print(navigation)

            path = os.path.join(siteRoot, handbookPath)
            createNextLevel(path, navigation)
    except IOError as e:
        print('Error: operation failed: {}'.format(e.strerror))

if __name__ == '__main__':
    processArgs()
    main()