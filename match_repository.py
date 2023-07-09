# Handles saving and loading matches to and from file

import json
from models.match import Match

class MatchRepository:
    def __init__(self, save_file):
        self.save_file = save_file
        self.matches = self.load_from_file()

    def save_to_file(self):
        matches_data = []
        for m in self.matches:
            matches_data.append(m.to_dict())
        with open(self.save_file, "w") as file:
            json.dump(matches_data, file, indent=2)

    def load_from_file(self):
        matches = []
        try:
            with open(self.save_file, "r") as file:
                matches_data = json.load(file)
        except:
            return matches
        else:
            for m in matches_data:
                matches.append(Match.from_dict(m))
            return matches

    def add(self, match):
        self.matches.append(match)
        self.save_to_file()

    def get(self, id):
        for match in self.matches:
            if match.id == id:
                return match
        return None

    def get_all(self):
        return self.matches

    def update(self, old_match, new_match):
        try:
            self.delete(old_match.id)
        except:
            raise Exception("match not found")
        else:
            self.add(new_match)
            self.save_to_file()

    def delete(self, id):
        for m in self.matches:
            if m.id == id:
                self.matches.remove(m)
                self.save_to_file()
                return
        raise Exception("match not found")
    
    def get_new_match_id(self):
        id=0
        for m in self.matches:
            if m.id >= id:
                id = m.id + 1
        return id
        