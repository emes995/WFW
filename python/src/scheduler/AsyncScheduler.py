#
#
#
from task.Task import Task
from dependency.DependencyManager import g_dependency_mgr
from dependency.Dependency import Dependency

import asyncio
import logging
import functools


class AsyncScheduler:

    SCHEDULE_NAME = 'AsyncScheduler'

    def __init__(self, parent_scheduler):
        self._run_queue = asyncio.Queue()
        self._pending_tasks = []
        self._completed_tasks = []
        self._failed_taks = []
        self._running_tasks = []
        self._parent_scheduler = parent_scheduler

    @property
    def parent_scheduler(self):
        return self._parent_scheduler

    async def _add_pending_task(self, task: Task):

        # async def _manage_dependencies(i_task: Task):
        #     _ordered_task = []
        #     for _td in i_task.dependencies:
        #         if _td.has_dependencies():
        #             _ordered_task.append(await _manage_dependencies(_td))
        #         else:
        #             _ordered_task.append(_td)
        #
        #     print(_ordered_task)
        #
        # await _manage_dependencies(task)
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

        def _task_completed(task: Task, instance_obj, completed_task):
            _result = completed_task.result()
            logging.info(f'Task Completed task: {task.task_name} with result: {_result}')
            instance_obj.parent_scheduler.set_result_for_task(_t, _result)

        async def _schedule_tasks(_tasks: list, instance_obj):
            _sched_tasks = []
            _l_results = []
            for _tk in _tasks:
                _sched_tasks.append(_tk.do_work())
                _t = asyncio.ensure_future(*_sched_tasks)
                _t.add_done_callback(functools.partial(_task_completed, _tk, instance_obj))

        while True:
            logging.debug('Attempting to fetch a task')
            _t = await self._run_queue.get()
            _dep: Dependency = await g_dependency_mgr.create_dependency(_t.task_name, _t)
            _tasks_to_execute = await g_dependency_mgr.get_tasks_in_dependency(_t.task_name)
            self._pending_tasks.remove(_t)
            self._running_tasks.append(_t)
            _tasks_to_execute.append(_t)
            await _schedule_tasks(_tasks_to_execute, self)

        logging.info('Stopping scheduler')
