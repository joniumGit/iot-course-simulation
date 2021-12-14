from dataclasses import dataclass
from random import Random

from paho.mqtt import client as mqtt

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
    mod = rand.random() * (1.4 - 0.8) + 0.8
    return Item(
        rand.choice(COLORS),
        DEFAULT_LENGTH * mod,
    )


def send_item(item: Item, c: mqtt.Client):
    import time
    time.sleep(rand.random())
    c.publish('iot-data', repr(item))


sink = mqtt.Client("iot-robot")
sink.connect('iot-mosquitto')
sink.loop_start()
while True:
    o = generate_item()
    send_item(o, sink)
