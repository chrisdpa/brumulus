from gpiozero import Energenie
import RPi.GPIO as GPIO


class EnergenieOutput(object):
    """
    Use energenie as an output for brumulus.
    """
    def __init__(self, socket):
        super(EnergenieOutput, self).__init__()
        self.socket = socket
        self.state = 'OFF'
        # set the pins numbering mode
        GPIO.setmode(GPIO.BCM)

        # Select the GPIO pins used for the encoder D0-D3 data inputs
        GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
        # Select GPIO used to select ASK/FSK (default ASK)
        GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
        # Select GPIO used to enable/disable modulator (default disabled)
        GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
        self.energenie = Energenie(socket)

    def is_state(self, state):
        if self.state == state:
            return True
        return False

    def set_state(self, state):
        if state == 'ON':
            self.energenie.on()
            self.state = 'ON'
            return 'ON'
        if state == 'OFF':
            self.energenie.off()
            self.state = 'OFF'
            return 'OFF'

        raise Exception('Cannot set EnergenieOutput state to {}'.format(state))

    def get_state(self):
        return self.state
