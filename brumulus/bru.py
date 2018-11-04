import requests
import time

control_endpoint = 'http://192.168.0.35:5002/control/?current_temp={}&target_temp={}&delta_temp_c={}&delta_time_ms={}'
heater_endpoint = 'http://192.168.0.35:5003/output/0/{}'
chiller_endpoint = 'http://192.168.0.35:5003/output/1/{}'
temperature_endpoint = 'http://192.168.0.32:5000/temp'
temp = requests.get(temperature_endpoint).content
prev = temp
setpoint = 20.0

while (True):
    temp = requests.get(temperature_endpoint).content
    diff = float(temp) - float(prev)
    control = requests.get(control_endpoint.format(temp, setpoint, diff, 15000)).content
    prev = temp
    if ('Output.off' == control):
        requests.get(heater_endpoint.format('OFF'))
        requests.get(chiller_endpoint.format('OFF'))

    if ('Output.chill' == control):
        requests.get(heater_endpoint.format('OFF'))
        requests.get(chiller_endpoint.format('ON'))

    if ('Output.heat' == control):
        requests.get(chiller_endpoint.format('OFF'))
        requests.get(heater_endpoint.format('ON'))

    time.sleep(15)
