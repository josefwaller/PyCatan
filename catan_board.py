from catan_harbor import CatanHarbor
from catan_player import CatanPlayer
from catan_statuses import CatanStatuses
from catan_building import CatanBuilding
from catan_cards import CatanCards

# used to shuffle the deck of hexes
import random

# used for lots of things
import math

# used for debugging
import pprint

class CatanBoard:
	
	# different types of hexes
	HEX_FOREST = 0
	HEX_HILLS = 1
	HEX_MOUNTAINS = 2
	HEX_PASTURE = 3
	HEX_FIELDS = 4
	HEX_DESERT = 5
	
	def __init__(self, game):
	
		# the game the board is in
		self.game = game
		
		# the hexes on the board
		self.hexes = []
		
		# the circular number tokens
		self.hex_nums = []
		
		# the points on the board
		# where the players can place settlements/cities
		self.points = []
		
		# the roads
		self.roads = []
		
		# the deck of hexes before they are placed on the board
		self.all_hexes = []
		
		# all of the circular number tokens in the game
		self.all_hex_nums = []
		
		# the locations of the harbors
		self.harbors = []
		
		# the location of the robber
		# going r, i
		self.robber = []
		
		# creates a new PrettyPrinter for debugging
		p = pprint.PrettyPrinter()
		
		# sets up all_hexes
		for i in range(4):
			
			# adds four fields, forests and pastures
			
			self.all_hexes.append(self.HEX_FIELDS)
			self.all_hexes.append(self.HEX_FOREST)
			self.all_hexes.append(self.HEX_PASTURE)
			
			# adds three mountains and hills
			if i < 3:
				self.all_hexes.append(self.HEX_MOUNTAINS)
				self.all_hexes.append(self.HEX_HILLS)
				
			# adds one desert
			if i == 0:
				self.all_hexes.append(self.HEX_DESERT)
				
		# shuffles the deck
		#random.shuffle(self.all_hexes)
		
		# sets up all_hex_nums
		for i in range(2):
			
			for x in range(2, 13):
			
				# does not add a number token with 7
				if x != 7:
					
					# only adds one 2 and one 12
					if x == 2 or x == 12:
						if i == 0:
							self.all_hex_nums.append(x)
						
					# adds two of everything else
					else:
						self.all_hex_nums.append(x) 
				
		# shuffles the hex numbers
		#random.shuffle(self.all_hex_nums)
		
		last_index = 0
		for i in range(5):
		
			# the length of this row of hexes
			length = round(-math.fabs(i - 2) + 5)
			
			self.hexes.append(self.all_hexes[last_index:last_index + length])
			self.hex_nums.append(self.all_hex_nums[last_index:last_index + length])
			
			# checks if the dessert was placed in this row
			if self.hexes[i].count(self.HEX_DESERT) > 0:
				
				# takes the chip off the desert and puts it at the back of the deck
				# so that it will be used at the end
				index = self.hexes[i].index(self.HEX_DESERT)
				self.all_hex_nums.append(self.hex_nums[i][index])
				self.hex_nums[i][index] = None
				
			last_index += length
		
		# adds None to points for each point on the hexes
		for i in range(6):
			
			self.points.append([])
			
			for x in range(round(12 - math.fabs(2 * i - 5))):
				
				self.points[i].append(None)
				
		print("Hex Numbers:")
		p.pprint(self.hex_nums)
		print("Hexes: ")
		p.pprint(self.hexes)
		print("Points: ")
		p.pprint(self.points)
		
		# adds harbors
		# each harbor is around the edge of the board
		# and are separated by n points, when n is a pattern of 2 3 2 repeating
		# so this gets all the points in segments of top, right, left, bottom
		# and then adds them together
		
		# adds the top and bottom layer
		top = []
		bottom = []
		
		# the index of the last row
		last = len(self.points) - 1
		
		# adds the points
		for i in range(len(self.points[0])):
			top.append([0, i])
			bottom.append([last, len(self.points[0]) - 1 - i])
		
		# adds all the points on the right and left
		right = []
		left = []
		
		for r in range(1, len(self.points) - 1):
			length = len(self.points[r]) - 1
			
			# orders the points depending if they are on the top half or bottom half
			if r < (len(self.points) - 1) / 2:
				right.append([r, length - 1])
				right.append([r, length])
				
				left.append([len(self.points) - 1 - r, 1])
				left.append([len(self.points) - 1 - r, 0])
			
			else:
				right.append([r, length])
				right.append([r, length - 1])
				
				left.append([len(self.points) - 1 - r, 0])
				left.append([len(self.points) - 1 - r, 1])
		
		outside_points = []
		outside_points.extend(top)
		outside_points.extend(right)
		outside_points.extend(bottom)
		outside_points.extend(left)
		
		# adds a harbor for each points in the pattern 2 3 2 2 3 2 etc
		
		# the index of the outside point to build a harbor on
		index = 0
		
		# the count of harbors build
		count = 0
		
		# the pattern of spaces between harbors
		pattern = [2, 3, 2]
		
		# goes around the board once and adds harbors
		while index < len(outside_points):
		
			# creates a new harbor
			harbor = CatanHarbor(point_one=outside_points[index], point_two=outside_points[index + 1], type=CatanHarbor.TYPE_WOOD)
			
			# adds it to harbors
			self.harbors.append(harbor)
			
			# increments index by the next pattern, adds one to fit with the width of each harbor being 2
			index += pattern[count % 3] + 1
			
			# adds one to count
			count += 1
		
		for h in self.harbors:
			print(h)
			
		# puts the robber on the desert hex to start
		
		for r in range(len(self.hexes)):
			# checks if this row has the desert
			if self.hexes[r].count(CatanBoard.HEX_DESERT) > 0:
				# places the robber
				self.robber = [r, self.hexes[r].index(CatanBoard.HEX_DESERT)]
			
	# gives the players cards for a certain roll
	def add_yield(self, roll):
		
		for r in range(len(self.points)):
			for i in range(len(self.points[r])):
				
				if self.points[r][i] != None:
					
					# the indexes of he hexes to check
					hex_indexes = []
					
					# gets the adjacent hexes differently depending on whether the point is in the top or the bottom
					if r < len(self.points) / 2:
						# gets the hexes below the point ------------------
						
						# adds the hexes to the right
						if i < len(self.points[r]) - 1:
							hex_indexes.append([r, math.floor(i / 2)])
						
						# if the index is even, the number is between two hexes
						if i % 2 == 0 and i > 0:
							hex_indexes.append([r, math.floor(i / 2) - 1])
							
						# gets the hexes above the point ------------------
						
						# gets the hex to the right
						if i > 0 and i < len(self.points[r]) - 2:
							hex_indexes.append([r - 1, math.floor((i - 1) / 2)])
							
						# gets the hex to the left
						if i % 2 == 1 and i < len(self.points[r]) - 1 and i > 1:
							hex_indexes.append([r - 1, math.floor((i - 1) / 2) - 1])
			
					else:
						
						# adds the below -------------
						
						# gets the hex to the right or directly below
						if i < len(self.points[r]) - 2 and i > 0:
							hex_indexes.append([r, math.floor((i - 1) / 2)])
							
						# gets the hex to the left
						if i % 2 == 1 and i > 1 and i < len(self.points[r]):
							hex_indexes.append([r, math.floor((i - 1) / 2 - 1)])
							
						# gets the hexes above ------------
						
						# gets the hex above and to the right or directly above
						if i < len(self.points[r]) - 1:
							hex_indexes.append([r - 1, math.floor(i / 2)])
							
						# gets the hex to the left
						if i > 1 and i % 2 == 0:
							hex_indexes.append([r - 1, math.floor((i - 1) / 2)])
					
					# checks if any hexes have the right number
					for num in hex_indexes:
					
						# makes sure the robber isn't there
						if self.robber[0] == num[0] and self.robber[1] == num[1]:
							
							# skips this hex
							continue
					
						if self.hex_nums[num[0]][num[1]] == roll:
							
							# adds the card to the player's inventory
							owner = self.points[r][i].owner
							
							card_type = self.hexes[num[0]][num[1]]
							# adds two if it is a city
							if self.points[r][i].type == CatanBuilding.BUILDING_CITY:
								(self.game).players[owner].add_cards([
									card_type,
									card_type
								])
							
							else:
								(self.game).players[owner].add_cards([
									card_type
								])
								
		
	# adds a CatanBuilding object to the board
	def add_building(self, building, r, i):
		self.points[r][i] = building
	
	# adds a CatanBuilding object, which must be a road	
	# since roads record their own position and are not in self.points
	def add_road(self, road):
		self.roads.append(road)
		
	# upgrades an existing settlement to a city
	def upgrade_settlement(self, player, r, i):
		
		# checks there is a settlement at r, i which is controlled by the player
		if self.points[r][i] == None:
			return CatanStatuses.ERR_NOT_EXIST
			
		elif self.points[r][i].owner != player:
			return CatanStatuses.ERR_BAD_OWNER

		# checks it is a settlement and not a city
		elif self.points[r][i].type != CatanBuilding.BUILDING_SETTLEMENT:
			return CatanStatuses.ERR_UPGRADE_CITY		

		# checks the player has the cards
		needed_cards = [
			CatanCards.CARD_WHEAT,
			CatanCards.CARD_WHEAT,
			CatanCards.CARD_ORE,
			CatanCards.CARD_ORE,
			CatanCards.CARD_ORE
		]
		if not (self.game).players[player].has_cards(needed_cards):
			return CatanStatuses.ERR_CARDS
			
		# removes the cards
		(self.game).players[player].remove_cards(needed_cards)
		
		# changes the settlement to a city
		self.points[r][i].type = CatanBuilding.BUILDING_CITY

		return CatanStatuses.ALL_GOOD

	# gets all the buildings on the board
	def get_buildings(self):
		
		buildings = []
		for r in range(len(self.points)):
			for i in range(len(self.points[r])):
				if self.points[r][i] != None:
					buildings.append([r, i])
					
		return buildings
		
	# moves the robber to a givne coord
	def move_robber(self, r, i):
		self.robber = [r, i]
	
	# checks if a point on the board is empty
	def point_is_empty(self, r, i):
		
		if self.points[r][i] == None:
			return True
			
		return False
		
	def get_connected_points(self, r, i):
		
		# the connected points
		connected_points = []
		
		# whether the point has another point directly above or directly below
		has_point_above = False
	
		# half of the last index
		# if the board has 6 rows, this will be 2.5
		# so that ceiling/flooring will give the two middle rows
		half_height = (len(self.points) - 1) / 2
		
		# if it is in the top half
		if r < half_height:
			
			# even points have a point below, odd points have one above
			if i % 2 == 0:
				
				# adds a point below
				
				if r == math.floor(half_height):
					# this connection has the same index because it is crossing over the middle
					connected_points.append([r + 1, i])
					
				else:
					connected_points.append([r + 1, i + 1])
			
			else: 
				# adds a point above
				if r < 0 and i < 0:
					connected_points.append([r - 1, i - 1])
			
		# if it is in the bottom half	
		else:
			if i % 2 == 0:
				
				# adds a point above
			
				if r == math.ceil(half_height):
					# same index because it is crossing the middle
					connected_points.append([r - 1, i])
					
				else:
					connected_points.append([r - 1, i + 1])
				
			else:
			
				# adds a point below
			
				if r < len(self.points) - 1 and i > 0:
					connected_points.append([r + 1, i - 1])
					
					
		# # The different in index 
		# #
		# #          ABOVE   | BELOW
		# # TOP    |   -1    |   +1
		# # BOTTOM |   +1    |   -1
		
		# gets the adjacent points
		if i > 0:
			connected_points.append([r, i - 1])
			
		if i < len(self.points[r]) - 1:
			connected_points.append([r, i + 1])
			
		return connected_points
			
	def get_point(self, r, i):
		return self.points[r][i]