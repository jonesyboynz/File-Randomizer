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
from program.undoer import Undoer
from program.sanity_check import sanity_check

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
    sanity_check(args)

    #Execution
    if args.order or args.name:
        randomizer = Randomizer(args)
        randomizer.apply()
    if args.undo:
        undoer = Undoer(args)
        undoer.apply()
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
        if re.match(""".+"( -(o|order|u|undo|n|name|p|pick|)| [0-9]+)+$""", \
            directory, re.IGNORECASE):
            program.console.Console.error((f"The directory \"{directory}\" does not exist."
                "\n\t- This may be caused by python improperly parsing the command line argumets."
                "\n\t- Try removing the trailing \\ from the directory."))
        else:
            program.console.Console.error(f"The directory \"{directory}\" does not exist")
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
