# Blackbirds modules.
from utilities.string import jleft, jright, wrap

class echo():
    def tar(self, tar, src, tar_str, src_str):
        # tar - target of the echo
        # src - source, object it emanates from (used for pronouns)
        # tar_str - what the target sees
        # src_str - what the source sees
        pass

    def tar_room(self, tar, src, tar_str, src_str, room_str):
        # same as tar, but passes a third formatted message to the room
        # room_str - what the room sees
        pass

    def room(self, room, str):
        # Echo to room
        pass

    def game(self, str):
        # Echo to game
        pass

    def func(self, ply, str):
        ply.msg(f"|w{str}|n")
    

def notify(title, string):
    """
    Represents standardized and generic OOC messages from the game, most often
    used during system reloads, news updates, etc.
    """
    title = f"|c[|C{title}|c]:|n "
    output_string = title + string
    return output_string

def divider(width = 80, color = "B", indent = 0, symbol = "-"):
    width -= indent * 2
    return "%s|%s%s|n" % (" " * indent, color, symbol * width)

def header(title, width = 80, color = "B", title_color = "W", indent = 0, symbol = "-"):
    color = str(color)
    title_color = str(title_color)
    width -= 4 + len(title) + (indent * 2)

    if not title:
        return divider(width, color, indent, symbol)

    return "%s|%s%s |%s%s |%s%s|n" % (" " * indent, color, symbol * 2, title_color, title, color, symbol * width)

def column(title, value, title_width = None, value_width = None, indent = 2, title_color = "x", value_color = "w", col_color = "c"):
    title_width = title_width if title_width else len(str(title))
    value_width = value_width if value_width else len(str(value))

    title = str(title)
    value = str(value)

    string = "%s|%s%s|n |%s|||n |%s%s|n" % (" " * indent, title_color, jright(title, title_width), col_color, value_color, jleft(value, value_width))

    return string

def bullet(string, width = 80, color = "c", indent = 1):
    prefix = "%s|%s-|n " % (" " * indent, color)
    if not string:
        return prefix

    string = wrap(prefix + string, initial_indent = 1, subsequent_indent = 3)

    return string