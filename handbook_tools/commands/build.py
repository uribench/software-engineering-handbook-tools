"""
'build' sub-command of the 'handbook' command.

This module builds the Handbook from configuration files.
"""

import os
from urllib.request import pathname2url
from jinja2 import Template
import yaml
from handbook_tools.lib.command_base import CommandBase
from handbook_tools.lib.navigation_tree import NavigationTree
from handbook_tools.lib.navigation_tree_node import NavigationTreeNode

__version__ = '1.1.8'

class Build(CommandBase):
    """
    Build the Handbook from configuration.

    Usage:
      build [options]

    Options:
      -h, --help        Show this help message and exit
      --version         Show the version and exit
      --no-stop         Ignore 'stop' tags to scan the entire tree
      -f, --force       Overwrite existing target directory

    Examples:
      handbook build -h
      handbook build --version
      handbook build
      handbook --root=tests/fixtures/site build
      handbook build --no-stop
    """

    def __init__(self, command_args=None, global_args=None):
        """"""
        super().__init__(command_args, global_args, version=__version__)

        # navigation file name (auto-generated)
        self.navigation_filename = 'index.md'
        # optional authored metadata YAML files for the navigation files
        self.metadata_path = 'config/metadata/'
        # path to template files
        self.templates_path = 'config/templates/'
        # Jinja2 template file for the navigation files
        self.navigation_file_template = 'navigation-file-template.j2'
        self._process_args()
        self.navigation_tree = None

    def execute(self):
        """Entry point for the execution of this sub-command"""
        self.navigation_tree = NavigationTree(self.site_root, self.verbose, self.no_stop)
        self.navigation_tree.fail_on_existing_root_node_dir(self.force)
        self.navigation_tree.scan(self.node_performer)

    def node_performer(self, root_path, root_options, root_children_nodes):
        """Custom performer executed for each visited node"""
        os.mkdir(root_path)
        root_name = os.path.basename(root_path)
        self._create_index_file(root_path, root_options, root_name, root_children_nodes)

    def _process_args(self):
        """Process command_args"""
        # default values not set by docopt were set in CommandBase
        self.no_stop = self.args['--no-stop']
        self.force = self.args['--force']

    def _create_index_file(self, path, options, title, children_nodes):
        """"""
        template = self._load_template(self.templates_path, self.navigation_file_template)
        metadata_filename = options['id'] + '.yml'
        metadata_full_filename = os.path.join(self.site_root,
                                              *[self.metadata_path, metadata_filename])

        intro = []
        raw_guides = []
        raw_topics = []

        if os.path.exists(metadata_full_filename):
            metadata = self._load_metadata(metadata_full_filename)
            intro = metadata.get('intro', [])
            raw_guides = metadata.get('guides', [])
            raw_topics = metadata.get('topics', [])

        contents = self._format_contents(path, children_nodes)
        guides = self._format_metadata_list_items('/Guides', raw_guides)
        topics = self._format_metadata_list_items('/Topics', raw_topics)

        index_file_contents = template.render(title=title, intro=intro, contents=contents,
                                              guides=guides, topics=topics)
        self._write_index_file(path, index_file_contents)

    def _load_template(self, template_path, template_name):
        """"""
        try:
            template_full_filename = os.path.join(self.site_root, *[template_path, template_name])
            with open(template_full_filename) as template_file:
                return Template(template_file.read())
        except IOError as err:
            print('Error: operation failed: {}'.format(err.strerror))

    @staticmethod
    def _load_metadata(filename):
        """"""
        try:
            with open(filename, 'r') as metadata_file:
                metadata = yaml.load(metadata_file)
        except IOError as err:
            print('Error: operation failed: {}'.format(err.strerror))

        return metadata

    def _format_contents(self, path, children_nodes):
        """"""
        contents = []
        for node in children_nodes:
            child_node = NavigationTreeNode(node)
            if not child_node.options['stop']:
                path = path.replace(self.site_root, '')
                link = os.path.join(path, child_node.name)
                item = self._format_markdown_linked_item(child_node.name, link)
            else:
                item = child_node.name

            contents.append(item)

        return contents

    def _format_metadata_list_items(self, path, raw_items):
        """"""
        items = []
        for item in raw_items:
            item_text = os.path.basename(item)
            link = os.path.join(path, item)
            formated_item = self._format_markdown_linked_item(item_text, link)
            items.append(formated_item)

        return items

    @staticmethod
    def _format_markdown_linked_item(item, link):
        """"""
        link_url = pathname2url(link)
        item = '[{}]({})'.format(item, link_url)

        return item

    def _write_index_file(self, path, content):
        """"""
        index_full_filename = os.path.join(path, self.navigation_filename)
        try:
            with open(index_full_filename, 'a') as index_file:
                index_file.write(content)
        except IOError as err:
            print('Error: Operation failed: {}'.format(err.strerror))
