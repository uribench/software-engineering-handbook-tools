import os

class ScanDirectoryTree:
    """
    Traverse a directory tree.

    An external performer is executed for each visited node.
    """

    def __init__(self, siteRoot):
        """"""
        self.siteRoot = siteRoot

    def scan(self, rootPath, nodePerformer):
        """Entry point for the scan of the directory tree"""
        self.nodePerformer = nodePerformer
        self.scanTree(rootPath)

    def scanTree(self, path):
        """Scan the provided directory tree recursively"""
        fileList = os.listdir(path)
        self.nodePerformer(path, fileList)

        for fileName in fileList:
            filePath = os.path.join(path, fileName)
            if os.path.isdir(filePath):
                self.scanTree(filePath)
