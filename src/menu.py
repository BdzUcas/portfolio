from gui import *
from movie_recommender import run_movie_searcher
from text_adventure import run_adventure
from maze_generator import run_maze_generator
from pet_sim import game_flow
games = {
    "Westville Sheriff": run_adventure,
    "Maze Generator": run_maze_generator,
    "Movie Recommender": run_movie_searcher,
    "Pet Simulator": game_flow.menu
}
game_descriptions = {
    "Westville Sheriff": ['### Westville Sheriff ###','A text based adventure game where you play as the sheriff of a wild west town.','Use text prompts to navigate westville, gain information, and bargain with citizens.','When making this project i learned about UX design, making the experience pleasant for the user','I also got my first taste of working on a large-scale project.','It was very challenging to make things intuitive. I didn\'t anticipate so many things being unintuitive for the user'],
    "Maze Generator": ['### Maze Generator ###','A simple program that generates a maze.','It uses recursive backtracking to make sure the maze is solvable from either end.','Close the window when you are done with your maze','When making it i learned how to do advanced data storage and logic','and how to make turtle draw efficiently.','It was difficult to figure out how to make a maze that was solvable every time.'],
    "Movie Recommender": ['### Movie Recommender ###','A program that lets you search through a list of movies','It accepts multiple conditions based on many prerequisites such as rating, title, or director.','When making this project i learned how to sort through and utilize data from files.','I also learned how to store conditions and search with them.','I challenged myself to make my functions very modulat in this project.','I have used them many times since.'],
    "Pet Simulator": ['### Pet Simulator ###','A game where you take care of pets.','Be careful, as everything you do costs time','Use text prompts to navigate your life as a pet owner and perform various actions such as shopping, working, and playing.','In this project i learned how to properly implement objects and classes','and how to store objects in files','It was challenging to implement proper choices off of a modular list','so i later turned this into a helper function i could use all the time']
}
def main_menu():
    display(['Welcome to my portfolio!','Once you are in the main menu, choose a project to get details.','There are four games to choose from.','Have fun!'],buttontext='continue',title_text='Portfolio')
    while True:
        game = menu(['Westville Sheriff','Maze Generator','Movie Recommender','Pet Simulator','Quit'],prompt='Choose a game',title_text='Portfolio Main Menu')
        if game == 'Quit':
            break
        if display(game_descriptions[game],buttontext='Play',alt_button_text='Menu'):
            games[game]()