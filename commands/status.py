"""
'status' sub-command of the 'handbook' command.

This module generates various status reports about the Handbook.
"""
import os
import sys
from lib.command_base import CommandBase
from lib.scan_directory_tree import ScanDirectoryTree

__version__ = '0.1.1'

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
        self.report = self._init_output_file()
        self.group_title = ''
        self.authored_files_count = 0
        self.scan_tree = None

    def execute(self):
        """Entry point for the execution of this sub-command"""
        self.scan_tree = ScanDirectoryTree(self.site_root)
        tasks_queue = [{'group_title': 'Metadata Files', 'root_path': self.metadata_path},
                       {'group_title': 'Guides Files', 'root_path': self.guides_path},
                       {'group_title': 'Topics Files', 'root_path': self.topics_path}]
        for task in tasks_queue:
            root_path = os.path.join(self.site_root, task['root_path'])
            self.scan_tree.scan(root_path, task['group_title'], self.node_performer)
        self.report.write('\n\n  **Total Authored Files Count: {}**'. \
                          format(self.authored_files_count))
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
        """Process global_args and command_args"""
        self.site_root = self.global_args['--root']
        self.output_filename = self.args['--output']

    def _init_output_file(self):
        """"""
        if self.output_filename is not None:
            report_full_filename = os.path.join(self.site_root, self.output_filename)
            if os.path.exists(report_full_filename):
                print('Error: Report file already exists: {}'.format(report_full_filename))
                sys.exit()

            report_file = open(report_full_filename, 'a')
        else:
            report_file = sys.stdout

        try:
            report_file.write(self.report_title)
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))

        return report_file

    def _filter_files(self, path, file_list):
        """"""
        ignore_list = []
        for filename in file_list:
            file_path = os.path.join(path, filename)
            if not os.path.isdir(file_path):
                extension = os.path.splitext(filename)[1]
                if extension not in self.white_list:
                    ignore_list.append(filename)
            else:
                ignore_list.append(filename)

        return list(set(file_list) - set(ignore_list + self.black_list))
