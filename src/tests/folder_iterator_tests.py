"""
Tests for program.folder_iterator
"""

# pylint: disable=C0116

import unittest
import os
import program.folder_iterator
import program.console

class FolderIteratorTests(unittest.TestCase):
    """
    Tests for program.folder_iterator
    """
    def setUp(self):
        program.console.Console.VERBOSE = False

    def tests_can_get_directory_list_non_recursive(self):
        under_test = program.folder_iterator.FolderIterator(get_test_data_folder(), False, None)
        root = None
        count = 0
        for specification in under_test:
            root = specification
            count += 1
        self.assertEqual(1, count)
        self.assertEqual(3, len(root))
        self.assertTrue(root.has_log())
        self.assertEqual(get_test_data_folder(), root.directory)
        self.assertIn("file1.txt", root.files)
        self.assertIn("file2.csv", root.files)

    def tests_can_get_directory_list_recursive_with_regex(self):
        under_test = program.folder_iterator.FolderIterator(get_test_data_folder(),
            True, ".*\\.txt")
        all_files = []
        count = 0
        for specification in under_test:
            all_files += specification.files
            count += 1
        self.assertEqual(4, count)
        self.assertEqual(5, len(all_files))
        self.assertIn("file1.txt", all_files)
        self.assertIn("file3.txt", all_files)
        self.assertIn("file4.txt", all_files)
        self.assertIn("file5.txt", all_files)
        self.assertIn("file8.txt", all_files)

def get_test_data_folder():
    """
    Gets the test data folder
    """
    return os.path.join(os.getcwd(), "test_data")
