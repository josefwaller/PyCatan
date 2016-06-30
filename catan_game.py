from catan_board import CatanBoard
from catan_player import CatanPlayer
from catan_statuses import CatanStatuses

import random

class CatanGame:
	
	def __init__(self, num_of_players):
		
		# creates a board
		self.board = CatanBoard(self);
		
		self.players = []
		
		# creates players
		for i in range(num_of_players):
			self.players.append(CatanPlayer(num=i, game=self))
		
	def add_settlement(self, player, settle_r, settle_i):
	
		# builds the settlement
		return self.players[player].build_settlement(settle_r=settle_r, settle_i=settle_i)
			
	# builds a road going from point start to point end
	def add_road(self, player, start, end):
		
		return self.players[player].build_road(start=start, end=end)
			
	# gives players the proper cards for a given roll
	def add_yield_for_roll(self, roll):
	
		self.board.add_yield(roll)
		
	def trade(self, player_one, player_two, cards_one, cards_two):
	
		# check if they players have the cards they are trading
		# Needs to do this before deleting because one might have the cards while the other does not
		if not self.players[player_one].has_cards(cards_one):
			return CatanStatuses.ERR_CARDS
			
		elif not self.players[player_two].has_cards(cards_two):
			return CatanStatuses.ERR_CARDS
			
		else:
			# removes the cards
			self.players[player_one].remove_cards(cards_one)
			self.players[player_two].remove_cards(cards_two)
			
			# add the new cards	
			self.players[player_one].add_cards(cards_two)
			self.players[player_two].add_cards(cards_one)
			
			return CatanStatuses.ALL_GOOD
	
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
	print("Settlement status is: %s" % (c.add_settlement(player=0, settle_r=2, settle_i=2)))
	
	# gets the yield for the new settlement
	c.add_yield_for_roll(5)
	
	# adds cards for a road
	(c.players[0]).add_card(CatanPlayer.CARD_WOOD)
	(c.players[0]).add_card(CatanPlayer.CARD_BRICK)
	
	# builds a road
	c.add_road(player=0, start=[2, 2], end=[2, 3])
	
	# gives the second player cards to build a settlement
	(c.players[1]).add_card(CatanPlayer.CARD_WOOD)
	(c.players[1]).add_card(CatanPlayer.CARD_BRICK)
	(c.players[1]).add_card(CatanPlayer.CARD_WHEAT)
	(c.players[1]).add_card(CatanPlayer.CARD_SHEEP)
	
	# the second player tries to build a settlement on the first player's
	stat = c.add_settlement(player=1, settle_r=2, settle_i=2)
	if stat == CatanStatuses.ERR_BLOCKED:
		print("Cannot build a settlement on top of another")
		
		# builds one 1 away
		if c.add_settlement(player=1, settle_r=2, settle_i=1) == CatanStatuses.ERR_BLOCKED:
			print("Cannot build a settlement one away, sideways")
			
			# builds one away, down
			if c.add_settlement(player=1, settle_r=3, settle_i=2) == CatanStatuses.ERR_BLOCKED:
				print("Cannot build a settlement one away, striaght down")
				
				# builds 2 away
				if c.add_settlement(player=1, settle_r=2, settle_i=0) == CatanStatuses.ALL_GOOD:
					print("All Good")
				
	else:
		print("Error with building Settlement on top of another: %s" % stat)
		
	# gives player 1 a sheep
	(c.players[0]).add_card(CatanPlayer.CARD_SHEEP)
	
	# gives player 2 a wood
	(c.players[1]).add_card(CatanPlayer.CARD_WOOD)
	
	# prints the cards
	print("Player 1 Cards:")
	CatanPlayer.print_cards(c.players[0].cards)
	print("Player 2 Cards")
	CatanPlayer.print_cards(c.players[1].cards)
	
	# trades sheep for wood
	trade_result = c.trade(player_one=0, player_two=1, cards_one=[CatanPlayer.CARD_SHEEP], cards_two=[CatanPlayer.CARD_WOOD])
	
	if trade_result == CatanStatuses.ALL_GOOD:
		print("Successfully traded")
		
	else:
		print("Trade Failed with error %s" % trade_result)
		
	print("Player 1 Cards:")
	CatanPlayer.print_cards(c.players[0].cards)
	print("Player 2 Cards")
	CatanPlayer.print_cards(c.players[1].cards)