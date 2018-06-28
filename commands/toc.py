"""
'toc' sub-command of the 'handbook' command.

This module composes a TOC for the Handbook from configuration files.
"""

import os
import sys
from urllib.request import pathname2url
from lib.command_base import CommandBase
from lib.scan_config_navigation_tree import ScanConfigNavigationTree

__version__ = '0.6.1'

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
      handbook.py toc --no-stop -o TOC.md
    """

    def __init__(self, command_args=None, global_args=None):
        """"""
        super().__init__(command_args, global_args, version=__version__)
        # kill bullets of unordered list (not supported by GitHub)
        self.toc_header = '<style>ul { list-style-type: none; }</style>\n\n'
        self.toc_title = '# Table of Contents\n\n'
        self.markdown_ul = '-'
        self._process_args()
        self.toc_file = self._init_output_file()
        self.depth = 0
        self.index = []
        self.scan_tree = None

    def execute(self):
        """Entry point for the execution of this sub-command"""
        self.scan_tree = ScanConfigNavigationTree(self.site_root, self.verbose, self.no_stop)
        self.scan_tree.scan(self.node_performer)
        self.toc_file.close()

    def node_performer(self, root_path, *_):
        """Custom performer executed for each visited node"""
        name = os.path.basename(root_path)
        link = root_path.replace(self.site_root, '')
        self._update_index_counter(link)

        # skip handbook root and too deep TOC items
        if self.depth > 1 and (self.depth - 1) <= self.max_depth:
            self.toc_file.write(self._format_toc(name, link))

    def _process_args(self):
        """Process global_args and command_args"""
        self.site_root = self.global_args['--root']
        self.verbose = self.global_args['--verbose']
        self.output_file = self.args['--output']
        self.max_depth = int(self.args['--depth'])
        self.no_stop = self.args['--no-stop']
        self.include_prefix = not self.args['--no-prefix']
        self.include_index = not self.args['--no-index']
        self.include_link = not self.args['--no-link']
        self.include_toc_header = self.args['--header']

    def _init_output_file(self):
        """"""
        if self.output_file is not None:
            toc_full_filename = os.path.join(self.site_root, self.output_file)
            if os.path.exists(toc_full_filename):
                print('Error: TOC file already exists: {}'.format(toc_full_filename))
                sys.exit()

            toc_file = open(toc_full_filename, 'a')
        else:
            toc_file = sys.stdout

        try:
            if self.include_toc_header:
                toc_file.write(self.toc_header)
            toc_file.write(self.toc_title)
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))

        return toc_file

    def _update_index_counter(self, link):
        """"""
        depth = len(link.split(os.sep)) - 1
        if depth > len(self.index):
            self.index += [1]
        if depth <= self.depth:
            self.index[depth-1] += 1
            self.index = self.index[:depth]
        self.depth = depth

    def _format_toc(self, name, link):
        """"""
        # compose indent string
        indent = ' ' * 2 * (self.depth - 2)
        # compose optional item prefix string
        prefix = ''
        if self.include_prefix:
            prefix = self.markdown_ul + ' '
        # compose optional index string
        index_string = ''
        if self.include_index:
            index_string = '.'.join(str(e) for e in self.index[1:self.depth])
            index_string += ' '
        # compose item string with optional link
        toc_item = name
        if self.include_link:
            link_url = pathname2url(link)
            toc_item = '[' + name + '](' + link_url + ')'

        return '{}{}{}{}\n'.format(indent, prefix, index_string, toc_item)
