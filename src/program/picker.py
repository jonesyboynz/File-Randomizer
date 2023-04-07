"""
Class for picking random files
"""

import os
import random
import program.folder_iterator
import program.console

class Picker:
    """
    Class for picking random files
    """
    def __init__(self, args):
        self.__pick_count = args.pick
        self.__iterator = program.folder_iterator.FolderIterator( \
            args.directory, args.recurse, args.regex)

    def apply(self):
        """
        Picks files randomly
        """
        all_files = []
        for specification in self.__iterator:
            for file in specification.files:
                all_files.append(os.path.join(specification.directory, file))
        Picker.pick_random(all_files, self.__pick_count)

    @staticmethod
    def pick_random(all_files, count):
        """
        Picks a number of random files
        """
        program.console.Console.display_optional(f"Picking {count} file(s)!")
        if len(all_files) < count:
            program.console.Console.display_optional( \
                f"Fewer files than pick number - pick {count} from {len(all_files)}")
        files = all_files.copy()
        for i in range(0, count):
            if len(files) == 0:
                break
            index = random.randint(0, len(files) - 1)
            picked = files.pop(index)
            if program.console.Console.VERBOSE:
                program.console.Console.display(f"P {i + 1} - \"{picked}\"")
            else:
                program.console.Console.display(f"{picked}")
