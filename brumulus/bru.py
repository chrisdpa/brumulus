import requests
import time

control_endpoint = 'http://192.168.0.35:5002/control/?current_temp={}&target_temp={}&delta_temp_c={}&delta_time_ms={}'
heater_endpoint = 'http://192.168.0.35/output/0/{}'
temperature_endpoing = 'http://192.168.0.32:5000/temp'
temp = requests.get('http://192.168.0.32:5000/temp').content
prev = temp
setpoint = 20.0

while (True):
    temp = requests.get(temperature_endpoing).content
    diff = float(temp) - float(prev)
    control = requests.get(control_endpoint.format(temp, setpoint, diff, 15000)).content
    prev = temp
    if ('Output.off' == control):
        requests.get(heater_endpoint.format('OFF'))

    if ('Output.chill' == control):
        requests.get(heater_endpoint.format('OFF'))

    if ('Output.heat' == control):
        requests.get(heater_endpoint.format('ON'))
    
    time.sleep(15)
