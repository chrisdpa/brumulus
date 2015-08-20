import numpy as np
import skfuzzy as fuzz
from decimal import *


class ControlTemperature(object):
    """docstring for ControlTemperature"""
    def __init__(self, lowest=0, highest=40, step=0.5):
        super(ControlTemperature, self).__init__()
        self.lowest = lowest
        self.highest = highest
        self.step = step

        self.temp      = np.arange(lowest, highest, step)
        self.temp_err  = np.arange(-50, 50, 0.1)
        self.temp_roc  = np.arange(-30, 30, 0.1)  # degress c per minute
        self.chill_out = np.arange(-100, 100, 1)
        # self.heat_out  = np.arange(0, 100, 1)

        #Current Temperature
        self.te_too_cold = fuzz.trapmf(self.temp_err, [-40, -30, -1.5, -1])
        self.te_cold     = fuzz.trimf(self.temp_err, [-1.5, -1, -0.5])
        self.te_optimal  = fuzz.trimf(self.temp_err, [-0.5, 0, 0.5])
        self.te_hot      = fuzz.trimf(self.temp_err, [0.5, 1, 1.5])
        self.te_too_hot  = fuzz.trapmf(self.temp_err, [1, 1.5, 30, 40])

        #Temperature Rate of Change (deg C per minute)
        self.tr_cooling_quickly = fuzz.trapmf(self.temp_roc, [-20, -10, -0.5, -0.25])

        # Output - Chiller
        self.co_off    = fuzz.trimf(self.chill_out, [0, 0, 5])
        self.co_low    = fuzz.trimf(self.chill_out, [5, 20, 40])
        self.co_medium = fuzz.trimf(self.chill_out, [20, 40, 60])
        self.co_high   = fuzz.trapmf(self.chill_out, [40, 60, 100, 100])

        # Output - Heater
        self.ho_off    = fuzz.trimf(self.chill_out, [-5, 0, 0])
        self.ho_low    = fuzz.trimf(self.chill_out, [-40, -20, -5])
        self.ho_medium = fuzz.trimf(self.chill_out, [-60, -40, -20])
        self.ho_high   = fuzz.trapmf(self.chill_out, [-100, -100, -60, -40])

    def temp_error_category(self, current, target_temp, rate_of_change_per_minute):
        te_current = float(current - target_temp)
        te_too_cold_cat = fuzz.interp_membership(self.temp_err, self.te_too_cold, te_current)
        te_cold_cat     = fuzz.interp_membership(self.temp_err, self.te_cold, te_current)
        te_optimal_cat  = fuzz.interp_membership(self.temp_err, self.te_optimal, te_current)
        te_hot_cat      = fuzz.interp_membership(self.temp_err, self.te_hot, te_current)
        te_too_hot_cat  = fuzz.interp_membership(self.temp_err, self.te_too_hot, te_current)

        tr_cooling_quickly = fuzz.interp_membership(self.temp_roc, self.tr_cooling_quickly, float(rate_of_change_per_minute))

        return dict(too_cold=te_too_cold_cat,
                    cold=te_cold_cat,
                    optimal=te_optimal_cat,
                    hot=te_hot_cat,
                    too_hot=te_too_hot_cat,
                    cooling_quickly=tr_cooling_quickly)

    def get_output(self, current_temp, target_temp, rate_of_change_per_minute):
        temp_err_in = self.temp_error_category(current_temp, target_temp, rate_of_change_per_minute)
        print "Temp Error", temp_err_in

        #What is the temperature doing?
        mf_temp_too_cold = temp_err_in['too_cold']
        mf_temp_cold     = temp_err_in['cold']
        mf_temp_optimal  = temp_err_in['optimal']
        mf_temp_hot      = temp_err_in['hot']
        mf_temp_too_hot  = temp_err_in['too_hot']

        mf_cooling_quickly = temp_err_in['cooling_quickly']

        #Then:
        when_too_cold = np.fmin(mf_temp_too_cold, self.ho_high)
        when_cold     = np.fmin(mf_temp_cold, self.ho_low)
        when_optimal  = np.fmin(mf_temp_optimal, self.co_off)
        when_hot      = np.fmin(mf_temp_hot, self.co_low)
        when_too_hot  = np.fmin(mf_temp_too_hot, self.co_high)

        #If the temperate is temp_hot AND cooling_quickly SET chiller off
        when_hot_and_cooling_quickly = np.fmin(np.fmin(mf_temp_hot, mf_cooling_quickly), self.co_off)

        aggregate_membership = np.fmax(when_hot_and_cooling_quickly, np.fmax(when_too_cold, np.fmax(when_cold, np.fmax(when_optimal, np.fmax(when_hot, when_too_hot)))))
        result = fuzz.defuzz(self.chill_out, aggregate_membership, 'centroid')

        return result
