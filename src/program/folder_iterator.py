"""
A class that retrieves viable files for actions
"""

import os
import re
import program.console
import program.constants

class FolderIterator:
    """
    A class that retrieves viable files for actions
    """

    def __init__(self, directory, recursive, regex):
        self.__directory = directory
        self.__recursive = recursive
        self.__regex = re.compile(regex, re.IGNORECASE) if regex is not None else None
        self.__folders = []
        self.__at_end = False

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.__folders) == 0 and not self.__at_end:
            self.__get_folders()
        if len(self.__folders) == 1:
            self.__at_end = True
        if len(self.__folders) == 0:
            self.__at_end = False
            raise StopIteration
        return self.__get_files(self.__folders.pop(0))

    def __get_folders(self):
        """
        Acquires the directories that this program needs to examine
        """
        if self.__recursive:
            self.__folders = self.__get_folders_recurse(self.__directory)
        else:
            self.__folders = [self.__directory]

    def __get_folders_recurse(self, path):
        """
        Recursive folder search
        """
        folders = [path]
        for item in os.listdir(path):
            object_path = os.path.join(path, item)
            if os.path.isdir(object_path):
                folders += self.__get_folders_recurse(object_path)
        return folders

    def __get_files(self, path):
        """
        Gets viable files from a directory
        """
        files = []
        log = None
        for item in os.listdir(path):
            object_path = os.path.join(path, item)
            if not os.path.isdir(object_path) \
                and (self.__regex is None or self.__regex.match(item)):
                if item == program.constants.LOG_FILENAME:
                    log = item
                else:
                    files.append(item)
        program.console.Console.display_optional(f"Found {len(files)} file(s) in \"{path}\"")
        return FolderSpecification(path, files, log)

class FolderSpecification:
    """
    Contents of a folder
    """
    def __init__(self, directory, files, log):
        self.directory = directory
        self.files = files
        self.log = log

    def __len__(self):
        return len(self.files)

    def __repr__(self): # for debugging
        return f"FolderSpecification: {self.directory}\n{self.files}\n{self.log}"

    def has_log(self):
        """
        Indicates if this folder has a log
        """
        return self.log is not None
