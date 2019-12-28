# Python modules.
import re

# Evennia modules.
from evennia.utils import search

def get_room(name):
    "Produces a valid room object, given a room name."
    room = [r for r in search.object_search(name) if r.__class__.__name__ == "Room"]
    if len(room) > 0:
        return room[0]

    return False

def get_room_id(name):
    "Similar to get_room, but returns its internal database ID. Needed for cases in which the room's data may change but references need to remain the same."
    r = get_room(name)
    if r:
        return f"#{r.id}"

def sanitize_roomname(name):
    "Removes all invalid characters from a room's name, and makes it lowercase for good measure."
    name = re.sub(r"\W+", "", name)

    return name.lower()

def roomname_exists(name):
    r_name = [r for r in search.object_search(name) if r.__class__.__name__ == "Room"]

    if len(r_name) > 0:
        return True

    return False

def inc_roomname(name):
    "Takes the supplied room name and adds _X to it, where X is the next available unused number."
    name = sanitize_roomname(name)

    # See if the given name exists. If not, this is the one to use.
    if not roomname_exists(name):
        return name

    # Strip the "_X" from the name.
    name = re.sub(r"_(\d+)", "", name)

    # Begin with 2 and iterate through numbers until we find one not in use.
    ext = 2
    while roomname_exists(name + "_" + str(ext)):
        ext += 1

    # Voila! This is our new free name.
    return name + "_" + str(ext)