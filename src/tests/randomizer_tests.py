"""
Tests for program.randomizer.py
"""

# pylint: disable=C0116

import unittest
import program.arguments
from program.randomizer import Randomizer

class RandomizerTests(unittest.TestCase):
    """
    Tests for program.randomizer.py
    """
    def tests_can_generate_order_prefixes(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -order".split())
        under_test = Randomizer(args)
        result = under_test.generate_file_order_prefixes(["a", "b", "c"])
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertTrue(result["a"] in ("0", "1", "2"))

    def tests_can_generate_random_filename_without_prefix(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -name".split())
        under_test = Randomizer(args)
        result = under_test.generate_name("something.pdf", None)
        self.assertTrue(result.endswith(".pdf"))

    def tests_can_generate_random_filename_with_prefix(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -name".split())
        under_test = Randomizer(args)
        result = under_test.generate_name("something.pdf", "01")
        self.assertTrue(result.endswith(".pdf"))
        self.assertTrue(result.startswith("01 - "))

    def tests_can_generate_filename_with_prefix(self):
        args = program.arguments.get_parser().parse_args("C:/stuff -order".split())
        under_test = Randomizer(args)
        result = under_test.generate_name("thefile", "024")
        self.assertEqual("024 - thefile", result)
