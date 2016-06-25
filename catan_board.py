
class CatanBoard:
	
	# different types of hexes
	HEX_FIELD = 0
	HEX_FOREST = 1
	HEX_PASTURE = 2
	HEX_MOUNTAINS = 3
	HEX_HILLS = 4
	HEX_DESERT = 5
	
	# the hexes on the board
	hexes = []
	
	# the deck of hexes before they are placed on the board
	all_hexes = []
	
	def __init__(self):
	
		print("New Board created")
		
		# sets up all_hexes
		for i in range(4):
			
			# adds four fields, forests and pastures
			all_hexes.append(HEX_FIELDS)
			all_hexes.append(HEX_FOREST)
			all_hexes.append(HEX_PASTURE)
			
			# adds three mountains and hills
			if i < 3:
				all_hexes.append(HEX_MOUNTAINS)
				all_hexes.append(HEX_HILLS)
				
			# adds one desert
			if i == 0:
				all_hexes.append(HEX_DESERT)
		