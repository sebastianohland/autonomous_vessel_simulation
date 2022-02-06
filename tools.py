import numpy as np


def theta_to_coord(theta, d):
    x = d * np.sin(np.radians(theta))
    y = d * np.cos(np.radians(theta))
    return x, y


def calculate_dcpa_tcpa(os_speed, ts_state):
    """Input: Own ship (OS) speed over ground, target ship (TS) state vector: [relative bearing (clockwise from OS
    heading line), distance from OS, course relative to OS, TS speed (over ground)]
    Returns: Distance to Closest Point of Approach (DCPA) and Time to Closest Point of Approach (TCPA)"""

    ts_x_pos, ts_y_pos = theta_to_coord(ts_state[0], ts_state[1])
    rel_x_vel, ts_y_vel = theta_to_coord(ts_state[3], ts_state[2])

    rel_y_vel = ts_y_vel - os_speed     # no change in x vel since TS course is relative to OS course

    tcpa = -(ts_x_pos * rel_x_vel + ts_y_pos * rel_y_vel) / (rel_x_vel ** 2 + rel_y_vel ** 2)   # Minimizing time to cpa
    dcpa = np.sqrt((ts_x_pos + rel_x_vel * tcpa) ** 2 + (ts_y_pos + rel_y_vel * tcpa) ** 2)     # Pythagorean theorem

    return tcpa, dcpa

"""
def next_timestep(os_speed, ts_state, timedelta):

    ts_x_pos, ts_y_pos = theta_to_coord(ts_state[0], ts_state[1])
    rel_x_vel, ts_y_vel = theta_to_coord(ts_state[3], ts_state[2])
    rel_y_vel = ts_y_vel - os_speed

    ts_state[1] = np.sqrt((ts_x_pos + rel_x_vel) ** 2 + (ts_y_pos + rel_y_vel) ** 2)
    ts_state[0] = np.degrees(np.arccos(ts_x_pos + rel_x_vel / ts_state[1]))

    return ts_state
"""