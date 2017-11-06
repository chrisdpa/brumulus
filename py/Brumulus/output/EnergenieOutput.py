from gpiozero import Energenie


class EnergenieOutput(object):
    """
    Use energenie as an output for brumulus.
    """
    def __init__(self, socket):
        super(EnergenieOutput, self).__init__()
        self.socket = socket
        self.state = 'OFF'
        self.energenie = Energenie(socket)

    def is_state(self, state):
        if self.state == state:
            return True
        return False

    def set_state(self, state):
        if state == 'ON':
            self.energenie.on()
            return 'ON'
        if state == 'OFF':
            self.energenie.off()
            return 'OFF'

        raise Exception('Cannot set EnergenieOutput state to {}'.format(state))
