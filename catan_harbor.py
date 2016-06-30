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
		
	def __str__(self):
		return "Harbor %s, %s Type %s" % (self.point_one, self.point_two, self.type)
		
	def get_points(self):
		return [self.point_one, self.point_two]