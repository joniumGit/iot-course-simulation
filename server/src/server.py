import logging

import redis

log = logging.getLogger('iot-server')
sink = redis.Redis(host='iot-datastack')

print("abc")
try:
    while True:
        import time, sys

        time.sleep(0.2)
        log.info(sink.lpop('iot-data'))
except Exception as e:
    print(e)
finally:
    sink.close()
