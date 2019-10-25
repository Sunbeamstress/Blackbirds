from typeclasses.zones import Zone
from utilities.display import header

SYMBOLS = {
    None: " ",
    "you": "@",
    "shop": "$",
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
        self.min_x = (self.orig_x - self.x_range) - 1
        self.max_x = (self.orig_x + self.x_range) + 1
        self.min_y = (self.orig_y - self.y_range) - 1
        self.max_y = (self.orig_y + self.y_range) + 1

        # Stores the actual appearance of the map.
        self.grid = self._create_grid()
        self.rooms = self._get_zone_rooms(caller.zone())

    def _create_grid(self):
        # Populates self.grid with a blank slate, each node representing a potential room.
        # Existent rooms get filled in appropriately, whereas we treat all blank space as
        # 'the background.'

        g_list = {}
        for y in range(self.min_y, self.max_y):
            g_list[y] = {}
            for x in range(self.min_x, self.max_x):
                g_list[y][x] = "|x_|n"

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
                    r_list[y] = []

                r_list[y].append(x)

        return r_list

    def _populate_grid(self):
        # Fill grid with appropriate rooms.
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                if y in self.rooms.keys() and x in self.rooms[y]:
                    self.grid[y][x] = "|Y!|n"

    def draw_map(self):
        self._populate_grid()

        string = ""
        string_row = ""
        ply_x, ply_y = str(self.caller.x()), str(self.caller.y())

        string_header = "|113%s|n\n" % ("-" * ((4 * self.max_width) - 1))
        string_footer = header(f"x{ply_x}, y{ply_y}",
            width = (4 * self.max_width) - 1,
            color = "113",
            title_color = "314"
        )

        for y in range(self.max_y - 1, self.min_y, -1):
            for x in range(self.min_x + 1, self.max_x):
                string_row += self.grid[y][x]
            string += string_row + "\n"
            string_row = ""

        return string_header + string + string_footer
        # return str(self.grid)