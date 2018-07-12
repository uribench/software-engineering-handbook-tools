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
        Fail on non-existing given path

        If does not exist, display the provided error_message and terminate.
        """
        if not os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @staticmethod
    def fail_on_existing_path(path, error_message):
        """
        Fail on existing given path

        If does exist, display the provided error_message and terminate.
        """
        if os.path.exists(path):
            print('Error: {}: {}'.format(error_message, path))
            sys.exit()

        return True

    @classmethod
    def confirm_or_fail_on_existing_path(cls, path, warning_message):
        """
        On existing given path, get user confirmation or fail.
        """
        if os.path.exists(path):
            print('Warning: {}: {}'.format(warning_message, path))
            if not cls._confirmed():
                sys.exit()

        return True

    @staticmethod
    def _confirmed():
        """"""
        is_confirmed = False
        user_input = input('Overwrite anyway [yN]? ').lower()

        if user_input in ('y', 'yes'):
            is_confirmed = True

        return is_confirmed

    @classmethod
    def fail_on_nonexisting_filesystem(cls, path, error_message):
        """
        Fail on non-existing key directories of the handbook exist.

        If any does not exist, display the provided error_message and terminate.
        """
        cls.fail_on_nonexisting_path(os.path.join(path, 'Guides'), error_message)
        cls.fail_on_nonexisting_path(os.path.join(path, 'Topics'), error_message)
        cls.fail_on_nonexisting_path(os.path.join(path, 'config'), error_message)

        return True
