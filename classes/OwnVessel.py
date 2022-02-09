
class OwnVessel:

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

    def set_course(self, new_course):
        self.course = new_course

    def set_speed(self, new_speed):
        self.speed = new_speed

    def nav_to_wpt(self, wpt_x, wpt_y):
        pass

