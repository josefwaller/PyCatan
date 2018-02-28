from pycatan.game import Game
from pycatan.building import Building
from pycatan.card import ResCard
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
        # Try creating a settlement on a point that does not exist
        res = g.add_settlement(0, 100, 0, True)
        assert res == Statuses.ERR_BAD_POINT
        # Make sure creating a settlement does not use any cards
        g.players[0].add_cards([
            ResCard.WOOD,
            ResCard.BRICK,
            ResCard.SHEEP,
            ResCard.WHEAT
        ])
        res = g.add_settlement(0, 0, 0, True)
        assert res == Statuses.ALL_GOOD
        assert g.board.points[0][0].building != None
        assert g.board.points[0][0].building.type == Building.BUILDING_SETTLEMENT
        assert len(g.players[0].cards) == 4

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
 
    # Test that player.add_settlement returns the proper value
    def test_add_settlement(self):
        g = Game()
        # Try to add a settlement without the cards
        g.add_settlement(0, 0, 0)
        # Add cards to build a settlement
        g.players[0].add_cards([
            ResCard.WOOD,
            ResCard.BRICK,
            ResCard.SHEEP,
            ResCard.WHEAT
        ])
        # Try adding an isolated settlement
        res = g.add_settlement(0, 0, 0)
        assert res == Statuses.ERR_ISOLATED
        assert g.board.points[0][0].building == None
        # Try adding a settlement at a point that is not on the board
        res = g.add_settlement(0, 500, 0)
        assert res == Statuses.ERR_BAD_POINT
        # Add starting settlement and two roads to ensure there is an available position
        g.add_settlement(0, 0, 2, True)
        g.add_road(0, [0, 2], [0, 1], True)
        g.add_road(0, [0, 0], [0, 1], True)
        res = g.add_settlement(0, 0, 0)
        assert res == Statuses.ALL_GOOD
        assert g.board.points[0][0].building != None
        assert g.board.points[0][0].building.type == Building.BUILDING_SETTLEMENT

