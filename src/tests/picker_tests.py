"""
Tests for program.picker.py
"""

# pylint: disable=C0116

import sys
import unittest
import program.arguments
import tests.test_utils
from program.picker import Picker

class PickerTests(unittest.TestCase):
    """
    Tests for program.picker.py
    """

    TEST_OUTPUT = tests.test_utils.TestFile()

    def setUp(self):
        program.console.Console.VERBOSE = False
        PickerTests.TEST_OUTPUT = tests.test_utils.TestFile()
        program.console.Console.STDOUT = PickerTests.TEST_OUTPUT

    def tearDown(self):
        program.console.Console.VERBOSE = True
        program.console.Console.STDOUT = sys.stdout

    def tests_can_pick_random_files(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -pick 3".split())
        under_test = Picker(args)
        under_test.pick_random(["a", "b", "c", "d", "e"], 3)
        # * 2 because the end produces an extra write
        self.assertEqual(3 * 2, len(PickerTests.TEST_OUTPUT))

    def tests_can_pick_random_files_from_undersized_array(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -pick 5".split())
        under_test = Picker(args)
        under_test.pick_random(["a", "b"], 5)
        # * 2 because the end produces an extra write
        self.assertEqual(2 * 2, len(PickerTests.TEST_OUTPUT))
