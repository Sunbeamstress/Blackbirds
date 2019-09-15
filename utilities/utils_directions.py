DIRECTION_MAP = ("northwest", "north", "northeast", "west", "east", "southwest", "south", "southeast", "up", "down", "in", "out")
ABBR_DIRECTION_MAP = ("nw", "n", "ne", "w", "e", "sw", "s", "se", "u", "d", "in", "out")
OPP_DIRECTION_MAP = ("southeast", "south", "southwest", "east", "west", "northeast", "north", "southwest", "down", "up", "out", "in")

def get_full_direction(dir):
    dir = dir.lower()

    if dir in DIRECTION_MAP:
        return dir

    if dir in ABBR_DIRECTION_MAP:
        return DIRECTION_MAP[ABBR_DIRECTION_MAP.index(dir)]

    return None

def valid_direction(dir):
    full_dir = get_full_direction(dir)
    return full_dir if full_dir else None

def opposite_direction(dir):
    full_dir = get_full_direction(dir)
    if full_dir:
        return OPP_DIRECTION_MAP[DIRECTION_MAP.index(full_dir)]

    return None