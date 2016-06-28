from catan_building import CatanBuilding
from catan_statuses import CatanStatuses

import math

# The player class for Catan
class CatanPlayer:

	# the different types of cards
	CARD_WOOD = 0
	CARD_BRICK = 1
	CARD_ORE = 2
	CARD_SHEEP = 3
	CARD_WHEAT = 4
	
	def __init__ (self, game, num):
	
		# the game the player belongs to
		self.game = game
		
		# the player number for this player
		self.num = num
		
		# the number of victory points
		self.victory_points = 0
		
		# the cards the player has
		# each will be a number corresponding with the static variables CARD_<type>
		self.cards = []
		
	def build_settlement (self, settle_r, settle_i):
	
		# makes sure the player has the cards to build a settlements
		cards_needed = [
			self.CARD_WOOD,
			self.CARD_BRICK,
			self.CARD_SHEEP,
			self.CARD_WHEAT
		]
		
		# the indexes of the cards needed
		# used to quickly delete them
		card_indexes = []
		
		for i in range(len(cards_needed)):
			
			# checks if the card exists
			if self.cards.count(cards_needed[i]) < 1:
				return CatanStatuses.ERR_CARDS
				
			else:
				# adds the index 
				card_indexes.append(self.cards.index(cards_needed[i]))
		
		# checks that a building does not already exist there
		if not (self.game).board.point_is_empty(settle_r, settle_i):
			return CatanStatuses.ERR_BLOCKED
		
		# checks all other settlements are at least 2 away
		# gets the connecting point's coords
		point_coords = (self.game).board.get_connected_points(settle_r, settle_i)
		for coord in point_coords:
			
			# checks if the point is occupied
			p = (self.game).board.get_point(coord[0], coord[1])
			if p != None:
				return CatanStatuses.ERR_BLOCKED
		
		# sorts in descending order, so that removing cards does not change the index of other cards
		card_indexes.sort(reverse=True)
		
		# removes the cards
		for i in range(len(card_indexes)):
			del self.cards[card_indexes[i]]
		
		# adds the house
		((self.game).board).add_building(CatanBuilding(owner=self.num, type=CatanBuilding.BUILDING_SETTLEMENT), r=settle_r, i=settle_i)
		
		return CatanStatuses.ALL_GOOD
		
	# checks if the player has all of the cards given in an array
	def has_cards(self, cards):
		
		# needs to duplicate the cards, and then delete them once found
		# otherwise checking if the player has multiple of the same card
		# will return true with only one card
		
		cards_dup = self.cards[:]
		for c in cards:
			if cards_dup.count(c) == 0:
				return False
			else:
				index = cards_dup.index(c)
				del cards_dup[index]
				
		return True
	
	def add_cards(self, cards):
		
		for c in cards:
			self.cards.append(c)
			
	def remove_cards(self, cards):
	
		# makes sure it has all the cards before deleting any
		if not self.has_cards(cards):
			return CatanStatuses.ERR_CARDS
			
		else:
			# removes the cards
			for c in cards:
				index = self.cards.index(c)
				del self.cards[index]
			
	# builds a road
	def build_road(self, start, end):
	
		# checks the two points are connected
		connected = False
		# gets the points connected to start
		points = (self.game).board.get_connected_points(r=start[0], i=start[1])
		for p in points:
			if end == p:
				connected = True
				break
		if not connected:
			return CatanStatuses.ERR_NOT_CON
			
		connected_by_road = False
		for road in (self.game).board.roads:
					
			# checks the road does not already exists with these points
			if road.point_one == start or road.point_two == start:
				
				if road.point_one == end or road.point_two == end:
					return CatanStatuses.ERR_BLOCKED
			
		# check this player has a settlement on one of these points or a connecting road
		is_connected = False
		
		# first checks if there is a settlements on either point
		point_one = (self.game).board.get_point(r=start[0], i=start[1])
		point_two = (self.game).board.get_point(r=end[0], i=end[1])
		
		if point_one != None:
		
			# checks if this player owns the settlement/city
			if point_one.owner == self.num:
				is_connected = True
				
		# does the same for the other point
		elif point_two != None:
			if point_two.owner == self.num:
				is_connected = True
				
		# then checks if there is a road connecting them
		roads = (self.game).board.roads
		points = [start, end]
		
		for r in roads:
			for p in points:
				if r.point_one == p or r.point_two == p:
					
					# checks that there is not another player's settlement here, so that it's not going through it
					if (self.game).board.points[p[0]][p[1]] == None:
						is_connected = True
					
					# if theere is a settlement/city there, the road can be built if this player owns it
					elif (self.game).board.points[p[0]][p[1]].owner == self.num:
						is_connected = True
		
		if not is_connected:
			return CatanStatuses.ERR_ISOLATED
			
		# checks that it has the proper cards
		cards_needed = [
			self.CARD_WOOD,
			self.CARD_BRICK
		]
		
		card_indexes = []
		
		for i in range(len(cards_needed)):
			if self.cards.count(cards_needed[i]) < 1:
				return CatanStatuses.ERR_CARDS
				
			else:
				card_indexes.append(i)
					
		# removes the cards
		card_indexes.sort(reverse=True)
		for i in card_indexes:
			del self.cards[i]
		
		# adds the road
		(self.game).board.add_road(CatanBuilding(owner=self.num, type=CatanBuilding.BUILDING_ROAD, point_one=start, point_two=end))
		
		return CatanStatuses.ALL_GOOD
		
	def add_card(self, card):
	
		self.cards.append(card)