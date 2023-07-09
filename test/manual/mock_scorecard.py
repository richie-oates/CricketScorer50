from view.scorecard import *
from models.wicket import *
from models.innings import Player

def __main__():
    batters = []
    batters.append({"#":1, "Name":"Rich","How Out":Wicket(Wicket_Type.CAUGHT, fielder="Dad", bowler=Player(1, "Dad")), "R":100, "B":50, "4s":10, "6s":5, "S/R":round(100 * 100/50, 2)})
    batters.append({"#":2, "Name":"Col","How Out":"not out", "R":200, "B":75, "4s":20, "6s":8, "S/R":round(100 * 200/75, 2)})
    print(subtitle("Leeds"))
    display_batters(batters)

    extras = {"total" : 12, "no_balls": 5, "wides":0, "byes":3, "leg_byes":5}
    display_extras(extras)
    display_totals(312, 1, 20.0)



if __name__ == "__main__":
    __main__()