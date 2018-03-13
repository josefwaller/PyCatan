from pycatan.game import Game
from pycatan.statuses import Statuses
from board_renderer import BoardRenderer
import blessings
import math

# Get an integer from standard input and return it
# If a non-integer value is entered, continue to prompt the user
def integer_input(str_prompt):
    while True:
        try:
            return int(input(str_prompt))
        except ValueError:
            print("Please enter a valid integer")
            continue

if __name__ == "__main__":
    terminal = blessings.Terminal()
    # Create a new game of Catan
    game = Game()
    # Set up board to render
    br = BoardRenderer(board=game.board, center=[math.floor(terminal.width / 2), math.floor(terminal.height / 2 - 1)])
    # Draw the board
    br.render()
    # Starting phase
    # Twice for each player
    for p in game.players + list(reversed(game.players)):
        # Render the board
        br.render()
        # Place a free settlement
        with terminal.location(0, terminal.height - 1):
            # Prompt the player for input
            print("Player %s, it is your turn" % p.num)
            while True:
                # Get the row
                row = integer_input("Enter the row you want to place the settlement: ")
                # Get the index
                index = integer_input("Enter the index you want to place your settlement: ")
                # Try to build the settlement
                res = game.add_settlement(player=p.num, r=row, i=index, is_starting=True)
                # If invalid, tell the player why and allow them to re-enter a position
                if res != Statuses.ALL_GOOD:
                    if res == Statuses.ERR_BLOCKED:
                        print("Another settlement is too close for you to build a settlement there!")
                    elif res == Statuses.ERR_BAD_POINT:
                        print("The point %s is not on the board!" % [row, index])
                    else:
                        # These are the only 2 errors that should run during the building phase, so something went terribly wrong
                        print("An internal error occured. res = %s." % res)
                    # Repeat the loop to allow the user to reenter the position
                    continue
                # Place a free road connected to that settlement
                points = game.board.points[row][index].connected_points
                # Render the board
                br.render()
                # Loop while road input is invalid
                while True:
                    with terminal.location(0, terminal.height - 1):
                        print("Please choose from one of the following points to build your road to:")
                        # Go through valid points
                        for i in range(len(points)):
                            # Print each point as an option
                            print("%s. %s" % (i, points[i].position))
                        # Prompt user to chose a point
                        choice = integer_input("Which point do you want to build your road to? ")
                        # Ensure choice is valid
                        if choice < 0 or choice > len(points) - 1:
                            print("Please choose a valid option")
                        else:
                            # Add the road
                            res = game.add_road(player=p.num, start=[row, index], end=points[choice].position, is_starting=True)
                            # If successful, break the loop and go to the next player
                            if res == Statuses.ALL_GOOD:
                                break
                # Break from outer loop, so that the next player is prompted:w
                break

    # While the game is not won
        # Roll the die
        # Hand out appropriate resources
        # Let this turn's player trade
        # Let this turn's player build

    # Announce winner
    pass
