from .catan_board import CatanBoard
from .catan_player import CatanPlayer
from .catan_statuses import CatanStatuses
from .catan_cards import CatanCards
from .catan_building import CatanBuilding

import random
import math

class CatanGame:
	
	# initializes the Catan game
	def __init__(self, num_of_players=3, on_win=None, starting_board=False):
		
		
		# creates a board
		self.board = CatanBoard(game=self, starting_board=starting_board);
		
		# creates players
		self.players = []
		for i in range(num_of_players):
			self.players.append(CatanPlayer(num=i, game=self))
		
		self.on_win = on_win
		
		# creates a new Developement deck
		self.dev_deck = []
		for i in range(14):
			
			if i < 2:
				self.dev_deck.append(CatanCards.DEV_ROAD)
				self.dev_deck.append(CatanCards.DEV_MONOPOLY)
				self.dev_deck.append(CatanCards.DEV_YOP)
				
			if i < 5:
				self.dev_deck.append(CatanCards.DEV_VP)
				
			self.dev_deck.append(CatanCards.DEV_KNIGHT)
			
		# random.shuffle(self.dev_deck)
	
		# the longest road owner and largest army owner
		self.longest_road_owner = None
		self.largest_army = None
		
		# whether the game has finished or not
		self.has_ended = False
	
	# creates a new settlement belong to the player at the coodinates
	def add_settlement(self, player, r, i, is_starting=False):
	
		# builds the settlement
		status = self.players[player].build_settlement(settle_r=r, settle_i=i, is_starting=is_starting)
			
		if status == CatanStatuses.ALL_GOOD:
			
			# checks if the player won
			if self.players[player].get_VP() >= 10:
				
				self.has_ended = True
				self.winner = player
		
		return status
			
	# builds a road going from point start to point end
	def add_road(self, player, start, end):
		
		# builds the road
		stat = self.players[player].build_road(start=start, end=end)
		
		# checks for a new longest road segment
		self.set_longest_road()
		
		# returns the status
		return stat
			
	# builds a new developement cards for the player
	def build_dev(self, player):
		
		# makes sure there is still at least one development card left
		if len(self.dev_deck) < 1:
			return CatanStatuses.ERR_DECK
			
		# makes sure the player has the right cards
		needed_cards = [
			CatanCards.CARD_WHEAT,
			CatanCards.CARD_ORE,
			CatanCards.CARD_SHEEP
		]
		if not self.players[player].has_cards(needed_cards):
			return CatanStatuses.ERR_CARDS
			
		# removes the cards
		self.players[player].remove_cards(needed_cards)
		
		# gives the player a dev card
		self.players[player].add_dev_card(self.dev_deck[0])
		
		# removes that dev card from the deck
		del self.dev_deck[0]
	
	# gives players the proper cards for a given roll
	def add_yield_for_roll(self, roll):
	
		self.board.add_yield(roll)
	
	# trades cards (given in an array) between two players	
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
	
	# moves the robber
	# Note that player is the player moving the robber 
	# and victim is the player whose card is being taken
	def move_robber(self, r, i, player, victim):
	
		# makes sure the input is valid		
		# checks the row exists
		if r < 0 or r >= len((self.board).points):
			return CatanStatuses.ERR_INPUJT
			
		# checks the index exists
		elif i < 0 or i >= len((self.board).points[r]):
			return CatanStatuses.ERR_INPUT
			
		# checks the player wants to take a card from somebody
		if victim != None:
			# checks the victim has a settlement on the hex
			has_settlement = False
			
			points = (self.board).get_hexes_for_point(r, i)
			for i in points:
				point = (self.board).points[i[0]][i[1]]
				if point != None:
					if point.owner == victim:
						has_settlement = True
		
			if not has_settlement:
				return CatanStatuses.ERR_INPUT
		
		# moves the robber
		self.board.move_robber(r, i)
	
		# takes a random card from the victim
		if victim != None:
			
			# removes a random card from the victim
			index = round(random.random() * (len(self.players[victim].cards) - 1))
			card = self.players[victim].cards[index]
			self.players[victim].remove_cards([card])
			
			# adds it to the player
			self.players[player].add_cards([card])
		
		return CatanStatuses.ALL_GOOD
		
	# trades cards from a player to the bank
	# either by 4 for 1 or using a harbor
	def trade_to_bank(self, player, cards, request):
		
		# makes sure the player has the cards
		if not (self.players[player]).has_cards(cards):
			return CatanStatuses.ERR_CARDS
		
		# checks all the cards are the same type
		card_type = cards[0]
		for c in cards[1:]:
			if c != card_type:
				return CatanStatuses.ERR_CARDS
		
		# if there are not four cards
		if len(cards) != 4:
			
			has_harbor = False
			# checks if the player has a settlement on the right type of harbor
			harbors = self.players[player].get_harbors()
			
			for h in harbors:
				if h == card_type:
					has_harbor = True
					break
					
			if not has_harbor:
				return CatanStatuses.ERR_HARBOR
				
					
		# removes cards
		(self.players[player]).remove_cards(cards)
		
		# adds the new card
		(self.players[player]).add_cards([request])
		
		return CatanStatuses.ALL_GOOD
		
	# gives the longest road to the correct player
	def set_longest_road(self):
		
		longest = 0
		owner = self.longest_road_owner
		
		for p in self.players:
			
			# longest road needs to be longer than anbody else's
			# and at least 5 road segments long
			if p.longest_road_length > longest and p.longest_road_length >= 5:
				
				longest = p.longest_road_length
				
				owner = self.players.index(p)
				
		if self.longest_road_owner != owner:
			
			self.longest_road_owner = owner
		
			# checks if the player has won now that they has longest road
			if self.players[owner].get_VP() >= 10:
				
				self.has_ended = True
				self.winner = owner
		
	# changes a settlement on the board for a city
	def add_city(self, r, i, player):
	
		status = self.board.upgrade_settlement(player, r, i)
		
		if status == CatanStatuses.ALL_GOOD:
			
			# checks if the player won
			if self.players[player].get_VP() >= 10:
				self.winner = player
		
		return status
		
	# uses a developement card
	def use_dev_card(self, player, card, args):
		
		# checks the player has the development card
		if not self.players[player].has_dev_cards([card]):
			return CatanStatuses.ERR_CARDS
		
		# applies the action
		if card == CatanCards.DEV_ROAD:	
			
			# checks the correct arguments are given
			road_names = [
				"road_one",
				"road_two"
			]	
			for r in road_names:
				if not r in args:
					return CatanStatuses.ERR_INPUT
					
				else:
					if not "start" in args[r] or not "end" in args[r]:
						return CatanStatuses.ERR_INPUT
						
			# checks the road location is valid
			
			# whether the other road is completely isolated but is connected to this road
			other_road_is_isolated = False
			
			for r in road_names:

				location_status = self.players[player].road_location_is_valid(args[r]['start'], args[r]['end'])
				
				# if the road location is not OK
				# since the player can build two roads, some 
				# locations that would be invalid are valid depending on the other road location
				if not location_status == CatanStatuses.ALL_GOOD:
				
					# checks if it is isolated, but would be connected to the other road
					if location_status == CatanStatuses.ERR_ISOLATED:
						
						# if the other road is also isolated, just return an error
						if other_road_is_isolated:
							return location_status
						
						# checks if the two roads are connected 
						# (since the other one is connected, this road is connected through it)
						road_points = [
							"start",
							"end"
						]
						roads_are_connected = False
						for p_one in road_points:
							for p_two in road_points:
								if args["road_one"][p_one] == args['road_two'][p_two]:
									other_road_is_isolated = True
									
									# doesn't return an isolated error
									roads_are_connected = True
						
						if not roads_are_connected:			
							return location_status
					else:
						return location_status
				
			# builds the roads
			for r in road_names:
				self.board.add_road(CatanBuilding(point_one=args[r]["start"], point_two=args[r]["end"], owner=player, type=CatanBuilding.BUILDING_ROAD))	
				
			return CatanStatuses.ALL_GOOD
			
		elif card == CatanCards.DEV_KNIGHT:
			
			# checks there are the right arguments
			if not ("robber_pos" in args and "victim" in args):
				return CatanStatuses.ERR_INPUT
			
			# checks the victim input is valid
			if args["victim"] != None:
				if args["victim"] < 0 or args["victim"] >= len(self.players) or args["victim"] == player:
					return CatanStatuses.ERR_INPUT
			
			# moves the robber
			result = self.move_robber(r=args["robber_pos"][0], i=args["robber_pos"][1], player=player, victim=args["victim"])
			
			if result != CatanStatuses.ALL_GOOD:
				return result
			
			# adds one to the player's knight count
			(self.players[player]).knight_cards += 1
			
			# checks for the largest army
			if self.largest_army == None:
				# if nobody has the largest army, the player needs at least 3 cards
				if self.players[player].knight_cards >= 3:
					self.largest_army = player
					
			else:
				# the player needs to have more than anybody else
				current_longest = self.players[self.largest_army].knight_cards
				
				if self.players[player].knight_cards > current_longest:
					self.largest_army = player
			
		elif card == CatanCards.DEV_MONOPOLY:
			
			# gets the type of card
			card_type = args['card_type']
			
			# for each player, checks if they have the card
			for p in self.players:
				
				if p.has_cards([card_type]):
					
					# gets how many this player has
					number_of_cards = p.cards.count(card_type)
					cards_to_give = [card_type] * number_of_cards
					
					# removes the cards
					p.remove_cards(cards_to_give)
					
					# adds them to the user's cards
					self.players[player].add_cards(cards_to_give)
			
		elif card == CatanCards.DEV_VP:
			
			# players do not play developement cards, so it returns an error
			return CatanStatuses.ERR_INPUT
			
		elif card == CatanCards.DEV_YOP:
			
			# checks the player gave two development cards
			if not 'card_one' in args and not 'card_two' in args:
				return CatanStatuses.ERR_INPUT
				
			# gives the player 2 resource cards of their choice
			self.players[player].add_cards([
				args['card_one'],
				args['card_two']
			])
			
		else:
			# error here
			return CatanStatuses.ERR_INPUT
		
		# removes the card
		self.players[player].remove_dev_card(card)
		
		return CatanStatuses.ALL_GOOD
		
	# simulates 2 dice rolling
	def get_roll(self):
		return round(random.random() * 6) + round(random.random() * 6)
		