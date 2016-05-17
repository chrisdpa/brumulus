#!/usr/bin/env python
import json
import os
from datetime import datetime
from datetime import timedelta
from dateutil.parser import *
import re

class SetPoints(object):
    """SetPoints
       Read from a file a list of setpoint for a Controlled variable
       Time Offset (ms), Variable Name, Variable Set Point
    """
    datetime_format = "%Y%m%dT%H%M%S"

    def __init__(self, setpointfile):
        super(SetPoints, self).__init__()
        self.setpointfile = setpointfile
        self.setpointfile_run = setpointfile + ".run"
        self.start()

    def get_data(self):
        return json.load(open(self.setpointfile))

    def get_start_now_delta(self):
        return datetime.now() - self.dt_init

    def string(self):
        data = self.get_data()
        time_delta = self.get_start_now_delta()
        time_delta_culm = timedelta()
        print "Start time:", self.dt_init
        print "Time since start:", time_delta
        for d in sorted(data):
            td = self.parse_time(data[d]['time_period'])
            active = (time_delta_culm < time_delta and time_delta <= td + time_delta_culm)
            print "{}[{}] {}: {} => TI:{} ({} >> {})".format(
                "*" if active else "",
                d,
                data[d]['note'],
                data[d]['time_period'],
                td,
                time_delta_culm,
                time_delta_culm + td)
            time_delta_culm = td + time_delta_culm

    def get_now(self):
        data = self.get_data()
        time_delta = self.get_start_now_delta()
        time_delta_culm = timedelta()
        for d in sorted(data):
            td = self.parse_time(data[d]['time_period'])
            if (time_delta_culm < time_delta and time_delta <= td + time_delta_culm):
                return data[d]
            time_delta_culm = td + time_delta_culm

    def start(self):
        if os.path.isfile(self.setpointfile_run):
            self.meta = json.load(open(self.setpointfile_run))
            self.dt_init = parse(self.meta["start_time"])
        else:
            self.dt_init = datetime.now()
            self.meta = {"start_time":self.dt_init.strftime(self.datetime_format)}
            with open(self.setpointfile_run, 'w') as outfile:
                json.dump(self.meta, outfile)

    def parse_time(self, time_str):
        # 10DT2H30M
        regex = re.compile(r'((?P<days>\d+?)DT?)?((?P<hours>\d+?)H)?((?P<minutes>\d+?)M)?')
        parts = regex.match(time_str.upper())
        if not parts:
            return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.iteritems():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)


if __name__ == "__main__":
    sp = SetPoints("test/setpoints.json")
    # print "Set points:", sp.get_data()
    # print "Meta:", sp.meta["start_time"]
    print sp.string()
    print sp.get_now()
