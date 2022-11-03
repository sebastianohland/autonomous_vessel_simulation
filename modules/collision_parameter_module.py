import numpy as np
from tools import theta_to_coord, coord_to_theta
from tools import m_to_nm
from tools import line_intersect


def calculate_collision_parameters(os_pos, os_cog, os_sog, os_len, ts_pos, ts_cog, ts_sog, ts_len):

    collision_parameters = []

    # x and y components of velocity vectors relative to vessel
    os_vel = theta_to_coord(os_cog, os_sog)
    ts_vel = theta_to_coord(ts_cog, ts_sog)

    # relative position and bearing to ts from os perspective
    rel_pos = (ts_pos[0] - os_pos[0], ts_pos[1] - os_pos[1])
    tb = coord_to_theta(rel_pos[0], rel_pos[1])
    Q = (tb - os_cog + 360) % 360   # relative bearing

    # relative position and bearing to os from ts perspective
    rel_pos_1 = (os_pos[0] - ts_pos[0], os_pos[1] - ts_pos[1])
    tb_1 = coord_to_theta(rel_pos_1[0], rel_pos_1[1])
    Q1 = (tb_1 - ts_cog + 360) % 360  # relative bearing

    # calculate range
    rng = np.sqrt(rel_pos[0] ** 2 + rel_pos[1] ** 2)

    # relative velocity
    rel_vel = (ts_vel[0] - os_vel[0], ts_vel[1] - os_vel[1])

    # CPA calculation
    tcpa = -(rel_pos[1] * rel_vel[1] + rel_pos[0] * rel_vel[0]) / (rel_vel[1] ** 2 + rel_vel[0] ** 2)
    dcpa = np.sqrt((rel_pos[1] + rel_vel[1] * tcpa) ** 2 + (rel_pos[0] + rel_vel[0] * tcpa) ** 2)

    # speed ratio (risk increases when speed ratio decreases)
    v_rat = os_sog / ts_sog

    # TODO: check bcr calculations

    # calculate absolute position of velocity vectors
    os_abs_vel = (os_pos[0] + os_vel[0], os_pos[1] + os_vel[1])
    ts_abs_vel = (ts_pos[0] + ts_vel[0], ts_pos[1] + ts_vel[1])

    # calculate bow cross position (intersecting lines)
    ts_bcr_pos = line_intersect(os_pos[0], os_pos[1], os_abs_vel[0], os_abs_vel[1], ts_pos[0], ts_pos[1], ts_abs_vel[0], ts_abs_vel[1])

    # time to BCR
    tbcr = np.sqrt((ts_pos[0] - ts_bcr_pos[0]) ** 2 + (ts_pos[1] - ts_bcr_pos[1]) ** 2) / np.abs(ts_sog)

    # help variables
    os_u_x = os_vel[0] / np.abs(os_sog)
    os_u_y = os_vel[1] / np.abs(os_sog)

    # converts ship length to nm
    os_len = m_to_nm(os_len)
    ts_len = m_to_nm(ts_len)
    # pos of os bow at point of bcr
    os_bcr_xpos = os_pos[0] + (os_len / 2) * os_u_x + os_vel[0] * tbcr
    os_bcr_ypos = os_pos[1] + (os_len / 2) * os_u_y + os_vel[1] * tbcr

    # BCR calculation
    bcr = np.sqrt((ts_bcr_pos[0] - os_bcr_xpos) ** 2 + (ts_bcr_pos[1] - os_bcr_ypos) ** 2)

    # help variables for BCR sign calculation
    ts_u_x = ts_vel[0] / np.abs(ts_sog)
    ts_u_y = ts_vel[1] / np.abs(ts_sog)

    # current pos of ts fore and aft
    ts_fore_xpos = ts_pos[0] + (ts_len / 2) * ts_u_x
    ts_fore_ypos = ts_pos[1] + (ts_len / 2) * ts_u_y
    ts_aft_xpos = ts_pos[0] - (ts_len / 2) * ts_u_x
    ts_aft_ypos = ts_pos[1] - (ts_len / 2) * ts_u_x

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
    collision_parameters.append(dcpa)
    collision_parameters.append(tcpa)
    collision_parameters.append(bcr)
    collision_parameters.append(tbcr)
    collision_parameters.append(Q)
    collision_parameters.append(Q1)
    collision_parameters.append(v_rat)

    return collision_parameters


def calculate_state_collision_parameters(state):

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


def print_collision_parameters(coll_parameters):
    for j in range(len(coll_parameters)):
        print("Range: {:0.2f} || DCPA: {:0.2f} || TCPA: {:0.2f} || BCR: {:0.2f} || TBCR: {:0.2f} || Q: {:0.2f} || Q1: {:0.2f} || v_rat: {:0.2f}"
              .format(coll_parameters[j][0],
                      coll_parameters[j][1],
                      coll_parameters[j][2] * 60,
                      coll_parameters[j][3],
                      coll_parameters[j][4] * 60,
                      coll_parameters[j][5],
                      coll_parameters[j][6],
                      coll_parameters[j][7]
                      )
              )
    print("")


