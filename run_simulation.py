import matplotlib.pyplot as plt
import numpy as np
import json
from classes.TargetVessel import TargetVessel
from classes.State import State
from tools import theta_to_coord
from modules.collision_parameter_module import calculate_state_collision_parameters, print_collision_parameters
from modules.encounter_situation_module import calculate_state_encounter_situations


def plot_state(state, scale, collision_parameters=None, encounter_situations=None):
    """Plots the current state on coordinate system."""
    fig = plt.figure(figsize=(10, 11.7))
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])     # axes for coordinate system
    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.2])    # axes for table
    ax2.axis("off")
    ax2.axis("tight")

    # setting up coordinate system
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.grid()
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
    for i in range(len(state["targetvessels"])):
        x = state["targetvessels"][i]["xpos"]
        y = state["targetvessels"][i]["ypos"]
        xvector, yvector = theta_to_coord(state["targetvessels"][i]["cog"], state["targetvessels"][i]["sog"])
        ax.scatter(x, y, color='red')
        ax.arrow(x, y, xvector, yvector, head_width=0.2, head_length=0.4, lw=1, fc='red', ec='red',
                 length_includes_head=True)
        # add encounter situation text if parameter is given
        if encounter_situations:
            ax.annotate(state["targetvessels"][i]["id"] + str(encounter_situations[i]), (x + 0.5, y))
        else:
            ax.annotate(state["targetvessels"][i]["id"], (x, y))

    # plot collision parameters as table if argument is given
    if collision_parameters:
        data = np.array(collision_parameters)
        # converting tcpa and tcbr to minutes
        for i in data:
            i[3] = i[5] * 60
            i[3] = i[5] * 60
        data = np.round(data, 2)
        columns = ["rng (nm)", "tb (deg)", "dcpa (nm)", "tcpa (min)", "bcr (nm)", "tbcr (min)"]
        rows = [i["id"] for i in state["targetvessels"]]
        table = ax2.table(cellText=data, rowLabels=rows, colLabels=columns, loc="center")
        table.scale(1, 1.7)

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

tv3 = TargetVessel(-5, -1, 95, 12, 150)
tv4 = TargetVessel(-2, 5.7, 280, 2, 250)

state = State(examplestate)
state.add_target_vessel(tv3)
state.add_target_vessel(tv4)


state_dict = state.get_state()
write_state(state_dict, "state/state.json")

timesteps = 5
scale = 10
timefactor = 6

for i in range(timesteps):
    coll_parameters = calculate_state_collision_parameters(state_dict)
    enc_situations = calculate_state_encounter_situations(coll_parameters, state_dict)
    plot_state(state_dict, scale, coll_parameters, enc_situations)
    print("Timestep: " + str(i + 1))
    print_collision_parameters(coll_parameters)
    state_dict = next_state(state_dict, timefactor)
