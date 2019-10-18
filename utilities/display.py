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

def header(width = 80, col_string = "|B", label = None, col_label = "|w"):
    if label:
        return "%s--|n %s%s|n %s%s|n" % (col_string, col_label, label, col_string, "-" * (width - (4 + len(label))))

    return "%s%s|n" % (col_string, "-" * width)