import typing
from aioredis import Redis

from scheduler.BaseQueue import BaseQueue
from task.BaseTask import BaseTask
from task.TaskParser import TaskParser


class RedisAsyncQueue(BaseQueue):
    def __init__(self, redis_connection: Redis, queue_name: str):
        self._redis: Redis = redis_connection
        self._queue_name: str = queue_name

    @property
    def queue_name(self):
        return self._queue_name

    async def add_task(self, task: BaseTask) -> bool:
        return await self._redis.lpush(self.queue_name, task.to_json())

    async def get_task(self) -> BaseTask:
        _jsonTask = await self._redis.lpop(self.queue_name)
        _task_inz = await TaskParser().parse(_jsonTask)
        return _task_inz[0]

    async def length(self):
        return await self._redis.llen(self.queue_name)

    # async def get_all(self, name: str):
    #     return await self._redis.hgetall(name=self.get_namespace(name=name))
    #
    # async def get(self, name: str, key: str):
    #     return await self._redis.hget(self.get_namespace(name=name), key=key)
    #
    # async def add(self, name: str, message: typing.Dict[str, typing.Any]):
    #     return await self._redis.hset(name=self.get_namespace(name=name), mapping=message)
    #
    # async def add_element(self, task: BaseTask):
    #     return await self.add(name=task.task_name, message={'task': task})
    #
    # async def queue_length(self, name: str):
    #     return await self._redis.hlen(name=self.get_namespace(name=name))
    #
    # async def delete(self, name: str):
    #     _keys = await self.get_all(name=name)
    #     _keys_deleted = []
    #     for _k in _keys:
    #         await self._redis.hdel(self.get_namespace(name=name), _k)
    #         _keys_deleted.append(_k)
    #     return _keys_deleted
