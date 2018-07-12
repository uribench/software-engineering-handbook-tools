"""
'status' sub-command of the 'handbook' command.

This module generates various status reports about the Handbook.
"""
import os
import sys
from handbook_tools.lib.command_base import CommandBase
from handbook_tools.lib.directory_tree import DirectoryTree

__version__ = '0.1.8'

class Status(CommandBase):
    """
    Generates various status reports about the Handbook.

    Usage:
      status [options]

    Options:
      -h, --help            Show this help message and exit
      --version             Show the version and exit
      -o, --output=FILE     Specify output report file relative to site root

    Examples:
      handbook status -h
      handbook status --version
      handbook status
      handbook --root=tests/fixtures/site status
      handbook status -o report.md
    """

    def __init__(self, command_args=None, global_args=None):
        """"""
        super().__init__(command_args, global_args, version=__version__)
        # optional authored metadata YAML files for the navigation files
        self.metadata_path = 'config/metadata/'
        # optional authored guide files
        self.guides_path = 'Guides/'
        # optional authored topic files
        self.topics_path = 'Topics/'
        # file extensions to look for
        self.white_list = ['.md', '.yml']
        # file names to ignore
        self.black_list = []
        self.report_title = '# Status Report\n'
        self._process_args()
        self.report = self._init_output_file(self.output_filename)

        try:
            self.report.write(self.report_title)
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))

        self.group_title = ''
        self.authored_files_count = 0
        self.directory_tree = None

    def execute(self):
        """Entry point for the execution of this sub-command"""
        self.directory_tree = DirectoryTree(self.site_root)
        tasks_queue = [{'group_title': 'Metadata Files', 'root_path': self.metadata_path},
                       {'group_title': 'Guides Files', 'root_path': self.guides_path},
                       {'group_title': 'Topics Files', 'root_path': self.topics_path}]
        for task in tasks_queue:
            root_path = os.path.join(self.site_root, task['root_path'])
            self.directory_tree.scan(root_path, task['group_title'], self.node_performer)

        try:
            self.report.write('\n\n  **Total Authored Files Count: {}**'. \
                          format(self.authored_files_count))
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))

        if self.report is not sys.stdout:
            self.report.close()

    def node_performer(self, path, group_title, file_list):
        """Custom performer executed for each visited node"""
        file_list = self._filter_files(path, file_list)
        short_path = path.replace(self.site_root, '')

        try:
            if group_title != self.group_title:
                self.report.write('\n## {}\n\n'.format(group_title))
                self.group_title = group_title
            for file in file_list:
                file_path = os.path.join(short_path, file)
                self.report.write('  - {}  \n'.format(file_path))
                self.authored_files_count += 1
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))

    def _process_args(self):
        """Process command_args"""
        # default values not set by docopt were set in CommandBase
        self.output_filename = self.args['--output']

    def _filter_files(self, path, file_list):
        """"""
        ignore_list = []
        for filename in file_list:
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                ignore_list.append(filename)
            else:
                extension = os.path.splitext(filename)[1]
                if extension not in self.white_list:
                    ignore_list.append(filename)

        return list(set(file_list) - set(ignore_list + self.black_list))
