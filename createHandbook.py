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


handbookPath = 'Handbook/'         # head of the handbook (relative to site root)
configPath = 'config/navigation/'  # one or more YAML navigation configuration files
rootConfigFile = 'root.yml'         # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
metadataPath = 'config/metadata/'  # optional YAML files with custom content for the README.md files

def createNextLevel(path, children):
    """"""
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
            print(navigation[2])

            # createNextLevel(fp)
    except IOError as e:
        print('Error: Operation failed: {}'.format(e.strerror))

if __name__ == '__main__':
    processArgs()
    main()