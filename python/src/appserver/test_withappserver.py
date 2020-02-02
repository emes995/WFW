#
# $Id$
#
from aiohttp import web
from dependency.DependencyManager import DependencyManager
from scheduler.Scheduler import Scheduler
from task.Task import Task

import logging
import logging.config
import asyncio
import os

gDepMgr = DependencyManager()
gSched = Scheduler(gDepMgr)


async def handle(request):

    class RunningTask(Task):
        def __init__(self, task_name: str):
            super().__init__(task_name=task_name)

        async def do_work(self):
            logging.info(f'Executing task name: {self.task_name}')
            for i in range(int(100)):
                await asyncio.sleep(1)
                logging.info(f'Task name {self.task_name} and index {i}')

            return self.task_name

    _name = request.query.get('name', 'RunningTask')
    logging.info(f'Running task {_name}')
    _rc = RunningTask(task_name=_name)
    await gSched.add_simple_task(_rc)
    return web.Response(text='queued up')


async def app_factory():
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
    asyncio.get_event_loop().create_task(gSched.start())
    return app


if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf'))
    web.run_app(app=app_factory())
