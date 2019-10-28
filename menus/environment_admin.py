import re

from evennia import create_object

from typeclasses.environments import Environment
from utilities.string import jleft, jright, sanitize

def _delete_environment(caller, raw_string, **kwargs):
    env = caller.search("#" + raw_string, global_search = True)
    if not env:
        caller.error_echo("Something seems to have gone wrong.")

    env.delete()
    caller.echo(f"Environment {raw_string} was deleted.")

    return "node_delete_environment"

def _edit_environment_parse_input(caller, raw_string, **kwargs):
    env = caller.search("#" + str(caller.ndb._menutree.selected_env), global_search = True)
    if not env:
        caller.error_echo("Something seems to have gone wrong.")

    input_string = sanitize(raw_string)
    input_list = input_string.split()
    if input_list[0] == "name":
        if len(input_list) <= 1:
            caller.error_echo("You must specify a name.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        new_name = " ".join(input_list[1:])
        env.name = new_name

    elif input_list[0] == "short":
        if len(input_list) <= 1:
            caller.error_echo("You must specify a valid shortname for your environment.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        if len(input_list[1]) > 5:
            caller.error_echo("The shortname of the zone must be no more than five characters.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        new_short = input_list[1]
        env.db.short = new_short.lower()

    elif input_list[0] == "color":
        if len(input_list) <= 1:
            caller.error_echo("You must specify a 3-digit color code for your environment.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        new_color = input_list[1]
        if len(new_color) != 3:
            caller.error_echo("The color of the environment must be precisely 3 digits.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        reg = re.search(r"[0-5][0-5][0-5]", new_color)
        if not reg:
            caller.error_echo("You may only use the numbers 0-5 for your environment's color.")
            return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

        env.db.color = new_color

    elif input_list[0] == "natural":
        env.db.natural = not env.db.natural

    return "node_edit_selected_environment", {"selected_env": caller.ndb._menutree.selected_env}

def _node_list_environments(caller):
    info = "All currently defined environments:\n"
    for env in Environment.objects.all():
        info += "\n|513%s|n %s |x%s|n" % (jright(str(env.id), 5), jleft(env.name, 24), env.short())
    return "environment_admin_base", {"info": info}

def _node_create_environment(caller, raw_string, **kwargs):
    new_env = create_object("typeclasses.environments.Environment", key = "NewEnvironment")
    caller.echo("Created a new environment.")
    return "node_edit_selected_environment", {"selected_env": new_env.id}

def node_delete_environment(caller, raw_string, **kwargs):
    text = "Delete which environment?"
    options = []
    for env in Environment.objects.all():
        options.append({"key": str(env.id), "desc": env.name, "goto": (_delete_environment)})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("environment_admin_base")})

    return text, options

def node_edit_environment(caller, raw_string, **kwargs):
    text = "Which environment will you edit?"

    options = []
    for env in Environment.objects.all():
        options.append({"key": str(env.id), "desc": env.name, "goto": ("node_edit_selected_environment", {"selected_env": env.id})})

    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("environment_admin_base")})

    return text, options

def node_edit_selected_environment(caller, raw_string, **kwargs):
    caller.ndb._menutree.selected_env = kwargs.get("selected_env", None)
    env = caller.search("#" + str(caller.ndb._menutree.selected_env), global_search = True)
    if not env:
        caller.error_echo("Something seems to have gone wrong.")
        return "environment_admin_base"

    text = ""
    options = []

    # We display a list of fake menu keys to the user.
    text += "\n|513%s |c|||n %s" % (jright("name", 10), env.name)
    text += "\n|513%s |c|||n %s" % (jright("short", 10), env.short())
    text += "\n|513%s |c|||n |%s%s|n" % (jright("color", 10), env.color(), env.color())
    text += "\n|513%s |c|||n %s" % (jright("natural", 10), str(env.is_natural()))

    # The actual "key" is a flexible input handler.
    options.append({"key": "_default", "goto": (_edit_environment_parse_input)})
    options.append({"key": "r", "desc": "Return to the previous menu.", "goto": ("node_edit_environment")})

    return text, options

def environment_admin_base(caller, raw_string, **kwargs):
    text = None
    if kwargs.get("info", None):
        text = kwargs.get("info")
    else:
        text = "Choose one of the following options."

    options = (
        {"desc": "See all currently defined environments.", "goto": (_node_list_environments)},
        {"desc": "Create a new environment.", "goto": (_node_create_environment)},
        {"desc": "Delete an existing environment.", "goto": ("node_delete_environment")},
        {"desc": "Edit a environment.", "goto": ("node_edit_environment")},
    )

    return text, options