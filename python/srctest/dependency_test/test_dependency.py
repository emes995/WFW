from dependency.Dependency import Dependency
from task.BaseTask import BaseTask
from testutils.WFWAsyncTestCase import WFWAsyncTestCase


class TestDependency(WFWAsyncTestCase):

    async def test_dependency(self):

        t1 = BaseTask('t1')
        dep_ = Dependency(t1)
        assert t1 == dep_.get_custodian_task

        t2 = BaseTask('t1-1')
        t3 = BaseTask('t1-2')
        t4 = BaseTask('t1-3')

        dep_.add_tasks([t2, t3, t4])
        assert len(dep_) == 3
