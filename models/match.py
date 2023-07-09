from enum import Enum, unique
from datetime import datetime, date
from models.innings import *

@unique
class match_status(str, Enum):
    PREGAME = 'pregame'
    IN_PLAY = 'inplay'
    COMPLETED = 'completed'
    NONE = 'none'

@unique
class result_type(str, Enum):
    WINNER = 'winner'
    DRAW = 'draw'
    ABANDONNED = 'abandonned'
    NONE = 'none'

class Match:
    def __init__(self, home, away, innings=1, overs=40, id=None, date=date.today()):
        self.home_team = home
        self.away_team = away
        self.innings_per_team = innings
        self.overs_limit = overs
        self.current_innings = None
        self.all_innings = list()
        self.status = match_status.PREGAME
        self.result_type = result_type.NONE
        self.winner = None
        self.id=id
        self.date=date

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

    def to_dict(self):
        innings = [i.to_dict() for i in self.all_innings]
        return {
            "home": self.home_team,
            "away": self.away_team,
            "innings_per_team": self.innings_per_team,
            "overs_limit": self.overs_limit,
            "all_innings": innings,
            "status": self.status,
            "result": self.result_type,
            "winner": self.winner,
            "id": self.id,
            "date": self.date.strftime('%Y-%m-%d')
        }

    @classmethod
    def from_dict(cls, data):
        home = data["home"]
        away = data["away"]
        innings_per_team = data["innings_per_team"]
        overs_limit = data["overs_limit"]
        all_innings = [Innings.from_dict(i) for i in data["all_innings"]]
        status = match_status(data["status"])
        result = result_type(data["result"])
        winner = data["winner"]

        instance = cls(home, away, innings_per_team, overs_limit)
        instance.all_innings = all_innings
        if status == match_status.IN_PLAY:
            instance.current_innings = instance.all_innings[-1]
        instance.status = status
        instance.result_type = result
        instance.winner = winner
        instance.id = data["id"]

        instance.date = datetime.strptime(data["date"], '%Y-%m-%d').date()

        return instance

    def start_innings(self, batting_team):
        if self.status == match_status.COMPLETED:
            raise Exception("Match completed, cannot start new innings")
        if len(self.all_innings) >= self.innings_per_team * 2:
            raise RuntimeError("Maximimum number of innings already completed")
        if self.home_team == batting_team:
            bowling_team = self.away_team
        else:
            bowling_team = self.home_team
        self.current_innings = Innings(batting_team, bowling_team)
        self.all_innings.append(self.current_innings)
        self.status = match_status.IN_PLAY

    def end_match(self):
        self.status = match_status.COMPLETED
        self.winner, self.result_type = self.check_result()

    def abandon_match(self):
        self.status = match_status.COMPLETED
        self.result_type = result_type.ABANDONNED
        
    def add_delivery(self, delivery):
        if self.status == match_status.COMPLETED:
            raise Exception("Match completed, cannot add more deliveries")
        if self.current_innings == None:
            raise RuntimeError("No current_innings set. Please start an innings before adding deliveries")
        self.current_innings.add_delivery(delivery)

    def check_result(self):
        if len(self.all_innings) < 2:
            return None, result_type.NONE
        if self.all_innings[0].team_runs > self.all_innings[1].team_runs:
            winner = self.all_innings[0].batting_team
            result = result_type.WINNER
        elif self.all_innings[1].team_runs > self.all_innings[0].team_runs:
            winner = self.all_innings[1].batting_team
            result = result_type.WINNER
        else:
            result = result_type.DRAW
            winner = None

        return winner, result

    @property
    def result_text(self):
        if self.status != match_status.COMPLETED:
            return "Match not completed"
        else:
            if self.result_type == result_type.WINNER:
                return f"{self.winner} won!"
            elif self.result_type == result_type.DRAW:
                return f"Match finished in a draw"
            elif self.result_type == result_type.ABANDONNED:
                return "Match abandonned"
            else:
                return "No result"

    @property
    def status_as_text(self):
        match self.status:
            case match_status.PREGAME:
                return "Pregame"
            case match_status.IN_PLAY:
                return "In play"
            case match_status.COMPLETED:
                return "Completed"
            case _:
                return "Unknown"