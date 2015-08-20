import os
import glob
import time
import re
from decimal import *

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class TemperatureSensor():
    base_dir = '/sys/bus/w1/devices/'
    file = '/w1_slave'

    def __init__(self, device_id=None):
        if not device_id:
            os.chdir(self.base_dir)
            device_id = glob.glob('28*')[0]
        self.device_id = device_id

    def get_device_file(self):
        return self.base_dir + self.device_id + self.file

    def read_temp_raw(self):
        f = open(self.get_device_file(), 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp_decimal(self):
        lines = self.read_temp_raw()
        if re.search(r"crc=.. YES", lines[0]):
            temp_raw_re = re.search("t=(-?\d+)", lines[1])
            temp_string = temp_raw_re.group(1)
            return Decimal(temp_string) / Decimal('1000')

    def read_temp_string(self):
        return '{0:.3f}'.format(self.read_temp_decimal())

if __name__ == "__main__":
    ts = TemperatureSensor()

    print ts.get_device_file()
    print ts.read_temp_raw()
    print ts.read_temp_decimal()
    print ts.read_temp_string()
