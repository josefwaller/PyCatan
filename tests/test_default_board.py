from pycatan.game import Game
from pycatan.default_board import DefaultBoard

class TestDefaultBoard:
    def test_get_connected_hexes(self):
        board = Game().board
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
            points = DefaultBoard.get_hex_indexes_for_point(case[0], case[1])
            for ans in answers:
                # Check it returned the correct point
                assert ans in points

    def test_points_have_reference_to_hexes(self):
        # Get board
        b = Game().board
        # Test cases
        # Keys are the coordinates of the points, whereas values
        # are the coordinates of the hexes surronding that point
        # 
        cases = {
            (0, 0): [(0, 0)],
            (1, 2): [(0, 0), (1, 0), (1, 1)],
            (2, 0): [(2, 0)],
            (5, 2): [(4, 0), (4, 1)]
        }
        # Check each point has references to the hexes around it
        for key in cases:
            point = b.points[key[0]][key[1]]
            answers = cases[key]
            for ans in answers:
                hex = b.hexes[ans[0]][ans[1]]
                assert hex in point.hexes

    def test_hexes_have_references_to_points(self):
        # Get board
        b = Game().board
        # Test cases
        cases = {
            (0, 0): [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 1),
                (1, 2),
                (1, 3)
            ],
            (2, 3): [
                (2, 6),
                (2, 7),
                (2, 8),
                (3, 6),
                (3, 7),
                (3, 8)
            ],
            (4, 2): [
                (4, 5),
                (4, 6),
                (4, 7),
                (5, 4),
                (5, 5),
                (5, 6)
            ]
        }
        for key in cases:
            hex = b.hexes[key[0]][key[1]]
            answers = cases[key]
            for ans in answers:
                point = b.points[ans[0]][ans[1]]
                assert point in hex.points

