import uuid
import sys


class Task:
    def __init__(self, task_name: str):
        self._id = uuid.uuid4()
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

    def add_dependency(self, tasks: list):
        self._dependencies.extend(tasks)

    def has_dependencies(self):
        return len(self._dependencies) > 0

    def do_work(self):
        print(f'do work({self._task_name}) {self._id}')

    def __str__(self):
        return f'{self._task_name}:{self._dependencies}'


class Dependency:

    def __init__(self, task: Task):
        self._dependent_tasks = []
        self._custodian_task = task
        self._id = uuid.uuid4()

    @property
    def dependent_tasks(self):
        return self._dependent_tasks

    @property
    def get_custodian_task(self):
        return self._custodian_task

    def __add__(self, other: Task):
        assert isinstance(other, Task)
        self.dependent_tasks.append(other)
        return self

    def __len__(self):
        return len(self.dependent_tasks)

    def __str__(self):
        return f'dependent_tasks {[str(_t) for _t in self.dependent_tasks]}'


class DependencyManager:

    def __init__(self):
        self._dependencies = dict()

    def create_dependency(self, dependency_name: str, custodian_task: Task):
        _dp = self._dependencies.get(dependency_name)
        if _dp is None:
            _dp = Dependency(custodian_task)
            self._dependencies[dependency_name] = _dp
        return self._dependencies[dependency_name]

    def add_task_to_dependency(self, dependency_name: str, task: Task) -> Dependency:

        _dp = self._dependencies[dependency_name]
        _dp = _dp + task
        _dp.get_custodian_task.add_dependency([task])

        return _dp

    def get_dependency(self, dependency_name: str):
        _dp = self._dependencies.get(dependency_name, None)
        return _dp

    def get_dependent_tasks(self, task_name: str) -> list:
        _tasks = []
        for _k, _v in self._dependencies.items():
            _tasks.extend([_t for _t in _v.dependent_tasks if _t.task_name == task_name])
        return _tasks

    def get_dependencies_for_task(self, task_name: str) -> list:
        _tasks = []
        for _k, _v in self._dependencies.items():
            _tasks.extend([_t for _t in _v.dependent_tasks if _k == task_name])
        return _tasks

    def __str__(self):
        _items = [{"dependency_name": _k, "tasks": str(_v)} for _k, _v in self._dependencies.items()]
        return str(_items)


class Scheduler:

    def __init__(self):
        self._tasks = []

    def add_task(self, task: Task):
        self._tasks.append(task)

    def resolve_task_dependencies(self, task: Task):
        _tasks = []
        for _t in task.dependencies:
            if _t.has_dependencies():
                _tasks.extend(self.resolve_task_dependencies(_t))
            _tasks.append(_t)
        return _tasks

    def execute_tasks(self):
        for _t in self._tasks:
            _deps = self.resolve_task_dependencies(_t)
            for _dt in _deps:
                _dt.do_work()
            _t.do_work()

        return self


if __name__ == '__main__':

    dpm = DependencyManager()
    t1 = Task('t1')
    t2 = Task('t2')
    t3 = Task('t3')

    dp1: Dependency = dpm.create_dependency('task_1', t1)
    dp2: Dependency = dpm.create_dependency('task_2', t2)
    dp3: Dependency = dpm.create_dependency('task_3', t3)

    print(dpm)

    t11 = Task('t11')
    t12 = Task('t12')
    t13 = Task('t13')

    dpm.add_task_to_dependency('task_1', t11)
    dpm.add_task_to_dependency('task_1', t12)
    dpm.add_task_to_dependency('task_1', t13)

    t21 = Task('t21')
    t22 = Task('t22')
    t23 = Task('t23')

    dpm.add_task_to_dependency('task_2', t21)
    dpm.add_task_to_dependency('task_2', t11)
    dpm.add_task_to_dependency('task_2', t12)
    dpm.add_task_to_dependency('task_2', t22)

    t31 = Task('t31')
    t32 = Task('t32')

    t4 = Task('t4')
    dp4: Dependency = dpm.create_dependency('task_4', t4)

    dpm.add_task_to_dependency('task_4', t31)
    dpm.add_task_to_dependency('task_4', t1)

    print(dpm)

    sch = Scheduler()
    sch.add_task(t1)
    sch.add_task(t2)
    sch.add_task(t4)

    sch.execute_tasks()

    sys.exit(0)