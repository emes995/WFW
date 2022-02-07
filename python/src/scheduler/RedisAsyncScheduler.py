#
#
#
import asyncio
import logging

import aioredis

from dependency.DependencyManager import DependencyManager
from scheduler.AsyncScheduler import AsyncScheduler


class RedisAsyncScheduler(AsyncScheduler):

    def __init__(self, dependency_manager: DependencyManager):
        super().__init__(dependency_manager=dependency_manager)
        self._redis = aioredis.from_url("redis://localhost:27645")
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
