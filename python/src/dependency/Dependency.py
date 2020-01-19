import uuid
from task.Task import Task


class Dependency:

    def __init__(self, task: Task):
        self._dependent_tasks = []
        self._custodian_task = task
        self._id = uuid.uuid4()

    @property
    def dependent_tasks(self):
        return self._dependent_tasks

    @property
    def get_custodian_task(self):
        return self._custodian_task

    async def remove_task(self, task: Task):
        return self.dependent_tasks.remove(task)

    async def add_tasks(self, tasks: list):
        for _t in tasks:
            assert isinstance(_t, Task)
            self + _t

    def __add__(self, other: Task):
        assert isinstance(other, Task)
        self.dependent_tasks.append(other)
        return self

    def __len__(self):
        return len(self.dependent_tasks)

    def __str__(self):
        return f'dependent_tasks {[str(_t) for _t in self.dependent_tasks]}'
