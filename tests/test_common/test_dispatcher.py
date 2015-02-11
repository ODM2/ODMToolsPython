import multiprocessing
from common.taskServer import Dispatcher

__author__ = 'jmeline'


class TestDispatcher:
    def setup(self):
        self.dispatcher = Dispatcher()

    def test_getTaskQueue(self):

        # check to see if we get a multiprocessing.Queue from the dispatcher
        assert isinstance(self.dispatcher.getTaskQueue(), multiprocessing.queues.Queue)

    def test_getResultQueue(self):

        # check to see if we get a multiprocessing.Queue from the dispatcher
        assert isinstance(self.dispatcher.getResultQueue(), multiprocessing.queues.Queue)

    def test_Task(self):

        task = [('task_type', 'task_args')]

        # test putting
        try:
            self.dispatcher.putTask(task)
        except:
            assert False

        # test getter
        result = self.dispatcher.getTask()
        assert result == task


    def test_Result(self):

        original_result = [('task_type', 'task_result')]
        try:
            self.dispatcher.putResult(original_result)
        except:
            assert False

        # test getter
        received_result = self.dispatcher.getResult()
        assert received_result == original_result


