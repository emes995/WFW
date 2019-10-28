import unittest
import uuid

from utils.OrderedIdGenerator import OrderedIdGenerator

class TestIdGenerator(unittest.TestCase):

    def test_sequenced_id_generator(self):
        start_sequence = f'{uuid.uuid4()}'
        _seq_1 = OrderedIdGenerator.generate_ordered_id(start_sequence)
        _seq_2 = OrderedIdGenerator.generate_ordered_id(start_sequence)

        assert _seq_1 < _seq_2
        assert _seq_1 != _seq_2
        assert _seq_2 > _seq_1
