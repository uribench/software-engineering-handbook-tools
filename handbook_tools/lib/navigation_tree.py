"""
Represents the configuration navigation tree.

When scanned, an external performer is executed for each visited node.
"""

import os
import shutil
import yaml
from handbook_tools.lib.navigation_tree_node import NavigationTreeNode
from handbook_tools.lib.handbook_validation import HandbookValidation

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
        self.tree_config_filename = 'root.yml'
        self.node_performer = None
        self.tree = self.load_tree_config_file(self.navigation_path, self.tree_config_filename)

    def scan(self, node_performer):
        """Entry point for the scan of the configuration navigation tree"""
        self.node_performer = node_performer
        self._scan_tree(self.site_root, self.tree)

    def fail_on_existing_root_node_dir(self, overwrite=False):
        """Make sure the root node directory does not exist already"""
        root_node, _ = self._get_root_node_and_children_trees(self.tree)
        tree_root_path = os.path.join(self.site_root, root_node.name)

        if not overwrite:
            warning_message = 'Target directory already exists'
            HandbookValidation.confirm_or_fail_on_existing_path(tree_root_path, warning_message)

        shutil.rmtree(tree_root_path, ignore_errors=True)

    def load_tree_config_file(self, path, filename):
        """Load navigation tree configuration file"""
        tree_config_full_filename = os.path.join(self.site_root, *[path, filename])

        error_message = 'Root config file does not exist'
        HandbookValidation.fail_on_nonexisting_path(tree_config_full_filename, error_message)

        try:
            with open(tree_config_full_filename, 'r') as tree_config_file:
                navigation_tree = yaml.load(tree_config_file)
        except IOError as err:
            print('Error: operation failed: {}'.format(err.strerror))

        return navigation_tree

    def _scan_tree(self, path, tree):
        """
        Scan the provided navigation tree recursively.

        Args:
            path (str): location for the root directory for the root node of the
                provided tree.
            tree (dict of {str: str} or str): nested data structure representing
                the navigation tree from path onward.
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
            # tree here is a string representing a 'leaf directory'
            # (having no children):
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
