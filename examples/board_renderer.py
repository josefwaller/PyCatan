from pycatan.board import Board
from pycatan.hex_type import HexType
from pycatan.game import Game
from blessings import Terminal
import math

# Render an board object in ascii in the command prompt
class BoardRenderer:

    def __init__(self, board, center):
        self.board = board
        self.center = center
        self.terminal = Terminal()
        # Different colors to use for the 4 players
        self.player_colors = [
            self.terminal.red,
            self.terminal.cyan,
            self.terminal.green,
            self.terminal.yellow
        ]

    def render(self):
        # Clear screen
        print(self.terminal.clear())
        # Render hexes
        for r in self.board.hexes:
            for h in r:
                self.render_hex(h)
        # Render roads
        for r in self.board.roads:
            self.render_road(r)
        # Render points
        for r in self.board.points:
            for p in r:
                self.render_point(p)
        # Reset cursor position
        print(self.terminal.position(0, 0))

    def render_hex(self, hex_obj):
        # the lines needed to draw each hex
        hex_lines = [
            "___",
            "/%s%s\\" % (BoardRenderer.get_hex_type_string(hex_obj.type), str(hex_obj.token_num).rjust(2) if hex_obj.token_num else "  "),
            "\\___/"
        ]
        # Get the x, y coordinates to render the hex
        coords = self.get_render_coords(hex_obj.position[0], hex_obj.position[1])
        # Draw each hex's lines
        for line_index in range(len(hex_lines)):
            # Shift the first line over by 1
            x_offset = 1 if line_index == 0 else 0
            # Get position
            position = self.terminal.move(self.center[1] + line_index + coords[1], x_offset + self.center[0] + coords[0])
            # Print the line
            print(position + hex_lines[line_index])

    # Draw a point on the hex
    def render_point(self, point_obj):
        # Get the building
        building = point_obj.building
        # Check it exists
        if building != None:
            # Check the point's coordinates
            coords = self.get_point_coords(point_obj.position[0], point_obj.position[1])
            # Draw a dot there
            position = self.terminal.move(self.center[1] + coords[1], self.center[0] + coords[0])
            # Get the owner of the point
            owner = building.owner
            print(self.player_colors[owner] + position + "." + self.terminal.normal)

    # Render a road onto the board
    def render_road(self, road_obj):
        # Position to draw the road
        pos = [0, 0]
        # String to draw representing the road
        # Should be either "\", "/" or "___"
        road_str = ""
        # Get the points
        point_one_pos = road_obj.point_one
        point_two_pos = road_obj.point_two
        # Get their coordinates
        p_one_coords = self.get_point_coords(point_one_pos[0], point_one_pos[1])
        p_two_coords = self.get_point_coords(point_two_pos[0], point_two_pos[1])
        # If they're on the same line
        if p_one_coords[1] == p_two_coords[1]:
            # Just draw a line between them
            pos = [min(p_one_coords[0], p_two_coords[0]), p_one_coords[1]]
            road_str = "___"
        else:
            if p_one_coords[0] < p_two_coords[0]:
                if p_one_coords[1] < p_two_coords[1]:
                    road_str = "\\"
                else:
                    road_str = "/"
            else:
                if p_one_coords[1] < p_two_coords[1]:
                    road_str = "/"
                else:
                    road_str = "\\"
            pos = [min(p_one_coords[0], p_two_coords[0]) + 1, max(p_two_coords[1], p_one_coords[1])]

        # Get position
        render_pos = self.terminal.move(pos[1] + self.center[1], pos[0] + self.center[0])
        # Print the road
        print(self.player_colors[road_obj.owner] + render_pos + road_str)
     
    # Get the x, y coordinates for a hex from a row and index
    def get_render_coords(self, row, index):
        # Initial coords
        x = 0
        y = 0
        # Width/Height of each hex
        # Each row is futher left than the previous, so decrease x based on row
        x -= 4 * row
        # Each row is also half a hex further down than the previous one
        y += 1 * row
        # Each index moves the hex down and to the right half a hex each
        x += 4 * index
        y += 1 * index
        # If the row is in the bottom half, it should move the hex down and to the left
        length = len(self.board.hexes)
        if row > length / 2:
            # Move if one hex to the right for every row between its row and the halfway row
            x += 4 * math.ceil(row - length / 2)
            # Move it one hex down for every row between its row and the halfway row
            y += 1 + math.floor(row - length / 2)
        # Return coords
        return [x, y]

    # Get the x, y coordinates for a point from a row and index
    def get_point_coords(self, row, index):
        # Initial coords
        x = 1
        y = 0
        # Each row moves the point down
        # Do different positioning if the row is in the top/bottom half of the board
        half_length = math.floor(len(self.board.points) / 2)
        if row < half_length:
            # Each index moves the point over two
            x += 2 * index
            # Each second index moves the point down one
            y += 1 * math.floor(index / 2)
            # Each row moves the point down and to the left
            x -= 4 * row
            y += 1 * row
        # If the row is in the bottom half, the point should be moved down and to the right
        if row >= half_length:
            diff = row - half_length
            # Move the point to the first position in the bottom row
            x -= 4 * half_length - 2
            y += half_length
            # Move down for each row
            y += 2 * diff
            # Move down and to the right for each index
            y += math.ceil(index / 2)
            x += 2 * index
        # Return point
        return [x, y]


    # Get a 1 letter long string representation on a certain hex type
    @staticmethod
    def get_hex_type_string(hex_type):
        if hex_type == HexType.HILLS:
            return "H"
        elif hex_type == HexType.MOUNTAINS:
            return "M"
        elif hex_type == HexType.PASTURE:
            return "P"
        elif hex_type == HexType.FOREST:
            return "F"
        elif hex_type == HexType.FIELDS:
            # Since F is already used, use W for "wheat"
            return "W"
        elif hex_type == HexType.DESERT:
            return "D"
        else:
            raise Exception("Unknown HexType %s passed to get_hex_type_string" % hex_type)



if __name__ == "__main__":
    g = Game()
    br = BoardRenderer(g.board, [50, 10])
    # Add some settlements
    g.add_settlement(player=0, r=0, i=0, is_starting=True)
    g.add_settlement(player=1, r=2, i=3, is_starting=True)
    g.add_settlement(player=2, r=4, i=1, is_starting=True)
    # Add some roads
    g.add_road(player=0, start=[0, 0], end=[0, 1], is_starting=True)
    g.add_road(player=1, start=[2, 3], end=[2, 2], is_starting=True)
    g.add_road(player=2, start=[4, 1], end=[4, 0], is_starting=True)
    br.render()
