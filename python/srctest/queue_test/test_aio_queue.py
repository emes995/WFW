import asyncio
import logging

from scheduler.aiobased.AsyncQueue import AsyncQueue
from task.BaseTask import BaseTask
from testutils.WFWAsyncTestCase import WFWAsyncTestCase


class TestRedisAsyncScheduler(WFWAsyncTestCase):
    async def test_aio_queue(self):
        _raq = AsyncQueue()
        self.assertEqual(_raq.length(), 0, f'Expected 0 but got {_raq.length()} instead')
        _result = await _raq.add_task(BaseTask(task_name='testing_add'))
        self.assertEqual(_raq.length(), 1, f'Expected 1 but got {_raq.length()} instead')
        _result = await _raq.get_task()
        self.assertEqual(_result.task_name, 'testing_add', f'Expected name: testing but got {_result.task_name}')
        self.assertEqual(_raq.length(), 0, f'Expected 0 but got {_raq.length()} instead')

    async def test_consumer_producer(self):
        _raq = AsyncQueue(max_size=10)
        _stopProducing = False

        async def _consume():
            while True:
                await asyncio.sleep(2.50)
                _t = await _raq.get_task_wait()
                logging.info(f'Task {_t} popped queue size {_raq.length()}')
                if _stopProducing and (_raq.length() == 0):
                    logging.info('Stopping consumer')
                    break

        async def _produce():
            _task_index = 0
            while True and not _stopProducing:
                await asyncio.sleep(0.15)
                _t = BaseTask(task_name=f'{_task_index}')
                await _raq.add_task(_t)
                logging.info(f'Task {_t} added queue size {_raq.length()}')
                _task_index += 1

        async def _stop():
            nonlocal _stopProducing
            logging.info('Attempting to stop aio queue test in 25 seconds')
            await asyncio.sleep(25)
            _stopProducing = True
            logging.info(f'Stopping producer. Tasks queued: {_raq.length()}')

        _t1 = asyncio.create_task(_produce())
        _t2 = asyncio.create_task(_consume())
        _t3 = asyncio.create_task(_stop())

        await _t1
        await _t2
        await _t3
