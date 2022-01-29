#
#
#
import asyncio
import logging
from task.BaseTask import BaseTask


class LongLastingTask(BaseTask):

    def __init__(self, task_name: str):
        super().__init__(task_name=task_name)

    async def do_work(self):
        logging.info(f'Executing task name: {self.task_name}')
        for i in range(int(10)):
            await asyncio.sleep(1)
            logging.info(f'Task name {self.task_name} and index {i}')

        return self.task_name
