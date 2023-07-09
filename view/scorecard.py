# Helper methods to display the scorecard from a match object

from tabulate import tabulate
from view.display_helpers import *

def display_full_scorecard(m):
    print_title("Scorecard")
    display_match_info(m)

    for i in m.all_innings:
        display_innings(i)
        print()    

def display_match_info(m):
    print(m.home_team, "vs", m.away_team)

def display_innings(i):
    print(subtitle(f"{i.batting_team} innings"))
    display_batters(i.get_all_batter_stats())
    display_extras(i.get_extras())
    display_totals(i.team_runs, i.team_wickets_count, i.overs_count)
    display_bowlers(i.get_all_bowler_stats())

def display_batters(b):    
    print(tabulate(b, headers="keys", tablefmt= "simple_outline"))

def display_extras(e):
    print(f"Extras {e['total']} (NB {e['no_balls']}, WD {e['wides']}, B {e['byes']}, LB {e['leg_byes']})")

def display_totals(runs, wickets, overs):
    print(subtitle(f"Total runs {runs} ({wickets} wkts, {overs} overs)"))
    
def display_bowlers(stats):
    print(tabulate(stats, headers="keys", tablefmt= "simple_outline"))
