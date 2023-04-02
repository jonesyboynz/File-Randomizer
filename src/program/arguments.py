"""
Defines the program's runtime arguments
"""

import argparse

def get_parser():
    """
    Gets the runtime arguments
    """
    parser = argparse.ArgumentParser(prog="File Randomizer",
                    description=
                    "A tool for randomizing filenames, the order of the files in a directory"
                    + " or for picking random files."
                    + "\nThe filename adjustments are fully reversable via an undo command.",
                    epilog="By Simon Jones")
    parser.add_argument("directory", type=str,
        help="Directory to apply the action.")
    parser.add_argument("-order", "-o", action="store_true", default=False,
        help="Randomize file order.")
    parser.add_argument("-name", "-n", action="store_true", default=False,
        help="Randomize filenames.")
    parser.add_argument("-undo", "-u", action="store_true", default=False,
        help="Undo randomizations.")
    parser.add_argument("-pick", "-p", type=int, default=0,
        help="Pick N random files.")
    parser.add_argument("-recurse", "-r", action="store_true", default=False,
        help="Recurse through all sub-directories and apply the action")
    parser.add_argument("-regex", "-re", type=str, default=None,
        help="Filters the matching files using a regex statement when picking"
            + " or randomizing filenames.")
    parser.add_argument("-verbose", "-v", type=int, default=1,
        help="Sets the verbosity in the console.")
    return parser
