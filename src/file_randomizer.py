"""
Program entrypoint
"""

import os
import re
import sys
import program.arguments
import program.console
from program.randomizer import Randomizer
from program.picker import Picker

def run():
    """
    Runs the program
    """
    #Arguments
    args = program.arguments.get_parser().parse_args()
    program.console.Console.VERBOSE = args.verbose != 0

    #Validation
    validate_folder_exists(args.directory)
    validate_regex(args.regex)

    #Execution
    if args.order or args.name:
        randomizer = Randomizer(args)
        randomizer.apply()
    if args.undo:
        pass #todo
    if args.pick > 0:
        picker = Picker(args)
        picker.apply()
    if not args.order and not args.name and not args.undo and args.pick <= 0:
        program.console.Console.display_optional("Not much to do -_-")
    program.console.Console.display_optional_raw("")

def validate_folder_exists(directory):
    """
    Validates the target directory exists
    """
    if not os.path.isdir(directory):
        program.console.Console.error(f"\"{directory}\" does not exist")
        sys.exit(1)

def validate_regex(regex):
    """
    Validates the provided regex statement
    """
    if regex is None:
        return
    try:
        re.compile(regex)
    except re.error:
        program.console.Console.error(f"Invalid regex \"{regex}\"")
        sys.exit(1)

if __name__ == "__main__":
    run()
