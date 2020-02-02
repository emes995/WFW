from task.Task import Task
from dependency.DependencyManager import DependencyManager
#from scheduler.SimpleScheduler import SimpleScheduler
from scheduler.AsyncScheduler import AsyncScheduler
import asyncio


class Scheduler:

    _SMALL_AMOUNT_OF_TIME = 0.001

    def __init__(self, dependency_manager: DependencyManager):
        self._dependency_manager = dependency_manager
        self._scheduler_helpers = {}
        self._task_to_scheduler = {}
        self._results = {}

        self._initialize()

    def add_scheduler(self, scheduler_type: str, scheduler):
        if scheduler_type not in self._scheduler_helpers:
            self._scheduler_helpers[scheduler_type] = scheduler

        return self._scheduler_helpers[scheduler_type]

    def _get_scheduler(self, scheduler_type: str):
        return self._scheduler_helpers[scheduler_type]

    def _initialize(self):
        # self.add_scheduler(SimpleScheduler.SCHEDULE_NAME, SimpleScheduler(self))
        self.add_scheduler(AsyncScheduler.SCHEDULE_NAME, AsyncScheduler(self))

    def _find_scheduler_for_task(self, task: Task):
        if task in self._task_to_scheduler:
            return self._task_to_scheduler[task]
        return None

    async def add_simple_task(self, task: Task):
        # await self._scheduler_helpers[SimpleScheduler.SCHEDULE_NAME].add_task(task)
        await self._scheduler_helpers[AsyncScheduler.SCHEDULE_NAME].add_task(task)

    async def delete_task(self, task: Task):
        _schd = self._find_scheduler_for_task(task)
        if not _schd:
            return None
        return _schd.delete_task(task)

    async def start(self):
        _schedulers = [_schd.start() for _k, _schd in self._scheduler_helpers.items()]
        await asyncio.gather(*_schedulers)

    def set_result_for_task(self, task, result):
        self._results[task] = result

    async def collect_results_for_task(self, task: Task):
        return self._results[task]
