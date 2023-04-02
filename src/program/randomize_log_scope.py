"""
Tracks and logs the filename randomizations applied to the files in a directory
"""

import os
import program.constants
import program.console

class RandomizationLogScope:
    """
    Tracks filename changes in a directory
    """

    def __init__(self, directory):
        self.__directory = directory
        self.__log_filename = os.path.join(self.__directory, program.constants.LOG_FILENAME)
        self.__mappings = None

    def __enter__(self):
        self.__mappings = {}
        if os.path.isfile(self.__log_filename):
            self.__load_file()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            raise Exception(f"{exception_type}: {exception_value}", traceback)
        self.optimize()
        try:
            self.__write_mappings(self.__log_filename)
        except Exception as error:
            #failure to log the changes is a catastropic error
            #The program will log the changes then throw an exception in order to exit
            program.console.Console.error(f"Failed to write log to {self.__log_filename}")
            program.console.Console.error("Dumping mappings")
            for key, value in self.__mappings.items():
                program.console.Console.display(f"{key}|{value}")
            raise error

    def __write_mappings(self, filename):
        with open(filename, "r+", encoding="utf-8") as file:
            content = "\n".join([f"{key}|{value}" for key, value in self.__mappings.items()])
            file.write(content)

    def __load_file(self):
        raw_data = None
        with open(self.__log_filename, "r", encoding="utf-8") as file:
            raw_data = file.read()
        for pair in [x.split("|") for x in raw_data.split("\n")]:
            if len(pair) == 2:
                self.__mappings[pair[0]] = pair[1]

    def add_change(self, prev_name, current_name):
        """
        Adds a mapping to the mappings dictionary
        """
        if current_name in self:
            raise KeyError(f"{current_name} is already registered in RandomizationLogScope")
        self.__mappings[current_name] = prev_name

    def remove_change(self, name):
        """
        Removes a mapping from the log file
        """
        if name in self.__mappings:
            original_name = self.__mappings[name]
            del self.__mappings[name]
            return original_name
        return None

    def __contains__(self, key):
        return key in self.__mappings

    def __getitem__(self, key):
        if key in self:
            return self.__mappings[key]
        raise KeyError(f"{key} not in RandomizationLogScope")

    def __repr__(self):
        return f"RandomizationLogScope {self.__directory}\n{self.__log_filename}\n{self.__mappings}"

    def optimize(self):
        """
        Optimizes the mappings in this scope
        """
        for key, value in list(self.__mappings.items()):
            if value in self.__mappings:
                self.__mappings[key] = self.__mappings[value]
                del self.__mappings[value]
