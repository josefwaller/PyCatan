# temporary
# will be removed once PyCatan is a pip package
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pycatan.catan_game import CatanGame
from pycatan.catan_cards import CatanCards
from pycatan.catan_statuses import CatanStatuses as STAT
from pycatan.catan_board import CatanBoard as c

from colorama import init, AnsiToWin32, Fore, Style

import math

class Colors:
	red = '\033[1;31;40m' # red
	blue = '\033[1;34;40m' # blue
	green = '\033[1;32;40m' # green
	yellow = '\033[1;33;40m' # yellow
	purple = '\033[1;35;40m'
	cyan = '\033[1;36;40m'
	grey = "\033[1;30;40m"
	end = '\033[0m'

def main():
	
	# initializes colorama
	init()
	
	# prints a welcome message
	print("Welcome to Text-Only Settles of Catan")
	print("How many players are playing?")
	num_of_players = int(input("--> "))
	
	game = CatanGame(num_of_players)
	
	# runs through the building phase
	for p in range(num_of_players):
		while True:
			print("Player {}, choose where you want to build your settlement:".format(p + 1))
			
			print_board(game)
			
			try:
				r = int(input("Enter the row: "))
				i = int(input("Enter the index: "))
			
			except ValueError:
				print("Please enter numbers")
				continue
			
			if game.add_settlement(player=p, r=r, i=i, is_starting=True) != STAT.ALL_GOOD:
				print("Please enter a valid row and index")
				
			else: break

def print_board(game):
	
	board_str = []
	# Example hex
	#
	#    .-'-.-'-.-'-.
	#    | H | F | F |
	#  .-'-.-'-.-'-.-'-.
	#  |   |   |   |   |
	
	b = game.board.hexes
	
	# x|y
	# 0|5
	# 1|3
	# 2|1
	# 3|3
	# 4|5
	
	# abs(2(x-3) - 1)	
	
	for r in range(len(b)):
		
		# gets the number of offset spaces
		# if r < 3:
		offset = int(math.fabs(2 * (r - 2)) + 1)
		# else :
		# 	offset = ((r + 1) * 2 - len(b))
		
		if r < 3:
			board_str.append(" " * offset)
			
		else:
			board_str.append(" " * round(offset / 2))
		
		board_str.append(" " * offset)
		
		for i in range(len(b[r])):
			
			type = "lol"
			# gets the type
			if b[r][i] == c.HEX_MOUNTAINS:
				type = Fore.WHITE + "M"
			
			elif b[r][i] == c.HEX_PASTURE:
				type = Style.BRIGHT + Fore.GREEN + "P"
				
			elif b[r][i] == c.HEX_HILLS:
				type = Fore.RED + "H"
				
			elif b[r][i] == c.HEX_FIELDS:
				type = Fore.YELLOW + "f" + Colors.end
				
			elif b[r][i] == c.HEX_FOREST:
				type = Fore.GREEN + "F"
				
			elif b[r][i] == c.HEX_DESERT:
				type = Style.BRIGHT + Fore.YELLOW + "D"
		
			if r < 3:
		
				board_str[2 * r] += (".-'-");
			
			else:
				
				board_str[2 * r] += ("'-.-");
				
				
			board_str[2 * r + 1] += "| {} ".format(Style.NORMAL + type + Style.RESET_ALL + Style.BRIGHT)
			
		if r < 3:
			board_str[2 * r] += "."
		else:
			board_str[r * 2] += "'-.-'"
			
		board_str[2 * r + 1] += "|"
		
	# adds the final row
	board_str.append(" " * offset + "'-.-'-.-'-.-'")			
	for i in board_str:
		print(i)
	
main()