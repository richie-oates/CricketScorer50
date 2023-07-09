from enum import Enum, unique
from models.wicket import *

@unique
class Delivery_type(str, Enum):
    GOOD = "GOOD"
    NO_BALL = "NO_BALL"
    WIDE = "WIDE"

@unique
class Runs_type(str, Enum):
    BAT = "BAT"
    BYE = "BYE"
    LEG_BYE = "LEG_BYE"
    EXTRAS = "EXTRAS"
    NONE = "NONE"

@unique
class Boundary(str, Enum):
    NONE = "NONE"
    FOUR = "FOUR"
    SIX = "SIX"
    
class Delivery:
    def __init__    (self,
                    runs=0,
                    bowler_number = 1,
                    batter_number = 1,
                    delivery_type = Delivery_type.GOOD,
                    runs_type = Runs_type.BAT,
                    boundary = Boundary.NONE,
                    wicket = None
                    ):

        self.bowler_number = bowler_number
        self.batter_number = batter_number
        self.delivery_type = delivery_type
        self.runs = runs
        if self.runs == 0:
            self.runs_type = Runs_type.NONE
        else:
            self.runs_type = runs_type
        self.boundary = boundary
        self.wicket = wicket

    def __str__(self):
        string = f"Bowler: {self.bowler_number} Batter: {self.batter_number} Runs: {self.runs} {self.delivery_type} {self.runs_type} Wicket: {self.wicket}"
        return string
    
    @property
    def abbreviation(self):
        if isinstance(self.wicket, Wicket):
            if self.runs > 0:
                return f"W{self.runs}"
            else:
                return "W"
        match self.delivery_type:
            case Delivery_type.GOOD:
                match self.runs_type:
                    case Runs_type.BAT:
                        return self.runs
                    case Runs_type.BYE:
                        return f"b{self.runs}"
                    case Runs_type.LEG_BYE:
                        return f"lb{self.runs}"
                    case Runs_type.NONE:
                        return 0
            case Delivery_type.NO_BALL:
                return f"nb{self.runs_actual}"
            case Delivery_type.WIDE:
                return f"wd{self.runs_actual}"
                
            
    
    def to_dict(self):
        wick_dict = self.wicket.to_dict() if self.wicket is not None else None 
        return {
            "runs": self.runs,
            "bowler_num": self.bowler_number,
            "batter_num": self.batter_number,
            "delivery_type": self.delivery_type,
            "runs_type": self.runs_type,
            "boundary": self.boundary,
            "wicket": wick_dict
        }
    
    @classmethod
    def from_dict(cls, data):
        wicket = None
        if "wicket" in data and data["wicket"] is not None:
            wicket = Wicket.from_dict(data["wicket"])
        delivery_type = Delivery_type(data["delivery_type"])
        runs = int(data["runs"])
        if delivery_type != Delivery_type.GOOD:
            runs -= 1
        
        return cls(
            runs=runs,
            bowler_number=data["bowler_num"],
            batter_number=data["batter_num"],
            delivery_type=delivery_type,
            runs_type=Runs_type(data["runs_type"]),
            boundary=Boundary(data["boundary"]),
            wicket=wicket
        )

    @property
    def runs(self):
        if self.delivery_type == Delivery_type.GOOD:
            return self._runs
        else:
            return self._runs + 1
        
    @property
    def runs_actual(self):
        return self._runs

    @runs.setter
    def runs(self, runs):
        if (runs >= 0):
            self._runs = runs
        else:
            raise ValueError("Runs cannot be negative")

    @property
    def bowler_number(self):
        return self._bowler_number
    
    @bowler_number.setter
    def bowler_number(self, bowler_number):
        if 1 <= bowler_number <= 11:
            self._bowler_number = bowler_number
        else:
            raise ValueError("Bowler number invalid") 

    @property
    def batter_number(self):
        return self._batter_number
    
    @batter_number.setter
    def batter_number(self, batter_number):
        if 1 <= batter_number <= 11:
            self._batter_number = batter_number
        else:
            raise ValueError("Batter number invalid")
        
    @property
    def batter_runs(self):
        if self.runs_type == Runs_type.BAT:
            return self._runs
        else:
            return 0
        
    @property
    def runs_against_bowler(self):
        if self.runs_type not in {Runs_type.BYE, Runs_type.LEG_BYE}:
            return self.runs
        else:
            return 0
        
    @property
    def delivery_type(self):
        return self._delivery_type

    @delivery_type.setter
    def delivery_type(self, delivery_type):
        if (isinstance(delivery_type, Delivery_type)):
            self._delivery_type = delivery_type
        else:
            raise ValueError("Invalid Delivery_type format")
        
    @property
    def runs_type(self):
        return self._runs_type

    @runs_type.setter
    def runs_type(self, runs_type):
        if isinstance(runs_type, Runs_type):
            if self.runs == 0 and not runs_type == Runs_type.NONE:
                raise ValueError("Invalid run type for 0 runs scored")
            elif self.runs > 0 and runs_type == Runs_type.NONE:
                raise ValueError("Invalid run type for runs scored")
            else:
                self._runs_type = runs_type
        else:
            raise ValueError("Invalid Runs_type format")
        
    @property
    def boundary(self):
        return self._boundary
    
    @boundary.setter
    def boundary(self, boundary):
        if boundary == Boundary.FOUR:
            if self.runs_actual == 4:
                self._boundary = boundary
            else:
                raise ValueError("Invalid boundary type for number of runs scored")
        elif boundary == Boundary.SIX:
            if self.runs_actual == 6:
                self._boundary = boundary
            else:
                raise ValueError("Invalid boundary type for number of runs scored")
        else:
            self._boundary = Boundary.NONE
