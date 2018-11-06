import requests
from queuelib import FifoDiskQueue
import time


class Thingsspeak(object):
    """docstring for Thingsspeak"""
    def __init__(self):
        super(Thingsspeak, self).__init__()
        self.retry_queue = FifoDiskQueue("/var/thingsspeak.queue")

    def send(self, values):
        print('Thingspeak.send: {}'.format(values))
        data = {'created_at': values['created_at'],
                  'key': 'MYA8R6YDMDQNM9M9',
                  'field1': values['target_temp'],
                  'field2': values['current_temp'],
                  'field3': values['control_value'],
                  'field4': values['chiller_raw'],
                  'field5': values['heater_raw'],
                  'field6': values['current_temp_2']
                  }
        print data

        try:
            r = requests.post(
                "https://api.thingspeak.com/update",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data))
            print(r)
        except e:
            print(e)
