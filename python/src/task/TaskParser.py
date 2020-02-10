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
        _i_task = _task['task']
        _pkg = import_module(f'{_i_task["package"]}.{_i_task["type"]}')
        _clz = getattr(_pkg, _i_task['type'])
        _task_inz = _clz(**_i_task['init'])

        _dependencies = _i_task.get('depends_on', [])
        _dep_name = _i_task['name']
        _dep_inz: Dependency = await g_dependency_mgr.create_dependency(_dep_name, _task_inz)

        _task_children = _i_task.get('children', [])
        for _tc in _task_children:
            if isinstance(_tc, str):
                logging.info(f'Looking for task {_tc}')
            else:
                _task_c_inz = cls.parse_task(_tc, _task_inz)
                await _dep_inz.add_tasks(_tc)

        return _task_inz

    @classmethod
    async def parse(cls, json_str: str):
        _root = json.loads(json_str)
        _root_tasks = []
        for _task in _root['tasks']:
            logging.debug(f'Parsing task {_task}')
            _root_tasks.append(await cls.parse_task(_task))

        return _root_tasks
