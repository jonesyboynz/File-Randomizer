"""
Tests for program.arguments
"""

# pylint: disable=C0116

import unittest
import program.arguments

class ArgumentsTests(unittest.TestCase):
    """
    Test cases
    """
    def tests_can_parse_arguments(self):
        under_test = program.arguments.get_parser()
        args = under_test.parse_args("C:/stuff -name -order".split())
        self.assertEqual("C:/stuff", args.directory)
        self.assertTrue(args.name)
        self.assertTrue(args.order)
        self.assertFalse(args.undo)
        self.assertEqual(0, args.pick)
        self.assertFalse(args.recurse)
        self.assertIsNone(args.regex)

    def tests_can_parse_arguments_with_regex(self):
        under_test = program.arguments.get_parser()
        args = under_test.parse_args("C:/docs -undo -r -regex .*\\.pfd".split())
        self.assertEqual("C:/docs", args.directory)
        self.assertFalse(args.name)
        self.assertFalse(args.order)
        self.assertTrue(args.undo)
        self.assertEqual(0, args.pick)
        self.assertTrue(args.recurse)
        self.assertEqual(".*\\.pfd", args.regex)

    def tests_can_parse_arguments_with_pick(self):
        under_test = program.arguments.get_parser()
        args = under_test.parse_args("C:/flowers -pick 5".split())
        self.assertEqual("C:/flowers", args.directory)
        self.assertFalse(args.name)
        self.assertFalse(args.order)
        self.assertFalse(args.undo)
        self.assertEqual(5, args.pick)
        self.assertFalse(args.recurse)
        self.assertIsNone(args.regex)
