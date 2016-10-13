# imports neccessary modules
from catan_game import CatanGame
from catan_statuses import CatanStatuses

# creates a new game of Catan
game = CatanGame()

# Do for each player twice:
for i in range(2 * len(game.players)):

    # saves the player's number as p
    p = i % 3

    has_error = True
    while (has_error):

        # ask them to build a settlement
        print("Player %s, where do you want to build your first settlement?" % (p + 1))
        r = int(input("Enter the row:"))
        i = int(input("Enter the index: "))
        
        # try to place the settlement
        status = game.add_settlement(player=p, r=r, i=i, is_starting=True)
        
    	# if it didn't work, tell them why and try again
        if status != CatanStatuses.ALL_GOOD:
           
            # figure out what went wrong
            if status == CatanStatuses.ERR_BLOCKED:
                print("That settlement position is to close to another settlement")
            
            elif status == CatanStatuses.ERR_BAD_POINT:
                print("That settlement position doesn't exist!")
    			
            else:
                print("An unexpected error occured: %s" % status)
            
        else:
            print("Successfully built a settlement")
            has_error = False
        
    
    # get all the possible places a road could go from their settlement
    
    # get them to choose one
    
    # try to build the road
    
        # if it didn't work, try again