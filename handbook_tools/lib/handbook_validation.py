"""
Validates various aspects of the handbook file system.
"""

import os
import sys

class HandbookValidation:
    """Validates various aspects of the handbook file system"""

    @staticmethod
    def validate_path_or_exit(path, error_message):
        """
        Validate that the given path exists.

        If does not exist, display the provided error_message and terminate.
        """
        if not os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @staticmethod
    def validate_no_path_or_exit(path, error_message):
        """
        Validate that the given path does not exist.

        If does exist, display the provided error_message and terminate.
        """
        if os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @classmethod
    def validate_filesystem_or_exit(cls, path, error_message):
        """
        Validate that key directories of the handbook exist.

        If any does not exist, display the provided error_message and terminate.
        """
        cls.validate_path_or_exit(os.path.join(path, 'Guides'), error_message)
        cls.validate_path_or_exit(os.path.join(path, 'Topics'), error_message)
        cls.validate_path_or_exit(os.path.join(path, 'config'), error_message)

        return True
