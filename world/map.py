from typeclasses.zones import Zone
from utilities.display import header

SYMBOLS = {
    None: " ",
    "you": "@",
    "shop": "$",
}

# For use with Map._populate_grid(); shifts exit directions appropriately.
DIR_SHIFT = {
    "northwest": (0.5, -0.5),
    "north": (0.5, 0),
    "northeast": (0.5, 0.5),
    "west": (0, -0.5),
    "east": (0, 0.5),
    "southwest": (-0.5, -0.5),
    "south": (-0.5, 0),
    "southeast": (-0.5, 0.5)
}

DIR_SYM = {
    "northwest": "\\",
    "north": " || ",
    "northeast": "/",
    "west": "-",
    "east": "-",
    "southwest": "/",
    "south": " || ",
    "southeast": "\\"
}

class Map():
    def __init__(self, caller, max_width = 9, max_height = 9):
        self.caller = caller

        # Keep the map's dimensions at an odd number, rounded up.
        # Actual value represents how many room nodes to display.
        max_width = max_width + 1 if max_width % 2 == 0 else max_width
        max_height = max_height + 1 if max_height % 2 == 0 else max_height

        # Enforce minimum size of 3 x 3.
        max_width = 3 if max_width <= 3 else max_width
        max_height = 3 if max_height <= 3 else max_height
        # Enforce maximum size of 19 x 19.
        max_width = 19 if max_width > 19 else max_width
        max_height = 19 if max_height > 19 else max_height
        self.max_width = max_width
        self.max_height = max_height
        self.x_range = int((self.max_width - 1) / 2)
        self.y_range = int((self.max_height - 1) / 2)

        # Coordinate handling
        self.orig_x = caller.x()
        self.orig_y = caller.y()
        self.orig_z = caller.z()
        self.min_x = (self.orig_x - self.x_range)
        self.max_x = (self.orig_x + self.x_range) + 1
        self.min_y = (self.orig_y - self.y_range) - 1
        self.max_y = (self.orig_y + self.y_range)

        # Stores the actual appearance of the map.
        self.grid = self._create_grid()
        self.rooms = self._get_zone_rooms(caller.zone())

    def _create_grid(self):
        # Populates self.grid with a blank slate, each node representing a potential room.
        # Existent rooms get filled in appropriately, whereas we treat all blank space as
        # 'the background.'

        g_list = {}
        # We create the table upside down, since higher y coordinates should be 'northward'.
        for y in range(self.max_y, self.min_y, -1):
            g_list[y + 0.5] = {}
            g_list[y] = {}
            for x in range(self.min_x, self.max_x):
                g_list[y + 0.5][x - 0.5] = " "
                g_list[y + 0.5][x] = "   "
                g_list[y][x - 0.5] = " "
                g_list[y][x] = "   "
            g_list[y + 0.5][self.max_x + 0.5] = " "
            g_list[y][self.max_x + 0.5] = "   "

        g_list[self.min_y - 0.5] = {}
        for x in range(self.min_x, self.max_x):
            g_list[self.min_y - 0.5][x - 0.5] = " "
            g_list[self.min_y - 0.5][x] = "   "
        g_list[self.min_y - 0.5][self.max_x + 0.5] = " "

        return g_list

    def _get_zone_rooms(self, id):
        zone = self.caller.zone()
        if not zone:
            return {}

        r_list = {}
        for room in zone.rooms():
            y, x, z = room.db.y, room.db.x, room.db.z
            if self.min_y < y < self.max_y and self.min_x < x < self.max_x and room.db.z == self.caller.z():
                if y not in r_list.keys():
                    r_list[y] = {}

                r_list[y][x] = room

        return r_list

    def _populate_grid(self):
        # Fill grid with appropriate rooms.
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                if y in self.rooms.keys() and x in self.rooms[y]:
                    # Iterate over the room's exits to tag appropriate exit nodes with a symbol.
                    for e_dir in self.rooms[y][x].get_exits():
                        shift_y, shift_x = 0, 0
                        if e_dir in DIR_SHIFT:
                            shift_y, shift_x = DIR_SHIFT[e_dir][0], DIR_SHIFT[e_dir][1]

                        # if shift_y != 0 and shift_x != 0:
                        sym = DIR_SYM[e_dir]
                        self.grid[y + shift_y][x + shift_x] = f"|w{sym}|n"

                    # Set the room's node to its environment color.
                    color = self.rooms[y][x].environment_color()
                    self.grid[y][x] = "|%s[|n |%s]|n" % (color, color)

    def draw_map(self):
        self._populate_grid()

        string = ""
        string_row = ""
        ply_x, ply_y = str(self.caller.x()), str(self.caller.y())

        string_header = "|113%s|n\n" % ("-" * ((4 * self.max_width) + 2))
        string_footer = header(f"x{ply_x}, y{ply_y}",
            width = (4 * self.max_width) + 2,
            color = "113",
            title_color = "314"
        )

        for y in self.grid:
            for x in self.grid[y]:
                string_row += self.grid[y][x]
            string += string_row + "\n"
            string_row = ""

        return string_header + string + string_footer
        # return string_header + string + string_footer + "\n\n" + str(self.grid)
        # return str(self.grid)