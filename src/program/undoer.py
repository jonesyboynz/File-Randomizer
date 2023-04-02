"""
Class for reversing file randomization
"""

import os
import program.folder_iterator
import program.randomize_log_scope
import program.console

class Undoer:
    """
    Class for reversing file randomization
    """
    def __init__(self, args):
        self.__iterator = program.folder_iterator.FolderIterator( \
            args.directory, args.recurse, None)

    def apply(self):
        """
        Applies the filename randomization
        """
        for specification in self.__iterator:
            if not specification.has_log():
                program.console.Console.display_optional( \
                    f"Skipping \"{specification.directory}\" - No log")
                continue
            Undoer.undo_randomization(specification)

    @staticmethod
    def undo_randomization(specification):
        """
        Reverses the randomization inside a directory
        """
        program.console.Console.display_optional( \
            f"Undoing randomizations in \"{specification.directory}\"")
        with program.randomize_log_scope.RandomizationLogScope(specification.directory) as scope:
            for current, previous in scope.mappings():
                full_path_old = os.path.join(specification.directory, previous)
                full_path_current = os.path.join(specification.directory, current)
                if os.path.exists(full_path_old):
                    program.console.Console.error( \
                        f"Undo failed: \"{full_path_current}\" → \"{full_path_old}\""
                        + " destination already exists")
                    continue
                try:
                    os.rename(full_path_current, full_path_old)
                    program.console.Console.display( \
                        f"U \"{full_path_current}\" → \"{full_path_old}\"")
                    scope.remove_change(current)
                except (FileExistsError, NotADirectoryError, IsADirectoryError, OSError) as error:
                    program.console.Console.error( \
                        f"Undo failed: \"{full_path_current}\" → \"{full_path_old}\"")
                    program.console.Console.error(str(error))
