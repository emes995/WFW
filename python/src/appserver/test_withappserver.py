#
# $Id$
#
from aiohttp import web
from dependency.DependencyManager import g_dependency_mgr
from scheduler.Scheduler import Scheduler
from task.Task import Task
from task.TaskParser import TaskParser

import logging
import logging.config
import asyncio
import os

gSched = Scheduler(g_dependency_mgr)


def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")


async def handle_task(request):
    _j_task = request.query.get('tasks', {})
    logging.info(f'Running task {_j_task}')
    _tasks = await TaskParser.parse(_j_task)
    for _t in _tasks:
        await gSched.add_task(_t)
    return web.Response(text=_t[0].task_name)


async def handle(request):

    class RunningTask(Task):
        def __init__(self, task_name: str):
            super().__init__(task_name=task_name)

        async def do_work(self):
            logging.info(f'Executing task name: {self.task_name}')
            for i in range(int(20)):
                await asyncio.sleep(1)
                logging.info(f'Task name {self.task_name} and index {i}')

            return self.task_name

    _name = request.query.get('name', 'RunningTask')
    logging.info(f'Running task {_name}')
    _rc = RunningTask(task_name=_name)
    await gSched.add_task(_rc)
    return web.Response(text='queued up')


async def app_factory():
    app = web.Application()
    app.add_routes([web.get('/', handle_task),
                    web.get('/{name}', handle_task),
                    web.get('/{tasks}', handle_task)])
    asyncio.get_event_loop().set_exception_handler(handle_exception)
    asyncio.get_event_loop().create_task(gSched.start())
    return app


if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf'))
    web.run_app(app=app_factory())
