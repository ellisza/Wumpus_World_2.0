from cave import Cave
from room import Room
from agent import Agent

PRINT_GAME_OUTPUT = True        # Change to False if you don't want the textual representation of the game to display
NUM_GAMES_TO_PLAY = 1000        # I had my program simulate 1000 games and ouput the statistical results

GAMES = []

def run_game():
    c = Cave()
    c.setup()
    a = Agent(c, PRINT_GAME_OUTPUT)
    a.run_agent()
    result = [a.dead, a.score]
    global GAMES
    GAMES.append(result)


def run_simulation():
    for i in range(NUM_GAMES_TO_PLAY):
        run_game()


def display_result():
    num_wins = 0
    total_win_scores = 0
    total_lose_scores = 0
    total_scores = 0
    num_losses = 0
    num_games = len(GAMES)
    for entry in GAMES:
        if entry[0] == True: # Means it's a loss
            num_losses = num_losses + 1
            total_lose_scores = total_lose_scores + entry[1]
        else:
            num_wins = num_wins + 1
            total_win_scores = total_win_scores + entry[1]
        total_scores = total_scores + entry[1]
    print("\n\n\n")
    print("RESULTS:")
    print("TOTAL # OF GAMES RAN: " + str(num_games))
    print("NUMBER OF WINS: " + str(num_wins))
    print("NUMBER OF LOSSES: " + str(num_losses))
    print("AVERAGE WIN SCORE: " + str(total_win_scores/num_wins))
    print("AVERAGE LOSE SCORE: " + str(total_lose_scores / num_losses))
    print("AVERAGE SCORE: " + str(total_scores / num_games))


run_simulation()
display_result()

