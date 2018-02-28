# a  settlement/city class

class Building:

    BUILDING_SETTLEMENT = 0
    BUILDING_ROAD = 1
    BUILDING_CITY = 2

    def __init__(self, owner, type, point_one=None, point_two=None):

        # sets the owner and type
        self.owner = owner
        self.type = type

        # records where it is if it is a road
        if self.type == Building.BUILDING_ROAD:

            self.point_one = point_one
            self.point_two = point_two

        else:
            self.point = point_one

    def __repr__(self):

        if self.type == Building.BUILDING_ROAD:
            return "Road, owned by player %s, from %s to %s" % (self.owner, self.point_one.position, self.point_two.position)

        elif self.type == Building.BUILDING_SETTLEMENT:
            return "Settlement, owned by player %s" % self.owner

        else:
            return "City, owned by player %s" % self.owner
