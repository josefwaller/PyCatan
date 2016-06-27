from catan_board import CatanBoard
from catan_player import CatanPlayer

import random

# errors
CATAN_ERR_CARDS = 0

class CatanGame:
	
	def __init__(self, num_of_players):
		
		# creates a board
		self.board = CatanBoard(self);
		
		self.players = []
		
		# creates players
		for i in range(num_of_players):
			self.players.append(CatanPlayer(num=i, game=self))
		
	def add_settlement(self, player, settle_r, settle_i):
		
		# checks the point on the board is empty
		if self.board.point_is_empty(r=settle_r, i=settle_i):
		
			# builds the settlement
			success = self.players[player].build_settlement(settle_r=settle_r, settle_i=settle_i)
			print(success)
			
	# builds a road going from point start to point end
	def add_road(self, player, start, end):
		
		print("Add Road is %s" % self.players[player].build_road(start=start, end=end))
			
	# gives players the proper cards for a given roll
	def add_yield_for_roll(self, roll):
	
		self.board.add_yield(roll)
		
	# simulates 2 dice rolling
	def get_roll(self):
		return round(random.random() * 6) + round(random.random() * 6)
		
# creates a new game for debugging
if __name__ == "__main__":

	# creates a new game with three players
	c = CatanGame(num_of_players=3)
	
	# gives the first player settlement cards
	(c.players[0]).add_card(CatanPlayer.CARD_WOOD)
	(c.players[0]).add_card(CatanPlayer.CARD_BRICK)
	(c.players[0]).add_card(CatanPlayer.CARD_WHEAT)
	(c.players[0]).add_card(CatanPlayer.CARD_SHEEP)
	
	# gets the first player to build a settlement
	c.add_settlement(player=0, settle_i=0, settle_r=5)
	
	# gets the yield for the new settlement
	c.add_yield_for_roll(5)
	
	# adds cards for a road
	(c.players[1]).add_card(CatanPlayer.CARD_WOOD)
	(c.players[1]).add_card(CatanPlayer.CARD_BRICK)
	
	# builds a road
	c.add_road(player=1, start=[1, 2], end=[2, 3])
	