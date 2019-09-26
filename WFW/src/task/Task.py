#
# @date:
# @version:
#

import uuid

class Task:
    def __init__(self, task_name: str):
        self._id = uuid.uuid4()
        self._task_name = task_name
        self._dependencies = []

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def task_name(self):
        return self._task_name

    @property
    def id(self):
        return self._id

    def __eq__(self, other):
        return isinstance(other, Task) and other.id == self.id

    def add_dependency(self, tasks: list):
        self._dependencies.extend(tasks)

    def has_dependencies(self):
        return len(self._dependencies) > 0

    def _resolve_dependencies(self, task):
        _tasks = []
        for _t in task.dependencies:
            if _t.has_dependencies():
                _tasks.extend(self._resolve_dependencies(_t))
            _tasks.append(_t)
        return _tasks

    def resolve_dependencies(self):
        return self._resolve_dependencies(self)

    def do_work(self):
        print(f'do work({self._task_name}) {self._id}')

    def __str__(self):
        return f'{self._task_name}:{self._dependencies}'
