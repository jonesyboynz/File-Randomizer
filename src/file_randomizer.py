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

def sanity_check(args):
    """
    Sanity checks the directory chosen by the user directory
    """
    if args.nocheck or (not args.name and not args.order and not args.undo):
        return #Check can be skipped if the action will not modify any files
    directory = args.directory.lower()
    cwd = os.getcwd().lower()
    if any(["windows" in directory, "users" in directory, "system32" in directory,
        "drivers" in directory, "Recovery" in directory, directory == "/", directory == "/.",
        cwd == "c:/", cwd == "root/", len(cwd) < 15]) \
        or (directory.startswith("c:/") and len(directory) < 15) \
        or directory.endswith("appdata/roaming") \
        or directory.startswith("/root"):
        answer = input("Warning: you may be about to perform a dangerous"
             + " operation in a system directory."
             + "\nThis may break permenantly break your computer."
             + " Please carefully examine the paths below."
             + f"\nWorking directory: \"{os.getcwd()}\""
             + f"\nTarget directory: \"{args.directory}\""
             + "\n\nIf you are sure you want to proceed then enter: thatsok"
             + "\n> ")
        if answer != "thatsok":
            program.console.Console.error("Exiting on sanity check")
            sys.exit(1)

if __name__ == "__main__":
    run()
