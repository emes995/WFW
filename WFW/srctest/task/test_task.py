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