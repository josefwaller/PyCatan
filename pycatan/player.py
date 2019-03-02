from pycatan.building import Building
from pycatan.statuses import Statuses
from pycatan.card import ResCard, DevCard

import math

# The player class for
class Player:

    def __init__ (self, game, num):
        # the game the player belongs to
        self.game = game
        # the player number for this player
        self.num = num
        # the starting roads for this player
        # used to determine the longest road
        self.starting_roads = []
        # the number of victory points
        self.victory_points = 0
        # the cards the player has
        # each will be a number corresponding with the static variables CARD_<type>
        self.cards = []
        # the development cards this player has
        self.dev_cards = []
        # the number of knight cards the player has played
        self.knight_cards = 0
        # the longest road segment this player has
        self.longest_road_length = 0

    # builds a settlement belonging to this player
    def build_settlement(self, point, is_starting=False):

        if not is_starting:
            # makes sure the player has the cards to build a settlements
            cards_needed = [
                ResCard.Wood,
                ResCard.Brick,
                ResCard.Sheep,
                ResCard.Wheat
            ]

            # checks the player has the cards
            if not self.has_cards(cards_needed):
                return Statuses.ERR_CARDS

            # checks it is connected to a road owned by the player
            connected_by_road = False
            # gets the roads
            roads = self.game.board.roads

            for r in roads:
                # checks if the road is connected
                if r.point_one is point or r.point_two is point:
                    # checks this player owns the road
                    if r.owner == self.num:
                        connected_by_road = True

            if not connected_by_road:
                return Statuses.ERR_ISOLATED

        # checks that a building does not already exist there
        if point.building != None:
            return Statuses.ERR_BLOCKED

        # checks all other settlements are at least 2 away
        # gets the connecting point's coords
        points = point.connected_points
        for p in points:

            # checks if the point is occupied
            if p.building != None:
                return Statuses.ERR_BLOCKED

        if not is_starting:
            # removes the cards
            self.remove_cards(cards_needed)

        # adds the settlement
        self.game.board.add_building(Building(
            owner = self.num,
            type = Building.BUILDING_SETTLEMENT,
            point_one = point),
            point = point)
        # adds a victory point
        self.victory_points += 1

        return Statuses.ALL_GOOD

    # checks if the player has all of the cards given in an array
    def has_cards(self, cards):

        # needs to duplicate the cards, and then delete them once found
        # otherwise checking if the player has multiple of the same card
        # will return true with only one card

        # cards_dup stands for cards duplicate
        cards_dup = self.cards[:]
        for c in cards:
            if cards_dup.count(c) == 0:
                return False
            else:
                index = cards_dup.index(c)
                del cards_dup[index]

        return True

    # adds some cards to a player's hand
    def add_cards(self, cards):
        for c in cards:
            self.cards.append(c)

    # removes cards from a player's hand
    def remove_cards(self, cards):
        # makes sure it has all the cards before deleting any
        if not self.has_cards(cards):
            return Statuses.ERR_CARDS

        else:
            # removes the cards
            for c in cards:
                index = self.cards.index(c)
                del self.cards[index]

    #adds a development card
    def add_dev_card(self, dev_card):
        self.dev_cards.append(dev_card)

    # removes a dev card
    def remove_dev_card(self, card):
        # finds the card
        for i in range(len(self.dev_cards)):
            if self.dev_cards[i] == card:

                # deletes the card
                del self.dev_cards[i]
                return Statuses.ALL_GOOD

        # error if the player does not have the cards
        return Statuses.ERR_CARDS

    # checks a road location is valid
    def road_location_is_valid(self, start, end):
        # checks the two points are connected
        connected = False
        # gets the points connected to start
        points = start.connected_points

        for p in points:
            if end == p:
                connected = True
                break

        if not connected:
            return Statuses.ERR_NOT_CON

        connected_by_road = False
        for road in self.game.board.roads:
            # checks the road does not already exists with these points
            if road.point_one == start or road.point_two == start:
                if road.point_one == end or road.point_two == end:
                    return Statuses.ERR_BLOCKED

        # check this player has a settlement on one of these points or a connecting road
        is_connected = False

        if start.building != None:
            # checks if this player owns the settlement/city
            if start.building.owner == self.num:
                is_connected = True

        # does the same for the other point
        elif end.building != None:
            if end.building.owner == self.num:
                is_connected = True

        # then checks if there is a road connecting them
        roads = self.game.board.roads
        points = [start, end]

        for r in roads:
            for p in points:
                if r.point_one == p or r.point_two == p:

                    # checks that there is not another player's settlement here, so that it's not going through it
                    if p.building == None:
                        is_connected = True

                    # if theere is a settlement/city there, the road can be built if this player owns it
                    elif p.building.owner == self.num:
                        is_connected = True

        if not is_connected:
            return Statuses.ERR_ISOLATED

        return Statuses.ALL_GOOD

    # builds a road
    def build_road(self, start, end, is_starting=False):

        # checks the location is valid
        location_status = self.road_location_is_valid(start=start, end=end)

        if not location_status == Statuses.ALL_GOOD:
            return location_status

        # if the road is being created on the starting turn, the player does not needed
        # to have the cards
        if not is_starting:

            # checks that it has the proper cards
            cards_needed = [
                ResCard.Wood,
                ResCard.Brick
            ]
            if not self.has_cards(cards_needed):
                return Statuses.ERR_CARDS

            # removes the cards
            self.remove_cards(cards_needed)

        # adds the road
        road = Building(owner=self.num, type=Building.BUILDING_ROAD, point_one=start, point_two=end)
        (self.game).board.add_road(road)

        self.get_longest_road(new_road=road)

        return Statuses.ALL_GOOD

    # returns an array of all the harbors the player has access to
    def get_connected_harbor_types(self):

        # gets the settlements/cities belonging to this player
        harbors = []
        all_harbors = self.game.board.harbors
        buildings = self.game.board.get_buildings()

        for b in buildings:
            # checks the building belongs to this player
            if b.owner == self.num:
                # checks if the building is connected to any harbors
                for h in all_harbors:
                    print(h)
                    print(b.point)
                    if h.point_one is b.point or h.point_two is b.point:
                        print("A")
                        # adds the type
                        if harbors.count(h.type) == 0:
                            harbors.append(h.type)

        return harbors

    # gets the longest road segment this player has which includes the road given
    # should be called whenever a new road is build
    # since this player's longest road will only change if a new road is build
    def get_longest_road(self, new_road):

        # gets the roads that belong to this player
        roads = self.get_roads()
        del roads[roads.index(new_road)]

        # checks for longest road
        self.check_connected_roads(road=new_road, all_roads=roads, length=1)

    # checks the roads for connected roads, and then checks those roads until there are no more
    def check_connected_roads(self, road, all_roads, length):

        # do both point one and two
        points = [
            road.point_one,
            road.point_two
        ]

        for p in points:
            # gets the connected roads
            connected = self.get_connected_roads(point=p, roads=all_roads)
            # if there are no new connected roads
            if len(connected) == 0:
                # if this is the longest road so far
                if length > self.longest_road_length:
                    # records the length
                    self.longest_road_length = length
                    # self.begin_celebration()

            # if there are connected roads
            else:
                # check each of them for connections if they have not been used
                for c in connected:
                    # checks it hasn't used this road before
                    if all_roads.count(c) > 0:
                        # copies all usable roads
                        c_roads = all_roads[:]
                        # removes this road from them
                        del c_roads[c_roads.index(c)]
                        # checks for connected roads to this road
                        self.check_connected_roads(c, c_roads, length + 1)

    # returns which roads in the roads array are connected to the point
    def get_connected_roads(self, point, roads):
        con_roads = []
        for r in roads:
            if r.point_one == point or r.point_two == point:
                con_roads.append(r)

        return con_roads

    # returns an array of all the roads belonging to this player
    def get_roads(self):
        # gets all the roads on the board
        all_roads = (self.game).board.roads
        # filters out roads that do not belong to this player
        roads = []
        for r in all_roads:
            if r.owner == self.num:
                roads.append(r)

        return roads

    # checks if the player has some development cards
    def has_dev_cards(self, cards):
        card_duplicate = self.dev_cards[:]
        for c in cards:
            if not card_duplicate.count(c) > 0:
                return False
            else:
                del card_duplicate[card_duplicate.index(c)]

        return True

    # returns the number of VP
    # if include_dev is False, it will not include points from developement cards
    # because other players aren't able to see them
    def get_VP(self, include_dev=False):

        # gets the victory points from settlements and cities
        points = self.victory_points

        # adds VPs from longest road
        if self.game.longest_road_owner == self.num:
            points += 2

        # adds VPs from largest army
        if self.game.largest_army == self.num:
            points += 2

        # adds VPs from developement cards
        if include_dev:
            for d in self.dev_cards:
                if d == DevCard.VP:
                    points += 1

        return points

    # prints the cards given
    @staticmethod
    def print_cards(cards):
        print("[")
        for c in cards:

            card_name = ""

            if c == ResCard.Wood:
                card_name = "Wood"

            elif c == ResCard.Sheep:
                card_name = "Sheep"

            elif c == ResCard.Brick:
                card_name = "Brick"

            elif c == ResCard.Wheat:
                card_name = "Wheat"

            elif c == ResCard.Ore:
                card_name = "Ore"

            else:
                print("INVALID CARD %s" % c)
                continue

            if cards.index(c) < len(cards) - 1:
                card_name += ","

            print("    %s" % card_name)

        print("]")
