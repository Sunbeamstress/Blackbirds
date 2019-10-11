from evennia import create_object

from typeclasses.newzones import Zone
from utilities.utils_string import jright

def _delete_zone(caller, raw_string, **kwargs):
    zone = caller.search("#" + raw_string, global_search = True)
    if not zone:
        caller.error_echo("Something seems to have gone wrong.")

    zone.delete()
    caller.echo(f"Zone {raw_string} was deleted.")

    return "zone_admin_base"

def _node_list_zones(caller):
    info = "All currently defined zones:\n"
    for zone in Zone.objects.all():
        info += "\n%s %s" % (jright(5))
    return "zone_admin_base", {"info": info}

def _node_create_zone(caller, raw_string, **kwargs):
    create_object("typeclasses.newzones.Zone", key = "Test")
    info = "Created a new zone."
    return "zone_admin_base", {"info": info}

def node_delete_zone(caller, raw_string, **kwargs):
    text = "Delete which zone?"
    options = []
    for zone in Zone.objects.all():
        options.append({"key": str(zone.id), "desc": zone.key, "goto": (_delete_zone)})

    return text, options

def zone_admin_base(caller, raw_string, **kwargs):
    text = ""
    if kwargs.get("info", None):
        text = kwargs.get("info")
    else:
        text = "Choose one of the following options."

    options = (
        {"desc": "See all currently defined zones.", "goto": (_node_list_zones)},
        {"desc": "Create a new zone.", "goto": (_node_create_zone)},
        {"desc": "Delete an existing zone.", "goto": ("node_delete_zone")},
    )

    return text, options