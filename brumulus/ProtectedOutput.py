import datetime


class ProtectedOutput(object):
    """docstring for ProtectedOutput"""
    def __init__(self, output, default_state='OFF', min_state_time=600):
        super(ProtectedOutput, self).__init__()
        self.min_state_time = datetime.timedelta(seconds=min_state_time)
        self.last_state_time = datetime.datetime.now()
        self.output = output
        output.set_state(default_state)

    def set_state(self, state):
        if not self.output.is_state(state):
            if self.is_protected():
                raise ProtectedOutputProtectedError(
                    "Cannot change state during Protected Window - seconds remaining: {}".format(
                        str(self.window_time_remaining())))
            self.output.set_state(state)
            self.last_state_time = datetime.datetime.now()
        return {'success': True, 'value': self.output.get_state()}

    def window_time_remaining(self):
        return (datetime.datetime.now() - self.min_state_time - self.last_state_time).total_seconds()

    def is_protected(self):
        window_start = datetime.datetime.now() - self.min_state_time
        return self.last_state_time > window_start

    def get_state(self):
        return self.output.get_state()


class ProtectedOutputProtectedError(Exception):
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return repr(self.comment)
