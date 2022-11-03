import json
import matplotlib.pyplot as plt
import numpy as np
from tools import theta_to_coord


class State:

    # TODO: add state attributes (ex TSS, restricted vis, narrow channel, etc.) (DO THIS FOR EACH INDIVIDUAL VESSEL!)
    # TODO: read in existing state

    def __init__(self, state=None):
        if state is None:
            state = {}
        self.state = state
        self.state["ownvessel"] = []
        self.state["targetvessels"] = []

    def add_target_vessel(self, target_vessel):
        tv_state = target_vessel.get_state()
        tv_state["id"] = "tv" + str(len(self.state["targetvessels"]) + 1)
        self.state["targetvessels"].append(tv_state)

    def add_own_vessel(self, own_vessel):
        ov_state = own_vessel.get_state()
        self.state["ownvessel"] = ov_state

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
        x = self.state["ownvessel"]["xpos"]
        y = self.state["ownvessel"]["ypos"]
        xvector, yvector = theta_to_coord(self.state["ownvessel"]["cog"], self.state["ownvessel"]["sog"])
        ax.scatter(x, y, color='blue')
        ax.arrow(x, y, xvector, yvector, head_width=0.4, head_length=0.4, lw=1, fc='blue', ec='blue', length_includes_head=True)

        # plot target vessels
        for i in range(len(self.state["targetvessels"])):
            x = self.state["targetvessels"][i]["xpos"]
            y = self.state["targetvessels"][i]["ypos"]
            xvector, yvector = theta_to_coord(self.state["targetvessels"][i]["cog"], self.state["targetvessels"][i]["sog"])
            ax.scatter(x, y, color='red')
            ax.arrow(x, y, xvector, yvector, head_width=0.2, head_length=0.4, lw=1, fc='red', ec='red', length_includes_head=True)
            # add encounter situation after id if parameter is given
            if encounter_situations:
                ax.annotate(self.state["targetvessels"][i]["id"] + str(encounter_situations[i]), (x + 0.5, y))
            else:
                ax.annotate(self.state["targetvessels"][i]["id"], (x, y))

        # plot collision parameters as table if argument is given
        if collision_parameters:
            data = np.array(collision_parameters)
            # converting tcpa and tcbr to minutes
            for i in data:
                i[2] = i[2] * 60
                i[4] = i[4] * 60
            data = np.round(data, 2)
            columns = ["rng (nm)", "dcpa", "tcpa", "bcr", "tbcr", "Q", "Q1", "v_rat"]
            rows = [i["id"] for i in self.state["targetvessels"]]
            table = ax2.table(cellText=data, rowLabels=rows, colLabels=columns, loc="center")
            table.scale(1, 1.7)

        plt.show()

    def next_state(self, timefactor):
        for i in self.state["targetvessels"]:
            new_x, new_y = theta_to_coord(i["cog"], i["sog"] / timefactor)
            i["xpos"] = new_x + i["xpos"]
            i["ypos"] = new_y + i["ypos"]
        new_x, new_y = theta_to_coord(self.state["ownvessel"]["cog"], self.state["ownvessel"]["sog"] / timefactor)
        self.state["ownvessel"]["xpos"] = new_x + self.state["ownvessel"]["xpos"]
        self.state["ownvessel"]["ypos"] = new_y + self.state["ownvessel"]["ypos"]
        return self
