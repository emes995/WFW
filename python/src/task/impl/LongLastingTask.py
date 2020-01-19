#
#
#
import asyncio
from task.Task import Task


class LongLastingTask(Task):

    def __init__(self, task_name: str):
        super().__init__(task_name=task_name)

    async def do_work(self):
        print(f'Executing task name: {self.task_name}')
        for i in range(int(10)):
            await asyncio.sleep(1)
            print(f'Task name {self.task_name} and index {i}')

        return self.task_name
