"""
Tests for program.randomize_log_scope.py
"""

# pylint: disable=C0116

import os
import unittest
from program.randomize_log_scope import RandomizationLogScope

class RandomizationLogScopeTests(unittest.TestCase):
    """
    Tests for program.randomize_log_scope.py
    """

    def tests_can_load_log_file(self):
        with RandomizationLogScope(get_test_data_folder()) as scope:
            self.assertIn("file10.altered", scope)
            self.assertFalse("xxxx" in scope)
            self.assertEqual("file10.txt", scope["file10.altered"])

    def tests_add_to_scope(self):
        with RandomizationLogScope(get_test_data_folder()) as scope:
            scope.add_change("prev", "new")
            self.assertIn("new", scope)
            self.assertEqual("prev", scope["new"])

    def tests_remove_from_scope(self):
        with RandomizationLogScope(get_test_data_folder()) as scope:
            scope.add_change("prev_1", "new_1")
            self.assertIn("new_1", scope)
            output = scope.remove_change("new_1")
            self.assertEqual("prev_1", output)

    def tests_optimize_scope(self):
        with RandomizationLogScope(get_test_data_folder()) as scope:
            scope.add_change("prev_2", "new_2")
            scope.add_change("new_2", "new_3")
            scope.optimize()
            self.assertFalse("new_2" in scope)
            self.assertEqual("prev_2", scope["new_3"])

def get_test_data_folder():
    """
    Gets the test data folder
    """
    return os.path.join(os.getcwd(), "test_data")
