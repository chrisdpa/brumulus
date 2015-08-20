import datetime
import RPi.GPIO as GPIO
import time


class ProtectedOutput(object):
    """docstring for ProtectedOutput"""
    def __init__(self, min_state_time=600, pin=23, default_state=1):
        super(ProtectedOutput, self).__init__()
        self.min_state_time = datetime.timedelta(seconds=min_state_time)
        self.last_state_time = datetime.datetime.now()
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, default_state)

    def set_output(self, state):
        if GPIO.input(self.pin) != state:
            if self.is_protected():
                raise ProtectedOutputProtectedError(
                    "Cannot change state during Protected Window - seconds remaining: " + str(self.window_time_remaining()))
            GPIO.output(self.pin, state)
            self.last_state_time = datetime.datetime.now()

    def window_time_remaining(self):
        return (datetime.datetime.now() - self.min_state_time - self.last_state_time).total_seconds()

    def is_protected(self):
        window_start = datetime.datetime.now() - self.min_state_time
        return self.last_state_time > window_start

    def get_output(self):
        return GPIO.input(self.pin)


class ProtectedOutputProtectedError(Exception):
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return repr(self.comment)

if __name__ == "__main__":
    out = ProtectedOutput(min_state_time=1)
    state = 0
    while True:
        time.sleep(1)
        out.set_output(state)
        if state == 1:
            state = 0
        else:
            state = 1
