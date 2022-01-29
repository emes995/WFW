import asyncio

import aiounittest
from dependency.Dependency import Dependency
from dependency.DependencyManager import DependencyManager
from scheduler.AsyncScheduler import AsyncScheduler
from task.impl.LongLastingTask import LongLastingTask
from scheduler.Scheduler import Scheduler
import logging
import logging.config
import os


class TestAsyncTask(aiounittest.AsyncTestCase):

    async def test_async_task(self):
        logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'config', 'logging.conf'))
        logging.info('Starting')
        dpm = DependencyManager()
        t1 = LongLastingTask('t1')
        t2 = LongLastingTask('t2')
        t3 = LongLastingTask('t3')

        dp1: Dependency = dpm.create_dependency('dep_1', t1)
        dp2: Dependency = dpm.create_dependency('dep_2', t2)
        dp3: Dependency = dpm.create_dependency('dep_3', t3)

        assert len(dpm.get_tasks_in_dependency('dep_1')) == 0

        t11 = LongLastingTask('t11')
        t12 = LongLastingTask('t12')
        t13 = LongLastingTask('t13')
        dpm.add_task_to_dependency('dep_1', t11)
        dpm.add_task_to_dependency('dep_1', t12)
        dpm.add_task_to_dependency('dep_1', t13)

        assert len(dpm.get_tasks_in_dependency('dep_1')) == 3

        t21 = LongLastingTask('t21')
        t22 = LongLastingTask('t22')
        t23 = LongLastingTask('t23')
        dpm.add_task_to_dependency('dep_2', t21)
        dpm.add_task_to_dependency('dep_2', t11)
        dpm.add_task_to_dependency('dep_2', t12)
        dpm.add_task_to_dependency('dep_2', t22)
        dpm.add_task_to_dependency('dep_2', t23)

        t31 = LongLastingTask('t31')
        t32 = LongLastingTask('t32')
        dpm.add_task_to_dependency('dep_3', t31)
        dpm.add_task_to_dependency('dep_3', t32)

        t4 = LongLastingTask('t4')
        dp4: Dependency = dpm.create_dependency('dep_4', t4)
        dpm.add_task_to_dependency('dep_4', t31)
        dpm.add_task_to_dependency('dep_4', t1)

        deps = t1.resolve_dependencies()
        assert len(deps) == 3, f'acquired {len(deps)} instead of 3'

        deps = dpm.get_tasks_in_dependency('dep_4')
        assert len(deps) == 5, f'acquired {len(deps)} instead of 5'

        sch = Scheduler(dpm)
        async_sched = AsyncScheduler(sch)
        sch.add_scheduler(AsyncScheduler.SCHEDULER_NAME, async_sched)

        await sch.add_task(t1)
        await sch.add_task(t2)
        await sch.add_task(t3)
        await sch.add_task(t4)

        class ExitTask(LongLastingTask):
            def __init__(self, scheduler: AsyncScheduler):
                self._scheduler = scheduler
                super().__init__(task_name='exit_task')

            async def do_work(self):
                logging.debug('Starting stop_scheduler_task')
                for _r in range(60):
                    await asyncio.sleep(1)

                logging.debug(f'Completed stop_scheduler_scheduler {self._scheduler.SCHEDULER_NAME}')
                self._scheduler.stop_scheduler()

        await sch.add_task(ExitTask(async_sched))
        await sch.start()
        results = await sch.collect_results_for_task(t1)
        logging.info(f'Results: {results}')