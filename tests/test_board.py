from pycatan.board import Board
from pycatan.game import Game
from pycatan.statuses import Statuses
from pycatan.card import ResCard
from pycatan.hex_type import HexType
from pycatan.hex import Hex

class TestBoard:

    def test_get_connected_hexes(self):
        board = Board(Game())
        test_cases = {
            (0, 0): [[0, 0]],
            (0, 1): [[0, 0]],
            (0, 2): [[0, 0], [0, 1]],
            (3, 4): [[2, 1], [2, 2], [3, 1]],
            (5, 0): [[4, 0]],
            (5, 1): [[4, 0]],
            (5, 2): [[4, 0], [4, 1]]
        }
        # Test that it returns the points connected properly
        for case, answers in test_cases.items():
            points = board.get_hexes_for_point(case[0], case[1])
            print(answers)
            for ans in answers:
                # Check it returned the correct point
                assert ans in points


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
