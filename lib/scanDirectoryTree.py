import os

class ScanDirectoryTree:
    """
    Traverse a directory tree.

    An external performer is executed for each visited node.
    """

    def __init__(self, site_root):
        """"""
        self.site_root = site_root

    def scan(self, root_path, title, node_performer):
        """Entry point for the scan of the directory tree"""
        self.node_performer = node_performer
        self.title = title
        self._scan_tree(root_path)

    def _scan_tree(self, path):
        """Scan the provided directory tree recursively"""
        file_list = os.listdir(path)
        self.node_performer(path, self.title, file_list)

        for filename in file_list:
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                self._scan_tree(file_path)
