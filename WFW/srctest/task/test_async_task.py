import aiounittest

from dependency.Dependency import Dependency
from dependency.DependencyManager import DependencyManager
from task.Task import Task
from task.impl.LongLastingTask import LongLastingTask
from scheduler.Scheduler import Scheduler

class TestAsyncTask(aiounittest.AsyncTestCase):

    async def test_async_task(self):
        dpm = DependencyManager()
        t1 = LongLastingTask('t1')
        t2 = LongLastingTask('t2')
        t3 = LongLastingTask('t3')

        dp1: Dependency = await dpm.create_dependency('dep_1', t1)
        dp2: Dependency = await dpm.create_dependency('dep_2', t2)
        dp3: Dependency = await dpm.create_dependency('dep_3', t3)

        assert len(await dpm.get_tasks_in_dependency('dep_1')) == 0

        t11 = LongLastingTask('t11')
        t12 = LongLastingTask('t12')
        t13 = LongLastingTask('t13')
        await dpm.add_task_to_dependency('dep_1', t11)
        await dpm.add_task_to_dependency('dep_1', t12)
        await dpm.add_task_to_dependency('dep_1', t13)

        assert len(await dpm.get_tasks_in_dependency('dep_1')) == 3

        t21 = LongLastingTask('t21')
        t22 = LongLastingTask('t22')
        t23 = LongLastingTask('t23')
        await dpm.add_task_to_dependency('dep_2', t21)
        await dpm.add_task_to_dependency('dep_2', t11)
        await dpm.add_task_to_dependency('dep_2', t12)
        await dpm.add_task_to_dependency('dep_2', t22)
        await dpm.add_task_to_dependency('dep_2', t23)

        t31 = LongLastingTask('t31')
        t32 = LongLastingTask('t32')
        await dpm.add_task_to_dependency('dep_3', t31)
        await dpm.add_task_to_dependency('dep_3', t32)

        t4 = LongLastingTask('t4')
        dp4: Dependency = await dpm.create_dependency('dep_4', t4)
        await dpm.add_task_to_dependency('dep_4', t31)
        await dpm.add_task_to_dependency('dep_4', t1)

        assert len(await dpm.get_tasks_in_dependency('dep_4')) == 5
        assert len(await t1.resolve_dependencies()) == 3

        sch = Scheduler(dpm)
        await sch.add_task(t1)
        await sch.add_task(t2)
        await sch.add_task(t4)

        await sch.execute_tasks()

