# represents a catan harbor 
class CatanHarbor:
	
	# the different 2:1 types
	TYPE_WOOD = 0
	TYPE_SHEEP = 1
	TYPE_BRICK = 2
	TYPE_WHEAT = 3
	TYPE_ORE = 4
	
	# the 3:1 type
	TYPE_ANY = 5
	
	def __init__(self, point_one, point_two, type):
		# sets the type
		self.type = type
		
		# sets the points
		self.point_one = point_one
		self.point_two = point_two
		
	def __repr__(self):
		return "Harbor %s, %s Type %s" % (self.point_one, self.point_two, self.type)
		
	def get_points(self):
		return [self.point_one, self.point_two]

	# returns a string representation of the type
	# Ex: 3:1, 2:1S, 2:1Wh
	def get_type(self):

		if self.type == CatanHarbor.TYPE_WOOD:
			return "2:1W"
		
		elif self.type == CatanHarbor.TYPE_SHEEP:
			return "2:1S"

		elif self.type == CatanHarbor.TYPE_BRICK:
			return "2:1B"

		elif self.type == CatanHarbor.TYPE_WHEAT:
			return "2:1Wh"

		elif self.type == CatanHarbor.TYPE_ORE:
			return "2:1O"

		elif self.type == CatanHarbor.TYPE_ANY:
			return "3:1"