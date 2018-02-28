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

    def test_get_outside_points(self):
        # Get outside points
        outside_points = DefaultBoard.get_outside_points()
        # Check the points exist
        cases = {
            (0, 0): True,
            (1, 2): False,
            (4, 0): True,
            (5, 3): True,
            (3, 2): False
        }
        for case in cases:
            ans = cases[case]
            assert (list(case) in outside_points) == ans
        # Check the points are in the right order
        # Each value in this dict is the point that should be directly after the key
        order_cases = {
            (0, 0): (0, 1),
            (0, 6): (1, 7),
            (2, 10): (3, 10),
            (5, 3): (5, 2),
            (2, 1): (1, 0),
            (1, 0): (1, 1)
        }
        for case in order_cases:
            ans = order_cases[case]
            assert outside_points.index(list(case)) + 1 == outside_points.index(list(ans))

    def test_harbors_are_placed_correctly(self):
        # Create board
        board = Game().board
        # Test that the harbors are on these spots
        cases = [
            (0, 2),
            (2, 9),
            (3, 0),
            (5, 2)
        ]
        # Flatten all harbor positions
        harbor_positions = list(sum(map(lambda x: [x.point_one, x.point_two], board.harbors), []))
        for case in cases:
            assert list(case) in harbor_positions

    def test_harbors_always_have_connected_points(self):
        # Create board
        board = Game().board
        # For every hrbor, check that the two points are connected
        for harbor in board.harbors:
            assert harbor.point_two in board.get_connected_points(harbor.point_one[0], harbor.point_one[1])
