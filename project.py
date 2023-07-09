# View / Presentation Layer
import sys
import cowsay
from datetime import datetime, date
from tabulate import tabulate

from models.match import *
from match_repository import MatchRepository
from match_controller import MatchController

from view.display_helpers import *
from view.scorecard import display_full_scorecard

MIN_OVERS = 1
MAX_OVERS = 50

def __main__():
    check_cl_args(sys.argv) 
    global match_repo # Match repository handles loading and saving match data to file
    match_repo = MatchRepository(sys.argv[1])
    global match_controller # Match controller handles business logic and ensures changes are saved immediately via match_repo
    match_controller = MatchController(match_repo)
    show_welcome_screen()
    input("Press enter to start... ")
    start_menu() # Go to start menu

# Ensures command line argument contains a json filename to save/load data
def check_cl_args(args):
    if len(args) != 2 or not args[1].endswith(".json"):
        sys.exit("Please provide json save file as command line argument")

# The main menu of application
def start_menu():
    print_title("Start Menu")   
    while True:
        print(subtitle("Start Menu Options"))
        print("n = create new match")
        print("l = load saved match")
        print("x = exit application")
        option = input("Please select an option: ").strip().lower()
        
        if option == "n":
            create_new_match()
            match_menu()
            return
        elif option == "l":
            load_match()
            return
        elif option == "x":
            if read_yes_no_answer("Confirm exit application"):
                exit_app()
        else:
            print("Invalid selection")

def exit_app():
    cowsay.pig("Thanks for using Cricket Scorer 50, CS50", 
                    char_lines='''\n  \\\n   \\\n    \\\n 
    .-.'  `; `-._  __  _
   (_,         .-:'  `; `-._
 ,'o"(        (_,           )
(__,-'      ,'o"(            )>
   (       (__,-'            )
    `-'._.--._(             )
       |||  |||`-'._.--._.-'
                  |||  |||  ''')
    sys.exit()


# Add basic match info and save to match repository
def create_new_match():
    print(subtitle("New Match"))
    date = read_date("Date ")
    home = read_string("Enter home team name: ")
    away = read_string("Enter away team name: ")
    overs = read_int("Overs per innings: ", MIN_OVERS, MAX_OVERS)
    try:
        match_controller.create_new_match(date, home, away, overs)
    except:
        print("Unable to create match")
    else:
        print(match_controller.current_match)

# Displays list of saved matches and option to load one
## TODO: sort and filter matches by date and team
## TODO: Add option to return to start menu
def load_match():
    matches =  match_controller.get_all_matches()
    if len(matches) == 0:
        print("No match data available")
        if read_yes_no_answer("Create new match?"):
            create_new_match()
            match_menu()
            return
    print("")
    print(subtitle("Load match menu"))
    matches_list = []
    for match in sorted(matches, key=lambda m: m.date):
        matches_list.append({"ID":match.id, "Date":match.date, "Home team":match.home_team, "Away team":match.away_team})
    print(tabulate(matches_list, headers="keys", tablefmt= "simple_outline"))


    while True:
        try:
            match_controller.set_current_match(int(read_string("Select match by ID: ")))
            match_menu()
            break
        except ValueError:
            print("Invalid match id, try again")

# Displays match options depending on match status
def match_menu():
    match = match_controller.current_match
    if match == None:
        print("Please create a new match or load a saved match")
        start_menu()
        return
        
    while True:
        print_title("Match Menu")
        print(subtitle(f"{match.home_team} vs {match.away_team}"))
        print(get_match_type_string(match))
        print(f"Status: {match.status_as_text}")
        print("")
        print("Match options:")
        if (match.status == match_status.COMPLETED or match.date != date.today()):
            print(get_result_string(match))
            choice = input("v = view scorecard, x = save and exit, d = delete match: ").strip().lower()
            if choice == "x":
                match_controller.save_current_match()
                start_menu()
                break
            elif choice == "v":
                show_scorecard(match)
                input("Press enter to continue")
            elif choice == "d":
                if read_yes_no_answer("DELETE! Are you sure you want to delete this permanently? This cannot be undone!"):
                    match_controller.delete_current_match()
                    start_menu()
                    break
        else:
            if (match.status == match_status.IN_PLAY):
                print(get_score_string(match))
            print("s = start scoring, v = view scorecard, x = save and exit, d = delete match")
            choice = input("Enter your choice: ").strip().lower()
            if choice == "s":
                scoring_menu()
                break
            elif choice == "v":
                show_scorecard(match)
            elif choice == "x":
                match_controller.save_current_match()
                start_menu()
                break
            elif choice == "d":
                if read_yes_no_answer("DELETE! Are you sure you want to delete this permanently? This cannot be undone!"):
                    match_controller.delete_current_match()
                    start_menu()
                    break
            else:
                print("Invalid selection")

# Starts scoring current match from current match state
def scoring_menu():
    m = match_controller.current_match
    if m == None:
        print ("No match loaded")
        start_menu()
        return
    i = m.current_innings

    if i == None:
        print(subtitle("New innings"))
        batting_team = read_int(f"Enter batting team: 1 = {m.home_team}, 2 = {m.away_team}: ", 1, 2)
        batting_team = m.home_team if batting_team == 1 else m.away_team
        match_controller.start_innings(batting_team)
        i = match_controller.current_innings
    if i.current_bowler == None:
        match_controller.add_new_bowler(read_string("Enter bowler name: "))
    if i.current_striker == None:
        match_controller.add_new_batter(read_string("Enter striker name: "), True)
    if i.current_nonstriker == None:
        match_controller.add_new_batter(read_string("Enter non-striker name: "), False)
    
    while True:
        print_title("Scoring Menu")
        # Check if chasing team reached target
        if match_controller.has_chasing_team_reached_target():
            end_match()
            break

        # Check if second innings completed
        if match_controller.are_no_more_overs_in_innings():
            if len(m.all_innings) == 2:
                end_match()
                break
            # if first innings completed
            else: 
                if read_yes_no_answer("No more overs, do you want to start a new innings? y/n "):
                    new_innings()
                    return
        
        # Check wickets remaining
        if match_controller.are_no_batters_left():
            if len(m.all_innings) == 2:
                end_match()
                break
            else:
                response = input("No more batters, do you want to start a new innings? y/n ").strip().lower()
                if response == "y":
                    new_innings()
                    return

        # Check if new batter needed
        while i.current_striker == None or i.current_nonstriker == None:
            name = read_string("New batter: ")
            is_on_strike = read_yes_no_answer("Is new batter on strike?")
            match_controller.add_new_batter(name, on_strike=is_on_strike)

        print(get_match_summary_string(m))

        print("d = new delivery, o = start new over, i = start new innings, s = batters switch ends, e = end match, \nv = view full scorecard, x = return to match menu")
        choice = input("Select option: ").strip().lower()
        if choice == "d":
            if not match_controller.is_current_over_completed() or read_yes_no_answer("Already reached limit of deliveries for the over, are you sure you want to add another delivery?"):
                while True:
                    try:
                        d = read_delivery()
                        match_controller.add_delivery(d)
                        if isinstance(d.wicket, Wicket):
                            print_title("Wicket!")
                            print("Wicket:", d.wicket.batter.name, d.wicket, i.get_batter_score(d.wicket.batter), "runs")
                        break
                    except ValueError:
                        input("Invalid delivery object, press enter to try again")
        elif choice == "o":
            start_new_over()
        elif choice == "i":
            if read_yes_no_answer("Confirm start new innings"):
                try:
                    new_innings()
                    return
                except RuntimeError:
                    print("Max innings reached")
                    input("End game (press enter)")
                    end_match()
                    return
                
        elif choice == "s":
            if read_yes_no_answer(f"{i.current_nonstriker} will be on strike, confirm"):
                i.batters_switch_ends()

        elif choice == "e":
            if read_yes_no_answer("Confirm end match"):
                m.result_type = result_type.ABANDONNED
                m.status = match_status.COMPLETED
                match_menu()
                return
        elif choice == "v":
            show_scorecard(m)
            input("Enter to continue: ")
        elif choice == "x":
            match_menu()
            return
            
def new_innings():
    m = match_controller.current_match
    if m == None:
        raise ValueError("No match loaded")
    if len(m.all_innings) % 2 != 0:
        match_controller.start_innings(m.all_innings[-1].bowling_team)
    else:
        batting_team = read_int(f"Enter batting team: 1 = {m.home_team}, 2 = {m.away_team}: ", 1, 2)
        batting_team = m.home_team if batting_team == 1 else m.away_team
        match_controller.start_innings(batting_team)
        
    scoring_menu()

def start_new_over():
    innings = match_controller.current_innings
    if not read_yes_no_answer("Starting new over, are you sure?"):
        return
    print(subtitle("Starting new over"))
    while True:
        print("Select new bowler from: ")
        print(f"{innings.current_bowler.name} unavailable")
        for bowler in innings.bowlers:
            if innings.current_bowler.number != bowler.number:
                print(f"{bowler.number} = {bowler.name}")
        print("'n' = add new bowler")
        choice = input("Selection: ")
        if choice == "n":
            name = input("Name: ")
            match_controller.add_new_bowler(name)    
            match_controller.start_new_over(innings.current_bowler.number)
            return
        else:
            try:
                match_controller.start_new_over(int(choice))
                return
            except ValueError:
                print(f"'{choice}' = Invalid selection, try again")

def end_match():
    match = match_controller.current_match
    match_controller.end_match()
    if match.result_type == result_type.WINNER:
        print(f"{match.winner} wins!!")
    else:
        print(f"Match drawn")
    input("Press enter to view scorecard")
    show_scorecard(match)
    input("Press enter to go to match_menu")
    match_menu()

## Display methods ##

# Displays application title    
def show_welcome_screen():
    print_title("Cricket Scorer 50")
    print(subtitle("Welcome to Cricket Scorer 50 (CS50)"))

# Displays scorecard
def show_scorecard(match):
    display_full_scorecard(match)

## Methods that return strings of match info ##
def get_match_summary_string(match):
    summary = "=" * 30 +"\n"
    i = match.current_innings

    if len(match.all_innings) == 1:
        summary += f"{i.batting_team} are batting 1st\n"
    elif len(match.all_innings) == 2:
        summary += f"{i.batting_team} are batting 2nd\n"

    summary += "=" * 30 +"\n"
    summary += f"Score: {i.team_runs}/{i.team_wickets_count}"
    summary += f" from {i.overs_count}/{match.overs_limit} overs\n"
    if len(match.all_innings) == 2:
        summary += f"{i.bowling_team} scored: {match.all_innings[0].team_runs}/{match.all_innings[0].team_wickets_count}"
        summary += f" from {match.all_innings[0].overs_count}/{match.overs_limit} overs\n"
    
    summary += "\nBatters:\n"
    striker = i.current_striker
    nonstriker = i.current_nonstriker
    if striker != None:
        summary += f"{striker.name}*, {i.get_batter_score(striker)}\n"
    if nonstriker != None:    
        summary += f"{nonstriker.name}, {i.get_batter_score(nonstriker)}\n"
    bowler_stats = i.get_bowler_stats(i.current_bowler.number)
    summary += f"\nBowler: \n{i.current_bowler.name}, {bowler_stats['Overs']} overs, {bowler_stats['Runs']} runs, {bowler_stats['Wickets']} wickets\n"
    
    return summary

def get_score_string(match):
    score = ""
    for count, i in enumerate(match.all_innings):
        score += f"Innings {count+1} {i.batting_team} {i.team_runs}/{i.team_wickets_count}\n"
    return score

def get_result_string(match):
    return match.result_text

def get_match_type_string(match):
    if match.innings_per_team == 1:
        return f"A {match.overs_limit} over game"
    else:
        return f"{match.innings_per_team} per team"

## Input helper methods
def read_int(prompt, min, max):
    while True:
        raw_input = input(prompt)
        try:
            value = int(raw_input)
        except ValueError:
            print(f"Please input integer in range {min} to {max}")
        else:
            if max >= value >= min:
                return value
            else:
                raise ValueError(f"Please input integer in range {min} to {max}")

def read_string(prompt):
    while True:
        response = input(prompt).strip()
        if response == None or response == "":
            raise ValueError("Invalid input")
        else:
            return response

def read_date(prompt):
    while True:
        date_raw = input(prompt + " DD/MM/YYYY: ").strip()
        try:
            match_date = convert_input_to_date_type(date_raw)
        except ValueError:
            print("Invalid date or format")
        else:
            if read_yes_no_answer(f'Date entered: {match_date.strftime("%d/%m/%Y")} correct?'):
                return match_date

def convert_input_to_date_type(input_date):
    try:
        d, m, y = input_date.split("/")
        return date(int(y), int(m), int(d))
    except :
        raise ValueError

def read_yes_no_answer(question):
    while True:
        answer = input(question + " y/n: ").strip().lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False

def read_delivery():
    innings = match_controller.current_innings
    print(subtitle("Add delivery"))
    print("d = dot ball, s = single, 2 = 2 runs, 4 = boundary four, 6 = boundary six, r = runs, \nnb = no ball, wd = wide, b = bye, lb = leg bye, wk = wicket")
    type = read_string("Option: ").strip().lower()
    match type:
        case "d":
            return Delivery()
        case "s":
            return Delivery(1)
        case "1":
            return Delivery(1)
        case "2":
            return Delivery(2)
        case "3":
            return Delivery(3)
        case "4":
            return Delivery(4, boundary=Boundary.FOUR)
        case "6":
            return Delivery(6, boundary=Boundary.SIX)
        case "r":
            runs = read_int("Runs: ", 1, 1000)
            return Delivery(int(runs))
        case "nb":
            runs = read_int("No Ball. Additional runs: ", 0, 1000)
            if runs > 0:
                if read_yes_no_answer("Runs scored from bat?"):
                    type = Runs_type.BAT
                else:
                    type = Runs_type.EXTRAS
            else:
                type = Runs_type.NONE
            return Delivery(runs, delivery_type=Delivery_type.NO_BALL, runs_type=type)
        case "wd":
            runs = read_int("Wide. Additional runs: ", 0, 1000)
            return Delivery(runs, delivery_type=Delivery_type.WIDE, runs_type=Runs_type.EXTRAS)
        case "b":
            runs = read_int("Byes: ", 1, 1000)
            return Delivery(runs, runs_type=Runs_type.BYE)
        case "lb":
            runs = read_int("Leg-Byes: ", 1, 1000)
            return Delivery(runs, runs_type=Runs_type.LEG_BYE)
        case "wk":
            wicket = read_wicket(innings.current_bowler, innings.current_striker, innings.current_nonstriker)
            delivery = Delivery(wicket=wicket)
            if wicket.type == Wicket_Type.RUN_OUT or wicket.type == Wicket_Type.OBSTRUCTING or wicket.type == Wicket_Type.CAUGHT:
                runs = read_int("Runs scored: ", 0, 1000)
                delivery.runs = runs
                if runs > 0:
                    if wicket.type == Wicket_Type.CAUGHT:
                        delivery.runs_type = Runs_type.BAT
                        delivery.delivery_type = Delivery_type.GOOD
                    else:
                        delivery.runs_type = read_runs_type()
                        if delivery.runs_type == Runs_type.BAT or delivery.runs_type == Runs_type.EXTRAS:
                            delivery.delivery_type = read_delivery_type()
            return delivery

def read_delivery_type():
    while True:
        type = input("Delivery type: g = good, nb = no ball, w = wide").strip().lower()
        match type:
            case "g":
                return Delivery_type.GOOD
            case "nb":
                return Delivery_type.NO_BALL
            case "w":
                return Delivery_type.WIDE
            case _:
                print("Invalid selection, try again...")

def read_runs_type():
    while True:
        type = input("Runs type: b = bat, e = extras, by = bye, lb = leg bye").strip().lower()
        match type:
            case "b":
                return Runs_type.BAT
            case "e":
                return Runs_type.EXTRAS
            case "by":
                return Runs_type.BYE
            case "lb":
                return Runs_type.LEG_BYE
            case _:
                print("Invalid selection, try again")      

def read_wicket(bowler, striker, nonstriker):
    while True:
        type = input("Select wicket type: \nb = bowled, c = caught, l = lbw, r = run out, s = stumped, \nhw = hit wicket, ht = hit twice, o = obstructing \n Selection: ").strip().lower()
        wicket = Wicket()
        match type:
            case "b":
                wicket.type = Wicket_Type.BOWLED
                break
            case "c":
                wicket.type = Wicket_Type.CAUGHT
                wicket.fielder = input("Who took the catch? ")
                break
            case "l":
                wicket.type = Wicket_Type.LBW
                break
            case "r":
                wicket.type = Wicket_Type.RUN_OUT
                out = read_int(f"Who was out? 1 = {striker}, 2 = {nonstriker} ", 1, 2)
                wicket.batter = striker if out == 1 else nonstriker
                wicket.fielder = input("Who fielded it? ").strip()
                wicket.assist = input("Who assisted? ").strip()
                return wicket
            case "s":
                wicket.type = Wicket_Type.STUMPED
                wicket.fielder = input("Wicket keeper name: ")
                break
            case "hw":
                wicket.type = Wicket_Type.HIT_WICKET
                break
            case "ht":
                wicket.type = Wicket_Type.HIT_TWICE
                wicket.batter = striker
                return wicket
            case "o":
                wicket.type = Wicket_Type.OBSTRUCTING
                out = read_int(f"Who was out? 1 = {striker.name}, 2 = {nonstriker.name} ", 1, 2)
                wicket.batter = striker if out == 1 else nonstriker
                return wicket
            case _:
                print(f"{type} is not a valid selection, try again")

    wicket.bowler = bowler
    wicket.batter = striker
    return wicket

if __name__ == "__main__":
    __main__()