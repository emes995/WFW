import typing
import uuid

from task.BaseTask import BaseTask


class Dependency:

    def __init__(self, task):
        self._dependent_tasks = []
        self._custodian_task = task
        self._id = uuid.uuid4()

    @property
    def dependent_tasks(self) -> typing.List[BaseTask]:
        return self._dependent_tasks

    @property
    def get_custodian_task(self) -> BaseTask:
        return self._custodian_task

    def remove_task(self, task: BaseTask):
        self.dependent_tasks.remove(task)

    def add_tasks(self, tasks: list):
        for _t in tasks:
            assert isinstance(_t, BaseTask)
            self + _t

    def __add__(self, other: BaseTask) -> typing.Any:
        assert isinstance(other, BaseTask)
        self.dependent_tasks.append(other)
        return self

    def __len__(self) -> int:
        return len(self.dependent_tasks)

    def __str__(self):
        return f'dependent_tasks {[str(_t) for _t in self.dependent_tasks]}'
