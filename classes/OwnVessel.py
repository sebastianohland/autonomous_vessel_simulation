
class OwnVessel:

    # TODO: add width to attributes
    # TODO: add vessel type to attributes
    # TODO: add vessel status to attributes

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

    def set_cog(self, new_cog):
        self.cog = new_cog

    def set_sog(self, new_sog):
        self.sog = new_sog

    def nav_to_wpt(self, wpt_x, wpt_y):
        pass

