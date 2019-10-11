from typeclasses.zones import Zone

SYMBOLS = {
    None: " ",
    "you": "@",
    "shop": "$",
}

# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
#  |   |   |   |   |   |   |   |   |
# [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]

class Map():
    def __init__(self, caller, max_width = 9, max_height = 9):
        self.caller = caller

        # Keep the map's dimensions at an odd number, rounded up.
        # Actual value represents how many room nodes to display.
        max_width = max_width + 1 if max_width % 2 == 0 else max_width
        max_height = max_height + 1 if max_height % 2 == 0 else max_height
        # Enforce minimum size of 3 x 3.
        max_width = 3 if max_width <= 0 else max_width
        max_height = 3 if max_height <= 0 else max_height
        self.max_width = max_width
        self.max_height = max_height
        self.x_range = int((self.max_width - 1) / 2)
        self.y_range = int((self.max_height - 1) / 2)
        # Coordinate handling
        self.orig_x = caller.x()
        self.orig_y = caller.y()
        self.orig_z = caller.z()
        self.min_x = self.orig_x - self.x_range
        self.max_x = self.orig_x + self.x_range + 1
        self.min_y = self.orig_y - self.y_range
        self.max_y = self.orig_y + self.y_range + 1
        self.cur_x = None
        self.cur_y = None
        self.cur_z = None

        # Stores the actual appearance of the map.
        self.grid = self._create_grid()
        self.rooms = self._get_zone_rooms(caller.zone())

    def _create_grid(self):
        # Populates self.grid with a blank slate, each node representing a potential room.
        # Existent rooms get filled in appropriately, whereas we treat all blank space as
        # 'the background.'

        # Behold, the legendary double list comprehension
        # TEMP: place a period to represent a blank space
        return [[str(" . ") for col in range(self.min_x, self.max_x)] for row in range(self.min_y, self.max_y)]

    def _get_zone_rooms(self, id):
        pass
        # Gather all rooms in the zone.
        # z = Zone()
        # room_list = z.rooms(id)
        # coord_list = []

        # for r in room_list:
        #     x, y, z = r.db.x, r.db.y, r.db.z
        #     # Throw out any rooms not on our z-level, or outside the map's range.
        #     if z != self.orig_z or (x < self.min_x or x > self.max_x) or (y < self.min_y or y > self.max_y):
        #         continue

        #     coord_list = 

        # return coord_list

    def _populate_grid(self):
        self.cur_x = self.min_x
        self.cur_y = self.min_y

        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):

                self.grid[y][x] = "[ ]"

    def draw_map(self):
        map_string = ""
        for row in self.grid:
            map_string += " ".join(row)
            map_string += "\n\n"

        return map_string