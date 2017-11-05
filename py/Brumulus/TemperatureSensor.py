import os
import glob
# import time
import re
from decimal import Decimal

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class TemperatureSensor():
    '''
    Ensure you enable 1 wire temperature sensors in the kernel, eg in
    /boot/config.txt:
      dtoverlay=w1-gpio,gpiopin=21
    '''
    base_dir = '/sys/bus/w1/devices/'
    file = '/w1_slave'
    device_ids = []

    def __init__(self):
        os.chdir(self.base_dir)
        index = 0
        for d in glob.glob('28*'):
            self.device_ids.append(d)
            print("Found: [{}]{}".format(index, d))
            index = index + 1
        if len(self.device_ids) == 0:
            raise Exception("No devices found")

    def get_device_file(self, index=0):
        return self.base_dir + self.device_ids[index] + self.file

    def read_temp_raw(self, index=0):
        f = open(self.get_device_file(index), 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp_decimal(self, index=0):
        lines = self.read_temp_raw(index)
        if re.search(r"crc=.. YES", lines[0]):
            temp_raw_re = re.search("t=(-?\d+)", lines[1])
            temp_string = temp_raw_re.group(1)
            return Decimal(temp_string) / Decimal('1000')

    def read_temp_string(self, index=0):
        return '{0:.3f}'.format(self.read_temp_decimal(index))

    def sensor_count(self):
        return len(self.device_ids)


if __name__ == "__main__":
    print("Basic sensor tests")
    ts = TemperatureSensor()
    print("Count {}".format(ts.sensor_count()))
    for i in range(0, ts.sensor_count()):
        print(ts.get_device_file(i))
        print(ts.read_temp_raw(i))
        print(ts.read_temp_decimal(i))
        print(ts.read_temp_string(i))
