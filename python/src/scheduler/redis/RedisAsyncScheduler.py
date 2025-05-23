#
#
#
import asyncio
import logging

import aioredis

from dependency.DependencyManager import DependencyManager
from scheduler.BaseQueue import BaseQueue, QueueEmptyException
from scheduler.aiobased.AsyncScheduler import AsyncScheduler
from scheduler.redis.RedisAsyncQueue import RedisAsyncQueue


class RedisAsyncScheduler(AsyncScheduler):

    def __init__(self, dependency_manager: DependencyManager, use_redis_db: int = 0):
        self._redis = aioredis.from_url(f'redis://localhost:6379/{use_redis_db}')
        super().__init__(dependency_manager=dependency_manager,
                         queue_impl=RedisAsyncQueue(redis_connection=self._redis, queue_name='scheduler'))
        self._ping_task = asyncio.create_task(self._ensure_connection_is_alive(ping_interval=5))

    async def _ensure_connection_is_alive(self, ping_interval: int):
        while True:
            _ping = await self._redis.ping()
            await asyncio.sleep(ping_interval)
            logging.info(f'Redis server responded with: {_ping}')

    async def close(self):
        logging.info('Cancelling connection monitoring')
        self._ping_task.cancel()
        logging.info('Closing redis connection')
        await self._redis.close()
        logging.info('Redis connection has been closed')

    async def stop_scheduler(self):
        await self.close()
        await super().stop_scheduler()

    async def start(self):
        logging.info('Starting Redis Scheduler')
        _qm: BaseQueue = self._queue_impl

        while True:
            try:
                _msg = await _qm.get_task()
            except QueueEmptyException:
                pass
            if self._stop_scheduler:
                logging.info(f'Stopping Scheduler {self.SCHEDULER_NAME} as requested')
                break
            await asyncio.sleep(1.0)
