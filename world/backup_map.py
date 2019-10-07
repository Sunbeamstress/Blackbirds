SYMBOLS = {
    None: "[ ]",
    "You": "[@]",
    "SECT_INSIDE": "[_]"
}

class Map():
    def __init__(self, caller, max_width = 9, max_height = 9):
        self.caller = caller

        max_width = max_width + 1 if max_width % 2 == 0 else max_width
        max_height = max_height + 1 if max_height % 2 == 0 else max_height

        self.max_width = max_width
        self.max_height = max_height
        self.max_worm_distance = (min(max_width, max_height) - 1) / 2
        self.worm_has_mapped = {}
        self.cur_x = None
        self.cur_y = None

        self.grid = self.create_grid()
        self.plot_map_room(caller.location, self.max_worm_distance)

    def create_grid(self):
        board = []
        for row in range(self.max_width):
            board.append([])
            for column in range(self.max_height):
                board[row].append("   ")
        return board

    def plot_map_room(self, room, max_distance):
        self.draw(room)

        if max_distance == 0:
            return

        for dir in room.db.exits:
            dest = room.get_exit_dest(dir)
            if not dest:
                continue

            if self.has_drawn(dest):
                continue

            self.update_position(room, dir)
            self.plot_map_room(dest, max_distance - 1)

    def draw(self, room):
        if room == self.caller.location:
            self.start_loc_on_grid()
            self.worm_has_mapped[room] = [self.cur_x, self.cur_y]
        else:
            self.worm_has_mapped[room] = [self.cur_x, self.cur_y]
            self.grid[self.cur_x][self.cur_y] = SYMBOLS[room.db.symbol]

    def has_drawn(self, room):
        return True if room in self.worm_has_mapped.keys() else False

    def median(self, num):
        lst = sorted(range(0, num))
        n = len(lst)
        m = n - 1
        return (lst[n // 2] + lst[m // 2]) / 2.0

    def start_loc_on_grid(self):
        x, y = self.median(self.max_width), self.median(self.max_height)
        x, y = int(x), int(y)
        self.grid[x][y] = SYMBOLS["You"]
        self.cur_x, self.cur_y = x, y # Update the worm's location.

    def update_position(self, room, exit_name):
        self.cur_x, self.cur_y = self.worm_has_mapped[room][0], self.worm_has_mapped[room][1]

        if exit_name == "northwest":
            self.cur_x += -1
            self.cur_y += -1
        elif exit_name == "north":
            self.cur_x += 0
            self.cur_y += -1
        elif exit_name == "northeast":
            self.cur_x += 1
            self.cur_y += -1
        elif exit_name == "west":
            self.cur_x += -1
            self.cur_y += 0
        elif exit_name == "east":
            self.cur_x += 1
            self.cur_y += 0
        elif exit_name == "southwest":
            self.cur_x += -1
            self.cur_y += 1
        elif exit_name == "south":
            self.cur_x += 0
            self.cur_y += 1
        elif exit_name == "southeast":
            self.cur_x += 1
            self.cur_y += 1

    def draw_map(self):
        map_string = ""
        for row in self.grid:
            map_string += " ".join(row)
            map_string += "\n"

        return map_string