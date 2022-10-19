import matplotlib.pyplot as plt
import numpy as np
import json
from classes.TargetVessel import TargetVessel
from classes.OwnVessel import OwnVessel
from classes.State import State
from tools import theta_to_coord
from modules.collision_parameter_module import calculate_collision_parameters_for_state


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
    xvector, yvector = theta_to_coord(state["ownvessel"]["cog"], state["ownvessel"]["sog"])
    ax.scatter(x, y, color='blue')
    ax.arrow(x, y, xvector, yvector, head_width=0.4, head_length=0.4, lw=1, fc='blue', ec='blue',
             length_includes_head=True)

    # plot target vessels
    for i in state["targetvessels"]:
        x = i["xpos"]
        y = i["ypos"]
        xvector, yvector = theta_to_coord(i["cog"], i["sog"])
        ax.scatter(x, y, color='red')
        ax.arrow(x, y, xvector, yvector, head_width=0.2, head_length=0.4, lw=1, fc='red', ec='red',
                 length_includes_head=True)
        ax.annotate(i["id"], (x, y))

    plt.show()


def next_state(state, timefactor):
    for i in state["targetvessels"]:
        new_x, new_y = theta_to_coord(i["cog"], i["sog"] / timefactor)
        i["xpos"] = new_x + i["xpos"]
        i["ypos"] = new_y + i["ypos"]
    new_x, new_y = theta_to_coord(state["ownvessel"]["cog"], state["ownvessel"]["sog"] / timefactor)
    state["ownvessel"]["xpos"] = new_x + state["ownvessel"]["xpos"]
    state["ownvessel"]["ypos"] = new_y + state["ownvessel"]["ypos"]
    return state


def write_state(state, path):
    with open(path, "w") as outfile:
        json.dump(state, outfile)


examplestate = {
    "ownvessel": {
        "xpos": 0,
        "ypos": 0,
        "cog": 90,
        "sog": 5,
        "length": 100
    },
    "targetvessels": [
        {
            "id": "tv1",
            "xpos": 3.5,
            "ypos": 3.5,
            "cog": 180,
            "sog": 4,
            "length": 60
        },
        {
            "id": "tv2",
            "xpos": 5,
            "ypos": -8,
            "cog": 10,
            "sog": 8,
            "length": 120
        },
    ],
    "staticobstacles": [

    ],
}

tv3 = TargetVessel(-2, 5.7, 280, 2, 250)
tv4 = TargetVessel(-5, -1, 95, 12, 150)

state = State(examplestate)
state.add_target_vessel(tv3)
state.add_target_vessel(tv4)


state_dict = state.get_state()
write_state(state_dict, "state/state.json")

epochs = 10
scale = 10
timefactor = 6

for i in range(epochs):
    plot_state(state_dict, scale)
    collision_parameters = calculate_collision_parameters_for_state(state_dict)
    print("Epoch: " + str(i + 1))
    for j in range(len(collision_parameters)):
        print("ID: {} || Range: {:0.2f} || TCPA: {:0.2f} || DCPA: {:0.2f} || BCR: {:0.2f} || TBCR: {:0.2f}".format(
            state_dict["targetvessels"][j]["id"],
            collision_parameters[j][0],
            collision_parameters[j][1] * 60,
            collision_parameters[j][2],
            collision_parameters[j][3],
            collision_parameters[j][4] * 60
        ))
    print("")
    state_dict = next_state(state_dict, timefactor)
