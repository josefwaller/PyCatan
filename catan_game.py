from catan_board import CatanBoard
from catan_player import CatanPlayer

import random

# errors
CATAN_ERR_CARDS = 0

class CatanGame:
	
	def __init__(self, num_of_players):
		
		# creates a board
		self.board = CatanBoard();
		
		self.players = []
		
		# creates players
		for i in range(num_of_players):
			self.players.append(CatanPlayer(num=i, game=self))
		
	def add_settlement(self, player_num, settle_r, settle_i):
		
		# checks the point on the board is empty
		if self.board.point_is_empty(r=settle_r, i=settle_i):
		
			# builds the settlement
			success = self.players[player_num].build_settlement(settle_r=settle_r, settle_i=settle_i)
			print(success)
			
	def add_yield_for_roll(self, roll):
	
		self.board.add_yield(roll)
		pass
		
	def get_roll(self):
		return round(random.random() * 6 + random.random() * 6)
		
# creates a new game for debugging
if __name__ == "__main__":

	# creates a new game with three players
	c = CatanGame(num_of_players=3)
	
	# gives the first player settlement cards
	(c.players[0]).add_card(0)
	(c.players[0]).add_card(1)
	(c.players[0]).add_card(3)
	(c.players[0]).add_card(4)
	
	# gets the first player to build a settlement
	c.add_settlement(player_num=0, settle_i=6, settle_r=5)
	
	c.add_yield_for_roll(5)
	