import aiounittest

from dependency.Dependency import Dependency
from task.Task import Task


class TestDependency(aiounittest.AsyncTestCase):

    async def test_dependency(self):

        t1 = Task('t1')
        dep_ = Dependency(t1)
        assert t1 == dep_.get_custodian_task

        t2 = Task('t1-1')
        t3 = Task('t1-2')
        t4 = Task('t1-3')

        dep_.add_tasks([t2, t3, t4])
        assert len(dep_) == 3
