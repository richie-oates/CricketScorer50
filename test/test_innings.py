import sys
sys.path.insert(0,"..")

import pytest
from models.innings import *

def test_add_batter():
    i = Innings("1","2")
    i.add_new_batter("Rich")
    for b in i.batters:
        print(b)

def test_delivery():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    for _ in range(6):
        i.add_delivery(Delivery(1))
    count = 0
    for o in i.overs:
        for d in o.deliveries:
            count += 1
            print (d)
    assert count == 6

def test_all_deliveries():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    for _ in range(6):
        i.add_delivery(Delivery(1))

    all = list()
    for d in i.all_deliveries:
        all.append(d)
        print(d)

    assert len(all) == 6

def test_all_deliveries_by_bowler():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    for _ in range(6):
        i.add_delivery(Delivery(1))

    i.add_new_bowler("Claire")
    for _ in range(6):
        i.add_delivery(Delivery(2))

    all = list()
    for d in i.get_all_deliveries_by_bowler_number(1):
        all.append(d)
        print(d)

    assert len(all) == 6

def test_bowler_stats():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    for _ in range(6):
        i.add_delivery(Delivery(1))
    stats = i.get_bowler_stats(1)
    print(i.get_bowler_stats(1))
    assert stats["Bowler"] == "Col"
    assert stats["Runs"] == 6
    assert stats["Overs"] == "1.0"
    assert stats["No_balls"] == 0
    assert stats["Wides"] == 0

def test_team_runs():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    for _ in range(6):
        i.add_delivery(Delivery(1))

    assert i.team_runs == 6

def test_wicket():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")
    
    for _ in range(6):
        i.add_delivery(Delivery(1))

    i.add_delivery(Delivery(wicket=Wicket(bowler = i.current_bowler)))

    assert i.team_wickets[0].bowler.name == "Col"
    with pytest.raises(RuntimeError):
        i.add_delivery(Delivery())

    i.add_new_batter("Claire")
    i.add_delivery(Delivery(1))

    stats = i.get_bowler_stats(1)
    assert stats["Wickets"] == 1

def test_caught_single():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")
    rich = i.current_striker
    Dad = i.current_nonstriker
    i.add_delivery(Delivery(runs = 1, wicket=Wicket(type=Wicket_Type.CAUGHT, batter=rich, bowler = i.current_bowler, fielder="Jess")))
    assert i.current_nonstriker == None
    assert i.current_striker == Dad

def test_add_nonstriker():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich", on_strike= False)
    i.add_new_batter("Dad", on_strike= False)
    assert i.current_striker.name == "Rich"
    assert i.current_nonstriker.name == "Dad"

def test_team_wickets():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")
    
    for _ in range(6):
        i.add_delivery(Delivery(1))

    i.add_delivery(Delivery(wicket=Wicket(bowler = i.current_bowler)))

    assert i.team_wickets_count == 1

def test_print_innings():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")
    
    for _ in range(5):
        i.add_delivery(Delivery(1))

    i.add_delivery(Delivery(wicket=Wicket(bowler = i.current_bowler)))

    print(i)
    for o in i.overs:
        print(o)

def test_out_obstructing():
    i = Innings("Sheffield","Leeds")
    i.add_new_batter("Rich")
    i.add_new_batter("Dad", on_strike= False)
    i.add_new_bowler("Col")

    i.add_delivery(Delivery(wicket=Wicket(Wicket_Type.OBSTRUCTING, bowler=i.current_bowler, batter=i.current_nonstriker)))
    assert i.current_nonstriker == None