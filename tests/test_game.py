from pycatan.game import Game
from pycatan.building import Building
from pycatan.card import ResCard
from pycatan.statuses import Statuses
from pycatan.harbor import HarborType
import random

class TestGame:

    def test_game_uses_three_players_by_default(self):
        game = Game()
        assert len(game.players) == 3
    def test_game_starts_with_variable_players(self):
        game = Game(num_of_players=5)
        assert len(game.players) == 5
    def test_adding_starting_settlements(self):
        # Create game
        g = Game();
        # Make sure creating a starting settlement does not use any cards
        g.players[0].add_cards([
            ResCard.Wood,
            ResCard.Brick,
            ResCard.Sheep,
            ResCard.Wheat
        ])
        # Test adding a starting settlement, i.e. no cards needed
        res = g.add_settlement(0, g.board.points[0][0], True)
        assert res == Statuses.ALL_GOOD
        assert g.board.points[0][0].building != None
        assert g.board.points[0][0].building.type == Building.BUILDING_SETTLEMENT
        assert g.board.points[0][0].building.point is g.board.points[0][0]
        assert len(g.players[0].cards) == 4
        # Test adding a settlement too close to another settlement
        res = g.add_settlement(1, g.board.points[0][1], True)
        assert res == Statuses.ERR_BLOCKED
        # Test adding a settlement the correct distance away
        res = g.add_settlement(2, g.board.points[0][2], True)
        assert res == Statuses.ALL_GOOD
    def test_adding_starting_roads(self):
        # Create game
        g = Game()
        # Add starting settlement
        g.add_settlement(0, g.board.points[0][0], True)
        # Try adding a road
        res = g.add_road(0, g.board.points[0][0], g.board.points[0][1], True)
        assert res == Statuses.ALL_GOOD
        res = g.add_road(0, g.board.points[1][1], g.board.points[0][0], True)
        assert res == Statuses.ALL_GOOD
        # Try adding a disconnected road
        res = g.add_road(0, g.board.points[2][0], g.board.points[2][1], True)
        assert res == Statuses.ERR_ISOLATED
        # Try adding a road whose point's are not connected
        res = g.add_road(0, g.board.points[0][0], g.board.points[5][5], True)
        assert res == Statuses.ERR_NOT_CON
        # Try adding a road connected to another player's settlement
        g.add_settlement(1, g.board.points[2][2], True)
        res = g.add_road(0, g.board.points[2][2], g.board.points[2][3], True)
        assert res == Statuses.ERR_ISOLATED
    # Test that player.add_settlement returns the proper value
    def test_add_settlement(self):
        g = Game()
        # Try to add a settlement without the cards
        g.add_settlement(0, g.board.points[0][0])
        # Add cards to build a settlement
        g.players[0].add_cards([
            ResCard.Wood,
            ResCard.Brick,
            ResCard.Sheep,
            ResCard.Wheat
        ])
        # Try adding an isolated settlement
        res = g.add_settlement(0, g.board.points[0][0])
        assert res == Statuses.ERR_ISOLATED
        assert g.board.points[0][0].building == None
        # Add starting settlement and two roads to ensure there is an available position
        assert g.add_settlement(0, g.board.points[0][2], True) == Statuses.ALL_GOOD
        assert g.add_road(0, g.board.points[0][2], g.board.points[0][1], True) == Statuses.ALL_GOOD
        assert g.add_road(0, g.board.points[0][0], g.board.points[0][1], True) == Statuses.ALL_GOOD
        res = g.add_settlement(0, g.board.points[0][0])
        assert res == Statuses.ALL_GOOD
        assert g.board.points[0][0].building != None
        assert g.board.points[0][0].building.type == Building.BUILDING_SETTLEMENT
    # Test trading in cards either directly through the bank
    def test_trade_in_cards_through_bank(self):
        g = Game()
        # Add 4 wood cards to player 0
        g.players[0].add_cards([ResCard.Wood] * 4)
        # Try to trade in for 1 wheat
        res = g.trade_to_bank(player=0, cards=[ResCard.Wood] * 4, request=ResCard.Wheat)
        assert res == Statuses.ALL_GOOD
        assert not g.players[0].has_cards([ResCard.Wood])
        assert g.players[0].has_cards([ResCard.Wheat])
        # Try to trade in cards the player doesn't have
        res = g.trade_to_bank(player=0, cards=[ResCard.Brick] * 4, request=ResCard.Ore)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.Ore])
        # Try to trade in with less than 4 cards, but more than 0
        g.players[0].add_cards([ResCard.Brick] * 3)
        res = g.trade_to_bank(player=0, cards=[ResCard.Brick] * 4, request=ResCard.Sheep)
        assert res == Statuses.ERR_CARDS
        assert g.players[0].has_cards([ResCard.Brick] * 3)
        assert not g.players[0].has_cards([ResCard.Sheep])
    def test_trade_in_cards_through_harbor(self):
        g = Game();
        # Add Settlement next to the harbor on the top
        res = g.add_settlement(0, g.board.points[0][2], is_starting=True)
        assert res == Statuses.ALL_GOOD
        # Make the harbor trade in ore for testing
        for h in g.board.harbors:
            if g.board.points[0][2] in h.get_points():
                h.type = HarborType.Ore
                print("found harbor lmao")
        g.players[0].add_cards([ResCard.Ore] * 2)
        # Try to use harbor
        res = g.trade_to_bank(player=0, cards=[ResCard.Ore] * 2, request=ResCard.Wheat)
        assert res == Statuses.ALL_GOOD
        assert g.players[0].has_cards([ResCard.Wheat])
        assert not g.players[0].has_cards([ResCard.Ore])
        # Try to trade in to a harbor that the player does not have access to
        g.players[0].add_cards([ResCard.Brick] * 2)
        res = g.trade_to_bank(player=0, cards=[ResCard.Brick] * 2, request=ResCard.Sheep)
        assert res == Statuses.ERR_HARBOR
        assert g.players[0].has_cards([ResCard.Brick] * 2)
        assert not g.players[0].has_cards([ResCard.Sheep])
        # Try to trade without the proper cards
        assert not g.players[0].has_cards([ResCard.Ore])
        res = g.trade_to_bank(player=0, cards=[ResCard.Ore] * 2, request=ResCard.Sheep)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.Sheep])
        # Try to trade with more cards than the player has
        g.players[0].add_cards([ResCard.Ore])
        res = g.trade_to_bank(player=0, cards=[ResCard.Ore] * 2, request=ResCard.Sheep)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.Sheep])
        assert g.players[0].has_cards([ResCard.Ore])
    def test_moving_robber(self):
        random.seed(1)
        g = Game()
        # Move the robber
        g.move_robber(g.board.tiles[0][0], None, None)
        assert g.board.robber is g.board.tiles[0][0]
        # Build a settlement at 1, 1
        g.add_settlement(player=0, point=g.board.points[1][1], is_starting=True)
        # Roll an 8
        g.add_yield_for_roll(8)
        # Ensure the player got nothing since the robber was there
        assert len(g.players[0].cards) == 0
        # Give the player a brick to steal
        g.players[0].add_cards([ResCard.Brick])
        # Move the robber to 1, 0 and steal the brick
        g.move_robber(g.board.tiles[1][0], 1, 0)
        # Make sure they stole the brick
        assert g.players[1].has_cards([ResCard.Brick])
