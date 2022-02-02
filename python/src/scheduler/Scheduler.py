from task.BaseTask import BaseTask
from dependency.DependencyManager import DependencyManager


class Scheduler:

    _SMALL_AMOUNT_OF_TIME = 0.001

    def __init__(self, dependency_manager: DependencyManager):
        self._dependency_manager = dependency_manager
        self._results = {}

    async def add_task(self, task: BaseTask):
        raise NotImplementedError(f'add_task must be implemented in {type(self)}')

    async def delete_task(self, task: BaseTask):
        raise NotImplementedError(f'delete_task must be implemented in {type(self)}')

    async def start(self):
        raise NotImplementedError(f'start must be implemented in {type(self)}')

    def set_result_for_task(self, task, result):
        raise NotImplementedError(f'set_result_for_task must be implemented in {type(self)}')
        # self._results[task.id] = result

    async def collect_results_for_task(self, task: BaseTask):
        raise NotImplementedError(f'collect_results_for_task must be implemented in {type(self)}')
