from tools import calculate_dcpa_tcpa


class TargetVessel:
    def __init__(self, xpos, ypos, course, speed):
        self.xpos = xpos
        self.ypos = ypos
        self.course = course
        self.speed = speed

    def get_state(self):
        return [self.xpos, self.ypos, self.course, self.speed]

    def calc_collision_parameters(self, os_speed):
        pass

