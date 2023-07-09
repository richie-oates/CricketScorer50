from models.delivery import *

class Over:
    def __init__(self, deliveries=None, bowlers=None):
        self.deliveries = list() if deliveries == None else deliveries
        self.bowlers = list() if bowlers == None else bowlers

    def __str__(self):
        over_string = "("
        if len(self.deliveries) > 0:
            for d in self.deliveries:
                over_string += f"{d.abbreviation} "
        over_string += ")"
        return over_string

    def to_dict(self):
        deliveries = list()
        for d in self.deliveries:
            deliveries.append(d.to_dict())
        bowlers = list()
        for b in self.bowlers:
            bowlers.append(b)
        return {
            "deliveries": deliveries,
            "bowler/s": bowlers
        }
    
    @classmethod
    def from_dict(cls, data):
        deliveries = list()
        if "deliveries" in data and data["deliveries"] is not None:
            deliveries = [Delivery.from_dict(delivery_data) for delivery_data in data["deliveries"]]
        bowlers = list()
        if "bowlers" in data and data["bowlers"] is not None:
            bowlers = [bowler_data for bowler_data in data["bowlers"]]
    
        return cls(deliveries, bowlers)


    def AddDelivery(self, delivery):
        self.deliveries.append(delivery)
        if not delivery.bowler_number in self.bowlers:
            self.bowlers.append(delivery.bowler_number)

    @property
    def runs(self):
        return sum(delivery.runs for delivery in self.deliveries)
    
    @property
    def legal_deliveries(self):
        # Counts elements in the list where the lambda function is satisfied
        return sum(map(lambda d : d.delivery_type == Delivery_type.GOOD, self.deliveries))
    
    @property
    def runs_against_bowler(self):
        # Filters list elements by lambda function
        return sum(d.runs_against_bowler for d in self.deliveries)
    
    @property
    def no_balls(self):
        # Count number of no_balls
        return sum(map(lambda d : d.delivery_type == Delivery_type.NO_BALL, self.deliveries))
    
    @property
    def no_ball_runs(self):
        # Count runs scored from no_balls
        return sum(d.runs for d in filter(lambda d : d.delivery_type == Delivery_type.NO_BALL
                                                            , self.deliveries))
    
    @property
    def wides(self):
        # Count number of wides
        return sum(map(lambda d : d.delivery_type == Delivery_type.WIDE, self.deliveries))
    
    @property
    def wide_runs(self):
        # Count runs scored from wides
        return sum(d.runs for d in filter(lambda d : d.delivery_type == Delivery_type.WIDE
                                                            , self.deliveries))