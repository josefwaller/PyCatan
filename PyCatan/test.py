from game import Game
from hex import Hex

# imports all the different types of cards (Resource and development)
from cards import Cards

# imports the board for static methods
from board import Board

# imports the different Statuses
from statuses import Statuses

# is used
import math

# tests the Game module
class Tester:

    def __init__(self):
        self.game = None

    def test_all(self):

        print("Testing module components:")
        print("")

        result = {
            "Initializing game": self.init_game(),
            "Building a settlement": self.test_settlement(),
            "Building a road": self.test_road(),
            "Getting longest road": self.test_longest_road(),
            "Using a road building card": self.test_road_building(),
            "Using a Knight card": self.test_knight(),
            "Getting largest army": self.test_largest_army(),
            "Victory Points": self.test_victory_points(),
            "Victory": self.test_victory(),
            "Upgrading to a City": self.test_city(),
            "Monopoly card": self.test_monopoly(),
            "Year of Plenty card": self.test_yop(),
            "Victory Point card": self.test_VP_card(),
            "Using the starting board": self.test_starting_board()
        }

        for r in result:

            status = ""
            if result[r] == True:
                status = "Successful"
            else:
                status = "Failure with code %s" % result[r]

            to_print = r + " "

            for i in range(48 - len(r)):
                to_print += "-"

            to_print += " " +status
            print(to_print)

    # tests creating a game
    def init_game(self):

        self.game = Game()

        return True

    # tests building a settlement at a location
    def test_settlement(self):

        game = Game()

        # tests just building a starting settlement
        res = game.add_settlement(player=0, r=0, i=0, is_starting=True)

        if res != Statuses.ALL_GOOD:
            return res

        # adds two roads leading away from the settlement
        game.players[0].add_cards([
            Cards.CARD_BRICK,
            Cards.CARD_BRICK,
            Cards.CARD_WOOD,
            Cards.CARD_WOOD
        ])

        for i in range(1, 3):

            stat = game.add_road(player=0, start=[0, i - 1], end=[0, i])

            if stat != Statuses.ALL_GOOD:
                return stat

        # tries to build an isolated settlement
        game.players[0].add_cards([
            Cards.CARD_BRICK,
            Cards.CARD_SHEEP,
            Cards.CARD_WOOD,
            Cards.CARD_WHEAT
        ])
        stat = game.add_settlement(player=0, r=0, i=3)

        if stat != Statuses.ERR_ISOLATED:
            return Statuses.ERR_TEST

        # builds a connected settlement
        stat = game.add_settlement(player=0, r=0, i=2)
        if stat != Statuses.ALL_GOOD:
            return stat

        return True

    # tests upgrading a settlement to a city and getting two of each resource
    def test_city(self):

        # creates a new game
        game = Game()

        # adds a settlement
        stat = game.add_settlement(player=0, r=0, i=0, is_starting=True)
        if stat != Statuses.ALL_GOOD:
            return stat

        # upgrades the settlement to a city
        game.players[0].add_cards([
            Cards.CARD_WHEAT,
            Cards.CARD_WHEAT,
            Cards.CARD_ORE,
            Cards.CARD_ORE,
            Cards.CARD_ORE
        ])
        stat = game.add_city(r=0, i=0, player=0)

        if stat != Statuses.ALL_GOOD:
            return stat

        # checks that the player gets 2 of each resource

        # gets the type of card the player will get
        card_type = Board.get_card_from_hex(game.board.hexes[0][0])
        hex_num = game.board.hex_nums[0][0]

        game.add_yield_for_roll(hex_num)

        if game.players[0].cards != [card_type, card_type]:
            return Statuses.ERR_TEST

        return True

    # tests building a road using resource cards
    def test_road(self):

        game = Game()

        game.add_settlement(player=0, r=0, i=0, is_starting=True)

        game.players[0].add_cards([
            Cards.CARD_WOOD,
            Cards.CARD_BRICK
        ])

        result = game.add_road(player=0, start=[0, 0], end=[0, 1])

        if result == Statuses.ALL_GOOD:
            return True

        else:
            return result

    # tests that longest road works as intended
    def test_longest_road(self):

        game = Game()

        # gives player 0 a settlement
        status = game.add_settlement(player=0, r=3, i=0, is_starting=True)

        if status != Statuses.ALL_GOOD:
            return status

        # gives player 0 a six long road segment
        for i in range(6):
            game.players[0].add_cards([
                Cards.CARD_WOOD,
                Cards.CARD_BRICK
            ])

            status = game.add_road(player=0, start=[3, i], end=[3, i + 1])

            if status != Statuses.ALL_GOOD:
                return status

        # prints player 0's longest road
        if game.players[0].longest_road_length != 6:
            return Statuses.ERR_TEST

        # prints the longest road owner
        if game.longest_road_owner != 0:
            return Statuses.ERR_TEST

        # checks player 0 got victory points
        # one from the settlement, two from longest road
        if not game.players[0].get_VP() == 3:
            return Statuses.ERR_TEST

        # gives player 1 a settlement
        stat = game.add_settlement(player=1, r=4, i=2, is_starting=True)

        if stat != Statuses.ALL_GOOD:
            return stat

        # gives player 1 a 10 long looping road segment
        points = []
        for count in range(10):
            game.players[1].add_cards([
                Cards.CARD_WOOD,
                Cards.CARD_BRICK
            ])

            r = math.floor(count / 5) + 4

            i = int(5 - math.fabs(count - 4))

            points.append([r, i])

        for index in range(len(points)):

            end_index = (index + 1) % len(points)
            status = game.add_road(player=1, start=points[index], end=points[end_index])

            if status != Statuses.ALL_GOOD:
                return status

        if game.longest_road_owner != 1:
            return Statuses.ERR_TEST

        # checks victory points are correctly given out
        if not game.players[0].get_VP() == 1:
            return Statuses.ERR_TEST

        if not game.players[1].get_VP() == 3:
            return Statuses.ERR_TEST

        return True

    # tests using a road building card
    def test_road_building(self):

        game = Game()

        game.add_settlement(player=0, r=0, i=1, is_starting=True)

        game.players[0].add_dev_card(Cards.DEV_ROAD)

        result = game.use_dev_card(player=0, card=Cards.DEV_ROAD, args={
            "road_one": {
                "start": [0, 2],
                "end": [0, 3]
            },
            "road_two": {
                "start": [0, 1],
                "end": [0, 2]
            }
        })

        if result != Statuses.ALL_GOOD:
            return result

        return True


    # tests using a knight card
    def test_knight(self):

        game = Game()

        # gives the player a knight card
        game.players[1].add_dev_card(Cards.DEV_KNIGHT)

        # makes sure player 0 only has a wood card and player 2 has no resource cards
        game.players[0].cards = [Cards.CARD_WOOD]
        game.players[1].cards = []

        # makes sure player 0 has a settlement on the target hex
        stat = game.add_settlement(r=0, i=0, player=0, is_starting=True)

        if not stat == Statuses.ALL_GOOD:
            return stat

        # uses the knight card
        # move the robber to robber_pos
        # takes a cad from player 0
        result = game.use_dev_card(player=1, card=Cards.DEV_KNIGHT, args={
            "robber_pos": [0, 0],
            "victim": 0
        })

        if result != Statuses.ALL_GOOD:
            return result

        if game.players[0].cards == []:
            if game.players[1].cards == [Cards.CARD_WOOD]:
                return True

        return Statuses.ERR_TEST

    # tests getting the largest army
    def test_largest_army(self):

        game = Game()

        # gives player 0 three knight cards
        for i in range(3):
            game.players[0].add_dev_card(Cards.DEV_KNIGHT)

            # plays it
            stat = game.use_dev_card(player=0, card=Cards.DEV_KNIGHT, args={
                "robber_pos": [0, i],
                "victim": None
            })

            if stat != Statuses.ALL_GOOD:
                return stat

        # checks if player 0 now has largest army
        if not game.largest_army == 0:
            return Statuses.ERR_TEST

        # gives player 2 three knight cards too
        for i in range(3):
            game.players[2].add_dev_card(Cards.DEV_KNIGHT)

            # plays it
            game.use_dev_card(player=2, card=Cards.DEV_KNIGHT, args={
                "robber_pos": [0, i],
                "victim": None
            })

        # checks that 0 still has the largest army
        if not game.largest_army == 0:
            return Statuses.ERR_TEST

        # gives player 2 another knight card
        game.players[2].add_dev_card(Cards.DEV_KNIGHT)

        # plays it
        game.use_dev_card(player=2, card=Cards.DEV_KNIGHT, args={
            "robber_pos": [0, 0],
            "victim": None
        })

        # checks player 2 now has the knight card
        if not game.largest_army == 2:
            return Statuses.ERR_TEST

        # checks player 2 gained 2 victory points
        if not game.players[2].get_VP() == 2:
            return Statuses.ERR_TEST

        return True

    # tests that victory points are given each time a settlement is built
    def test_victory_points(self):

        # creates a new game
        game = Game()

        # makes sure the players has 0 VP
        if not game.players[0].get_VP() == 0:
            return Statuses.ERR_TEST

        # adds a settlement
        game.add_settlement(player=0, r=1, i=2, is_starting=True)

        # checks the player gained a victory point for it
        if not game.players[0].get_VP() == 1:
            return Statuses.ERR_TEST

        # upgrades the settlement to a city
        game.players[0].add_cards([
            Cards.CARD_WHEAT,
            Cards.CARD_WHEAT,
            Cards.CARD_ORE,
            Cards.CARD_ORE,
            Cards.CARD_ORE
        ])

        game.add_city(r=1, i=2, player=0)

        if not game.players[0].get_VP() == 2:
            return Statuses.ERR_TEST

        return True

    # tests winning after gaining 10 victory points
    def test_victory(self):

        game = Game()

        # gives player 0 ten settlements

        for i in range(5):

            # builds two settlements
            stat = game.add_settlement(player=0, r=2, i=2 * i, is_starting=True)

            if stat != Statuses.ALL_GOOD:
                return stat

            stat = game.add_settlement(player=0, r=3, i=2 * i + 1, is_starting=True)

            if stat != Statuses.ALL_GOOD:
                return stat

        if not game.has_ended:
            return Statuses.ERR_TEST

        if not game.winner == 0:
            return Statuses.ERR_TEST

        return True

    # tests the monopoly developement card
    def test_monopoly(self):

        game = Game()

        # gives player 0 a YOP card
        game.players[0].add_dev_card(Cards.DEV_MONOPOLY)

        # gives players 1 and 2 some cards
        game.players[1].add_cards([
            Cards.CARD_BRICK,
            Cards.CARD_BRICK,
            Cards.CARD_BRICK,
            Cards.CARD_WOOD,
        ])

        game.players[2].add_cards([
            Cards.CARD_BRICK,
            Cards.CARD_WHEAT,
            Cards.CARD_WHEAT,
            Cards.CARD_ORE,
            Cards.CARD_ORE,
            Cards.CARD_ORE,
        ])

        # uses the dev card
        game.use_dev_card(player=0, card=Cards.DEV_MONOPOLY, args={
            "card_type": Cards.CARD_BRICK
        })

        # makes sure player 0 got a bunch of brick
        if not game.players[0].cards == [Cards.CARD_BRICK] * 4:
            return Statuses.ERR_TEST


        # makes sure players 1 and 2 lost their cards
        if not game.players[1].cards == [Cards.CARD_WOOD]:
            return Statuses.ERR_TEST

        if not game.players[2].cards == [
            Cards.CARD_WHEAT,
            Cards.CARD_WHEAT,
            Cards.CARD_ORE,
            Cards.CARD_ORE,
            Cards.CARD_ORE
        ]:
            return Statuses.ERR_TEST

        return True

    # tests the year of plenty developement card
    def test_yop(self):

        # creates a new game
        game = Game()

        # gives player 0 a yop card
        game.players[0].add_dev_card(Cards.DEV_YOP)

        # player one uses it to get two brick
        stat = game.use_dev_card(player=0, card=Cards.DEV_YOP, args={
            "card_one": Cards.CARD_BRICK,
            "card_two": Cards.CARD_BRICK
        })
        if stat != Statuses.ALL_GOOD:
            return stat

        # checks it worked
        if not game.players[0].cards == [Cards.CARD_BRICK] * 2:
            return Statuses.ERR_TEST

        # gives player 2 a yop card
        game.players[2].add_dev_card(Cards.DEV_YOP)

        # uses it to get one wood and one brick
        stat = game.use_dev_card(player=2, card=Cards.DEV_YOP, args={
            "card_one": Cards.CARD_BRICK,
            "card_two": Cards.CARD_WOOD
        })
        if stat != Statuses.ALL_GOOD:
            return stat

        # checks it worked
        if not (game.players[2].cards.count(Cards.CARD_BRICK) == 1
        and game.players[2].cards.count(Cards.CARD_WOOD) == 1):
            return Statuses.ERR_TEST

        return True

    # tests gaining VP from developement cards
    def test_VP_card(self):

        # creates a new game
        game = Game()

        # gives player 0 a VP dev card
        game.players[0].add_dev_card(Cards.DEV_VP)

        # checks it doesn't show up when getting VPs
        if not game.players[0].get_VP() == 0:
            return Statuses.ERR_TEST

        # checks it does show up if explicitly told to
        if not game.players[0].get_VP(include_dev=True) == 1:
            return Statuses.ERR_TEST

        # checks it works with multiple dev cards
        game.players[0].add_dev_card(Cards.DEV_VP)

        if not game.players[0].get_VP(include_dev=True) == 2:
            return Statuses.ERR_TEST

        return True

    # tests starting a game with the beginner's board
    def test_starting_board(self):

        # makes sure it doesn't crash
        game = Game(starting_board=True)

        # makes sure some hexes are in the right place
        if not game.board.hexes[0][0] == Hex.FOREST:
            return Statuses.ERR_TEST

        elif not game.board.hexes[4][2] == Hex.FOREST:
            return Statuses.ERR_TEST

        elif not game.board.hexes[2][2] == Hex.FIELDS:
            return Statuses.ERR_TEST

        return True

if __name__ == "__main__":
    tester = Tester()
    tester.test_all()
