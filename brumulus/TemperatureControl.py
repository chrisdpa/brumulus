from enum import Enum


Temperature = Enum('Temperature', 'wellover over setpoint under wellunder')
RateOfChange = Enum('RateOfChange', 'risingrapidly rising steady falling fallingrapidly dontcare')
Output = Enum('Output', 'chill off heat')

# TODO read these from a config file
temp_far_limit = 2
temp_near_limit = 0.25
temp_roc_far_limit = 0.5
temp_roc_near_limit = 0.1


temp_memberships = {
    Temperature.wellover: lambda t, sp: t >= sp+temp_far_limit,
    Temperature.over: lambda t, sp: sp+temp_near_limit < t and t < sp+temp_far_limit,
    Temperature.setpoint: lambda t, sp: t >= sp-temp_near_limit and t <= sp+temp_near_limit,
    Temperature.under: lambda t, sp: sp-temp_near_limit > t and t > sp-temp_far_limit,
    Temperature.wellunder: lambda t, sp: t <= sp-temp_far_limit
}

rate_of_change_memberships = {
    RateOfChange.risingrapidly: lambda dte, dt: dte/dt >= temp_roc_far_limit,
    RateOfChange.rising: lambda dte, dt: temp_roc_near_limit < dte/dt and dte/dt < temp_roc_far_limit,
    RateOfChange.steady: lambda dte, dt: -temp_roc_near_limit <= dte/dt and dte/dt <= temp_roc_near_limit,
    RateOfChange.falling: lambda dte, dt: -temp_roc_near_limit > dte/dt and dte/dt > -temp_roc_far_limit,
    RateOfChange.fallingrapidly: lambda dte, dt: dte/dt <= -temp_roc_far_limit
}

rules = {
    (Temperature.wellover,  RateOfChange.risingrapidly):  Output.chill,
    (Temperature.wellover,  RateOfChange.rising):         Output.chill,
    (Temperature.wellover,  RateOfChange.steady):         Output.chill,
    (Temperature.wellover,  RateOfChange.falling):        Output.chill,
    (Temperature.wellover,  RateOfChange.fallingrapidly): Output.chill,

    (Temperature.over,     RateOfChange.risingrapidly):  Output.chill,
    (Temperature.over,     RateOfChange.rising):         Output.chill,
    (Temperature.over,     RateOfChange.steady):         Output.chill,
    (Temperature.over,     RateOfChange.falling):        Output.chill,
    (Temperature.over,     RateOfChange.fallingrapidly): Output.off,

    (Temperature.setpoint,  RateOfChange.risingrapidly):  Output.chill,
    (Temperature.setpoint,  RateOfChange.rising):         Output.off,
    (Temperature.setpoint,  RateOfChange.steady):         Output.off,
    (Temperature.setpoint,  RateOfChange.falling):        Output.off,
    (Temperature.setpoint,  RateOfChange.fallingrapidly): Output.heat,

    (Temperature.under,     RateOfChange.risingrapidly):  Output.off,
    (Temperature.under,     RateOfChange.rising):         Output.heat,
    (Temperature.under,     RateOfChange.steady):         Output.heat,
    (Temperature.under,     RateOfChange.falling):        Output.heat,
    (Temperature.under,     RateOfChange.fallingrapidly): Output.heat,

    (Temperature.wellunder,  RateOfChange.risingrapidly):  Output.heat,
    (Temperature.wellunder,  RateOfChange.rising):         Output.heat,
    (Temperature.wellunder,  RateOfChange.steady):         Output.heat,
    (Temperature.wellunder,  RateOfChange.falling):        Output.heat,
    (Temperature.wellunder,  RateOfChange.fallingrapidly): Output.heat
}


def __get_temperature_membership(current_temp, target_temp):
    for t in temp_memberships.keys():
        if (temp_memberships[t](current_temp, target_temp)):
            return t


def __get_rate_of_change_membership(delta_temp_c, delta_time_ms):
    print(float(delta_temp_c)/(float(delta_time_ms)/60000))
    for r in rate_of_change_memberships.keys():
        if (rate_of_change_memberships[r](float(delta_temp_c), float(delta_time_ms)/60000)):
            return r


def __get_membership(current_temp, target_temp, delta_temp_c, delta_time_ms):
    return (__get_temperature_membership(current_temp, target_temp),
            __get_rate_of_change_membership(delta_temp_c, delta_time_ms))


def get_output(current_temp, target_temp, delta_temp_c, delta_time_ms):
    return rules[__get_membership(current_temp, target_temp, delta_temp_c, delta_time_ms)]
