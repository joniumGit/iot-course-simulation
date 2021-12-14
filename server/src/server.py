import logging

import redis
from paho.mqtt import client as mqtt

data = {}

log = logging.getLogger('iot-server')
sink = redis.Redis(host='iot-datastack')
provider = mqtt.Client('iot-server')
provider.connect('iot-mosquitto')


@provider.message_callback()
def on_message(_: mqtt.Client, __: str, message: mqtt.MQTTMessage):
    import json
    pl = message.payload
    if pl is not None:
        color, length = pl.decode('ascii').split(',')
        color: str = color.split('(')[1]
        length: float = float(length[:-1].strip())
        if color not in data:
            data[color] = [1, length]
        else:
            data[color][0] = data[color][0] + 1
            data[color][1] = (data[color][1] + length) / 2
    sink.set('iot-data', json.dumps(data))


provider.connect('iot-mosquitto')
provider.subscribe('iot-data')
provider.loop_forever()
