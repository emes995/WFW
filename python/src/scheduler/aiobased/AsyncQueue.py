#
#
#
import asyncio
from asyncio import QueueFull, QueueEmpty

from scheduler.BaseQueue import BaseQueue, QueueEmptyException
from scheduler.BaseQueue import QueueFullException
from task.BaseTask import BaseTask


class AsyncQueue(BaseQueue):

    def __init__(self, wait_interval: float = 0.01, max_wait: float = 5.0):
        self._queue = asyncio.Queue()
        self._wait_interval = wait_interval
        self._max_wait = max_wait

    async def add_task(self, task: BaseTask):
        _local_wait: float = 0.0
        _status = False
        while _local_wait < self._max_wait:
            try:
                await self._queue.put(item=task)
                _status = True
                break
            except QueueFull:
                await asyncio.sleep(self._wait_interval)
                _local_wait += self._wait_interval

        if not _status:
            raise QueueFullException()

    async def get_task(self) -> BaseTask:
        try:
            _task = self._queue.get_nowait()
        except QueueEmpty:
            raise QueueEmptyException()

        return _task

    async def length(self):
        return self._queue.qsize()
