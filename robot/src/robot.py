from dataclasses import dataclass
from random import Random

import redis

rand = Random(0)

COLORS = [
    'RED',
    'GREEN',
    'BLUE',
    'CYAN',
    'YELLOW',
    'BLACK',
    'WHITE'
]
DEFAULT_LENGTH = 10
SMALLEST_SLEEP = 0.4


@dataclass
class Item:
    color: str
    length: float

    def __repr__(self):
        return f"Item({self.color}, {self.length})"


def generate_item() -> Item:
    import time
    time.sleep(rand.random() + SMALLEST_SLEEP)
    mod = rand.random()
    return Item(
        rand.choice(COLORS),
        DEFAULT_LENGTH if mod < 0.8 else DEFAULT_LENGTH * mod,
    )


def send_item(item: Item, r: redis.Redis):
    import time
    time.sleep(rand.random())
    r.rpush('iot-data', repr(item))


sink = redis.Redis(host='iot-datastack')
try:
    while True:
        o = generate_item()
        send_item(o, sink)
finally:
    sink.close()
