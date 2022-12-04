import aioredis

from scheduler.redis.RedisAsyncQueue import RedisAsyncQueue
from task.BaseTask import BaseTask
from testutils.WFWAsyncTestCase import WFWAsyncTestCase


class TestRedisAsyncScheduler(WFWAsyncTestCase):
    async def test_redis_queue(self):
        _connection = aioredis.from_url(f'redis://localhost:27645/0')
        _raq = RedisAsyncQueue(redis_connection=_connection, queue_name='testing')
        self.assertEqual(await _raq.length(), 0, f'Expected 0 but got {await _raq.length()} instead')
        _result = await _raq.add_task(BaseTask(task_name='testing_add'))
        self.assertEqual(await _raq.length(), 1, f'Expected 1 but got {await _raq.length()} instead')
        _result = await _raq.get_task()
        self.assertEqual(_result.task_name, 'testing_add', f'Expected name: testing but got {_result.task_name}')
        self.assertEqual(await _raq.length(), 0, f'Expected 0 but got {await _raq.length()} instead')

        await _connection.connection_pool.disconnect()
        await _connection.close()
