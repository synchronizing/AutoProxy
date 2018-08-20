"""
Class to run asychronous functions.
"""

from autoproxy.Config import Config

# Modules Import
import asyncio
import aiohttp

class Task():
    """ Class for task management and execution.

    Attributes
    ----------
    config : Config() class
        Configuration for the given task class.
    tasks : list
        List of tasks that will be executed on the run command.
    loop : asyncion event loop
        Event loop given by asyncio for asynchronous execution.

    Methods
    -------
    add_task()
        Adds task to the current task class.
    add_tasks()
        Adds tasks (plural) to the current task class.
    run()
        Runs the added tasks.
    """

    def __init__(self, config = Config()):
        """ Initialization method.

        Parameters
        ----------
        config : Config() class
            A configuration class for variable management.
        """
        self.config = config

        self.tasks = []
        self.loop = asyncio.get_event_loop()

    def add_task(self, task):
        """ Adds task to the current task class.

        Parameters
        ----------
        task : asynchronous function
            A function that can be ran asychronously by asyncio.

        Example
        -------
        def asynchronous_function():
            print("hey!")
            asyncio.timeout(0)

        c = Config()
        t = Task(config = c)
        t.add_task(asynchronous_function())
        """

        self.tasks.append(asyncio.ensure_future(task))

    def add_tasks(self, tasks):
        """ Adds tasks (plural) to the current task class.

        Parameters
        ----------
        task : list
            A list of asynchronous functions that can be ran asychronously by asyncio.

        Example
        -------
        def asynchronous_function():
            print("hey!")
            asyncio.timeout(0)

        c = Config()
        t = Task(config = c)
        t.add_tasks([
            asynchronous_function(),
            asynchronous_function(),
            asynchronous_function(),
        ])
        """

        for task in tasks:
            self.add_task(task)

    def run(self):
        """ Runs the added tasks.

        Example
        -------
        def asynchronous_function():
            print("hey!")
            asyncio.timeout(0)

        c = Config()
        t = Task(config = c)
        t.add_task(asynchronous_function())
        t.run()
        hey!

        Notes
        -----
        This function will either run on the existing Jupyter's notebook event loop,
        or will run a new loop until completion; this is managed automatically.
        """
        if self.config.IN_NOTEBOOK is True:
            self.loop.create_task(asyncio.wait(self.tasks))
        else:
            self.loop.run_until_complete(asyncio.wait(self.tasks))
