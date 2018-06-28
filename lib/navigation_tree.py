"""
Represents the configuration navigation tree.

When scanned, an external performer is executed for each visited node.
"""

import os
import sys
import yaml
from lib.navigation_tree_node import NavigationTreeNode

class NavigationTree:
    """Represents the configuration navigation tree"""

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

        # bail out if the tree root is marked as a 'stub' with the 'stop' tag
        # and we were not asked to ignore it
        if root_node.options['stop'] and not self.no_stop:
            return

        root_path = os.path.join(path, root_node.name)
        self.node_performer(root_path, root_node.options, root_children_nodes)

        # continue building the navigation tree recursively
        for child_tree in root_children_trees:
            self._scan_tree(root_path, child_tree)

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

        node = NavigationTreeNode(root_node)

        return node, root_children_trees

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
            node_name, _ = NavigationTreeNode.split_node_name_and_tags(node)
            root_names.append(node_name)

        return root_names
