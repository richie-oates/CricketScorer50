from models.over import *

class Innings:
    def __init__(self, batting_team, bowling_team):
        if not isinstance(batting_team, str):
            raise ValueError("Team IDs must be of type string")
        else:
            self.batting_team = batting_team

        if not isinstance(bowling_team, str):
            raise ValueError("Team IDs must be of type string")
        else:
            self.bowling_team = bowling_team

        self.batters = list()
        self.bowlers = list()
        self.current_striker = None
        self.current_nonstriker = None
        self.current_bowler = None
        self.overs = list()
        self.current_over = Over()
        self.overs.append(self.current_over)

    def to_dict(self):
        batters = [batter.to_dict() for batter in self.batters]
        bowlers = [bowler.to_dict() for bowler in self.bowlers]
        overs = [over.to_dict() for over in self.overs]
        wickets = [wicket.to_dict() for wicket in self.team_wickets]

        return {
            "batting": self.batting_team,
            "bowling": self.bowling_team,
            "batters": batters,
            "striker": self.current_striker.to_dict() if self.current_striker is not None else None,
            "nonstriker": self.current_nonstriker.to_dict() if self.current_nonstriker is not None else None,
            "bowlers": bowlers,
            "bowler": self.current_bowler.to_dict() if self.current_bowler is not None else None,
            "overs": overs,
            "wickets": wickets
        }
    
    @classmethod
    def from_dict(cls, data):
        batting_team = data["batting"]
        bowling_team = data["bowling"]

        instance = cls(batting_team, bowling_team)

        batters = [Player.from_dict(batter_data) for batter_data in data["batters"]]
        instance.batters = batters

        if "striker" in data and data["striker"] is not None:
            instance.current_striker = Player.from_dict(data["striker"])

        if "nonstriker" in data and data["nonstriker"] is not None:
            instance.current_nonstriker = Player.from_dict(data["nonstriker"])

        bowlers = [Player.from_dict(bowler_data) for bowler_data in data["bowlers"]]
        instance.bowlers = bowlers

        if "bowler" in data and data["bowler"] is not None:
            instance.current_bowler = Player.from_dict(data["bowler"])

        overs = [Over.from_dict(over_data) for over_data in data["overs"]]
        instance.overs = overs
        
        if len(instance.overs) > 0:
            instance.current_over = instance.overs[-1]


        return instance

    def __str__(self):
        return f"Batting: {self.batting_team}\nBowling: {self.bowling_team}\nScore: {self.team_runs}/{self.team_wickets_count}\nOvers: {self.overs_count:.1f}"

    @property
    def all_deliveries(self):
        a = list()
        for o in self.overs:
            for d in o.deliveries:
                a.append(d)
        return a
    
    @property
    def team_runs(self):
        runs = sum(d.runs for d in self.all_deliveries)
        return runs
    
    @property
    def team_wickets(self):
        wickets = []
        for d in self.all_deliveries:
            if isinstance(d.wicket, Wicket):
                wickets.append(d.wicket)
        return wickets
    
    @property
    def team_wickets_count(self):
        return len(self.team_wickets)
    
    @property
    def overs_count(self):
        if self.current_over.legal_deliveries >= 6:
            return len(self.overs)
        else:
            return (10 * (len(self.overs) - 1) + self.current_over.legal_deliveries)/10

    def get_all_deliveries_by_bowler_number(self, number):
        a = list()
        for d in self.all_deliveries:
            if d.bowler_number == number:
                a.append(d)
        return a

    def get_overs_by_bowler_number(self, number):
        a = list()
        for o in self.overs:
            if number in o.bowlers:
                a.append(o)
        return a

    def add_new_bowler(self, name, id=None, is_current_bowler=True):
        b = Player(len(self.bowlers) + 1, name, id = id)
        self.bowlers.append(b)
        if is_current_bowler:
            self.current_bowler = b

    def add_new_batter(self, name, id=None, on_strike=True):
        new_batter = Player(len(self.batters) + 1, name, id)
        self.batters.append(new_batter)
        if on_strike:
            if self.current_striker == None:
                self.current_striker = new_batter
            else:
                if self.current_nonstriker == None:
                    self.current_nonstriker = self.current_striker
                    self.current_striker = new_batter
                else:
                    raise RuntimeError("Cannot add batsman until one is removed")
        else:
            if self.current_nonstriker == None:
                self.current_nonstriker = new_batter
            else:
                if self.current_striker == None:
                    self.current_striker = self.current_nonstriker
                    self.current_nonstriker = new_batter
                else:
                    raise RuntimeError("Cannot add batsman until one is removed")

    def batters_switch_ends(self):
        temp = self.current_nonstriker
        self.current_nonstriker = self.current_striker
        self.current_striker = temp

    def start_new_over(self, bowler):
        self.set_bowler(bowler)
        # Batters switch ends if not first over of innings
        if len(self.overs) > 0:
            self.batters_switch_ends()
        self.current_over = Over()
        self.overs.append(self.current_over)

    def set_bowler(self, bowler_number=None):
        if bowler_number == None:
            bowler_number = len(self.bowlers) + 1
        if not isinstance(bowler_number, int):
            print(bowler_number)
            raise ValueError("Bowler number must be of type 'int'")
        self.current_bowler = self.get_bowler(bowler_number)

    def get_bowler(self, number):
        if len(self.bowlers) >= int(number):
            return self.bowlers[int(number)-1]
        else:
            raise ValueError("Please add new bowler to list first")

    def add_delivery(self, delivery):
        # Check batters and bowler have been set
        if self.current_striker == None:
            raise RuntimeError("current_striker cannot be None")
        if self.current_nonstriker == None:
            raise RuntimeError("current_nonstriker cannot be None")
        if self.current_bowler == None:
            raise RuntimeError("current_bowler cannot be None")

        # include batter and bowler numbers in delivery object
        try:
            delivery.batter_number = self.current_striker.number
            delivery.bowler_number = self.current_bowler.number
        except:
            raise ValueError("Invalid delivery object")
        
        # Add delivery to current over
        self.current_over.AddDelivery(delivery)

        # If delivery included a wicket
        if isinstance(delivery.wicket, Wicket):

            # If delivery type not run_out or obstructing, ensure batter is set to striker
            if (delivery.wicket.type not in [Wicket_Type.RUN_OUT, Wicket_Type.OBSTRUCTING]) and not (delivery.wicket.type == Wicket_Type.CAUGHT and delivery.runs % 2 != 0):
                if delivery.wicket.batter == None:
                    delivery.wicket.batter = self.current_striker
                elif delivery.wicket.batter != self.current_striker:
                    raise ValueError(f"For wicket type {delivery.wicket.type} batsman must be current striker")                
            
            # Remove batsman out
            if self.current_striker == delivery.wicket.batter:
                self.current_striker = None
            elif self.current_nonstriker == delivery.wicket.batter:
                self.current_nonstriker = None
            else:
                raise ValueError("No batter given for wicket")
            
            # Add bowler to wicket
            delivery.wicket.bowler = self.current_bowler

        # Switch ends if batter ran an odd number of runs
        if delivery.runs_actual % 2 != 0:
            self.batters_switch_ends()
        
    def get_batter_score(self, batter):
        deliveries_faced = self.get_deliveries_faced(batter)
        return sum(d.runs_actual for d in filter(lambda d: d.runs_type == Runs_type.BAT, deliveries_faced))
    
    def get_deliveries_faced(self, batter):
        return filter(lambda d: d.batter_number == batter.number, self.all_deliveries)
    
    def get_batter_wicket(self, batter):
        wickets = list(filter(lambda w: w.batter.number == batter.number, self.team_wickets))
        if len(wickets) == 0:
            return "Not Out"
        else:
            return wickets[0]

    def get_batter_stats(self, batter):
        runs = self.get_batter_score(batter)
        balls = self.get_balls_faced_count(batter)
        wicket = self.get_batter_wicket(batter)
        fours = self.get_4_count(batter)
        sixes = self.get_6_count(batter)
        strike_rate = 0 if balls == 0 else round(100 * runs/balls, 2)
        return {"#":batter.number, "Batter":batter.name, "How out":wicket, "R":runs, "B":balls, "4s":fours, "6s":sixes, "S/R":strike_rate}
    
    def get_4_count(self, batter):
        return sum(map(lambda d: d.boundary == Boundary.FOUR, self.get_deliveries_faced(batter)))
        
    def get_6_count(self, batter):
        return sum(map(lambda d: d.boundary == Boundary.SIX, self.get_deliveries_faced(batter)))

    def get_all_batter_stats(self):
        stats = []
        for batter in self.batters:
            stats.append(self.get_batter_stats(batter))
        return stats

    def get_balls_faced_count(self, batter):
        return sum(map(lambda d: d.batter_number == batter.number, self.all_deliveries))

    def get_bowler_stats(self, number):
        name = "Unknown"
        for bowler in self.bowlers:
            if bowler.number == number:
                name = bowler.name
                break

        balls = sum(map(lambda d:  d.delivery_type == Delivery_type.GOOD, self.get_all_deliveries_by_bowler_number(number)))
        completed_overs = int(balls/6)
        part_over = balls % 6
        overs = f"{completed_overs}.{part_over}"
        runs = sum(d.runs_against_bowler for d in self.get_all_deliveries_by_bowler_number(number))
        no_balls = sum(d.runs for d in filter(lambda d : d.delivery_type == Delivery_type.NO_BALL, self.get_all_deliveries_by_bowler_number(number)))
        wides = sum(d.runs for d in filter(lambda d : d.delivery_type == Delivery_type.WIDE, self.get_all_deliveries_by_bowler_number(number)))
        wickets = sum(map(lambda w : w.bowler.number == number and w.type not in {Wicket_Type.RUN_OUT, Wicket_Type.OBSTRUCTING}, self.team_wickets))
        economy = 0 if balls == 0 else round(runs / (balls/6), 2)
        return {"Bowler" : name, "Overs" : overs, "Runs" : runs, "Wickets" : wickets, "No_balls" : no_balls, "Wides" : wides, "Economy": economy}

    def get_all_bowler_stats(self):
        stats = []
        for b in self.bowlers:
            stats.append(self.get_bowler_stats(b.number))
        return stats

    def get_extras(self):
        # sum of all no balls + runs scored of no balls where runs_type == extras
        no_balls = sum(d.runs_actual for d in filter(lambda d : d.delivery_type == Delivery_type.NO_BALL and d.runs_type == Runs_type.EXTRAS, self.all_deliveries))
        no_balls += sum(map(lambda d : d.delivery_type == Delivery_type.NO_BALL, self.all_deliveries))

        wides = sum(d.runs for d in filter(lambda d : d.delivery_type == Delivery_type.WIDE, self.all_deliveries))
        byes = sum(d.runs for d in filter(lambda d : d.runs_type == Runs_type.BYE, self.all_deliveries))
        leg_byes = sum(d.runs for d in filter(lambda d : d.runs_type == Runs_type.LEG_BYE, self.all_deliveries))
        total = no_balls + wides + byes + leg_byes
        return {"total": total, "no_balls":no_balls, "wides":wides, "byes":byes, "leg_byes":leg_byes}