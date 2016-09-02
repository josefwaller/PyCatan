# a Catan settlement/city class

class CatanBuilding:
	
	BUILDING_SETTLEMENT = 0
	BUILDING_ROAD = 1
	BUILDING_CITY = 2
	
	def __init__(self, owner, type, point_one=None, point_two=None):
		
		# sets the owner and type
		self.owner = owner
		self.type = type
		
		# records where it is if it is a road
		if self.type == CatanBuilding.BUILDING_ROAD:
		
			self.point_one = point_one
			self.point_two = point_two
	
	def __repr__(self):
		
		if self.type == CatanBuilding.BUILDING_ROAD:
			return "CatanRoad, owned by player %s, from %s to %s" % (self.owner, self.point_one, self.point_two)
			
		elif self.type == CatanBuilding.BUILDING_SETTLEMENT:
			return "CatanSettlement, owned by player %s" % self.owner
			
		else:
			return "CatanCity, owned by player %s" % self.owner