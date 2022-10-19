import numpy as np
from tools import theta_to_coord
from tools import m_to_nm
from tools import line_intersect


def calculate_collision_parameters(os_pos, os_cog, os_sog, os_length, ts_pos, ts_cog, ts_sog, ts_length):

    collision_parameters = []

    # converts length to nm
    os_length = m_to_nm(os_length)
    ts_length = m_to_nm(ts_length)

    # x and y components of velocity vectors
    os_vel = theta_to_coord(os_cog, os_sog)
    ts_vel = theta_to_coord(ts_cog, ts_sog)

    # relative position and velocity
    rel_pos = (ts_pos[0] - os_pos[0], ts_pos[1] - os_pos[1])
    rel_vel = (ts_vel[0] - os_vel[0], ts_vel[1] - os_vel[1])

    # range calculation
    rng = np.sqrt(rel_pos[0] ** 2 + rel_pos[1] ** 2)

    # CPA calculation
    tcpa = -(rel_pos[1] * rel_vel[1] + rel_pos[0] * rel_vel[0]) / (rel_vel[1] ** 2 + rel_vel[0] ** 2)
    dcpa = np.sqrt((rel_pos[1] + rel_vel[1] * tcpa) ** 2 + (rel_pos[0] + rel_vel[0] * tcpa) ** 2)

    # calculates absolute position of velocity vector endpoints in coordinate system
    os_abs_vel = (os_pos[0] + os_vel[0], os_pos[1] + os_vel[1])
    ts_abs_vel = (ts_pos[0] + ts_vel[0], ts_pos[1] + ts_vel[1])

    # cbr pos calculation (intersecting lines)
    ts_bcr_pos = line_intersect(os_pos[0], os_pos[1], os_abs_vel[0], os_abs_vel[1], ts_pos[0], ts_pos[1], ts_abs_vel[0], ts_abs_vel[1])

    # time to BCR
    tbcr = np.sqrt((ts_pos[0] - ts_bcr_pos[0]) ** 2 + (ts_pos[1] - ts_bcr_pos[1]) ** 2) / np.abs(ts_sog)

    # help variables
    os_u_x = os_vel[0] / np.abs(os_sog)
    os_u_y = os_vel[1] / np.abs(os_sog)

    # pos of os bow at point of bcr
    os_bcr_xpos = os_pos[0] + (os_length / 2) * os_u_x + os_vel[0] * tbcr
    os_bcr_ypos = os_pos[1] + (os_length / 2) * os_u_y + os_vel[1] * tbcr

    # BCR calculation
    bcr = np.sqrt((ts_bcr_pos[0] - os_bcr_xpos) ** 2 + (ts_bcr_pos[1] - os_bcr_ypos) ** 2)

    # help variables for BCR sign calculation
    ts_u_x = ts_vel[0] / np.abs(ts_sog)
    ts_u_y = ts_vel[1] / np.abs(ts_sog)

    # current pos of ts fore and aft
    ts_fore_xpos = ts_pos[0] + (ts_length / 2) * ts_u_x
    ts_fore_ypos = ts_pos[1] + (ts_length / 2) * ts_u_y
    ts_aft_xpos = ts_pos[0] - (ts_length / 2) * ts_u_x
    ts_aft_ypos = ts_pos[1] - (ts_length / 2) * ts_u_x

    # BCR sign calculation. Checks if ts fore or aft is closer to point of BCR
    bcr_distance_fore = np.sqrt((ts_fore_xpos - ts_bcr_pos[0]) ** 2 + (ts_fore_ypos - ts_bcr_pos[1]) ** 2)
    bcr_distance_aft = np.sqrt((ts_aft_xpos - ts_bcr_pos[0]) ** 2 + (ts_aft_ypos - ts_bcr_pos[1]) ** 2)
    bcr_sign = 0
    if bcr_distance_fore <= bcr_distance_aft:
        bcr_sign = 1
    elif bcr_distance_fore > bcr_distance_aft:
        bcr_sign = -1

    # adds sign to bcr
    tbcr = tbcr * bcr_sign

    collision_parameters.append(rng)
    collision_parameters.append(tcpa)
    collision_parameters.append(dcpa)
    collision_parameters.append(bcr)
    collision_parameters.append(tbcr)

    return collision_parameters


def calculate_collision_parameters_for_state(state):

    os_pos = (state["ownvessel"]["xpos"], state["ownvessel"]["ypos"])
    os_cog = state["ownvessel"]["cog"]
    os_sog = state["ownvessel"]["sog"]
    os_length = state["ownvessel"]["length"]

    all_coll_par = []

    for i in state["targetvessels"]:
        ts_pos = (i["xpos"], i["ypos"])
        ts_cog = i["cog"]
        ts_sog = i["sog"]
        ts_length = i["length"]

        col_par = calculate_collision_parameters(os_pos, os_cog, os_sog, os_length, ts_pos, ts_cog, ts_sog, ts_length)

        all_coll_par.append(col_par)

    return all_coll_par

