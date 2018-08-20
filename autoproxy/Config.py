"""
Class to store config variables for app-wide.
"""

# Modules Import
import re
import colored
from colored import stylize

""" Config Class """
class Config():
    """ Class for app-wide config management.

    Attributes
    ----------
    TO_LOG : bool
        Default is true. Append app-wide logs to log list.
    ERROR_TO_LOG : bool
        Default is true. Append app-wide error logs to log list.
    PRINT_LOG : bool
        Default is true. Print out app-wide log through execution.
    PRINT_ERROR_LOG : bool
        Default is true. Print out app-wide error log through execution.
    IN_NOTEBOOK : bool
        Default is set on file opening. Identification variable for Jupyter notebook.
    PROGRESS_BAR : bool
        Default is false. App-wide progress bar.
    USE_PROXY : bool
        Default is true. App-wide proxy support.
    LOGS : list
        List of application-wide logs.

    Methods
    -------
    add_log()
        Creates and/or prints log entry based on configurations set.
    print_log()
        Prints out all of the logs in the log list.
    """

    def __init__(self):
        """ Initialization method. """

        # Append to log list.
        self.TO_LOG = True
        self.ERROR_TO_LOG = True

        # Print log.
        self.PRINT_LOG = False
        self.PRINT_ERROR_LOG = False

        # Notebook settings.
        import __main__ as main
        if not hasattr(main, '__file__'):
            self.IN_NOTEBOOK = True
        else:
            self.IN_NOTEBOOK = False

        # Lists.
        self.LOGS = []

    """ LOG COMMANDS """
    def add_log(self, err, log):
        """ Creates and/or prints log entry based on configurations set.

        Parameters
        ----------
        err : bool
            Indicates whether this is an error log or not.
        log : string
            String of the given log.

        Example
        -------
        c = Config()
        c.add_log(err = False, "This is not an error log.")
        -> This is not an error message.
        c.add_log(err = True, "This is an error log.")
        [ERROR] -> This is not an error log.
        """

        if self.TO_LOG and err is False:
            fin = ' - > ' + log
            self.LOGS.append(fin)
        elif self.ERROR_TO_LOG and err is True:
            fin = '[ERROR] - > ' + log
            self.LOGS.append(fin)

        colored_log = []
        for text in log.split():
            if "[" in text and "]" in text:
                content_dict = {',':'', '.':'', ';': ''}
                for key in content_dict:
                    text = text.replace(key, content_dict[key])

                if 'False' or 'True' or 'None' in text:
                    inner_text = text.replace('[', '').replace(']', '')
                    if 'False' in text or 'None' in text:
                        inner_text = stylize(inner_text, colored.fg('light_red'))
                    elif 'True' in text:
                        inner_text = stylize(inner_text, colored.fg('green'))
                    else:
                        inner_text = stylize(inner_text, colored.fg('yellow'))

                    text = '[' + inner_text + ']'
                colored_log.append(text)
            else:
                colored_log.append(text)

        log = ' '.join(colored_log)

        if self.PRINT_LOG is True and err is False:
            print(stylize(' -> ', colored.fg('white')) + log)

        if self.PRINT_ERROR_LOG is True and err is True:
            print(stylize('[ERROR]', colored.fg('red')) + stylize(' -> ', colored.fg('white')) + log)

    def print_log(self):
        """ Prints out all of the logs in the log list.

        Example
        -------
        c = Config()
        c.PRINT_LOG = False
        c.PRINT_ERROR_LOG = False
        c.add_log(err = False, "This is not an error log.")
        c.add_log(err = True, "This is an error log.")

        c.print_log()
        -> This is not an error message.
        [ERROR] -> This is not an error log.
        """
        for log in self.LOGS:
            print(log)
