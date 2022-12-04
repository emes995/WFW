import aiounittest
import logging
import logging.config
import os

from task.TaskParser import TaskParser
from testutils.WFWAsyncTestCase import WFWAsyncTestCase


class TestAsyncTask(WFWAsyncTestCase):

    async def test_task_parser(self):
        _curDir = os.path.dirname(__file__)
        logging.config.fileConfig(fname=os.path.join(_curDir, '..', '..', 'src', 'config', 'logging.conf'))
        logging.info('Starting')

        with open(os.path.join(_curDir, 'json', 'simpletask.json')) as _jF:
            _js = _jF.read()

        _tasks = await TaskParser.parse(_js)
        self.assertEqual('task-1', _tasks[0].task_name)
