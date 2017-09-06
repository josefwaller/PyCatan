# different statuses in the Game module
# skips 0 and 1 because there are already equal to True and False
class Statuses:

    # the action was successfully completed
    ALL_GOOD = 2

# the action cannot be completed because:

    # the player does not have the correct cards
    ERR_CARDS = 3
    # a building is blocking the action
    ERR_BLOCKED = 4
    # the point given is not on the board
    ERR_BAD_POINT = 5
    # the road's points are not connected
    ERR_NOT_CON = 6
    # the building in not connected to any of the player's buildings
    ERR_ISOLATED = 7
    # the player is trying to use a harbor they are not connected to
    ERR_HARBOR = 8
    # the player is trying to use a building that does not exist
    ERR_NOT_EXIST = 9
    # the player is trying to use a building that does not belong to them
    ERR_BAD_OWNER = 10
    # the player is trying to build a city on another city rather than a settlement
    ERR_UPGRADE_CITY = 11
    # there are not enough cards in the deck to perform this action
    ERR_DECK = 12
    # the input given is missing components/invalid
    ERR_INPUT = 13
    # when running the testing module, an error was found
    ERR_TEST = 14
