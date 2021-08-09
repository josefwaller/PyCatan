# DEPRECATED: PyCatan has moved to this respository: https://github.com/josefwaller/PyCatan2
# PyCatan

A Library for simulating a game of *The Settlers of Catan*

## Run

### Download from pip3
pip3 install pycatan

### Run tests from source

#### Easy way
Run the bash file test.sh
`.test.sh'

#### Hard Way
* Install [virtualenv](https://virtualenv.pypa.io/en/stable/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
* Create a new virtual environment (`mkvirtualenv test`)
* Install [pytest](https://docs.pytest.org/en/latest/)
* Run (from root directory) `python -m pytest tests`

## Contents
* Documentation
  * `CatanGame`
  * `CatanBoard`
  * `CatanPlayer`
  * Etc
* Example game
  * Something

## Documentation

### `CatanGame` module

Represents a game of Catan

#### Atttributes

* `board`
  * The `CatanBoard` in the game
* `players`
  * An array of `CatanPlayer`s (representing the players)
* `longest\_road\_owner`
  * The index of the player who has the longest road

#### Functions

##### `CatanGame.__init__(self, num_of_players=3, on_win=None, starting_board=False)`

Creates a new `CatanGame`
* `num_of_players`: The number of players playing the game
* `on_win`: Optional function to run when the game is won
* `starting_board`: Whether or not to use the beginner's board



##### `CatanGame.add_settlement(self, player, r, i, is_starting=False)`

Builds a new settlement

* `player`: The index of the player who is building the settlement
* `r`: The row at which to build the settlement
* `i`: The index at which to build the settlement
* `is_starting`: Whether or not the settlement is being build during the building phase, and thus should be build for free

Returns a `CatanStatus` value.



##### `CatanGame.add_road(self, player, start, end, is_starting=False)`

Builds a new road

* `player`: The index of the player building the road
* `start`: An array with the coordinate of one the the road's points (given `[row, index]`)
* `end`: An array with the coordinate of the road's other point (given `[row, index]`)
* `is_starting`: Whether or not the road is being built during the building phase and thus should be build for free

Returns a `CatanStatus` value

##### `CatanGame.add_city(self, r, i, player)`

Builds a city on top of a settlement

* `r`: The row at which to build the city
* `i`: The index at which to build the city
* `player`: The index of the player who is building the city

Returns a `CatanStatus` value

##### `CatanGame.build_dev(self, player)`

Builds a new developement card

* `player`: The player who is building the developement card

Returns a `CatanStatus` value

##### `CatanGame.use_dev_card(self, player, card, args)`

Uses a developement card

* `player`: The player who is using the card
* `card`: The `CatanCard` value representing the type of card
* `args`: Variable arguments in a dictionary depending on which type of developement card is played
  * `CatanCards.DEV_ROAD`: `args` contains `'road_one'` and `'road_two'` values, both of which are arrays of arrays coresponding to the point which the roads should be built
    * `road_one`: An array representing the first road in arrays representing points
      * Ex: `[[0, 0], [0, 1]]` would represent a road going from `0, 0` to `0, 1`
    * `road_two`: Same as `road_one`, but for the other road
  * `CatanCards.DEV_KNIGHT`: `args` contains `'robber_pos'` and `'victim'` values.
    * `robber_pos`: The position for the robber to be placed as an array, given as `[row, index]`
    *  `victim`: The index of the player to take the card from. Can be `None` if the player playing the knight card doesn't want to take a card from anybody.
  * `CatanCards.DEV_MONOPOLY`: `args` contains a `'card_type'` value.
    * `card_type`: The `CatanCards` value representing the card the player wants to take
  * `CatanCards.DEV_YOP`: `args` contains `'card_one'` and `'card_two'` values.
    * `card_one`: The `CatanCards` value of the first card the player wants to take
    * `card_two`: The `CatanCards` value of the second card
  * `CatanCards.DEV_VP`: Do not call `CatanGame.use_dev_card` on `CatanCards.DEV_VP`, as players do not play VP cards, but keep them until the end of the game.

##### `CatanGame.add_yield_for_roll(self, roll)`

Distributes cards based on a dice roll

* `roll`: The dice roll

Returns nothing

##### `CatanGame.get_roll(self)`

Optional. Simulates 2 dice rolls added together.

Returns a number

##### `CatanGame.trade(self, player_one, player_two, cards_one, cards_two)`

Trades cards between players
* `player_one`: The first player in the trade
* `player_two`: The second player in the trade
* `cards_one`: The cards the first player is giving
* `cards_two`: The cards the second player is giving

Returns a `CatanStatus` value

##### `CatanGame.trade_to_bank(self, player, cards, request)`

Trades 4 cards to the bank for 1 card.
Also will trade only 2 cards if the player is connected to the right harbor

* `player`: The player who is trading the cards
* `cards`: An array of numbers (`CatanCard` values) to trade from the player to the bank
* `request`: The `CatanCard` value the player will receive

Returns a `CatanStatus` value


### `CatanBoard`

Represents a Catan game board.

#### Static values

* `CatanBoard.HEX_FOREST`
  * Represents a forest hex
* `CatanBoard.HEX_Hills`
  * Represents a hills hex
* `CatanBoard.HEX_MOUNTAINS`
  * Represents a mountains hex
* `CatanBoard.HEX_PASTURE`
  * Represents a pasture hex
* `CatanBoard.HEX_FIELDS`
  * Represents a fields hex
* `CatanBoard.HEX_DESERT`
  * Represents a desert hex

#### Attributes

* `hexes`
  * An array representing the hexes on the board
* `hex_nums`
  * An array representing the number tokens on the board
* `points`
  * An array representing the intersections between hexes (where settlements are placed)
* `roads`
  * An array of `CatanBuildings` representing all the roads in the game
* `harbors`
  * An array of `CatanHarbors` representing all the harbors on the board
* `robber`
  * An array representing the robber's position (given as `[row, index]`)

#### Functions

##### `CatanBoard.get_card_from_hex(hex)`
Gets a `CatanCards` value for a corresponding `CatanBoard` Hex value
* `hex`: The `CatanBoard` hex value to get the card for

Ex: `CatanBoard.get_card_from_hex(CatanBoard.HEX_HILLS)` would return `CatanCards.CARD_BRICK`

Returns a `CatanCards` value

### `CatanBuilding`

Represents a Catan Building

#### Static Values

##### `CatanBuilding.BUILDING_ROAD`

Represents a road

##### `CatanBuilding.BUILDING_SETTLEMENT`

Represents a settlement

##### `CatanBuilding.BUILDING_CITY`

Represents a city

### `CatanCards`

Contains values representing different resource and developement cards

#### Static Values

##### `CatanCards.CARD_WOOD`

Represents a wood resource card.

##### `CatanCards.CARD_BRICK`

Represents a brick resource card.

##### `CatanCards.CARD_SHEEP`

Represents a sheep resource card.

##### `CatanCards.CARD_ORE`

Represents a ore resource card.

##### `CatanCards.CARD_WHEAT`

Represents a wheat resource card.

##### `CatanCards.DEV_ROAD`

Represents a road building developement card.

##### `CatanCards.DEV_VP`

Represents a victory point developement card.

##### `CatanCards.DEV_MONOPOLY`

Represents a monopoly developement card.

##### `CatanCards.DEV_YOP`

Represents a year of plenty developement card.

##### `CatanCards.DEV_KNIGHT`

Represents a knight developement card.

### `CatanHarbor`

Represents a harbor.

#### Static values

##### `CatanHarbor.TYPE_WOOD`

Represents a 2:1 Wood harbor

##### `CatanHarbor.TYPE_BRICK`

Represents a 2:1 Brick harbor

##### `CatanHarbor.TYPE_WHEAT`

Represents a 2:1 Wheat harbor

##### `CatanHarbor.TYPE_ORE`

Represents a 2:1 Ore harbor

##### `CatanHarbor.TYPE_SHEEP`

Represents a 2:1 Sheep harbor

#### Functions

##### `CatanHarbor.get_type(self)`

Returns a string representation of the harbor's type

### `CatanPlayer`

Represents a player in the game.

#### Functions

##### `CatanPlayer.get_VP(self, include_dev=False)`

Returns the number of victory points the player has.

* `include_dev`: Whether to include victory points from developement cards, which are only counted if the player wins and should be hidden otherwise.

### `CatanStatuses`

Interger representation of different statuses returned by functions.

#### Static values

##### `CatanStatuses.ALL_GOOD`

The function ran successfully

##### `CatanStatuses.ERR_CARDS`

The player trying to perform an action lacks the necessary cards.

##### `CatanStatuses.ERR_BLOCKED`

A building is blocking the action.

##### `CatanStatuses.ERR_BAD_POINT`

The point being used does not exist.

##### `CatanStatuses.ERR_NOT_CON`

The player is trying to build a building which is not connected to any of their roads.

##### `CatanStatuses.ERR_HARBOR`

The player is trying to use a harbor which they are not connected to

##### `CatanStatuses.ERR_NOT_EXIST`

The player is trying to use a building which does not exist

##### `CatanStatuses.ERR_BAD_OWNER`

The player is trying to use a building which belongs to another player

##### `CatanStatuses.ERR_UPGRADE_CITY`

The player is trying to build a city on an invalid location

##### `CatanStatuses.ERR_DECK`

There are not enough cards in the deck to perform this action

##### `CatanStatuses.ERR_INPUT`

The input given is missing mandatory information

##### `CatanStatuses.ERR_TEST`

When running the test module, an error was encountered



## Example game

We're going to make an example text-game of Catan using *PyCatan*

First, create a new file.


`game.py`

```
def main():
	print("Playing Catan!")

if __name__ == "__main__":
	main()
```


Now let's set up a new game of Catan

`game.py`

```
from PyCatan import CatanGame

def main():

	num_of_players = int(input("How many players are playing? "))

	game = CatanGame(num_of_players)

```
