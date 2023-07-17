"""
Sanity checks the directory chosen by the user
"""
import sys
import os
import program.console

def sanity_check(args):
    """
    Sanity checks the directory chosen by the user
    """
    if args.nocheck or (not args.name and not args.order and not args.undo):
        return #Check can be skipped if the action will not modify any files
    directory = args.directory.lower()
    cwd = os.getcwd().lower()
    if any(["windows" in directory,
        "users" in directory,
        "system32" in directory,
        "drivers" in directory,
        "Recovery" in directory,
        directory == "/",
        directory == "/.",
        cwd == "root/",
        cwd.startswith("c:/") and len(cwd) < 10]) \
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
