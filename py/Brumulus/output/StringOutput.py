

class StringOutput(object):
    """
    Test string as an output for brumulus.
    """
    def __init__(self):
        self.state = 'OFF'

    def is_state(self, state):
        if self.state == state:
            return True
        return False

    def set_state(self, state):
        if state == 'ON':
            print('ON')
            return 'ON'
        if state == 'OFF':
            print('OFF')
            return 'OFF'

        raise Exception('Cannot set StringOutput state to {}'.format(state))
