import sys
sys.path.insert(0,"..")

from models.over import *

def test_maiden_over():
    over = Over()
    for _ in range(6):
        over.AddDelivery(Delivery())

    assert over.runs == 0
    assert over.runs_against_bowler == 0
    assert over.legal_deliveries == 6

def test_no_balls():
    over = Over()
    over.AddDelivery(Delivery(2, delivery_type=Delivery_type.NO_BALL, runs_type=Runs_type.BAT))
    for _ in range(6):
        over.AddDelivery(Delivery())

    assert over.runs == 3
    assert over.legal_deliveries == 6
    assert over.no_balls == 1
    assert over.no_ball_runs == 3

def test_wides():
    over = Over()
    over.AddDelivery(Delivery(2, delivery_type=Delivery_type.WIDE, runs_type=Runs_type.BAT))
    for _ in range(6):
        over.AddDelivery(Delivery())

    assert over.runs == 3
    assert over.legal_deliveries == 6
    assert over.wides == 1
    assert over.wide_runs == 3

def test_maximum_legal():
    over = Over()
    for _ in range(6):
        over.AddDelivery(Delivery(6, boundary=Boundary.SIX))
    
    assert over.runs == 36
    sixes = sum(map(lambda d : d.boundary == Boundary.SIX, over.deliveries))
    assert sixes == 6