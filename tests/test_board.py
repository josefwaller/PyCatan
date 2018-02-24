from pycatan.board import Board
from pycatan.game import Game
from pycatan.statuses import Statuses
from pycatan.card import ResCard
from pycatan.hex_type import HexType
from pycatan.hex import Hex

class TestBoard:

    def test_get_connected_hexes(self):
        board = Board(Game())
        # Test that it returns the points connected properly
        points = board.get_hexes_for_point(1, 2)
        assert [0, 0] in points
        assert [1, 0] in points
        assert [1, 1] in points


    def test_get_connected_points(self):
        board = Board(Game())
        # test that it returns the right points
        points = board.get_connected_points(1, 1)
        assert [0, 0] in points
        assert [1, 0] in points
        assert [1, 2] in points

    def test_card_to_hex_conversion(self):
        # Check that the board switches between hex types and the corresponding card properly
        assert Board.get_card_from_hex(HexType.FOREST), ResCard.WOOD

    def test_give_proper_yield(self):
        game = Game()
        board = game.board
        # set hex to test
        board.hexes[0][0] = Hex(HexType.FOREST, 8, [])
        # add settlement
        game.add_settlement(0, 0, 0, True)
        # give the roll
        board.add_yield(8)
        # check the board gave the cards correctly
        assert game.players[0].has_cards([ResCard.WOOD])
