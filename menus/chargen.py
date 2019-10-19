# Python modules.
import re, string

# Blackbirds modules.
from typeclasses.species import Human, Carven, Sacrilite, Luum, Idol
from utilities.string import jleft, jright, capital, sanitize, article
from world.names import CURRENCY_FULL

_VALID_UNUSUAL_NAME_CHARS = string.ascii_letters + string.digits + "-" + "." + "'"

def anatomy_display(text, val):
    conv_val = "|xNo|n"
    if val == True:
        conv_val = "|WYes|n"

    return "%s%s" % (jleft(text, 32), conv_val)

def name_validate(new_name, unusual_names = False):
    valid = True
    err_msg = ""

    if len(new_name) < 3 or len(new_name) > 24:
        valid = False
        err_msg = f"Your name must be no fewer than 3 and no greater than 24 characters. You attempted to use {len(new_name)} character(s)."

    elif not new_name.isalpha():
        if unusual_names == False:
            valid = False
            err_msg = "For your name, you may only use the characters A-Z."

        elif new_name.isspace():
            valid = False
            err_msg = "As funny as it would be, I'm afraid you can't have a name consisting only of spaces."

        elif not re.search("^[a-zA-Z0-9\-\.\']+$", new_name):
            valid = False
            err_msg = "You attempted to use one or more invalid characters in your name. You may use only letters, numbers, dashes, periods, and apostrophes."


        elif not re.search("[a-zA-Z]", new_name):
            valid = False
            err_msg = "Your name must include at least one letter."

        elif not new_name[0].isalpha():
            valid = False
            err_msg = "The first character of your name must be a letter."

    return valid, err_msg

def name_selection(caller, new_name = None, no_args = False):
    if no_args:
        caller.echo("|RYou must specify a name. This can be from 3 to 24 characters.|n")
        if caller.db.species.unusual_names:
            caller.echo("\n |c-|n You may use letters, numbers, dashes, periods, or apostrophes.")
            caller.echo("\n |c-|n Your name must start with a letter.")
            caller.echo("\n |c-|n You do not have to capitalize the first letter of your name.")
        else:
            caller.echo("\n |c-|n You may only use letters.")
            caller.echo("\n |c-|n Your name will be automatically capitalized, with the rest converted to")
            caller.echo("\n   lowercase.")
        caller.echo("\n")
        return

    new_name = new_name.strip()


    valid, err_msg = name_validate(new_name, caller.db.species.unusual_names)
    if valid == False:
        caller.echo(f"|R{err_msg}|n")
        return

    if caller.db.species.unusual_names == False:
        # Python's built-in capitalize() forces the rest of the string to be lowercase.
        new_name = new_name.capitalize()

    if new_name.lower() == "clear":
        caller.echo("|RSorry, you will have to have a name!|n\n")
    else:
        caller.name = new_name

def surname_selection(caller, new_name = None, no_args = False):
    if no_args:
        caller.echo("|RYou must specify a surname. This can be from 3 to 24 characters.|n")
        if caller.db.species.unusual_names:
            caller.echo("\n |c-|n You may use letters, numbers, dashes, periods, or apostrophes.")
            caller.echo("\n |c-|n Your surname must start with a letter.")
            caller.echo("\n |c-|n You do not have to capitalize the first letter of your surname.")
        else:
            caller.echo("\n |c-|n You may only use letters.")
            caller.echo("\n |c-|n Your surname will be automatically capitalized, with the rest converted to")
            caller.echo("\n   lowercase.")
        if not caller.db.species.requires_surname:
            caller.echo("\n\n |c-|n You may opt not to have a surname by entering |Rsurname clear|n.")
        caller.echo("\n")
        return

    new_name = new_name.strip()


    valid, err_msg = name_validate(new_name, caller.db.species.unusual_names)
    if valid == False:
        caller.echo(f"|R{err_msg}|n")
        return

    if caller.db.species.unusual_names == False:
        new_name = capital(new_name) # We won't lowercase in the event of names like McGee

    if new_name.lower() == "clear":
        caller.db.surname = ""
    else:
        caller.db.surname = new_name

def age_selection(caller, new_age = None):
    min_age = caller.db.species.min_age
    max_age = caller.db.species.max_age

    if not new_age:
        caller.echo(f"|RYou must specify an age. For your species, this can be anywhere from {min_age} to {max_age}.\n")
        return

    if not new_age.isnumeric():
        caller.echo("|RYou must enter a number.|n\n")
        return

    new_age = int(new_age)
    if new_age < min_age:
        caller.echo(f"|RYour character must be at least {min_age} years of age.|n\n")
        return

    if new_age > max_age:
        caller.echo(f"|RYour character can be no older than {max_age} years of age.|n\n")
        return

    caller.db.age = new_age

def anatomy_selection(caller, **kwargs):
    anatomy = kwargs.get("anatomy")

    if anatomy == "breasts":
        caller.db.has_breasts = not caller.db.has_breasts
    elif anatomy == "pregnancy":
        caller.db.can_carry_child = not caller.db.can_carry_child
    elif anatomy == "four_arms":
        caller.db.has_four_arms = not caller.db.has_four_arms

def _chargen_base_species_info(caller, raw_string, **kwargs):
    input_string = sanitize(raw_string).lower()

    species = None
    if input_string == "human" or input_string == "humans":
        species = Human()
    elif input_string == "carven" or input_string == "carvens":
        species = Carven()
    elif input_string == "sacrilite" or input_string == "sacrilites":
        species = Sacrilite()
    elif input_string == "luum" or input_string == "luums" or input_string == "loom" or input_string == "looms":
        species = Luum()
    elif input_string == "idol" or input_string == "idols":
        species = Idol()

    if species:
      caller.echo(species.chargen_documentation + "\n")

    return "chargen_base"

def _chargen_select_species(caller, raw_string, **kwargs):
    species = kwargs.get("species", None)

    if not species:
        caller.error_echo("Something went wrong with species selection! Please notify the admin.")
        return "chargen_base"

    if species == "Human":
        caller.db.species = Human()
    elif species == "Carven":
        caller.db.species = Carven()
    elif species == "Sacrilite":
        caller.db.species = Sacrilite()
    elif species == "Luum":
        caller.db.species = Luum()
    elif species == "Idol":
        caller.db.species = Idol()

    return "chargen_identity"

def pronoun_selection(caller, raw_string, **kwargs):
    sel = kwargs.get("pronoun_choice")
    he, him, his, hiss = "he", "him", "his", "his"

    if sel == 1:
        pass
    elif sel == 2:
        he, him, his, hiss = "she", "her", "her", "hers"
    elif sel == 3:
        he, him, his, hiss = "they", "them", "their", "theirs"
    elif sel == 4:
        he, him, his, hiss = "it", "it", "its", "its"

    caller.db.pronoun_he = he
    caller.db.pronoun_him = him
    caller.db.pronoun_his = his
    caller.db.pronoun_hiss = hiss

    return "chargen_identity"

def _chargen_identity_parse_input(caller, raw_string, **kwargs):
    input_string = sanitize(raw_string)
    input_list = input_string.split()

    sub_cmd = input_list[0]
    no_args = True if len(input_list) <= 1 else False

    if sub_cmd == "name":
        name_selection(caller, " ".join(input_list[1:]), no_args)

    elif sub_cmd == "surname" or sub_cmd == "lastname":
        surname_selection(caller, " ".join(input_list[1:]), no_args)

    elif sub_cmd == "age":
        if no_args:
            age_selection(caller, None)
        else:
            age_selection(caller, input_list[1])

    elif sub_cmd == "pronoun" or sub_cmd == "pronouns":
        return "chargen_pronoun_menu"

    return "chargen_identity"

def chargen_pronoun_menu(caller, raw_string, **kwargs):
    text = "You may choose from the following pronouns for your character. These will affect the way your character is referred to throughout the game, as well as which pronouns appear when you are the target of emotes or combat skills.\n\nYou may change these at any time."

    options = (
        {"desc": "he, him, his, his", "goto": (pronoun_selection, {"pronoun_choice": 1})},
        {"desc": "she, her, her, hers", "goto": (pronoun_selection, {"pronoun_choice": 2})},
        {"desc": "they, them, their, theirs", "goto": (pronoun_selection, {"pronoun_choice": 3})},
        {"desc": "it, it, its, its", "goto": (pronoun_selection, {"pronoun_choice": 4})},
        {"key": "r", "desc": "Return to character identity.", "goto": "chargen_identity"},
    )

    return text, options

def chargen_archetype(caller, raw_string, **kwargs):
    text = "Your |Warchetype|n is analogous to a character class/job in other games. In Blackbirds you can build your character to excel at most abilities - archetypes, then, are a way of expressing that your character is very specialized in certain of these abilities. As there are numerous archetypes and they affect even more numerous abilities, it is recommended you find the time to read about them in the help files at your earliest convenience."

    options = (
        {"desc": f"Archetype: {caller.archetype()}", "goto": "chargen_archetype"},
        {"key": "r", "desc": "Return to character anatomy.", "goto": "chargen_anatomy"},
    )

    return text, options

def chargen_anatomy(caller, raw_string, **kwargs):
    text = f"Here, you'll specify certain aspects of your character's anatomy. Your choices here are dependent on your character's species, and can affect various game mechanics, from clothing slots, to ability use, to the ability to bear children. Please take care in selecting these, as none of these choices are easily altered.\n\nAs {article(caller.db.species.name)}, {caller.name}..."

    options = []
    options.append({"desc": anatomy_display("has breasts.", caller.db.has_breasts), "goto": (anatomy_selection, {"anatomy": "breasts"})})

    if caller.db.species.can_reproduce:
        options.append({"desc": anatomy_display("can become pregnant.", caller.db.can_carry_child), "goto": (anatomy_selection, {"anatomy": "pregnancy"})})

    if caller.db.species.can_be_fourarmed:
        options.append({"desc": anatomy_display("has four arms.", caller.db.has_four_arms), "goto": (anatomy_selection, {"anatomy": "four_arms"})})

    options.append({"key": "n", "desc": "Continue to archetype.", "goto": "chargen_archetype"})
    options.append({"key": "r", "desc": "Return to character identity.", "goto": "chargen_identity"})

    return text, options

def chargen_identity(caller, raw_string, **kwargs):
    text = "Next, we'll ask you to fill out some identifying information about your character. It's here that you'll choose a thematically appropriate name, an age, as well as some other details about yourself.\n\nTo change a field, simply type in the name of a |513field|n, along with the desired info. Type in a |513field|n by itself to see what information it will accept. This may change based on your chosen species.\n"

    text += f"\n     |513name|n |c|||n {caller.name}"
    text += f"\n  |513surname|n |c|||n {caller.db.surname}"
    text += f"\n      |513age|n |c|||n {caller.db.age}"
    text += f"\n |513pronouns|n |c|||n {caller.db.pronoun_he}, {caller.db.pronoun_him}, {caller.db.pronoun_his}, {caller.db.pronoun_hiss}"

    options = (
        {"key": "n", "desc": "Continue to anatomical details.", "goto": "chargen_anatomy"},
        {"key": "r", "desc": "Return to species selection.", "goto": "chargen_base"},
        {"key": "_default", "goto": (_chargen_identity_parse_input)},
    )

    return text, options

def chargen_base(caller, raw_string, **kwargs):
    text = "To begin, choose the species of your character. Enter the name of the species to read more about them. Enter the number to select the one you want."

    options = (
        {"desc": "Human", "goto": (_chargen_select_species, {"species": "Human"})},
        {"desc": "Carven", "goto": (_chargen_select_species, {"species": "Carven"})},
        {"desc": "Sacrilite", "goto": (_chargen_select_species, {"species": "Sacrilite"})},
        {"desc": "Luum", "goto": (_chargen_select_species, {"species": "Luum"})},
        {"desc": "Idol", "goto": (_chargen_select_species, {"species": "Idol"})},
        {"key": "_default", "goto": (_chargen_base_species_info)},
    )

    return text, options