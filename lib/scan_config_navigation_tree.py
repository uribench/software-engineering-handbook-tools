"""
Scan the configuration navigation tree.

An external performer is executed for each visited node.
"""

import os
import sys
import re
import yaml

class ScanConfigNavigationTree:
    """Scan the configuration navigation tree"""

    def __init__(self, site_root, verbose=False, no_stop=False):
        """"""
        self.site_root = site_root
        self.verbose = verbose
        self.no_stop = no_stop

        # one or more YAML navigation configuration files
        self.navigation_path = 'config/navigation/'
        # should be save as UTF-8 without BOM (i.e., Byte Order Mark)
        self.root_config_filename = 'root.yml'
        self.node_performer = None

    def scan(self, node_performer):
        """Entry point for the scan of the configuration navigation tree"""

        self.node_performer = node_performer
        root_config_full_filename = os.path.join(self.site_root,
                                                 *[self.navigation_path, self.root_config_filename])

        if not os.path.exists(root_config_full_filename):
            print('Error: root config file <{}> does not exist'.format(root_config_full_filename))
            sys.exit()

        try:
            with open(root_config_full_filename, 'r') as root_config_file:
                navigation_tree = yaml.load(root_config_file)
                self._scan_tree(self.site_root, navigation_tree)
        except IOError as err:
            print('Error: operation failed: {}'.format(err.strerror))

    def parse_node(self, node):
        """
        Parse a navigation node string and returns its parts.

        Args:
            node (str): A navigation node including a directory name (Human readable string),
                followed by optional space-separated arguments as tags, each with the
                following syntax: @<key>[=<value>]

        Returns:
            str, str: nodeName, nodeTags
        """

        node_name, node_tags = self._split_node_name_and_tags(node)
        node_options = self._get_node_options(node_tags, node_name)

        return node_name, node_options

    def _scan_tree(self, path, tree):
        """
        Scan the provided navigation tree recursively.

        Args:
            path (str): location for the root directory for the root node of the provided tree.
            tree (dict of {str: str} or str): nested data structure representing the navigation
                tree from path onward.
                For more information and examples see: config/navigation/README.md
        """

        root_node, root_children_trees = self._get_root_node_and_children_trees(tree)
        root_children_nodes = self._forest_to_root_nodes(root_children_trees)
        root_name, root_options = self.parse_node(root_node)

        # bail out if the tree root is marked as a 'stub' with the 'stop' tag
        # and we were not asked to ignore it
        if root_options['stop'] and not self.no_stop:
            return

        root_path = os.path.join(path, root_name)
        self.node_performer(root_path, root_options, root_children_nodes)

        # continue building the navigation tree recursively
        for child_tree in root_children_trees:
            self._scan_tree(root_path, child_tree)

    def _get_handbook_name(self, tree):
        """"""
        root_node, _ = self._get_root_node_and_children_trees(tree)
        node_name, _ = self._split_node_name_and_tags(root_node)

        return node_name

    @staticmethod
    def _get_root_node_and_children_trees(tree):
        """"""
        if isinstance(tree, dict):
            # tree here is a one-item dictionary representing a 'non-leaf directory'
            # (having children):
            #   - the 'key' is a string (root name followed by optional arguments)
            #   - the 'value' is a list of root's children trees
            root_node, root_children_trees = list(tree.items())[0]
        else:
            # tree here is a string representing a 'leaf directory' (having no children):
            #   - root name followed by optional arguments
            root_node = tree
            root_children_trees = []

        return root_node, root_children_trees

    @staticmethod
    def _forest_to_root_nodes(forest):
        """Return the root nodes of all the trees in forest"""

        root_nodes = []
        for tree in forest:
            if isinstance(tree, dict):
                root_nodes.append(list(tree.keys())[0])
            else:
                root_nodes.append(tree)

        # root node is root name followed by optional arguments
        return root_nodes

    def _forest_to_root_names(self, forest):
        """Return the root names of all the trees in forest"""

        root_nodes = self._forest_to_root_nodes(forest)

        root_names = []
        for node in root_nodes:
            node_name, _ = self._split_node_name_and_tags(node)
            root_names.append(node_name)

        return root_names

    @staticmethod
    def _split_node_name_and_tags(node):
        """"""
        split_pattern = re.compile(r'^(?P<name>[^@]+)(?P<tags>.*)$')
        split_match = split_pattern.match(node)
        node_name = split_match.group('name').strip()
        node_tags = split_match.group('tags').strip().split(' ')

        return node_name, node_tags

    def _get_node_options(self, tags, name):
        """"""
        # parse explicit arguments
        valid_keys = ['id', 'include', 'stop']
        node_options = {}
        options_pattern = re.compile(r'@(?P<k>[a-z]+)=?(?P<v>.*)')
        for tag in tags:
            options_match = options_pattern.match(tag)
            if options_match is None:
                continue
            if options_match.group('k') in valid_keys:
                node_options.update({options_match.group('k') : options_match.group('v')})
            else:
                print('Error: Unknown argument: {}'.format(options_match.group('k')))
                sys.exit()

        # set defaults
        node_options['stop'] = True if 'stop' in node_options else False
        if 'id' not in node_options or node_options['id'] == '':
            node_options['id'] = self._node_name_to_node_id(name)
        if 'include' in node_options and node_options['include'] == '':
            node_options['include'] = self._node_name_to_node_id(name)

        return node_options

    @staticmethod
    def _node_name_to_node_id(node_name):
        """"""
        # remove invalid characters
        valid_chars_pattern = re.compile(r'[^\w\-. ()]+')
        name = valid_chars_pattern.sub('', node_name)

        # additional formatting
        name = re.sub(' ', '-', name)
        name = re.sub('-+', '-', name)
        node_id = name.lower()

        return node_id
