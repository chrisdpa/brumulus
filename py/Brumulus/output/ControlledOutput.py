import traceback
import sys


class ControlledOutput(object):
    """docstring for ControlledOutput"""
    def __init__(self, protected_output, name, on_state=0, control_scale=1):
        super(ControlledOutput, self).__init__()

        self.output = protected_output
        self.name = name
        self.on_state = on_state
        self.control_scale = control_scale

        self.override = 'auto'
        self.off_state = 1
        if on_state == 1:
            self.off_state = 0

        self.info = None

    def get_state_str(self):
        if self.output.get_output() == self.on_state:
            return 'On'
        else:
            return 'Off'

    def get_mode(self):
        return self.override

    def mode_toggle(self):
        if self.override == 'off':
            self.mode_auto()
        else:
            self.mode_off

    def mode_off(self):
        self.override = 'off'

    def mode_auto(self):
        self.override = 'auto'

    def control(self, desired_value):
        self.info = None

        try:
            if (self.override == 'off'):
                self.output.set_output(self.off_state)
                self.info = 'Off Mode'
            elif (control_value * self.control_scale) > 10:
                self.output.set_output(self.on_state)
            else:
                self.output.set_output(self.off_state)
        except ProtectedOutputProtectedError as pe:
            print(str(pe))
            self.chiller_ssr_info = 'Wait minumum cycle time'
        except Exception as e:
            print(e)
            self.err = str(e)
            traceback.print_exc(file=sys.stdout)

        print(self.name, ':', self.get_state_str())

    def get_info(self):
        return self.info

    def get_raw(self):
        return self.output.get_output()
