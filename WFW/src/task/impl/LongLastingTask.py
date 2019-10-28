#
#
#
import asyncio
from src.task.Task import Task


class LongLastingTask(Task):

    def __init__(self, task_name: str):
        super().__init__(task_name=task_name)

    async def do_work(self):
        async for i in range(1e+4):
            asyncio.sleep(1)
