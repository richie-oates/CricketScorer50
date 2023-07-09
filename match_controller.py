from models.match import *

DELIVERIES_PER_OVER = 6

class MatchController():
    def __init__(self, match_repo):
        self.match_repo = match_repo
        self.current_match = None

    # MatchRepository CRUD operations

    def get_all_matches(self):
        return self.match_repo.get_all()

    def get_match_by_id(self, id):
        return self.match_repo.get(id)
    
    def set_current_match(self, id):
        match = self.get_match_by_id(id)
        if match is not None:
            self.current_match = match
        else:
            raise ValueError("Invalid match ID")

    def create_new_match(self, date, home_team, away_team, over_limit):
        try:
            self.current_match = Match(home = home_team, away=away_team, overs=over_limit, date=date)
            self.current_match.id = self.match_repo.get_new_match_id()
            self.match_repo.add(self.current_match)
        except :
            raise ValueError("Failed to create new match")

    def save_current_match(self):
        old_match = self.match_repo.get(self.current_match.id)
        if (old_match is not None):
            self.match_repo.update(old_match, self.current_match)
        else:
            self.match_repo.add(self.current_match)

    def update_current_match(self, match):
        if self.current_match.id != match.id:
            raise ValueError("Match IDs are not equivalent")
        else:
            self.current_match = match
            self.save_current_match()

    def delete_current_match(self):
        self.match_repo.delete(self.current_match.id)
    
    # "Business" logic

    @property
    def current_innings(self):
        return self.current_match.current_innings
    
    def start_innings(self, batting_team):
        self.current_match.start_innings(batting_team=batting_team)
        self.update_current_match(self.current_match)

    def add_new_bowler(self, bowler_name):
        self.current_innings.add_new_bowler(bowler_name)
        self.update_current_match(self.current_match)

    def add_new_batter(self, name, on_strike=True):
        self.current_innings.add_new_batter(name, on_strike=on_strike)
        self.update_current_match(self.current_match)

    def add_delivery(self, delivery):
        self.current_innings.add_delivery(delivery)
        self.update_current_match(self.current_match)

    def start_new_over(self, bowler_number):
        if self.current_match == None:
            raise ValueError("Match not loaded")
        else:
            self.current_innings.start_new_over(bowler_number)

    def end_match(self):
        if self.current_match == None:
            raise ValueError("Match not loaded")
        else:
            self.current_match.end_match()
            
    
    # Queries

    def are_no_more_overs_in_innings(self):
        if len(self.current_innings.overs) >= self.current_match.overs_limit and self.is_current_over_completed():
            return True
        return False

    def are_no_batters_left(self):
        if self.current_innings.team_wickets_count >= 10:
            return True
        return False
    
    def is_current_over_completed(self):
        return self.is_over_completed(self.current_innings.current_over)

    def is_over_completed(self, over):
        return over.legal_deliveries >= DELIVERIES_PER_OVER
    
    def has_chasing_team_reached_target(self):
        if len(self.current_match.all_innings) == 2:
            winner, result = self.current_match.check_result()
            if winner == self.current_innings.batting_team:
                return True  
        return False
