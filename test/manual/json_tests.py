from models.match import *
from dummy_match import get_simple_match
from view.scorecard import display_full_scorecard
import json

def test_simple_match():
    match = get_simple_match()
    display_full_scorecard(match)
    with open("saves.json", "w") as file:
        json.dump(match.to_dict(), file, indent=2)

    with open("saves.json", "r") as file:
        m_json = json.load(file)

    new_match = Match.from_dict(m_json)
    display_full_scorecard(new_match)

    print(new_match.all_innings[0].get_bowler_stats(1))

    assert match.all_innings[0].overs == new_match.all_innings[0].overs