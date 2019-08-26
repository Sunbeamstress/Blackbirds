class echo():
    def tar(self, tar, src, tar_str, src_str):
        # tar - target of the echo
        # src - source, object it emanates from (used for pronouns)
        # tar_str - what the target sees
        # src_str - what the source sees

    def tar_room(self, tar, src, tar_str, src_str, room_str):
        # same as tar, but passes a third formatted message to the room
        # room_str - what the room sees

    def room(self, room, str):
        # Echo to room
        pass

    def game(self, str):
        # Echo to game

    def func(self, ply, str):
        ply.msg(f"|w{str}|n")
    

def Notify(title, string):
    """
    Represents standardized and generic OOC messages from the game, most often
    used during system reloads, news updates, etc.
    """
    title = f"|c[|C{title}|c]:|n "
    output_string = title + string
    return output_string