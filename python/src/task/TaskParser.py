#
#
#

from dependency.DependencyManager import g_dependency_mgr
from dependency.Dependency import Dependency
import json
import logging
from importlib import import_module


class TaskParser:

    @classmethod
    async def parse_task(cls, _task: dict, _parent: dict = None):
        _pkg = import_module(f'{_task["package"]}.{_task["type"]}')
        _clz = getattr(_pkg, _task['type'])
        _task_inz = _clz(**_task['init'])

        _dependencies = _task.get('depends-on', [])
        _dep_name = _task['name']
        _dep_inz: Dependency = await g_dependency_mgr.create_dependency(_dep_name, _task_inz)

        _task_children = _task.get('children', [])
        for _tc in _task_children:
            if isinstance(_tc, str):
                logging.info(f'Looking for task {_tc}')
            else:
                _task_c_inz = await cls.parse_task(_tc, _task_inz)
                await g_dependency_mgr.add_task_to_dependency(_dep_name, _task_c_inz)

        return _task_inz

    @classmethod
    async def parse(cls, json_str: str):
        _root = json.loads(json_str)
        _root_tasks = []
        for _task in _root['tasks']:
            logging.debug(f'Parsing task {_task}')
            _root_tasks.append(await cls.parse_task(_task))

        return _root_tasks
