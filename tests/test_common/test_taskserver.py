from odmtools.common.taskServer import TaskServerMP
from multiprocessing import cpu_count

__author__ = 'jmeline'


class TestTaskServer:
    def setup(self):
        self.numprocess = cpu_count()
        self.taskserver = TaskServerMP(numproc=self.numprocess)


    def test_init_and_Shutdown(self):

        # check that there are the same number of processes as cpu_count
        assert len(self.taskserver.Processes) == self.numprocess
        # check that dispatcher is available
        assert self.taskserver.dispatcher
        # check that there are no tasks
        assert len(self.taskserver.tasks) == 0
        # check that there are no completed tasks yet
        assert len(self.taskserver.completedTasks) == 0

        self.shutdown()

    def test_workers(self):

        task_type = "task_1"
        task_args = "task_1_args"
        # put a task into the task queue
        tasks = [(task_type, task_args)]

        # put tasks into the task server to be executed
        self.taskserver.setTasks([tasks])

        # check that there is a task in the task list
        assert len(self.taskserver.tasks) == 1

        # unfortunately unable to test multiprocessor within py.test, need to manually run it from commandline

        self.shutdown()

    def shutdown(self):
        # test that there are running processes
        for i in self.taskserver.Processes:
            assert i.is_alive()

        # test stopping of the processes
        self.taskserver.processTerminate()

        # check that the task server has completed shutting down
        assert not self.taskserver.anyAlive()

        # test that there are no running processes individually
        for i in self.taskserver.Processes:
            assert not i.is_alive()




