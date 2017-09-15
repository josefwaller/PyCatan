from pycatan.game import Game

class TestGame:

    def test_game_uses_three_players_by_default(self):
        game = Game()
        assert len(game.players) == 3
