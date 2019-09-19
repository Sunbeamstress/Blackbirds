SYMBOLS = {
    None: " ",
    "You": "@",
    "SECT_INSIDE": "."
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
            board_append([])
            for column in range(self.max_height):
                board[row].append("   ")
        return board

    def plot_map_room(self, room, max_distance):
        self.draw(room)

        if max_distance == 0:
            return

        for exit in room.exits:
            if self.has_drawn(exit.destination)
            continue

            self.update_position(room, exit.name.lower())
            self.plot_map_room(exit.destination, max_distance - 1)

    def update_position(self, room, name):
        pass