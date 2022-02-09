
class TargetVessel:
    def __init__(self, xpos, ypos, course, speed):
        self.xpos = xpos
        self.ypos = ypos
        self.course = course
        self.speed = speed

    def get_state(self):
        return {
            "xpos": self.xpos,
            "ypos": self.ypos,
            "course": self.course,
            "speed": self.speed
        }
