from enum import Enum, unique
from models.player import Player

@unique
class Wicket_Type(str, Enum):
    BOWLED = "bwld"
    CAUGHT = "ct"
    LBW = "lbw"
    RUN_OUT = "r.o"
    STUMPED = "st"
    HIT_WICKET = "hw_wckt"
    HIT_TWICE = "ht_twc"
    OBSTRUCTING = "obstr"

class Wicket:
    def __init__(self, type = Wicket_Type.BOWLED, batter=None, bowler=None, fielder=None, assist=None):
        self.type = type
        self.batter = batter
        self.bowler = bowler
        self.fielder = fielder
        self.assist = assist

    def to_dict(self):
        return {
        "type" : self.type,
        "batter" : self.batter.to_dict(),
        "bowler" : self.bowler.to_dict(),
        "fielder" : self.fielder,
        "assist" : self.assist           
        }
    
    @classmethod
    def from_dict(cls, data):
        batter = Player.from_dict(data["batter"])
        bowler = Player.from_dict(data["bowler"])
        return(cls(data["type"], batter, bowler, data["fielder"], data["assist"]))

    def get_readable_string(self):
        match self.type:
            case Wicket_Type.BOWLED:
                return f"{self.batter.name} was bowled out by {self.bowler.name}"
            case Wicket_Type.CAUGHT:
                return f"{self.batter.name} was caught by {self.fielder} off {self.bowler.name}'s bowling"
            case Wicket_Type.LBW:
                return f"{self.batter.name} was out lbw by {self.bowler.name}"
            case Wicket_Type.RUN_OUT:
                str = f"{self.batter.name} was run out by {self.fielder}"
                if self.assist is not None or self.assist != "":
                    str += f" and {self.assist}"
                return  str
            case Wicket_Type.STUMPED:
                return f"{self.batter.name} was stumped by {self.fielder} off {self.bowler.name}'s bowling"
            case Wicket_Type.HIT_WICKET:
                return f"{self.batter.name} was out 'hit wicket' off {self.bowler.name}'s bowling"
            case Wicket_Type.HIT_TWICE:
                return f"{self.batter.name} was out 'hit ball twice'"
            case Wicket_Type.OBSTRUCTING:
                return f"{self.batter.name} was out obstructing the field"
            case _:
                return "Incomplete wicket type"
            
    def __str__(self):
        match self.type:
            case Wicket_Type.BOWLED:
                return f"b {self.bowler.name}"
            case Wicket_Type.CAUGHT:
                if self.fielder == self.bowler.name:
                    return f"c&b {self.bowler.name}"
                return f"c {self.fielder} b {self.bowler.name}"
            case Wicket_Type.LBW:
                return f"lbw {self.bowler.name}"
            case Wicket_Type.RUN_OUT:
                str = f"run out {self.fielder}"
                if self.assist is not None or self.assist != "":
                    str += f" & {self.assist}"
                return  str
            case Wicket_Type.STUMPED:
                return f"st {self.fielder} b {self.bowler.name}"
            case Wicket_Type.HIT_WICKET:
                return f"hit wicket b {self.bowler.name}"
            case Wicket_Type.HIT_TWICE:
                return f"hit ball twice"
            case Wicket_Type.OBSTRUCTING:
                return f"obstructing the field"
            case _:
                return "Incomplete wicket type"