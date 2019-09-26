from task.Task import Task
from dependency.DependencyManager import DependencyManager

class Scheduler:

    def __init__(self, dependency_manager: DependencyManager):
        self._tasks = []
        self._dependency_manager = dependency_manager

    def add_task(self, task: Task):
        self._tasks.append(task)

    def execute_tasks(self):
        for _t in self._tasks:
            _tasks = _t.resolve_dependencies()
            for _dt in _tasks:
                _dt.do_work()
            _t.do_work()

        return self
