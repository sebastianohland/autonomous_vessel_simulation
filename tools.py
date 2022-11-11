import numpy as np


def theta_to_coord(theta, d):
    x = np.round(d * np.sin(np.radians(theta)), 5)
    y = np.round(d * np.cos(np.radians(theta)), 5)
    return x, y


def coord_to_theta(x, y):
    theta = np.round((360 + np.degrees(np.arctan2(x, y))) % 360, 5)
    return theta


def line_intersect(A1, A2, B1, B2):
    """Returns intersection coordinates of lines A and B or None if there is no intersection.
    Source from: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines"""

    xdiff = (A1[0] - A2[0], B1[0] - B2[0])
    ydiff = (A1[1] - A2[1], B1[1] - B2[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(A1, A2), det(B1, B2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def nm_to_m(nm):
    return nm * 1852


def m_to_nm(m):
    return m * (1 / 1852)
