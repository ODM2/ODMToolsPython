from multiprocessing import Process, Queue

__author__ = 'jmeline'

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

class TaskServerMP:
    """
    The TaskServerMP class provides a target worker class method for queued processes
    """

    def __init__(self, numproc):
        """
        Initialize TaskServerMP and create the Dispatcher and Processes
        """

        self.numprocesses = numproc

        self.Processes = []
        self.keepgoing = True

        # Initialize Dispatcher
        self.dispatcher = Dispatcher()

        for n in range(self.numprocesses):
            process = Process(target=TaskServerMP.worker, args=(self.dispatcher,))
            process.start()
            self.Processes.append(process)

    def processTasks(self, resfunc=None):
        """
        Start the execution of tasks by the processes.
        """

        self.keepgoing = True



        pass


    def worker(cls, dispatcher):
        """
        The worker creates a TaskProcessor Object
        :return:
        """

        pass

    # The multiprocessing worker must not require any existing object for execution
    worker = classmethod(worker)


