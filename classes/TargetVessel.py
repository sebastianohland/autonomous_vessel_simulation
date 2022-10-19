
class TargetVessel:
    def __init__(self, xpos, ypos, cog, sog, length):
        self.xpos = xpos
        self.ypos = ypos
        self.cog = cog
        self.sog = sog
        self.length = length

    def get_state(self):
        return {
            "xpos": self.xpos,
            "ypos": self.ypos,
            "cog": self.cog,
            "sog": self.sog,
            "length": self.length
        }
