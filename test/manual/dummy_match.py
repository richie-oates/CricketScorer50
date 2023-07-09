from project import *   

def over_of_singles(match):
    for _ in range(6):
        match.current_innings.add_delivery(Delivery(1))

def two_overs_of_singles(match):
    match.current_innings.start_new_over(1)
    over_of_singles(match)
    match.current_innings.start_new_over(2)
    over_of_singles(match)

def get_simple_match():
    match = Match("Leeds", "Sheffield", 1, 20)
    match.start_innings("Leeds")
    match.current_innings.add_new_bowler("Rich")
    match.current_innings.add_new_batter("Col")
    match.current_innings.add_new_batter("Dad", on_strike=False)

    over_of_singles(match)
    match.current_innings.add_new_bowler("Claire")
    match.current_innings.start_new_over(2)
    over_of_singles(match)


    for _ in range(9):
        two_overs_of_singles(match)

    return match