from catan_building import CatanBuilding

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
		selfvictory_points = 0
		
		# the structures the player has built
		self.buidlings = []
		self.roads = []
		
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
		
		# sorts in descending order, so that removing cards does not change the index of other cards
		card_indexes.sort(reverse=True)
		
		# removes the cards
		for i in range(len(card_indexes)):
			del self.cards[card_indexes[i]]
		
		# adds the house
		((self.game).board).add_building(CatanBuilding(self.num), r=settle_r, i=settle_i)
		
		return 1
		
	def add_card(self, card):
		self.cards.append(card)