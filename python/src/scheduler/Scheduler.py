from task.Task import Task
from dependency.DependencyManager import DependencyManager

class Scheduler:

    def __init__(self, dependency_manager: DependencyManager):
        self._tasks = []
        self._dependency_manager = dependency_manager

    async def add_task(self, task: Task):
        self._tasks.append(task)

    async def execute_tasks(self):
        for _t in self._tasks:
            _tasks = _t.resolve_dependencies()
            for _dt in _tasks:
                await _dt.do_work()
            await _t.do_work()

        return self
