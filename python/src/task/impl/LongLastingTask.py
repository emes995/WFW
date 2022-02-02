#
#
#
import asyncio
import logging
from task.BaseTask import BaseTask


class LongLastingTask(BaseTask):

    def __init__(self, task_name: str, no_iterations: int = 60):
        super().__init__(task_name=task_name)
        self._no_iterations = no_iterations

    async def do_work(self):
        logging.info(f'Executing task name: {self.task_name}')
        for i in range(int(self._no_iterations)):
            await asyncio.sleep(1)
            logging.info(f'Task name {self.task_name} and index {i}')

        return self.task_name
