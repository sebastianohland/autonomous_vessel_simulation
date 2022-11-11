
class TargetShip:

    def __init__(self, xpos, ypos, cog, sog, length, type=None, status=None, tss=False, nar_ch=False, res_vis=False):
        self.xpos = xpos
        self.ypos = ypos
        self.cog = cog
        self.sog = sog
        self.length = length
        self.type = type
        self.status = status
        self.tss = tss
        self.nar_ch = nar_ch
        self.res_vis = res_vis

    def get_state(self):
        return {
            "xpos": self.xpos,
            "ypos": self.ypos,
            "cog": self.cog,
            "sog": self.sog,
            "length": self.length,
            "type": self.type,
            "status": self.status,
            "tss": self.tss,
            "nar_ch": self.nar_ch,
            "res_vis": self.res_vis
        }
