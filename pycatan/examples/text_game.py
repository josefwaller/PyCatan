from PyCatan import CatanGame, CatanCards, CatanStatuses as STAT

import sys
import pprint

from board_printer import print_board

from colorama import AnsiToWin32, Fore, Style, init

game = None

player_colors = [
	Style.BRIGHT + Fore.RED,
	Style.BRIGHT + Fore.MAGENTA,
	Style.BRIGHT + Fore.CYAN,
	Style.NORMAL + Fore.MAGENTA,
	Style.NORMAL + Fore.CYAN
]

def main():
	
	# prints a welcome message
	print("Welcome to Text-Only Settles of Catan")
	print("How many players are playing?")
	num_of_players = int(input("--> "))
	
	global game
	game = CatanGame(num_of_players)
	
	# runs through the building phase
	for _ in range(2):
		for p in range(num_of_players):
		
			# gets a settlement placement for the player
			while True:
				print("{}Player {}{}, choose where you want to build your settlement:".format(
					player_colors[p],
					p + 1, 
					Style.RESET_ALL))
				
				print_board(game.board, player_colors)
				
				try:
					r = int(input("Enter the row: ")) - 1
					i = int(input("Enter the index: ")) - 1
				
				except ValueError:
					print("Please enter numbers")
					continue
				
				if game.add_settlement(player=p, r=r, i=i, is_starting=True) != STAT.ALL_GOOD:
					print("Please enter a valid row and index")
					
				else: break
					
			# gets the road location
			while True:
			
				# asks them to build a road
				con_points = game.board.get_connected_points(r, i)
				print("Where would you like to build your road to?")
				for x in range(len(con_points)):
					print("{}. Row {}, Index {}".format(x + 1, con_points[x][0] + 1, con_points[x][1] + 1))
					
				try:
					choice = int(input("--> ")) - 1
					
				except ValueError:
					print("Please enter an integer value")
					continue
					
				# tries to build the road
				stat = game.add_road(
					player=p, 
					start=[r, i],
					end=con_points[choice],
					is_starting=True)
				if stat != STAT.ALL_GOOD:
					print("That road location is not valid")
					continue
					
				else: break

		# goes through each player's turn
		count = 0
		while True:
			count += 1
			
			player = count % num_of_players
			player_str = "{}Player {}{}".format(
				player_colors[player], 
				player + 1, 
				Style.RESET_ALL)
			
			roll = game.get_roll()
			
			print("{} rolls a {}".format(player_str, roll))
			
			print("{}, what would you like to do?".format(player_str))
				
			print("1 - Build something")
			print("2 - Offer a trade")

if __name__ == "__main__":
	main()