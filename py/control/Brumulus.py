from ControlTemperature import ControlTemperature
from TemperatureSensor import TemperatureSensor
from ProtectedOutput import *
from ControlledOutput import *
from Thingsspeak import Thingsspeak
from Lager import LagerThread
from twisted.internet import task
from twisted.internet import reactor
import sys
import traceback
import csv
import json
from datetime import datetime
from decimal import *
import signal


class Brumulus(object):
    """docstring for Brumulus"""
    def __init__(self):
        super(Brumulus, self).__init__()

        self.flight_recorder_file = open('brumulus.csv', 'a')
        self.flight_recorder = csv.writer(self.flight_recorder_file)

        #TODO make this configurable
        self.temp = TemperatureSensor(device_id='28-000004f2300b')
        self.control = ControlTemperature()

        self.chiller = ControlledOutput(ProtectedOutput(min_state_time=180, pin=17), name='Chiller')
        self.heater = ControlledOutput(ProtectedOutput(min_state_time=30, pin=23), name='Heater', control_scale=-1)

        self.target_temp = 4
        self.datetime = None
        self.current_temp = None

        self.thingsspeak = Thingsspeak()

        self.control_loop_timer = task.LoopingCall(self.control_loop)
        self.lager_api = LagerThread(self)

    def start(self):
        self.control_loop_timer.start(30)
        self.lager_api.start()
        reactor.run()
    
    def stop(self):
        self.lager_api.stop()
        reactor.callFromThread(reactor.stop)
        sys.exit(0)

    def control_loop(self):
        prev_datetime = self.datetime
        prev_temp = self.current_temp

        self.datetime = datetime.now()
        self.time = str(self.datetime.isoformat(' '))
        self.err = ''
        self.current_temp = self.temp.read_temp_decimal()
        print "current_temp", self.current_temp

        if self.current_temp is None:
            self.err = "current_temp cannot be read"
            print self.err
        else:
            try:
                self.temp_delta = self.get_temp_delta(prev_datetime, prev_temp)
                print "Temp delta ", self.temp_delta
                self.control_value = self.control.get_output(self.current_temp, self.target_temp, self.temp_delta)
                print "control_value", self.control_value
                self.chiller.control(self.control_value)
                self.heater.control(self.control_value)

                # self.recorder()
                self.thingsspeak.send(self.get_all())
            except Exception as e:
                print e
                self.err = str(e)
                print '-' * 60
                traceback.print_exc(file=sys.stdout)
                print '-' * 60

    def get_temp_delta(self, prev_datetime, prev_temp):
        if (prev_datetime is None or prev_temp is None):
            return 0

        time_delta = Decimal((self.datetime - prev_datetime).total_seconds())
        temp_delta = self.current_temp - prev_temp

        return Decimal((temp_delta / time_delta) * 60)

    def recorder(self):
        data = [self.time, self.target_temp, '{0:.3f}'.format(self.current_temp), self.chiller_ssr_raw, self.control_value, self.err]
        print data
        self.flight_recorder.writerow(data)

    actions = {'increment_target_temp', 'decrement_target_temp'}

    def action(self, action):
        if action == 'decrement_target_temp':
            return self.decrement_target_temp()

        if action == 'increment_target_temp':
            return self.increment_target_temp()

        if action == 'get_all':
            return self.get_all()

    def decrement_target_temp(self):
        self.target_temp -= 1
        return self.get_all()

    def increment_target_temp(self):
        self.target_temp += 1
        return self.get_all()

    def get_all(self):
        values = {'created_at': self.time,
                  'target_temp': str(self.target_temp),
                  'current_temp': '{0:.3f}'.format(self.current_temp),
                  'control_value': '{0:.0f}'.format(self.control_value),
                  'chiller': self.chiller.get_state_str(),
                  'chiller_raw': self.chiller.get_raw(),
                  'chiller_info': self.chiller.get_info(),
                  'heater': self.heater.get_state_str(),
                  'heater_info': self.heater.get_info(),
                  'heater_raw': self.heater.get_raw()
                  }
        return values

brumulus = None

def signal_handler(signal, frame):
    print('Caught Ctrl+C!')
    global brumulus
    brumulus.stop()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    global brumulus
    brumulus = Brumulus()
    brumulus.start()

if __name__ == "__main__":
    main()
