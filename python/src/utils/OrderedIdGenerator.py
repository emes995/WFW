#
#
#

from datetime import datetime


class OrderedIdGenerator:
    @classmethod
    def generate_ordered_id(cls, start_seed: str):
        _ms = datetime.utcnow().microsecond

        return f'{start_seed}{_ms}'
