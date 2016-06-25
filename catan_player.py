from catan_board import CatanBoard;
class CatanPlayer:
	
	board = None
	
	def __init__(self, numOfPlayers):
		
		# creates a board
		self.board = CatanBoard();