from multiprocessing import Process, Queue
from controller.logicPlotOptions import SeriesPlotInfo, Probability, BoxWhisker, Statistics

__author__ = 'jmeline'


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

        # i = tasks
        self.i = 0

        # j = completed_tasks
        self.j = 0

        self.completedTasks = {}


        # initialize task id
        self.taskId = None

        for n in range(self.numprocesses):
            process = Process(target=TaskServerMP.worker, args=(self.dispatcher,))
            process.start()
            self.Processes.append(process)

    def setTaskType(self, taskId):
        """
        Sets the task ID to determine which type of tasks to run
        """
        self.taskId = taskId

    def setTasks(self, taskList):
        """
        Sets the tasks for the TaskServerMP to handle.
        """
        self.tasks = taskList
        self.numtasks = len(taskList)

        # reset counters
        self.i = 0
        self.j = 0


    def processTasks(self, resfunc=None):
        """
        Start the execution of tasks by the processes.
        """

        for i in self.tasks:
            self.dispatcher.putTask(i)
            self.getOutput()

    def getOutput(self):
        """
        Collect completed tasks
        """

        print "Trying to get something..."

        output = self.dispatcher.getResult()

        print "Got %s, %s" % output

        self.completedTasks[output[0]] = output[1]

        self.j += 1


    def getCompletedTasks(self):
        """
        Retrieve all of the completedTasks
        """

        return self.completedTasks

    def anyAlive(self):
        """
        Check if any processes are alive.
        """
        isalive = False
        for n in range(self.numprocesses):
            isalive = (isalive or self.Processes[n].is_alive())
        return isalive


    def worker(cls, dispatcher):
        """
        The worker creates a TaskProcessor Object
        :return:
        """

        while True:
            arg = dispatcher.getTask()

            result = None

            task_type = arg[0]
            task = arg[1]

            if task_type == "Probability":
                result = Probability(task)
            if task_type == "BoxWhisker":
                result = BoxWhisker(task[0], task[1])
            if task_type == "Summary":
                result = Statistics(task)

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

