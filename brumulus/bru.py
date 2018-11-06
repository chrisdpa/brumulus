import requests
import time
from datetime import datetime

control_endpoint = 'http://192.168.0.35:5002/control/?current_temp={}&target_temp={}&delta_temp_c={}&delta_time_ms={}'
heater_endpoint = 'http://192.168.0.35:5003/output/0/{}'
chiller_endpoint = 'http://192.168.0.35:5003/output/1/{}'
temperature_endpoint = 'http://192.168.0.32:5000/temp'
logging_endpoint = 'http://192.168.0.35:5004/log'

temp = requests.get(temperature_endpoint).content
prev = temp
setpoint = 20.0

while (True):
    data  = dict()
    data['created_at'] = datetime.now().isoformat(' ')
    data['target_temp'] = setpoint
    data['current_temp'] = requests.get(temperature_endpoint).content

    diff = float(data['current_temp']) - float(prev)
    data['control'] = str(requests.get(control_endpoint.format(data['current_temp'], setpoint, diff, 15000)).content)
    prev = data['current_temp']
    if (data['control'] == 'Output.off'):
        requests.get(heater_endpoint.format('OFF'))
        requests.get(chiller_endpoint.format('OFF'))
        data['control_value'] = 0

    if (data['control'] == 'Output.chill' ):
        requests.get(heater_endpoint.format('OFF'))
        requests.get(chiller_endpoint.format('ON'))
        data['control_value'] = -1

    if (data['control'] == 'Output.heat'):
        requests.get(chiller_endpoint.format('OFF'))
        requests.get(heater_endpoint.format('ON'))
        data['control_value'] = 1

    data['heater_raw'] = 1
    if (str(requests.get(heater_endpoint.format(''))) == 'OFF'):
        data['heater_raw'] = 0

    data['chiller_raw'] = 1
    if (str(requests.get(chiller_endpoint.format(''))) == 'OFF'):
        data['chiller_raw'] = 0

    print("*** data: {}".format(data))

    try:
        requests.post(logging_endpoint, data=data)
    except e:
        print(e)

    time.sleep(15)
