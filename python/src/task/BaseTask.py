#
# @date:
# @version:
#
import json
import typing

from utils.OrderedIdGenerator import OrderedIdGenerator

_BEGIN_SEED_KEY = 'f{uuid.uuid4()}'


class BaseTask:
    def __init__(self, task_name: str):
        self._id = OrderedIdGenerator.generate_ordered_id(_BEGIN_SEED_KEY)
        self._task_name = task_name
        self._dependencies = []

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def task_name(self):
        return self._task_name

    @property
    def id(self):
        return self._id

    def __hash__(self):
        return hash(self.id)

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return isinstance(other, BaseTask) and other.id == self.id

    def delete_dependency(self, task):
        self.dependencies.remove(task)

    def add_dependency(self, tasks: list):
        _myself = [_t for _t in tasks if _t == self]
        assert len(_myself) == 0, 'Can not add task onto itself as a dependency'
        self._dependencies.extend(tasks)

    def has_dependencies(self):
        return len(self._dependencies) > 0

    def _resolve_dependencies(self, task) -> list:
        _tasks = []
        for _t in task.dependencies:
            if _t.has_dependencies():
                _tasks.extend(self._resolve_dependencies(_t))
            _tasks.append(_t)
        return _tasks

    def resolve_dependencies(self) -> typing.List[typing.Any]:
        return self._resolve_dependencies(self)

    async def do_work(self):
        print(f'do work({self._task_name}) {self._id}')

    def to_json(self) -> str:
        from dependency.DependencyManager import g_dependency_mgr
        _dep = g_dependency_mgr.get_dependency(dependency_name=self._task_name)
        _dep_tasks: typing.List[BaseTask] = _dep.dependent_tasks
        return json.dumps(
            {
                'name': self._task_name,
                'type': type(self),
                'package': str(self.__class__),
                'init': {},
                'depends-on': [_t.task_name for _t in self.resolve_dependencies()],
                'do-work': (),
                'children': [_d.task_name for _d in _dep_tasks]
            })

    def __str__(self):
        return f'{self._task_name}:{self._dependencies}'
