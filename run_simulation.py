import matplotlib.pyplot as plt
import numpy as np
import json
from classes.TargetVessel import TargetVessel
from classes.OwnVessel import OwnVessel
from classes.State import State
from tools import theta_to_coord


def plot_state(state, scale):

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

    plt.show()


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

print(state.get_state())
state.write_json("state/state.json")

plot_state(state.get_state(), 10)
