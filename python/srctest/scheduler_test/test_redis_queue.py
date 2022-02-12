import asyncio

import aioredis
import aiounittest

from scheduler.redis.RedisAsyncQueue import RedisQueue


class TestRedisQueue(aiounittest.AsyncTestCase):
    async def test_redis_implementation(self):
        _connection = aioredis.from_url(f'redis://localhost:27645/0')
        _rq = RedisQueue(redis_connection=_connection, channel='channel-1')
        _name = 'testing'
        _len = await _rq.queue_length(name=_name)
        self.assertEqual(0, _len, f'Queue length for name {_name} expected 0 but got {_len}')
        _nm = await _rq.add(name=_name, message={'message': 'hello'})
        _len = await _rq.queue_length(name=_name)
        self.assertEqual(1, _len, f'Queue length for name {_name} expected 1 but got {_len}')
        _del = await _rq.delete(name=_name)
        self.assertEqual(1, len(_del), f'Expected 1 element but got {len(_del)}')
        await _connection.close()
        await _connection.connection_pool.disconnect()
