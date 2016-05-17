#!/usr/bin/env python
import json
import os
from SetPoints import SetPoints

class ControlSetPoint(object):
    """docstring for ControlSetPoint"""
    def __init__(self, setpointfile="/var/data/brumulus/setpoints.json", gui_setpointfile = "/var/data/brumulus/gui_setpoint.json"):
        super(ControlSetPoint, self).__init__()
        self.setpointfile = setpointfile
        self.gui_setpointfile = gui_setpointfile
        self.gui_setpoint = 4
        self.init()

    def get_setpoint(self):
        if self.is_gui_control():
            return self.gui_setpoint
        return self.setpoints.get_now_value()

    def is_gui_control(self):
        return (self.setpointfile is None) or not os.path.isfile(self.setpointfile)

    def init(self):
        if self.is_gui_control():
            self.get_gui_setpoint()
        else:
            self.setpoints = SetPoints(self.setpointfile)

    def get_gui_setpoint(self):
        if not os.path.isfile(self.gui_setpointfile):
            self.save_gui_setpoint()
        meta = json.load(open(self.gui_setpointfile))
        self.gui_setpoint = meta["gui_setpoint"]

    def save_gui_setpoint(self):
        with open(self.gui_setpointfile, 'w') as outfile:
            json.dump({"gui_setpoint":self.gui_setpoint}, outfile)

if __name__ == "__main__":
    sp = ControlSetPoint(gui_setpointfile = "test/gui_setpoint.json")
    print sp.get_setpoint()
    sp = ControlSetPoint(setpointfile = "test/setpoints.json")
    print sp.get_setpoint()
