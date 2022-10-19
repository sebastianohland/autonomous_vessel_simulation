import json


class State:

    def __init__(self, state=None):
        if state is None:
            state = {}
        self.state = state

    def add_target_vessel(self, target_vessel):
        tv_state = target_vessel.get_state()
        if 'targetvessels' not in self.state:
            self.state['targetvessels'] = []
            tv_id = "tv" + str(1)
        else:
            tv_id = "tv" + str(len(self.state['targetvessels']) + 1)
        tv_state["id"] = tv_id
        self.state['targetvessels'].append(tv_state)

    def add_own_vessel(self, own_vessel):
        pass

    def add_static_obstacle(self, obstacle):
        pass

    def get_state(self):
        return self.state

    def write_json(self, path):
        with open(path, "w") as outfile:
            json.dump(self.state, outfile)
