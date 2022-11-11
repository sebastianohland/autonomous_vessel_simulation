import json
import matplotlib.pyplot as plt
import numpy as np
from tools import theta_to_coord


class State:

    def __init__(self, state=None):
        if state is None:
            state = {"ownship": [], "targetships": []}
        self.state = state

    def add_target_ship(self, target_vessel):
        tv_state = target_vessel.get_state()
        tv_state["id"] = "ts" + str(len(self.state["targetships"]) + 1)
        self.state["targetships"].append(tv_state)

    def add_own_ship(self, own_vessel):
        ov_state = own_vessel.get_state()
        self.state["ownship"] = ov_state

    def get_state(self):
        return self.state

    def write_state(self, path):
        with open(path, "w") as outfile:
            json.dump(self.state, outfile)

    def add_static_obstacle(self, obstacle):
        pass

    def plot(self, scale, collision_parameters=None, encounter_situations=None):
        """Plots the current state on coordinate system."""
        fig = plt.figure(figsize=(10, 11.7))
        ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])  # axes for coordinate system
        ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.2])  # axes for table
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
        x = self.state["ownship"]["xpos"]
        y = self.state["ownship"]["ypos"]
        xvector, yvector = theta_to_coord(self.state["ownship"]["cog"], self.state["ownship"]["sog"])
        ax.scatter(x, y, color='blue')
        ax.arrow(x, y, xvector, yvector, head_width=0.4, head_length=0.4, lw=1, fc='blue', ec='blue', length_includes_head=True)

        # plot target vessels
        for i in range(len(self.state["targetships"])):
            x = self.state["targetships"][i]["xpos"]
            y = self.state["targetships"][i]["ypos"]
            xvector, yvector = theta_to_coord(self.state["targetships"][i]["cog"], self.state["targetships"][i]["sog"])
            ax.scatter(x, y, color='red')
            ax.arrow(x, y, xvector, yvector, head_width=0.2, head_length=0.4, lw=1, fc='red', ec='red', length_includes_head=True)

            # add encounter situation after id if parameter is given
            if encounter_situations:
                ax.annotate(self.state["targetships"][i]["id"] + str(encounter_situations[i]), (x + 0.5, y))
            else:
                ax.annotate(self.state["targetships"][i]["id"], (x, y))

        # plot collision parameters as table if argument is given
        if collision_parameters:
            columns = ["rng", "dcpa", "tcpa", "bcr", "tbcr", "Q", "Q1", "v_rat"]
            rows = [i["id"] for i in self.state["targetships"]]
            table = ax2.table(cellText=collision_parameters, rowLabels=rows, colLabels=columns, loc="center")
            table.scale(1, 1.7)

        plt.show()

    def next_state(self, timefactor):
        for i in self.state["targetships"]:
            new_x, new_y = theta_to_coord(i["cog"], i["sog"] / timefactor)
            i["xpos"] = new_x + i["xpos"]
            i["ypos"] = new_y + i["ypos"]
        new_x, new_y = theta_to_coord(self.state["ownship"]["cog"], self.state["ownship"]["sog"] / timefactor)
        self.state["ownship"]["xpos"] = new_x + self.state["ownship"]["xpos"]
        self.state["ownship"]["ypos"] = new_y + self.state["ownship"]["ypos"]
        return self


def read_state(path):
    with open(path, "r") as f:
        data = json.load(f)
    return State(data)
