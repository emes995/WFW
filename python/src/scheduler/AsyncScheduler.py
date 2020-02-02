#
#
#
from task.Task import Task
from dependency.DependencyManager import DependencyManager
from dependency.Dependency import Dependency

import asyncio
import logging

g_dependency_mgr = DependencyManager()

class AsyncScheduler:

    SCHEDULE_NAME = 'AsyncScheduler'

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
        logging.debug('Starting scheduler')

        async def _schedule_tasks(_tasks: list):
            _sched_tasks = []
            _l_results = []
            for _tk in _tasks:
                _sched_tasks.append(_tk.do_work())
            _l_results = await asyncio.gather(*_sched_tasks)
            return _l_results

        while True:
            logging.debug('Attempting to fetch a task')
            _t = await self._run_queue.get()
            _dep: Dependency = await g_dependency_mgr.create_dependency(_t.task_name, _t)
            _tasks_to_execute = await g_dependency_mgr.get_tasks_in_dependency(_t.task_name)
            self._pending_tasks.remove(_t)
            self._running_tasks.append(_t)
            _tasks_to_execute.append(_t)
            _results = await _schedule_tasks(_tasks_to_execute
                                             )
            self._parent_scheduler.set_result_for_task(_t, _results)

        logging.info('Stopping scheduler')
