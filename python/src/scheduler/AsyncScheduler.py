#
#
#
from asyncio import QueueEmpty

from task.BaseTask import BaseTask
from dependency.DependencyManager import g_dependency_mgr
from dependency.Dependency import Dependency
from scheduler.Exceptions import ResultNotAvailable

import asyncio
import logging
import functools
import typing


class AsyncScheduler:

    SCHEDULER_NAME = 'AsyncScheduler'

    def __init__(self, parent_scheduler):
        self._run_queue = asyncio.Queue()
        self._pending_tasks: typing.List[BaseTask] = []
        self._completed_tasks: typing.List[BaseTask] = []
        self._failed_tasks: typing.List[BaseTask] = []
        self._running_tasks: typing.Dict[BaseTask, asyncio.Task] = dict()
        self._parent_scheduler = parent_scheduler
        self._stop_scheduler = False

    @property
    def parent_scheduler(self):
        return self._parent_scheduler

    def stop_scheduler(self):
        self._stop_scheduler = True

    def cancel_task(self, task: BaseTask):
        _task = self._running_tasks[task]
        if not _task.cancelled() and not _task.done():
            logging.info(f'Canceling task {task.task_name}')
            _task.cancel(msg=f'Canceling task: {task.task_name}')
        else:
            logging.info(f'Attempting to cancel completed/canceled task {_task.task_name}')

    async def _add_pending_task(self, task: BaseTask):
        self._pending_tasks.append(task)
        await self._run_queue.put(task)

    async def add_task(self, task: BaseTask):
        await self._add_pending_task(task)

    def delete_task(self, task: BaseTask):
        if task in self._pending_tasks:
            self._pending_tasks.remove(task)
        return task

    async def start(self):
        logging.debug('Starting Async scheduler')

        def _task_completed(task: typing.Type[BaseTask], instance_obj, completed_task):
            _result = completed_task.result()
            logging.info(f'Task Completed task_test: {task.task_name} with result: {_result}')
            instance_obj.parent_scheduler.set_result_for_task(task, _result)

        def _schedule_tasks(_tasks: typing.List[BaseTask], instance_obj):
            for _tk in _tasks:
                _tf = asyncio.create_task(_tk.do_work(), name=_tk.task_name)
                _tf.add_done_callback(functools.partial(_task_completed, _tk, instance_obj))
                self._running_tasks[_tk] = _tf

        while True:
            try:
                _t = self._run_queue.get_nowait()
                logging.debug(f'Fetched task {_t.task_name}')
                _dep: Dependency = g_dependency_mgr.create_dependency(_t.task_name, _t)
                _tasks_to_execute = g_dependency_mgr.get_tasks_in_dependency(_t.task_name)
                self._pending_tasks.remove(_t)
                _tasks_to_execute.append(_t)
                _schedule_tasks(_tasks_to_execute, self)
            except QueueEmpty:
                pass
            await asyncio.sleep(0.001)
            if self._stop_scheduler:
                logging.info(f'Stopping Scheduler {self.SCHEDULER_NAME} as requested')
                break

        logging.info(f'Stopping scheduler {self.SCHEDULER_NAME}')

    async def collect_results_for_task(self, task: BaseTask):
        logging.debug(f'Collecting result for task {task.id}')
        _task = self._running_tasks[task]
        if _task.done() and not _task.cancelled():
            return self._results[task.id]

        raise ResultNotAvailable()
