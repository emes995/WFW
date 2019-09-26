import uuid
from dependency.Dependency import Dependency
from task.Task import Task

class DependencyManager:

    def __init__(self):
        self._dependencies = dict()

    def create_dependency(self, dependency_name: str, custodian_task: Task):
        _dp = self._dependencies.get(dependency_name)
        if _dp is None:
            _dp = Dependency(custodian_task)
            self._dependencies[dependency_name] = _dp
        return self._dependencies[dependency_name]

    def add_task_to_dependency(self, dependency_name: str, task: Task) -> Dependency:
        _dp = self._dependencies[dependency_name]
        _dp = _dp + task
        _dp.get_custodian_task.add_dependency([task])

        return _dp

    def get_dependency(self, dependency_name: str):
        _dp = self._dependencies.get(dependency_name, None)
        return _dp

    def get_dependent_tasks_for_task(self, task_name: str) -> list:
        _tasks = []
        for _k, _v in self._dependencies.items():
            _tasks.extend([_t for _t in _v.dependent_tasks if _t.task_name == task_name])
        return _tasks

    def get_tasks_in_dependency(self, dependency_name: str) -> list:
        _tasks = []
        for _t in self.get_dependency(dependency_name).dependent_tasks:
            _tasks.append(_t)
            _tasks.extend(_t.resolve_dependencies())
        return _tasks

    def __str__(self):
        _items = [{"dependency_name": _k, "tasks": str(_v)} for _k, _v in self._dependencies.items()]
        return str(_items)