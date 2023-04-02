"""
Utilities for the unit testing
"""

import os

def get_test_data_folder():
    """
    Gets the test data folder
    """
    return os.path.join(os.getcwd(), "test_data")

class TestFile:
    """
    A file for use in unit tests
    """
    def __init__(self):
        self.messages = []

    def write(self, message):
        """
        Stores the written message
        """
        self.messages.append(message)

    def __len__(self):
        return len(self.messages)
