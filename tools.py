import numpy as np


def course_to_rel_course(target_course, own_course):
    return (360 - own_course + target_course) % 360


def theta_to_coord(theta, d):
    x = round(d * np.sin(np.radians(theta)), 4)
    y = round(d * np.cos(np.radians(theta)), 4)
    return x, y


def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection, from rosettacode.org"""
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        return -1, -1   # TODO: WHAT TO RETURN???
    #if not (0 <= uA <= 1 and 0 <= uB <= 1):
    #    return -1, -1   # TODO: WTF?
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)

    return x, y

def nm_to_m(nm):
    return nm * 1852


def m_to_nm(m):
    return m * (1 / 1852)









"""
OLD FUNCTION DELETE THIS!!!
def calculate_dcpa_tcpa(os_speed, ts_state):

    ts_x_pos, ts_y_pos = theta_to_coord(ts_state[0], ts_state[1])
    rel_x_vel, ts_y_vel = theta_to_coord(ts_state[3], ts_state[2])

    rel_y_vel = ts_y_vel - os_speed     # no change in x vel since TS course is relative to OS course

    tcpa = -(ts_x_pos * rel_x_vel + ts_y_pos * rel_y_vel) / (rel_x_vel ** 2 + rel_y_vel ** 2)   # Minimizing time to cpa
    dcpa = np.sqrt((ts_x_pos + rel_x_vel * tcpa) ** 2 + (ts_y_pos + rel_y_vel * tcpa) ** 2)     # Pythagorean theorem

    return tcpa, dcpa
"""

"""
OLD FUNCTION DELETE THIS!!!
def calculate_collision_parameters(state):
    Input: State of the system in form of dictionary.
    Returns: List of collision parameters (tuple containing TCPA, DCPA) for every target vessel.
    collision_parameters = []

    for i in state["targetvessels"]:
        x = state["ownvessel"]["xpos"]
        y = state["ownvessel"]["ypos"]
        theta = state["ownvessel"]["cog"]
        v = state["ownvessel"]["sog"]

        xb = i["xpos"]
        yb = i["ypos"]
        thetab = i["cog"]
        vb = i["sog"]

        k2 = ((np.cos(np.radians(theta)) ** 2) * (v ** 2)) \
             - (2 * np.cos(np.radians(theta)) * v * np.cos(np.radians(thetab)) * vb) \
             + ((np.cos(np.radians(thetab)) ** 2) * (vb ** 2)) \
             + ((np.sin(np.radians(theta)) ** 2) * (v ** 2)) \
             - (2 * np.sin(np.radians(theta)) * v * np.sin(np.radians(thetab)) * vb) \
             + (np.sin(np.radians(thetab)) * (vb ** 2))

        k1 = (2 * np.cos(np.radians(theta)) * v * y) \
             - (2 * np.cos(np.radians(theta)) * v * yb) \
             - (2 * y * np.cos(np.radians(thetab)) * vb) \
             + (2 * np.cos(np.radians(thetab)) * vb * yb) \
             + (2 * np.sin(np.radians(theta)) * v * x) \
             - (2 * np.sin(np.radians(theta)) * v * xb) \
             - (2 * x * np.sin(np.radians(thetab)) * vb) \
             + (2 * np.sin(np.radians(thetab)) * vb * xb)

        k0 = (y ** 2) - (2 * y * yb) + (yb ** 2) + (x ** 2) - (2 * x * xb) + (xb ** 2)

        tcpa = -k1 / (2 * k2)
        dcpa = np.sqrt(k2 * tcpa ** 2 + k1 * tcpa + k0)

        collision_parameters.append((tcpa, dcpa))

    return collision_parameters
"""