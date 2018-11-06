from ControlTemperature import ControlTemperature
from TemperatureSensor import TemperatureSensor
from ProtectedOutput import *
from ControlledOutput import *
from Thingsspeak import Thingsspeak
from Lager import LagerThread
from ControlSetPoint import ControlSetPoint
from collections import deque
import sys
import traceback
import csv
import json
from datetime import datetime
from decimal import *
import signal
import time
from daemon import *


class Brumulus(object):
    """docstring for Brumulus"""
    def __init__(self):
        super(Brumulus, self).__init__()

        # TODO make this configurable
        self.temp = TemperatureSensor(device_id='28-000004f2300b')
        self.temp_2 = TemperatureSensor(device_id='28-000004f17ab8')
        self.control = ControlTemperature()
        self.setpoint = ControlSetPoint()

        self.chiller = ControlledOutput(
            ProtectedOutput(EnergenieOutput(1), min_state_time=180),
            name='Chiller')

        self.heater = ControlledOutput(
            ProtectedOutput(EnergenieOutput(2), min_state_time=30),
            name='Heater',
            control_scale=-1)

        self.target_temp = self.setpoint.get_setpoint()
        self.datetime = None
        self.current_temp = None

        # self.thingsspeak = Thingsspeak()

        # self.control_loop_timer = task.LoopingCall(self.control_loop)
        # self.lager_api = LagerThread(self)

        # self.history = deque()
        # self.history_max = 20

    # def start(self):
    #     self.control_loop_timer.start(30)
    #     self.lager_api.start()
    #     reactor.run()
    #
    # def stop(self):
    #     try:
    #         reactor.callFromThread(reactor.stop)
    #     except:
    #         pass
    #
    #     try:
    #         self.lager_api.stop()
    #     except:
    #         pass

    def control_loop(self):
        prev_datetime = self.datetime
        prev_temp = self.current_temp

        self.target_temp = self.setpoint.get_setpoint()
        self.datetime = datetime.now()
        self.time = str(self.datetime.isoformat(' '))
        self.err = ''
        self.current_temp = self.temp.read_temp_decimal()
        self.current_temp_2 = self.temp_2.read_temp_decimal()
        print "current_temp: {} setpoint: {}".format(self.current_temp, self.target_temp)

        # if self.current_temp is None:
        #     self.err = "current_temp cannot be read"
        #     print self.err
        # else:
        #     try:
        #         self.temp_delta = self.get_temp_delta(prev_datetime, prev_temp)
        #         print "Temp delta ", self.temp_delta
        #         self.control_value = self.control.get_output(self.current_temp, self.target_temp, self.temp_delta)
        #         print "control_value", self.control_value
        #         self.chiller.control(self.control_value)
        #         self.heater.control(self.control_value)
        #
        #         # self.recorder()
        #         # values = self.get_all()
        #         # self.history.append(values)
        #         # if len(self.history) > self.history_max:
        #         #     self.history.popleft()
        #         # self.thingsspeak.send(values)
        #     except Exception as e:
        #         print e
        #         self.err = str(e)
        #         print '-' * 60
        #         traceback.print_exc(file=sys.stdout)
        #         print '-' * 60

    def get_temp_delta(self, prev_datetime, prev_temp):
        if (prev_datetime is None or prev_temp is None):
            return 0

        time_delta = Decimal((self.datetime - prev_datetime).total_seconds())
        temp_delta = self.current_temp - prev_temp

        return Decimal((temp_delta / time_delta) * 60)

    # def recorder(self):
    #     data = [self.time, self.target_temp, '{0:.3f}'.format(self.current_temp), self.chiller_ssr_raw, self.control_value, self.err]
    #     print data
    #     self.flight_recorder.writerow(data)

    actions = {'increment_target_temp', 'decrement_target_temp'}

    def action(self, action):
        if action == 'decrement_target_temp':
            return self.decrement_target_temp()

        if action == 'increment_target_temp':
            return self.increment_target_temp()

        if action == 'get_all':
            return self.get_all()

        if action == 'toggle_chiller_mode':
            self.chiller.mode_toggle()

        if action == 'toggle_heater_mode':
            self.heater.mode_toggle()

        if action == 'get_history':
            return self.get_history()

    def decrement_target_temp(self):
        self.setpoint.set_gui_setpoint(self.target_temp - 1)
        self.target_temp = self.setpoint.get_setpoint()
        return self.get_all()

    def increment_target_temp(self):
        self.setpoint.set_gui_setpoint(self.target_temp + 1)
        self.target_temp = self.setpoint.get_setpoint()
        return self.get_all()

    def get_history(self, count=60):
        print "current hist: {}".format(self.history)
        return list(self.history)[-1 * count:]

    def get_all(self):
        values = {'created_at': self.time,
                  'target_temp': str(self.target_temp),
                  'target_temp_mode': self.setpoint.get_mode(),
                  'current_temp': '{0:.3f}'.format(self.current_temp),
                  'current_temp_2': '{0:.3f}'.format(self.current_temp_2),
                  'temp_delta': '{0:.3f}'.format(self.temp_delta),
                  'control_value': '{0:.0f}'.format(self.control_value),
                  'chiller': self.chiller.get_state_str(),
                  'chiller_raw': self.chiller.get_raw(),
                  'chiller_info': self.chiller.get_info(),
                  'chiller_mode': self.chiller.get_mode(),
                  'heater': self.heater.get_state_str(),
                  'heater_info': self.heater.get_info(),
                  'heater_raw': self.heater.get_raw(),
                  'heater_mode': self.heater.get_mode(),
                  }
        return values


# brumulus = None


# def signal_handler(signal, frame):
    # print('Caught Ctrl+C!')
    # global brumulus
    # brumulus.stop()


def main():
    # signal.signal(signal.SIGINT, signal_handler)
    # global brumulus

    # logger = logging.getLogger('brumulus')
    # logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # fh = logging.FileHandler('/var/log/brumulus.log')
    # fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    # add the handlers to the logger
    # logger.addHandler(fh)
    # logger.addHandler(ch)

    brumulus = Brumulus()
    while True:
        brumulus.control_loop()
        time.sleep(30)

if __name__ == "__main__":
    main()
