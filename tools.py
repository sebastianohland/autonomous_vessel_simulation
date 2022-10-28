import numpy as np


def theta_to_coord(theta, d):
    x = d * np.sin(np.radians(theta))
    y = d * np.cos(np.radians(theta))
    return x, y


def coord_to_theta(x, y):
    theta = (360 + np.degrees(np.arctan2(x, y))) % 360
    d = np.sqrt(x ** 2 + y ** 2)
    return d, theta


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
