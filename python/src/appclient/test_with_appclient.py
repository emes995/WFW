#
#
#

import aiohttp
import asyncio
import logging
import logging.config
import os


async def fetch(client):
    _f = os.path.join(os.path.dirname(__file__), '..', '..', 'srctest', 'task', 'json', 'simpletask.json')
    with open(_f, 'r') as _if:
        _j_str = _if.read()
    _params = {'tasks': _j_str}
    async with client.get('http://localhost:8080/tasks', params=_params) as resp:
        assert resp.status == 200, f'Respoinse acquired is {resp.status}'
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)

if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
