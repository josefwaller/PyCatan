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
	
	# the player is trying to use a harbor they are not connected to
	ERR_HARBOR = 6
	
	# the player is trying to use a building that does not exist
	ERR_NOT_EXIST = 7
	
	# the player is trying to use a building that does not belong to them
	ERR_BAD_OWNER = 8
	
	# the player is trying to build a city on another city rather than a settlement
	ERR_UPGRADE_CITY = 9
	
	# there are not enough cards in the deck to perform this action
	ERR_DECK = 10