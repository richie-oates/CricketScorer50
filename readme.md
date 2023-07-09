# CS50P Final Project:
## Requirements
- [x] Must be written in python
- [x] Must have main function in project.py
- [x] Must have at least three custom functions in project.py
- [x] Must have three test functions in test_project.py named test__custom_function
- [x] Additional classes and functions are permitted
- [x] Any pip installable libraries must be listed, one per line in a file called requirements.txt

## CRICKET SCORER
#### Video Demo:  https://www.youtube.com/watch?v=lGvARdqnyqY&ab_channel=RichardOates
#### Description:

### Purpose
The purpose of this application is to provide a means of recording the score for a cricket match. It records all the information for each delivery of the game, batters scores, bowlers statistics, details of wickets, and the final result of the match. It gives the user the option to view the full scoreboard and to save and load Matches to and from file in local memory

### Models and TDD
I decided to use Test Driven Development (TDD) to build up the model classes which would be used to represent the various aspects of a cricket game. 
In its simplest form, cricket is made up of a series of deliveries. So I began by writing tests to ensure the Delivery object held the data needed to represent the outcome of each delivery, e.g. runs scored, batter, bowler, no-balls etc. Within the class I performed data validation to ensure the correct type was used and certain invalid types and combinations raised errors.
Deliveries in the game come in a series of overs, and each team has a certain amount of overs for each innings. Next I carried on with the TDD process to create the Over and Innings classes, Wicket, Player and then finally Match. This provided me with a robust model to create a cricket Match, score the match, and then access certain statistics from the state of the match

### UI / project.py
I wanted to create an application that could be run using different user interfaces. For this version I decided to use a command line interface, but on future versions I may provide a desktop GUI or a Web based version. This UI provides options to create a new match or load a saved one. Once the match is loaded, the user may view the scorecard or start/continue scoring a match which is not already completed. Whilst scoring, the user is prompted to provide details for each delivery of the game, as well as info about players and wickets. The UI creates and updates the Match models via the MatchController class but use instances of the model classes to display the state of the match. I am considering adding further abstraction so that the UI gains independence from the model classes (time considerations are currently preventing me from doing this)

### MatchController
The MatchController class accesses the Match data via the MatchRepository and contains functions to modify the Match objects. After each change, the data is saved via the MatchRepository

### MatchRepository
The match repository provides a CRUD system to save, access, and modify the match data. In this case I decided to save to file a json string. This meant converting the model data into dictionaries by creating "to_dict" and "from_dict" methods in each of my model classes

### view folder
- scorecard:
    - takes a Match object and displays in a series of tables the current state of the match
    - Uses 'tabulate'
- display_helpers:
    - Methods to display text titles
    - Uses pyfiglet

### PIP packages
- pyfiglet - Used for menu titles.
- tabulate - Used for scoreboard.
- cowsay - Used for goodbye message when exiting application


## Backlog: Things I would like to implement in the future
- Alternative UI:
    - Desktop GUI
    - Browser/ web based

- Dedicated server for database

- User registration and log in

- Restricted user privelidges:
    - ie. only allocated members from a team can edit and save data
    - Other members can search and view

- Search matches by attributes:
    - date
    - team
    - player

- Addidtional repositories:
    - Players
    - Teams

- Statistics:
    - Team
    - Player

- League tables

- Edit data after saving for error correction
    - but after a certain time lock data so can no longer be edited

- Database

- Display all deliveries in over