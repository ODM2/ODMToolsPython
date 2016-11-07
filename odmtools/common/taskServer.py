from multiprocessing import Process, Queue
from odmtools.controller.logicPlotOptions import Probability, BoxWhisker, Statistics
import time
from odmtools.odmservices import SeriesService

__author__ = 'jmeline'

import logging
from odmtools.common.logger import LoggerTool


# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

class TaskServerMP:
    """
    The TaskServerMP class provides a target worker class method for queued processes
    """

    def __init__(self, numproc):
        """
        Initialize TaskServerMP and create the Dispatcher and Processes
        """

        self.numprocesses = numproc

        self.keepgoing = True

        # Initialize Dispatcher
        self.dispatcher = Dispatcher()

        # List of running processes
        self.Processes = []

        # List of tasks to be run
        self.tasks = []
        self.numtasks = len(self.tasks)

        self.completedTasks = {}

        for n in range(self.numprocesses):
            process = Process(target=TaskServerMP.worker, args=(self.dispatcher,))
            process.start()
            self.Processes.append(process)

    def setTasks(self, taskList):
        """
        Sets the tasks for the TaskServerMP to handle.
        """
        self.tasks.extend(taskList)
        self.numtasks = len(taskList)

    def processTasks(self):
        """
        Start the execution of tasks by the processes.
        """

        for i in self.tasks:
            self.dispatcher.putTask(i)


    def getOutput(self):
        """
        Collect completed tasks
        """


        #pull the output from completed tasks
        logger.debug("Trying to get something...")

        output = self.dispatcher.getResult()

        logger.debug("Got %s, %s" % output)

        self.completedTasks[output[0]] = output[1]

    def getCompletedTasks(self):
        """
        Retrieve all of the completedTasks
        """
        #wait for all tasks to complete running
        for _ in range(len(self.tasks)):
            self.getOutput()
        self.tasks = []

        return self.completedTasks

    def anyAlive(self):
        """
        Check if any processes are alive.
        """
        isalive = False
        for n in range(self.numprocesses):
            isalive = (isalive or self.Processes[n].is_alive())
        return isalive

    def processTerminate(self):
        """
        Stop the execution of tasks by the processes.
        """
        for n in range(self.numprocesses):
            # Terminate any running processes
            self.Processes[n].terminate()

        # Wait for all processes to stop
        while (self.anyAlive()):
            time.sleep(0.5)


    def worker(cls, dispatcher):
        """
        The worker creates a TaskProcessor Object
        :return:
        """

        while True:
            arg = dispatcher.getTask()

            task_type = arg[0] #(task_type, (arg1, arg2))
            task = arg[1]

            result = arg

            if task_type == "Probability":
                result = Probability(task)
            if task_type == "BoxWhisker":
                result = BoxWhisker(task[0], task[1])
            if task_type == "Summary":
                result = Statistics(task)
            if task_type == "InitEditValues":
                connection = SeriesService("sqlite:///:memory:")
                # connection._
                df = task[1]
                logger.debug("Load series from db")
                #setSchema(self.mem_service._session_factory.engine)
                df.to_sql(name="timeseriesresultvalues", con=connection._connection.engine, flavor='sqlite', index = False, chunksize = 10000)

                logger.debug("done loading database")
                result = connection
            if task_type == "UpdateEditDF":
                connection = task[1]
                result = connection.get_values()

            result = (task_type, result)

            # save the result
            dispatcher.putResult(result)


    # The multiprocessing worker must not require any existing object for execution
    worker = classmethod(worker)

    def worker_sp(self):
        """
        A single-process version of the worker method
        """



class Dispatcher:
    """
    The Dispatcher class manages the task and result queues.
    """

    def __init__(self):
        """
        Initialise the Dispatcher.
        """
        self.taskQueue = Queue()
        self.resultQueue = Queue()

    def getTaskQueue(self):
        """
        Get taskQueue
        """
        return self.taskQueue

    def getResultQueue(self):
        """
        Get resultQueue
        """
        return self.resultQueue

    def putTask(self, task):
        """
        Put a task on the task queue.
        """
        self.taskQueue.put(task)

    def getTask(self):
        """
        Get a task from the task queue.
        """
        return self.taskQueue.get()

    def putResult(self, output):
        """
        Put a result on the result queue.
        """
        self.resultQueue.put(output)

    def getResult(self):
        """
        Get a result from the result queue.
        """
        return self.resultQueue.get()

