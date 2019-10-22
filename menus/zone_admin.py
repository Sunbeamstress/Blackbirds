from evennia import create_object

from typeclasses.areas import area_list
from typeclasses.zones import Zone
from utilities.string import jleft, jright, sanitize

def _delete_zone(caller, raw_string, **kwargs):
    zone = caller.search("#" + raw_string, global_search = True)
    if not zone:
        caller.error_echo("Something seems to have gone wrong.")

    zone.delete()
    caller.echo(f"Zone {raw_string} was deleted.")

    return "node_delete_zone"

def _delete_zone_room(caller, raw_string, **kwargs):
    zone = caller.ndb._menutree.selected_zone
    r = kwargs.get("selected_room")

    zone.remove_room(r)
    caller.echo("Room removed.")

def _edit_zone_parse_input(caller, raw_string, **kwargs):
    zone = caller.search("#" + str(caller.ndb._menutree.selected_zone), global_search = True)
    if not zone:
        caller.error_echo("Something seems to have gone wrong.")

    input_string = sanitize(raw_string)
    input_list = input_string.split()
    if input_list[0] == "name":
        if len(input_list) <= 1:
            caller.error_echo("You must specify a name.")
            return "node_edit_selected_zone", {"selected_zone": caller.ndb._menutree.selected_zone}

        new_name = input_list[1]
        zone.name = new_name

    elif input_list[0] == "fullname":
        if len(input_list) <= 1:
            caller.error_echo("You must specify the full name of your zone.")
            return "node_edit_selected_zone", {"selected_zone": caller.ndb._menutree.selected_zone}

        new_fullname = " ".join(input_list[1:])
        zone.db.fullname = new_fullname

    elif input_list[0] == "area":
        caller.error_echo("Not yet implemented.")

    elif input_list[0] == "pvp":
        zone.db.open_pvp = not zone.db.open_pvp

    elif input_list[0] == "rooms":
        return "node_edit_selected_zone_rooms", {"selected_zone": caller.ndb._menutree.selected_zone}

    elif input_list[0] == "clearrooms":
        zone.clear_rooms()

    elif input_list[0] == "areas":
        caller.echo(area_list() + "\n")

    return "node_edit_selected_zone", {"selected_zone": caller.ndb._menutree.selected_zone}

def _node_list_zones(caller):
    info = "All currently defined zones:\n"
    for zone in Zone.objects.all():
        info += "\n|513%s|n %s |x%s|n" % (jright(str(zone.id), 5), jleft(zone.name, 24), zone.db.fullname)
    return "zone_admin_base", {"info": info}

def _node_create_zone(caller, raw_string, **kwargs):
    new_zone = create_object("typeclasses.zones.Zone", key = "NewZone")
    caller.echo("Created a new zone.")
    return "node_edit_selected_zone", {"selected_zone": new_zone.id}

def node_delete_zone(caller, raw_string, **kwargs):
    text = "Delete which zone?"
    options = []
    for zone in Zone.objects.all():
        options.append({"key": str(zone.id), "desc": zone.name, "goto": (_delete_zone)})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("zone_admin_base")})

    return text, options

def node_edit_zone(caller, raw_string, **kwargs):
    text = "Which zone will you edit?"

    options = []
    for zone in Zone.objects.all():
        options.append({"key": str(zone.id), "desc": zone.name, "goto": ("node_edit_selected_zone", {"selected_zone": zone.id})})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("zone_admin_base")})

    return text, options

def node_edit_selected_zone_rooms(caller, raw_string, **kwargs):
    caller.ndb._menutree.selected_zone = kwargs.get("selected_zone", None)
    zone = caller.search("#" + str(caller.ndb._menutree.selected_zone), global_search = True)
    if not zone:
        caller.error_echo("Something seems to have gone wrong.")
        return "zone_admin_base"

    text = "Enter a room's number to delete it from the zone."
    options = []

    for i, r in enumerate(zone.db.rooms):
        options.append({"key": str(i), "desc": r.name, "goto": (_delete_zone_room, {"selected_room": r})})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("node_edit_selected_zone", {"selected_zone": caller.ndb._menutree.selected_zone})})

    return text, options

def node_edit_selected_zone(caller, raw_string, **kwargs):
    caller.ndb._menutree.selected_zone = kwargs.get("selected_zone", None)
    zone = caller.search("#" + str(caller.ndb._menutree.selected_zone), global_search = True)
    if not zone:
        caller.error_echo("Something seems to have gone wrong.")
        return "zone_admin_base"

    text = ""
    options = []

    # We display a list of fake menu keys to the user.
    text += "\n|513%s |c|||n %s" % (jright("name", 10), zone.name)
    text += "\n|513%s |c|||n %s" % (jright("fullname", 10), zone.db.fullname)
    text += "\n|513%s |c|||n %s" % (jright("area", 10), zone.db.area)
    text += "\n|513%s |c|||n %s" % (jright("pvp", 10), zone.db.open_pvp)

    text += "\n\n|513%s |c|||n %s" % (jright("rooms", 10), "Edit this zone's rooms.")
    text += "\n|513%s |c|||n %s" % (jright("clearrooms", 10), "Clear all of this zone's rooms.")

    text += "\n\n|513%s |c|||n %s" % (jright("areas", 10), "See a list of areas.")

    # The actual "key" is a flexible input handler.
    options.append({"key": "_default", "goto": (_edit_zone_parse_input)})
    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("node_edit_zone")})

    return text, options

def zone_admin_base(caller, raw_string, **kwargs):
    text = None
    if kwargs.get("info", None):
        text = kwargs.get("info")
    else:
        text = "Choose one of the following options."

    options = (
        {"desc": "See all currently defined zones.", "goto": (_node_list_zones)},
        {"desc": "Create a new zone.", "goto": (_node_create_zone)},
        {"desc": "Delete an existing zone.", "goto": ("node_delete_zone")},
        {"desc": "Edit a zone.", "goto": ("node_edit_zone")},
    )

    return text, options