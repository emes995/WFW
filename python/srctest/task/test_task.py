import unittest
from task.Task import Task

class TestTask(unittest.TestCase):

    def test_single_task(self):
        t1 = Task('task_1')

        assert t1.task_name == 'task_1'

    def test_single_task_dependency(self):
        t1 = Task('task_2')
        t1.add_dependency([Task('task_3'), Task('task_4')])

        assert t1.has_dependencies()
        assert len(t1.dependencies) == 2

    def test_basic_operations(self):

        t1 = Task('t1')
        t2 = Task('t2')
        t3 = Task('t3')
        t4 = Task('t4')

        assert t1 != t2
        assert t1 < t2

        t1.add_dependency([t2, t3, t4])
        assert len(t1.dependencies) == 3

        t1.delete_dependency(t2) == 2
        assert len(t1.dependencies)


    def test_lots_of_tasks(self):
        for i in range(int(1e+6)):
            _t = Task('{i}')
