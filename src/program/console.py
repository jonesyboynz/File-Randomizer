"""
Controls the program console
"""

import sys
import datetime

class Console:
    """
    Controls the program console
    """

    VERBOSE=True
    DATE_FORMAT="%Y/%m/%d %H:%M:%S"
    MESSAGE_FORMAT="[{0}]: {1}{2}"
    STDOUT=sys.stdout
    STDERR=sys.stderr

    @staticmethod
    def error(message, end="\n"):
        """
        Displays an error
        """
        print(Console.format_message(message, end), file=Console.STDERR,end="")

    @staticmethod
    def display(message, end="\n"):
        """
        Displays a message
        """
        print(Console.format_message(message, end), file=Console.STDOUT,end="")

    @staticmethod
    def display_optional(message, end="\n"):
        """
        Displays a message if verbose is enabled
        """
        if Console.VERBOSE:
            print(Console.format_message(message, end), file=Console.STDOUT,end="")

    @staticmethod
    def display_optional_raw(message, end="\n"):
        """
        Displays a raw message if verbose is enabled
        """
        if Console.VERBOSE:
            print(message, end=end)

    @staticmethod
    def format_message(message, end):
        """
        Formats the provided message
        """
        time = datetime.datetime.now().strftime(Console.DATE_FORMAT)
        if Console.VERBOSE:
            return Console.MESSAGE_FORMAT.format(time, message, end)
        return message + end
