from evennia.utils import search

from data import visibility as vis

def find_target(ply, tar):
    # A flexible search utility to bring up a viable object based on player input.
    matches = [obj for obj in search.object_search(tar) if obj.access(ply, "view") and obj.visibility == vis.NORMAL]
    return matches[0] if len(matches) else False

def find_living_target(ply, tar):
    # Like find_target() but searches only for players and NPCs.
    matches = [obj for obj in search.object_search(tar) if obj.access(ply, "view") and obj.visibility == vis.NORMAL and obj.account]
    return matches[0] if len(matches) else False