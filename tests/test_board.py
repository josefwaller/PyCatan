from pycatan.board import Board
from pycatan.game import Game
from pycatan.statuses import Statuses
from pycatan.card import ResCard
from pycatan.hex_type import HexType
from pycatan.hex import Hex

import random

class TestBoard:
    def test_card_to_hex_conversion(self):
        # Check that the board switches between hex types and the corresponding card properly
        assert Board.get_card_from_hex(HexType.FOREST), ResCard.WOOD
    def test_give_proper_yield(self):
        # Set seeed to ensure the board is the same as the testcase
        random.seed(1)
        # Create new game and get the board
        game = Game()
        board = game.board
        # Make sure robber is not on the top-left hex
        board.robber = [1, 1]
        # add settlement
        game.add_settlement(0, game.board.points[0][0], True)
        # give the roll
        board.add_yield(8)
        # check the board gave the cards correctly
        assert game.players[0].has_cards([ResCard.BRICK])
    def test_robber_prevents_yield(self):
        random.seed(1)
        game = Game()
        board = game.board
        # Move robber to top-left corner
        board.robber = [0, 0]
        # Add settlement
        game.add_settlement(0, game.board.points[0][0], True)
        # Roll an 8
        board.add_yield(8)
        # Ensure the robber prevented the player from getting the card
        assert not game.players[0].has_cards([ResCard.BRICK])

