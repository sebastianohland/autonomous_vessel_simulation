import json


class State:

    def __init__(self, state=None):
        if state is None:
            state = {}
        self.state = state

    def add_target_vessel(self, target_vessel):

        if 'targetvessels' not in self.state:
            self.state['targetvessels'] = []
            tv_id = "tv" + str(1)
        else:
            tv_id = "tv" + str(len(self.state['targetvessels']) + 1)

        tv = {
            "id": tv_id,
            "xpos": target_vessel.xpos,
            "ypos": target_vessel.ypos,
            "course": target_vessel.course,
            "speed": target_vessel.speed
        }
        self.state['targetvessels'].append(tv)

    def add_own_vessel(self, own_vessel):
        ov = {
            "xpos": own_vessel.xpos,
            "ypos": own_vessel.ypos,
            "course": own_vessel.course,
            "speed": own_vessel.speed
        }
        self.state['ownvessel'] = ov

    def add_static_obstacle(self, obstacle):
        pass

    def get_state(self):
        return self.state

    def write_json(self, path):
        with open(path, "w") as outfile:
            json.dump(self.state, outfile)
