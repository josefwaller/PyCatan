from pycatan.board import Board
from pycatan.game import Game
from pycatan.statuses import Statuses

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
