# different statuses in the CatanGame module
class CatanStatuses:
	
	# the action was successfully completed
	ALL_GOOD = 0
	
# the action cannot be completed because:
	
	# the player does not have the correct cards
	ERR_CARDS = 1
	
	# a building is blocking the action
	ERR_BLOCKED = 2
	
	# the point given is not on the board
	ERR_BAD_POINT = 3
	
	# the road's points are not connected
	ERR_NOT_CON = 4
	
	# the building in not connected to any of the player's buildings
	ERR_ISOLATED = 5