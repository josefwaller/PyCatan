from pycatan.harbor import Harbor, HarborType
from pycatan.player import Player
from pycatan.statuses import Statuses
from pycatan.building import Building
from pycatan.tile_type import TileType
from pycatan.card import ResCard, DevCard
from pycatan.tile import Tile
from pycatan.point import Point

# used to shuffle the deck of tiles
import random

import abc

# used for debugging
import pprint

# Base class for different Catan boards
# Should not be instantiated, otherwise the board will be empty
class Board(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game):
        # The game the board is in
        self.game = game
        # The tiles on the board
        # Should be set in a subclass
        self.tiles = ()
        # The points on the board
        # Where the players can place settlements/cities
        # Will be set at the end of __init__
        self.points = ()
        # The roads
        self.roads = []
        # The locations of the harbors
        self.harbors = []
        # The location of the robber
        # going r, i
        self.robber = None

    # gives the players cards for a certain roll
    def add_yield(self, roll):

        for r in self.points:
            for p in r:
                # Check there is a building on the point
                if p.building != None:
                    building = p.building
                    tiles = p.tiles

                    # checks if any tiles have the right number
                    for current_tile in tiles:

                        print(self.robber, current_tile)
                        # makes sure the robber isn't there
                        if self.robber is current_tile:
                            # skips this tile
                            continue

                        if current_tile.token_num == roll:
                            # adds the card to the player's inventory
                            owner = building.owner
                            # gets the card type
                            card_type = Board.get_card_from_tile(current_tile.type)
                            # adds two if it is a city
                            if building.type == Building.BUILDING_CITY:
                                self.game.players[owner].add_cards([
                                    card_type,
                                    card_type
                                ])

                            else:
                                self.game.players[owner].add_cards([
                                    card_type
                                ])


    # adds a Building object to the board
    def add_building(self, building, point):
        point.building = building

    # adds a Building object, which must be a road
    # since roads record their own position and are not in self.points
    def add_road(self, road):
        self.roads.append(road)

    # upgrades an existing settlement to a city
    def upgrade_settlement(self, player, point):
        # Get building at point
        building = point.building

        # checks there is a settlement at r, i
        if building == None:
            return Statuses.ERR_NOT_EXIST

        # checks the settlement is controlled by the correct player
        # if no player is specified, uses the current controlling player
        if building.owner != player:
            return Statuses.ERR_BAD_OWNER

        # checks it is a settlement and not a city
        if building.type != Building.BUILDING_SETTLEMENT:
            return Statuses.ERR_UPGRADE_CITY

        # checks the player has the cards
        needed_cards = [
            ResCard.Wheat,
            ResCard.Wheat,
            ResCard.Ore,
            ResCard.Ore,
            ResCard.Ore
        ]
        if not self.game.players[player].has_cards(needed_cards):
            return Statuses.ERR_CARDS

        # removes the cards
        self.game.players[player].remove_cards(needed_cards)
        # changes the settlement to a city
        building.type = Building.BUILDING_CITY
        # adds another victory point
        self.game.players[player].victory_points += 1

        return Statuses.ALL_GOOD

    # gets all the buildings on the board
    def get_buildings(self):

        buildings = []
        for r in self.points:
            for p in r:
                if p.building != None:
                    buildings.append(p.building)

        return buildings

    # moves the robber to a givne coord
    def move_robber(self, tile_pos):
        self.robber = tile_pos

    def __repr__(self):
        return ("Board Object")

    # Get a shuffled deck of the correct number of each type of tile in a board
    @staticmethod
    def get_shuffled_tile_deck():
        deck = []
        # sets up all_tiles
        for i in range(4):

            # adds four fields, forests and pastures
            deck.append(TileType.Fields)
            deck.append(TileType.Forest)
            deck.append(TileType.Pasture)
            # adds three mountains and hills
            if i < 3:
                deck.append(TileType.Mountains)
                deck.append(TileType.Hills)

            # adds one desert
            if i == 0:
                deck.append(TileType.Desert)

        # shuffles the deck
        random.shuffle(deck)
        return deck

    @staticmethod
    def get_shuffled_tile_nums():
        nums = []
        # Get 2 of each number, most of the time
        for i in range(2):
            # Go through each type
            for x in range(2, 13):
                # Does not add a number token with 7
                if x != 7:
                    # Only adds one 2 and one 12
                    if x == 2 or x == 12:
                        if i == 0:
                            nums.append(x)
                    # Adds two of everything else
                    else:
                        nums.append(x)
        random.shuffle(nums)
        return nums

    # returns the card associated with the tile
    # for example, Brick for Hills, Wood for forests, etc
    @staticmethod
    def get_card_from_tile(tile):

        # returns the appropriete card
        if tile == TileType.Forest:
            return ResCard.Wood

        elif tile == TileType.Hills:
            return ResCard.Brick

        elif tile == TileType.Pasture:
            return ResCard.Sheep

        elif tile == TileType.Fields:
            return ResCard.Wheat

        elif tile == TileType.Mountains:
            return ResCard.Ore

        else:
            return None
