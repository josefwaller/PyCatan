from pycatan.game import Game
from pycatan.statuses import Statuses

class TestGame:

    def test_game_uses_three_players_by_default(self):
        game = Game()
        assert len(game.players) == 3

    def test_adding_starting_settlements(self):
        # Create game
        game = Game();
        # Test adding a starting settlement, i.e. no cards needed
        res = game.add_settlement(0, 0, 0, True)
        assert res == Statuses.ALL_GOOD
        # Test adding a settlement too close to another settlement
        res = game.add_settlement(1, 0, 1, True)
        assert res == Statuses.ERR_BLOCKED
        # Test adding a settlement the correct distance away
        res = game.add_settlement(2, 0, 2, True)
        assert res == Statuses.ALL_GOOD

    def test_adding_starting_roads(self):
        # Create game
        game = Game()
        # Add starting settlement
        game.add_settlement(0, 0, 0, True)
        # Try adding a road
        res = game.add_road(0, [0, 0], [0, 1], True)
        assert res == Statuses.ALL_GOOD
        # Try adding a disconnected road
        res = game.add_road(0, [1, 1], [1, 0], True)
        assert res == Statuses.ERR_ISOLATED
        # Try adding a road whose point's are not connected
        res = game.add_road(0, [0, 0], [5, 5], True)
        assert res == Statuses.ERR_NOT_CON
        # Try adding a road connected to another player's settlement
        res = game.add_road(1, [0, 0], [1, 1], True)
        assert res == Statuses.ERR_ISOLATED
