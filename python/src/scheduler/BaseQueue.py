from abc import abstractmethod, ABCMeta
from task.BaseTask import BaseTask


class QueueFullException(Exception):
    pass

class QueueEmptyException(Exception):
    pass


class BaseQueue(metaclass=ABCMeta):

    @abstractmethod
    async def add_task(self, task: BaseTask) -> bool:
        pass

    @abstractmethod
    async def get_task(self) -> BaseTask:
        pass

    @abstractmethod
    async def length(self):
        pass
