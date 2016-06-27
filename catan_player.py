from catan_building import CatanBuilding

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
				return -1
				
			else:
				# adds the index 
				card_indexes.append(self.cards.index(cards_needed[i]))
		
		# checks that a building does not already exist there
		
		# checks all other settlements are at least 2 away
		
		# sorts in descending order, so that removing cards does not change the index of other cards
		card_indexes.sort(reverse=True)
		
		# removes the cards
		for i in range(len(card_indexes)):
			del self.cards[card_indexes[i]]
		
		# adds the house
		((self.game).board).add_building(CatanBuilding(owner=self.num, type=CatanBuilding.BUILDING_SETTLEMENT), r=settle_r, i=settle_i)
		
		return 1
		
	# builds a road
	def build_road(self, start, end):
	
		# checks the two points are connected
		# if they are in the same row, just checks if they are adjacent
		if start[0] == end[0]:
			if math.fabs(start[1] - end[1]) != 1:
				return -1
		
		# if they are in different rows
		else:
			
			board_height = len((self.game).board.points) - 1
			# if they are both in the top half, the bottom one needs its index to be +1
			if start[0] < board_height / 2 and end[0] < board_height / 2:
				
				if (start[0] < end[0] and end[1] != start[1] + 1) or (start[0] > end[0] and start[1] != end[1] + 1):
					
					return -1
					
			# if they are both in the bottom half, the top one needs its index to be + 1
			elif start[0] > board_height / 2 and end[0] > board_height / 2:
				
				if not (start[0] < end[0] and start[1] == end[1] + 1) and not (start[0] > end[0] and end[1] == start[1] + 1):
				
					return -1
					
			# if one is in the top and the other is in the bottom
			else:
				# the only option is for one to be the row above half and the other to be the one beneath it
				top = math.floor(board_height / 2)
				bot = math.ceil(board_height / 2)
				
				# checks if one is top and the other is bot
				if not (start[0] == top and end[0] == bot) or not (start[0] == top and end[0] == bot):
				
					return -1
					
				# if they are, the indexes must be the same and the number must be even
				if start[1] != end[1] or start[1] % 2 == 1:
					return -1
		
		connected_by_road = False
		for road in (self.game).board.roads:
					
			# checks the road does not already exists with these points
			if road.point_one == start or road.point_two == start:
				
				if road.point_one == end or road.point_two == end:
					return -1
			
		# check this player has a settlement on one of these points or a connecting road
		is_connected = False
		
		# first checks if there is a settlements on either point
		point_one = (self.game).board.points[start[0]][start[1]]
		point_two = (self.game).board.points[end[0]][end[1]]
		
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
			return -1
			
		# checks that it has the proper cards
		cards_needed = [
			self.CARD_WOOD,
			self.CARD_BRICK
		]
		
		card_indexes = []
		
		for i in range(len(cards_needed)):
			if self.cards.count(cards_needed[i]) < 1:
				return -1
				
			else:
				card_indexes.append(i)
					
		# removes the cards
		card_indexes.sort(reverse=True)
		for i in card_indexes:
			del self.cards[i]
		
		# adds the road
		(self.game).board.add_road(CatanBuilding(owner=self.num, type=CatanBuilding.BUILDING_ROAD, point_one=start, point_two=end))
		
		return 1
		
	def add_card(self, card):
	
		self.cards.append(card)