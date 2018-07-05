"""
Represents the site directory tree.

When scanned, an external performer is executed for each visited node.
"""

import os

class DirectoryTree:
    """Traverse a directory tree"""

    def __init__(self, site_root):
        """"""
        self.site_root = site_root
        self.node_performer = None

    def scan(self, root_path, group_title, node_performer):
        """Entry point for the scan of the directory tree"""
        self.node_performer = node_performer
        self._scan_tree(root_path, group_title)

    def _scan_tree(self, path, group_title):
        """Scan the provided directory tree recursively"""
        file_list = os.listdir(path)
        self.node_performer(path, group_title, file_list)

        for filename in file_list:
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                self._scan_tree(file_path, group_title)
