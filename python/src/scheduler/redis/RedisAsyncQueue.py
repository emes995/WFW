from aioredis import Redis

from scheduler.BaseQueue import BaseQueue
from task.BaseTask import BaseTask
from task.TaskParser import TaskParser


class RedisAsyncQueue(BaseQueue):
    def __init__(self, redis_connection: Redis, queue_name: str):
        self._redis: Redis = redis_connection
        self._queue_name: str = queue_name

    @property
    def queue_name(self) -> str:
        return self._queue_name

    async def add_task(self, task: BaseTask) -> bool:
        return await self._redis.lpush(self.queue_name, task.to_json())

    async def get_task(self) -> BaseTask:
        _jsonTask = await self._redis.lpop(self.queue_name)
        _task_inz = await TaskParser().parse(_jsonTask)
        return _task_inz[0]

    async def length(self) -> int:
        return await self._redis.llen(self.queue_name)
