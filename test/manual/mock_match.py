from project import *

def __main__():
    match = Match("Leeds", "Sheffield", 1, 20)
    match.start_innings("Leeds")
    match.current_innings.add_new_bowler("Rich")
    match.current_innings.add_new_batter("Col")
    match.current_innings.add_new_batter("Dad", on_strike=False)
    i = match.current_innings
    i.add_delivery(Delivery(wicket=Wicket(Wicket_Type.OBSTRUCTING, bowler=i.current_bowler,batter=i.current_nonstriker)))


if __name__ == "__main__":
    __main__()