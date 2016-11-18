# PyCatan

A Library for simulating a game of *The Settlers of Catan*

## Contents
* Documentation
  * Other stuff
* Example game
  *

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

###### `CatanGame.__init__(self, num_of_players=3, on_win=None, starting_board=False)`

Creates a new `CatanGame`

* `num_of_players`: The number of players playing the game
* `on_win`: Optional function to run when the game is won
* `starting_board`: Whether or not to use the beginner's board
* 
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