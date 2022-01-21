import unittest
import logging
import logging.config
import os


class TestLogging(unittest.TestCase):

    def test_logging(self):
        logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'config', 'logging.conf'))
        logging.getLogger('hello').info('Testing logging information')
