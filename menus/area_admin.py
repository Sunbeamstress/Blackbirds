from evennia import create_object

from typeclasses.areas import Area
from utilities.utils_string import jleft, jright, sanitize

def _delete_area(caller, raw_string, **kwargs):
    area = caller.search("#" + raw_string, global_search = True)
    if not area:
        caller.error_echo("Something seems to have gone wrong.")

    area.delete()
    caller.echo(f"Area {raw_string} was deleted.")

    return "node_delete_area"

def _edit_area_parse_input(caller, raw_string, **kwargs):
    area = caller.search("#" + str(caller.ndb._menutree.selected_area), global_search = True)
    if not area:
        caller.error_echo("Something seems to have gone wrong.")

    input_string = sanitize(raw_string)
    input_list = input_string.split()
    if input_list[0] == "name":
        if len(input_list) <= 1:
            caller.error_echo("You must specify a name.")
            return "node_edit_selected_area", {"selected_area": caller.ndb._menutree.selected_area}

        new_name = input_list[1]
        area.name = new_name

    elif input_list[0] == "fullname":
        if len(input_list) <= 1:
            caller.error_echo("You must specify the full name of your area.")
            return "node_edit_selected_area", {"selected_area": caller.ndb._menutree.selected_area}

        new_fullname = " ".join(input_list[1:])
        area.db.fullname = new_fullname

    elif input_list[0] == "city":
        area.db.is_city = not area.db.is_city

    elif input_list[0] == "pvp":
        area.db.open_pvp = not area.db.open_pvp

    return "node_edit_selected_area", {"selected_area": caller.ndb._menutree.selected_area}

def _node_list_areas(caller):
    info = "All currently defined areas:\n"
    for area in Area.objects.all():
        info += "\n|513%s|n %s |x%s|n" % (jright(str(area.id), 5), jleft(area.name, 24), area.db.fullname)
    return "area_admin_base", {"info": info}

def _node_create_area(caller, raw_string, **kwargs):
    new_area = create_object("typeclasses.areas.Area", key = "NewArea")
    caller.echo("Created a new area.")
    return "node_edit_selected_area", {"selected_area": new_area.id}

def node_delete_area(caller, raw_string, **kwargs):
    text = "Delete which area?"
    options = []
    for area in Area.objects.all():
        options.append({"key": str(area.id), "desc": area.name, "goto": (_delete_area)})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("area_admin_base")})

    return text, options

def node_edit_area(caller, raw_string, **kwargs):
    text = "Which area will you edit?"

    options = []
    for area in Area.objects.all():
        options.append({"key": str(area.id), "desc": area.name, "goto": ("node_edit_selected_area", {"selected_area": area.id})})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("area_admin_base")})

    return text, options

def node_edit_selected_area(caller, raw_string, **kwargs):
    caller.ndb._menutree.selected_area = kwargs.get("selected_area", None)
    area = caller.search("#" + str(caller.ndb._menutree.selected_area), global_search = True)
    if not area:
        caller.error_echo("Something seems to have gone wrong.")

    text = ""
    options = []

    # We display a list of fake menu keys to the user.
    text += "\n|513%s |c|||n %s" % (jright("name", 10), area.name)
    text += "\n|513%s |c|||n %s" % (jright("fullname", 10), area.db.fullname)
    text += "\n|513%s |c|||n %s" % (jright("city", 10), area.db.is_city)
    text += "\n|513%s |c|||n %s" % (jright("pvp", 10), area.db.open_pvp)

    # The actual "key" is a flexible input handler.
    options.append({"key": "_default", "goto": (_edit_area_parse_input)})
    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("node_edit_area")})

    return text, options

def area_admin_base(caller, raw_string, **kwargs):
    text = None
    if kwargs.get("info", None):
        text = kwargs.get("info")
    else:
        text = "Choose one of the following options."

    options = (
        {"desc": "See all currently defined areas.", "goto": (_node_list_areas)},
        {"desc": "Create a new area.", "goto": (_node_create_area)},
        {"desc": "Delete an existing area.", "goto": ("node_delete_area")},
        {"desc": "Edit an area.", "goto": ("node_edit_area")},
    )

    return text, options