from task.Task import Task
from dependency.DependencyManager import DependencyManager
import asyncio

class Scheduler:

    def __init__(self, dependency_manager: DependencyManager):
        self._tasks = []
        self._dependency_manager = dependency_manager

    async def add_task(self, task: Task):
        self._tasks.append(task)

    async def execute_tasks(self):

        async def _schedule_tasks(_tasks: Task):
            _sched_tasks = []
            for _t in _tasks:
                _sched_tasks.append(_t.do_work())
            _results = await asyncio.gather(*_sched_tasks)
            return _results

        for _t in self._tasks:
            print(f'Executing task {_t.task_name}')
            _tasks = await _t.resolve_dependencies()
            _results = await _schedule_tasks(_tasks)
            _results.append(await _t.do_work())

        return self
