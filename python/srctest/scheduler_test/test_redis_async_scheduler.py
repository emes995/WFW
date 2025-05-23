import asyncio
import logging
import logging.config
import os

from dependency.DependencyManager import DependencyManager
from scheduler.redis.RedisAsyncScheduler import RedisAsyncScheduler
from testutils.WFWAsyncTestCase import WFWAsyncTestCase


class TestRedisAsyncScheduler(WFWAsyncTestCase):

    async def test_redis_async_scheduler(self):
        logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__),
                                                     '..', '..', 'src', 'config', 'logging.conf'))
        dpm = DependencyManager()
        async_sched = RedisAsyncScheduler(dependency_manager=dpm)
        self.assertEqual(True, True)

        async def do_work():
            for _r in range(40):
                await asyncio.sleep(1.0)
            logging.info('Attempting to close RedisAsyncScheduler')
            await async_sched.stop_scheduler()

        asyncio.create_task(do_work())
        await async_sched.start()
