import matplotlib.pyplot as plt
import numpy as np
import json
from classes.TargetVessel import TargetVessel
from classes.OwnVessel import OwnVessel
from classes.State import State
from tools import theta_to_coord


def calculate_collision_parameters(state):
    """Input: State of the system in form of dictionary.
    Returns: List of collision parameters (tuple containing TCPA, DCPA) for every target vessel."""
    collision_parameters = []

    for i in state["targetvessels"]:
        x = state["ownvessel"]["xpos"]
        y = state["ownvessel"]["ypos"]
        theta = state["ownvessel"]["course"]
        v = state["ownvessel"]["speed"]

        xb = i["xpos"]
        yb = i["ypos"]
        thetab = i["course"]
        vb = i["speed"]

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


def plot_state(state, scale):
    """Plots the current state on coordinate system."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(-scale, scale)
    plt.ylim(-scale, scale)
    plt.grid()

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xticks(np.linspace(-scale, scale, 2 * scale + 1))
    ax.set_yticks(np.linspace(-scale, scale, 2 * scale + 1))

    # plot own vessel
    x = state["ownvessel"]["xpos"]
    y = state["ownvessel"]["ypos"]
    xvector, yvector = theta_to_coord(state["ownvessel"]["course"], state["ownvessel"]["speed"])
    ax.scatter(x, y, color='blue')
    ax.arrow(x, y, xvector, yvector, head_width=0.4, head_length=0.4, lw=1, fc='blue', ec='blue',
             length_includes_head=True)

    # plot target vessels
    for i in state["targetvessels"]:
        x = i["xpos"]
        y = i["ypos"]
        xvector, yvector = theta_to_coord(i["course"], i["speed"])
        ax.scatter(x, y, color='red')
        ax.arrow(x, y, xvector, yvector, head_width=0.2, head_length=0.4, lw=1, fc='red', ec='red',
                 length_includes_head=True)
        ax.annotate(i["id"], (x, y))

    plt.show()


def write_state(state, path):
    with open(path, "w") as outfile:
        json.dump(state, outfile)


examplestate = {
    "ownvessel": {
        "xpos": 0,
        "ypos": 0,
        "course": 90,
        "speed": 5
    },
    "targetvessels": [
        {
            "id": "tv1",
            "xpos": 3.5,
            "ypos": 3.5,
            "course": 180,
            "speed": 4
        },
        {
            "id": "tv2",
            "xpos": 5,
            "ypos": -8,
            "course": 0,
            "speed": 8
        },
    ],
    "staticobstacles": [

    ],
}


ow = OwnVessel(0, 0, 90, 5)
tv1 = TargetVessel(-2, 5.7, 280, 2)
tv2 = TargetVessel(-5, -1, 95, 12)

state = State(examplestate)
state.add_target_vessel(tv1)
state.add_target_vessel(tv2)
state.add_own_vessel(ow)

state_dict = state.get_state()
write_state(state_dict, "state/state.json")
plot_state(state_dict, 10)

collision_parameters = calculate_collision_parameters(state.get_state())
for i in range(len(collision_parameters)):
    print("Target vessel ID: {} TCPA: {:0.2f} DCPA: {:0.2f}".format(state_dict["targetvessels"][i]["id"],
                                                                    collision_parameters[i][0] * 60,
                                                                    collision_parameters[i][0]))


