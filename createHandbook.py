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
from urllib.request import pathname2url
from docopt import docopt


handbookPath = 'HandbookTest/'     # head of the handbook (relative to site root)
configPath = 'config/navigation/'  # one or more YAML navigation configuration files
rootConfigFile = 'root.yml'        # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
metadataPath = 'config/metadata/'  # optional YAML files with custom content for the README.md files

def createNextLevel(path, children):
    """"""
    if type(children) is not list:
        print('Error: list was expected and received a {} instead: {}'.format(type(children), children))
        sys.exit()

    for dir in children:
        if type(dir) is dict:
            for key, value in dir.items():
                dirPath = os.path.join(path, key)
                print('Non-Leaf directory: {}, path: {}'.format(key, dirPath))
                os.mkdir(dirPath)
                createNextLevel(dirPath, value)
        else:
            dirPath = os.path.join(path, dir)
            print('Leaf directory: {}, path: {}'.format(dir, dirPath))
            os.mkdir(dirPath)

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
            # print(navigation)

            path = os.path.join(siteRoot, handbookPath)
            createNextLevel(path, navigation)
    except IOError as e:
        print('Error: Operation failed: {}'.format(e.strerror))

if __name__ == '__main__':
    processArgs()
    main()