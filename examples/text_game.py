# temporary
# will be removed once PyCatan is a pip package
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catan_game import CatanGame
from catan_cards import CatanCards
from catan_statuses import CatanStatuses as STAT
from catan_board import CatanBoard as c

from colorama import init, AnsiToWin32, Fore, Style

import math

player_colors = [
	Style.BRIGHT + Fore.RED,
	Style.BRIGHT + Fore.MAGENTA,
	Style.BRIGHT + Fore.CYAN,
	Style.NORMAL + Fore.MAGENTA,
	Style.NORMAL + Fore.CYAN
]

up_point_empty = "'"
up_point_settle = "^"
up_point_city = '"'

down_point_empty = "."
down_point_settle = ","
dow_point_city = "„"

def main():
	
	# initializes colorama
	init()
	
	# prints a welcome message
	print("Welcome to Text-Only Settles of Catan")
	print("How many players are playing?")
	num_of_players = int(input("--> "))
	
	game = CatanGame(num_of_players)
	
	# runs through the building phase
	for _ in range(2):
		for p in range(num_of_players):
			while True:
				print("{}Player {}{}, choose where you want to build your settlement:".format(player_colors[p],p + 1, Style.RESET_ALL))
				
				print_board(game)
				
				try:
					r = int(input("Enter the row: ")) - 1
					i = int(input("Enter the index: ")) - 1
				
				except ValueError:
					print("Please enter numbers")
					continue
				
				if game.add_settlement(player=p, r=r, i=i, is_starting=True) != STAT.ALL_GOOD:
					print("Please enter a valid row and index")
					
				else: break

		print_board(game)

def print_board(game):
	
	board_str = []
	# Example hex
	#
	#    .-'-.-'-.-'-.
	#    | H | F | F |
	#  .-'-.-'-.-'-.-'-.
	#  |   |   |   |   |
	
	b = game.board.hexes
	p = game.board.points
	
	# x|y
	# 0|5
	# 1|3
	# 2|1
	# 3|3
	# 4|5
	
	# abs(2(x-3) - 1)	
	
	for r in range(len(b)):
		
		# gets the number of offset spaces
		offset = int(math.fabs(2 * (r - 2)) + 1)
		
		# adds a string for the top/bottom of the hex
		# if we are drawing the bottom half of the board, 
		# we need to move over the top part of the hexes
		if r < 3:
			board_str.append(" " * offset)
		
		else:
			board_str.append(" " * (offset - 2))

		# adds a new string for the middle of the hex
		board_str.append(" " * offset)
		
		for i in range(len(b[r])):
			
			hex_type = "lol"
			# gets the hex_type
			if b[r][i] == c.HEX_MOUNTAINS:
				hex_type = Style.NORMAL + Fore.WHITE + "M"
			
			elif b[r][i] == c.HEX_PASTURE:
				hex_type = Style.BRIGHT + Fore.GREEN + "P"
				
			elif b[r][i] == c.HEX_HILLS:
				hex_type = Style.NORMAL + Fore.RED + "H"
				
			elif b[r][i] == c.HEX_FIELDS:
				hex_type = Style.NORMAL + Fore.YELLOW + "f"
				
			elif b[r][i] == c.HEX_FOREST:
				hex_type = Style.NORMAL + Fore.GREEN + "F"
				
			elif b[r][i] == c.HEX_DESERT:
				hex_type = Style.BRIGHT + Fore.YELLOW + "D"
			
			# PRINTS THE TOP PARTH OF THE HEX ------------

			# gets the point characters
			# see get_point()
			left_point = get_point(r=r, i=2 * i, points=p)
			middle_point = get_point(r=r, i=2 * i + 1, points=p)

			# formats the next part of the hex
			# will either be " .-'-. " or " '-.-' "
			board_str[2 * r] += ("{}-{}-".format(left_point, middle_point));
				
			# prints the desert normally
			if b[r][i] == c.HEX_DESERT:
				board_str[2 * r + 1] += "| {} ".format(Style.NORMAL + hex_type + Style.RESET_ALL + Style.BRIGHT)
			
			else:

				# CURRENTLY DEBUGGING THIS part
				try:

					# starts with just a line
					hex_str = "|"

					# adds the color and hex num
					hex_str += hex_type

					# if the number is 2 digits long (10, 11) it needs to be printed now
					# otherwise a space is inserted inbetween
					if game.board.hex_nums[r][i] >= 10:
						hex_str += str(game.board.hex_nums[r][i])

					else:
						hex_str += " " + str(game.board.hex_nums[r][i])

					hex_str += Style.RESET_ALL + Style.BRIGHT

					board_str[2 * r + 1] += hex_str

				except Exception as e:
					sys.exit("ERROR {}: {},{},{},{},{},{}".format(e, b[r], i, hex_str, game.board.hex_nums[r],r, i))
					

		if r < 3:
			board_str[2 * r] += get_point(r=r, i=2 * i + 2, points=p)
		else:
			board_str[r * 2] += "{}-{}-{}".format(
				get_point(r, 2 * i + 2, p),
				get_point(r, 2 * i + 3, p),
				get_point(r, 2 * i + 4, p)
			)
			
		board_str[2 * r + 1] += "|"

		# adds the arrow
		while len(board_str[2 * r]) < 23:
			board_str[2 * r] += " "

		board_str[2 * r] += ("<-- Row {}".format(r + 1))
		
	# gathers all the points fot the final row
	final_points = []
	for i in range(7):
		final_points.append(get_point(r=len(game.board.points) - 1, i=i, points=p))

	# adds the final row
	final_row = (" " * offset + ("{}-" * 6 + "{}").format(*final_points))
	final_row += " " * (23 - len(final_row)) + "<-- Row 6"

	board_str.append(final_row)
	
	for i in board_str:
		print(i)

# gets a point for the graphic representation of the board
# with color and stuff
def get_point(r, i, points):

	use_top = True

	if r < 3 and i % 2 == 0:
		use_top = False

	elif r > 2 and i % 2 == 1:
		use_top = False

	if points[r][i] != None:

		# colors the point
		color = player_colors[points[r][i].owner]

		if use_top:
			char = up_point_settle
		
		else:
			char = down_point_settle

		return color + char + Style.RESET_ALL

	if use_top:
		return up_point_empty
	
	else:
		return down_point_empty

if __name__ == "__main__":
	main()