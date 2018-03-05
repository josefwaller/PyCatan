from pycatan.game import Game
from board_renderer import BoardRenderer

g = Game()
br = BoardRenderer(g.board)
br.render()
