import sys
sys.path.insert(0,"..")

import pytest
from models.delivery import *

def test_create_delivery():
    delivery = Delivery(1)
    assert delivery.runs == 1

def test_negative_runs():
    with pytest.raises(ValueError):
        delivery = Delivery(-1)

def test_runs():
    delivery = Delivery(100)
    assert delivery.runs == 100

def test_default_delivery_type():
    delivery = Delivery()
    assert delivery.delivery_type == Delivery_type.GOOD
    assert delivery.runs == 0
    assert delivery.runs_type == Runs_type.NONE

def test_delivery_type_no_ball():
    delivery = Delivery(delivery_type=Delivery_type.NO_BALL)
    assert delivery.delivery_type == Delivery_type.NO_BALL
    assert delivery.runs_type == Runs_type.BAT
    assert delivery.runs == 1

def test_delivery_type_wide():
    delivery = Delivery(2, delivery_type=Delivery_type.WIDE)
    assert delivery.delivery_type == Delivery_type.WIDE
    assert delivery.runs_type == Runs_type.BAT
    assert delivery.runs == 3

def test_delivery_type_invalid():
    with pytest.raises(ValueError):
        delivery = Delivery(1, delivery_type="good")

def test_runs_type_default():
    delivery = Delivery(1)
    assert delivery.runs_type == Runs_type.BAT

def test_runs_type_bye():
    delivery = Delivery(1, runs_type= Runs_type.BYE)
    assert delivery.runs_type == Runs_type.BYE

def test_runs_type_leg_bye():
    delivery = (Delivery(1, runs_type= Runs_type.LEG_BYE))
    assert delivery.runs_type == Runs_type.LEG_BYE

def test_runs_type_none():
    delivery = Delivery(0)
    assert delivery.runs_type == Runs_type.NONE

def test_runs_type_invalid():
    with pytest.raises(ValueError):
        delivery = Delivery(1, runs_type="bat")

def test_batter_number():
    test_number = 1
    delivery = Delivery(batter_number= test_number)
    assert delivery.batter_number == test_number

def test_invalid_batter_number():
    with pytest.raises(ValueError):
        d = Delivery(1, batter_number=12)
    
def test_bowler_number():
    test_number = 2
    d = Delivery(0, bowler_number= test_number)
    assert d.bowler_number == test_number

def test_invalid_bowler_number():
    with pytest.raises(ValueError):
        d = Delivery(1, bowler_number=0)
    
def test_invalid_run_types():
    with pytest.raises(ValueError):
        d =Delivery(1, runs_type=Runs_type.NONE)
    with pytest.raises(ValueError):
        d = Delivery(0)
        d.runs_type = Runs_type.BAT

def test_runs_on_no_ball():
    d = Delivery(4, delivery_type=Delivery_type.NO_BALL, runs_type=Runs_type.BAT)
    assert d.batter_runs == 4
    assert d.runs == 5
    d.runs_type = Runs_type.EXTRAS
    assert d.batter_runs == 0
    d.runs_type = Runs_type.BYE
    assert d.batter_runs == 0

def test_runs_on_wide():
    d = Delivery(4, delivery_type=Delivery_type.WIDE, runs_type=Runs_type.BAT)
    assert d.batter_runs == 4
    assert d.runs == 5
    d.runs_type = Runs_type.EXTRAS
    assert d.batter_runs == 0
    d.runs_type = Runs_type.BYE
    assert d.batter_runs == 0

def test_wickets():
    d = Delivery(wicket = Wicket(type = Wicket_Type.BOWLED))
    assert d.wicket.type == Wicket_Type.BOWLED