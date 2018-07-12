"""
Validates various aspects of the handbook file system.
"""

import os
import sys

class HandbookValidation:
    """Validates various aspects of the handbook file system"""

    @staticmethod
    def fail_on_nonexisting_path(path, error_message):
        """
        Validate that the given path exists, or fail.

        If does not exist, display the provided error_message and terminate.
        """
        if not os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @staticmethod
    def fail_on_existing_path(path, error_message):
        """
        Validate that the given path does not exist, or fail.

        If does exist, display the provided error_message and terminate.
        """
        if os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @classmethod
    def fail_on_nonexisting_filesystem(cls, path, error_message):
        """
        Validate that key directories of the handbook exist, or fail.

        If any does not exist, display the provided error_message and terminate.
        """
        cls.fail_on_nonexisting_path(os.path.join(path, 'Guides'), error_message)
        cls.fail_on_nonexisting_path(os.path.join(path, 'Topics'), error_message)
        cls.fail_on_nonexisting_path(os.path.join(path, 'config'), error_message)

        return True
