from pycatan.game import Game
from pycatan.building import Building
from pycatan.card import ResCard
from pycatan.statuses import Statuses
from pycatan.harbor import HarborType

class TestGame:

    def test_game_uses_three_players_by_default(self):
        game = Game()
        assert len(game.players) == 3

    def test_adding_starting_settlements(self):
        # Create game
        g = Game();
        # Make sure creating a starting settlement does not use any cards
        g.players[0].add_cards([
            ResCard.WOOD,
            ResCard.BRICK,
            ResCard.SHEEP,
            ResCard.WHEAT
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
            ResCard.WOOD,
            ResCard.BRICK,
            ResCard.SHEEP,
            ResCard.WHEAT
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
        g.players[0].add_cards([ResCard.WOOD] * 4)
        # Try to trade in for 1 wheat
        res = g.trade_to_bank(player=0, cards=[ResCard.WOOD] * 4, request=ResCard.WHEAT)
        assert res == Statuses.ALL_GOOD
        assert not g.players[0].has_cards([ResCard.WOOD])
        assert g.players[0].has_cards([ResCard.WHEAT])
        # Try to trade in cards the player doesn't have
        res = g.trade_to_bank(player=0, cards=[ResCard.BRICK] * 4, request=ResCard.ORE)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.ORE])
        # Try to trade in with less than 4 cards, but more than 0
        g.players[0].add_cards([ResCard.BRICK] * 3)
        res = g.trade_to_bank(player=0, cards=[ResCard.BRICK] * 4, request=ResCard.SHEEP)
        assert res == Statuses.ERR_CARDS
        assert g.players[0].has_cards([ResCard.BRICK] * 3)
        assert not g.players[0].has_cards([ResCard.SHEEP])

    def test_trade_in_cards_through_harbor(self):
        g = Game();
        # Add Settlement next to the harbor on the top
        res = g.add_settlement(0, g.board.points[0][2], is_starting=True)
        assert res == Statuses.ALL_GOOD
        # Make the harbor trade in ore for testing
        for h in g.board.harbors:
            if g.board.points[0][2] in h.get_points():
                h.type = HarborType.ORE
                print("found harbor lmao")
        g.players[0].add_cards([ResCard.ORE] * 2)
        # Try to use harbor
        res = g.trade_to_bank(player=0, cards=[ResCard.ORE] * 2, request=ResCard.WHEAT)
        assert res == Statuses.ALL_GOOD
        assert g.players[0].has_cards([ResCard.WHEAT])
        assert not g.players[0].has_cards([ResCard.ORE])
        # Try to trade in to a harbor that the player does not have access to
        g.players[0].add_cards([ResCard.BRICK] * 2)
        res = g.trade_to_bank(player=0, cards=[ResCard.BRICK] * 2, request=ResCard.SHEEP)
        assert res == Statuses.ERR_HARBOR
        assert g.players[0].has_cards([ResCard.BRICK] * 2)
        assert not g.players[0].has_cards([ResCard.SHEEP])
        # Try to trade without the proper cards
        assert not g.players[0].has_cards([ResCard.ORE])
        res = g.trade_to_bank(player=0, cards=[ResCard.ORE] * 2, request=ResCard.SHEEP)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.SHEEP])
        # Try to trade with more cards than the player has
        g.players[0].add_cards([ResCard.ORE])
        res = g.trade_to_bank(player=0, cards=[ResCard.ORE] * 2, request=ResCard.SHEEP)
        assert res == Statuses.ERR_CARDS
        assert not g.players[0].has_cards([ResCard.SHEEP])
        assert g.players[0].has_cards([ResCard.ORE])
