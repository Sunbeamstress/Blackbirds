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
        self.cur_x = None
        self.cur_y = None

        # Stores the actual appearance of the map.
        self.grid = self.create_grid()

    def create_grid(self):
        board = []
        x_range = int((self.max_width - 1) / 2)
        y_range = int((self.max_height - 1) / 2)
        # Behold, the legendary double list comprehension
        board = [[str(col) for col in range(x_range * -1, x_range + 1)] for row in range(y_range * -1, y_range + 1)]
        return board

    def draw_map(self):
        map_string = ""
        for row in self.grid:
            map_string += " - ".join(row)
            map_string += "\n\n"

        return map_string