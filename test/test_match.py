import sys
sys.path.insert(0,"..")

import pytest
from models.match import *

def test_create_match():
    match = Match("Sheffield", "Leeds")
    assert match.home_team == "Sheffield"
    assert match.away_team == "Leeds"

def test_start_innings():
    match = Match("Sheffield", "Leeds")
    match.start_innings("Leeds")
    assert match.current_innings.batting_team == "Leeds"

def test_no_innings():
    match = Match("Sheffield", "Leeds")
    with pytest.raises(RuntimeError):
        match.add_delivery(Delivery())

def test_no_bowler():
    match = Match("Sheffield", "Leeds")
    match.start_innings("Leeds")
    with pytest.raises(RuntimeError):
        match.add_delivery(Delivery())

def test_status_pregame():
    match = Match("Sheffield", "Leeds")
    assert match.status == match_status.PREGAME

def test_status_inplay():
    match = Match("Sheffield", "Leeds")
    match.start_innings("Leeds")
    assert match.status == match_status.IN_PLAY

def test_status_completed():
    match = Match("Sheffield", "Leeds")
    match.end_match()
    assert match.status == match_status.COMPLETED