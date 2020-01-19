#
#
#
from task.Task import Task
import asyncio


class SimpleScheduler:

    SCHEDULE_NAME = 'SimpleScheduler'

    def __init__(self, parent_scheduler):
        self._run_queue = asyncio.Queue()
        self._pending_tasks = []
        self._completed_tasks = []
        self._failed_taks = []
        self._running_tasks = []
        self._parent_scheduler = parent_scheduler

    async def _add_pending_task(self, task: Task):
        self._pending_tasks.append(task)
        await self._run_queue.put(task)

    async def add_task(self, task: Task):
        await self._add_pending_task(task)

    async def delete_task(self, task: Task):
        if task in self._pending_tasks:
            self._pending_tasks.remove(task)
        return task

    async def start(self):
        async def _schedule_tasks(_tasks: list):
            _sched_tasks = []
            _l_results = []
            for _tk in _tasks:
                _sched_tasks.append(_tk.do_work())
            _l_results = await asyncio.gather(*_sched_tasks)
            return _l_results

        while not self._run_queue.empty():
            _t = await self._run_queue.get()
            self._pending_tasks.remove(_t)
            self._running_tasks.append(_t)
            _tasks = await _t.resolve_dependencies()
            _results = await _schedule_tasks(_tasks)
            self._parent_scheduler.set_result_for_task(_t, _results)
