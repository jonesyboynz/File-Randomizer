"""
Class for file randomization
"""

import os
import uuid
import random
import math
import program.folder_iterator
import program.randomize_log_scope
import program.console

class Randomizer:
    """
    Class for file randomization
    """
    def __init__(self, args):
        self.__name = args.name
        self.__order = args.order
        self.__iterator = program.folder_iterator.FolderIterator( \
            args.directory, args.recurse, args.regex)

    def apply(self):
        """
        Applies the filename randomization
        """
        for specification in self.__iterator:
            self.__randomize_directory(specification)

    def __randomize_directory(self, specification):
        program.console.Console.display_optional(f"Processing \"{specification.directory}\"")
        order_prefixes = self.generate_file_order_prefixes(specification.files)
        with program.randomize_log_scope.RandomizationLogScope(specification.directory) as scope:
            for file in specification.files:
                original_name = scope[file] if file in scope else file
                new_name = self.generate_name(original_name, order_prefixes[file])
                full_path_old = os.path.join(specification.directory, file)
                full_path_new = os.path.join(specification.directory, new_name)
                if os.path.exists(full_path_new):
                    program.console.Console.error( \
                        f"Rename failed: \"{full_path_old}\" → \"{full_path_new}\""
                        + " destination already exists")
                    continue
                try:
                    os.rename(full_path_old, full_path_new)
                    program.console.Console.display(f"R \"{full_path_old}\" → \"{full_path_new}\"")
                    scope.add_change(file, new_name)
                except (FileExistsError, NotADirectoryError, IsADirectoryError, OSError) as error:
                    program.console.Console.error( \
                        f"Rename failed: \"{full_path_old}\" → \"{full_path_new}\"")
                    program.console.Console.error(str(error))

    def generate_file_order_prefixes(self, specification_files):
        """
        Generates a dictionary that provides an order prefix for each file
        """
        orders = {}
        files = specification_files.copy()
        if not self.__order:
            for file in files:
                orders[file] = None
        else:
            random.shuffle(files)
            i = 0
            fill = int(math.log(len(files), 10)) + 1
            for file in files:
                orders[file] = str(i).zfill(fill)
                i += 1
        return orders

    def generate_name(self, filename, order_prefix):
        """
        Generates a new filename for a file
        """
        filename, ext = os.path.splitext(filename)
        if self.__name:
            filename = str(uuid.uuid4())
        if order_prefix is not None:
            return f"{order_prefix} - {filename}{ext}"
        return f"{filename}{ext}"
