import unittest
from logging import config
import os

from aiounittest import AsyncTestCase


class WFWTestCase(unittest.TestCase):
    def setUp(self) -> None:
        config.fileConfig(fname=os.path.join(os.path.dirname(__file__),
                                             '..', '..', 'src', 'config', 'logging.conf'))


class WFWAsyncTestCase(AsyncTestCase):
    pass
