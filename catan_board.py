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
		
			print(last_index)
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
				
		print("!")
		p.pprint(self.hex_nums)
		p.pprint(self.hexes)
		p.pprint(self.points)
		print("!")
		
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
						if self.hex_nums[num[0]][num[1]] == roll:
							
							# adds the card to the player's inventory
							owner = self.points[r][i].owner
							
							(self.game).players[owner].add_card(self.hexes[num[0]][num[1]])
							
		
	# adds a CatanBuilding object to the board
	def add_building(self, building, r, i):
		self.points[r][i] = building
	
	# adds a CatanBuilding object, which must be a road	
	# since roads record their own position and are not in self.points
	def add_road(self, road):
		self.roads.append(road)
		
	# checks if a point on the board is empty
	def point_is_empty(self, r, i):
		
		if self.points[r][i] == None:
			return True
			
		return False
		