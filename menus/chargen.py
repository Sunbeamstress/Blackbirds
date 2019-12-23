# Python modules.
import re, string

# Blackbirds modules.
from server.conf import settings
from typeclasses.species import Human, Carven, Sacrilite, Luum, Idol, Blackbird
from utilities.characters import name_is_taken
from utilities.display import bullet
from utilities.number import cm_to_ft
from utilities.string import jleft, jright, capital, sanitize, an
from world.names import CURRENCY_FULL

_SPAWN_ROOM = settings.SPAWN_LOCATION

def identity_validate(caller):
    # Check the player's name, age, etc. and make sure it's all appropriate for
    # their chosen species.
    valid, err_msg = name_validate(caller.name, caller.name, unusual_names = caller.db.species.unusual_names, check_duplicates = False)
    if valid == False:
        caller.echo(f"|RThe name you have selected is not appropriate for {an(caller.db.species.name)}.|n")
        caller.echo(f"|Y{err_msg}|n")
        return "chargen_identity"

    return "chargen_anatomy"

def anatomy_display(text, val, bool = True):
    conv_val = ""
    if bool:
        conv_val = "|WYes|n" if val == True else "|xNo|n"

    return "%s%s" % (jleft(text, 32), conv_val)

def name_validate(new_name, old_name, unusual_names = False, check_duplicates = True):
    valid = True
    err_msg = ""

    if name_is_taken(new_name) and check_duplicates == True and new_name != old_name:
        valid = False
        err_msg = f"The name {new_name} is already taken. Please use another."

    elif len(new_name) < 3 or len(new_name) > 24:
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


    valid, err_msg = name_validate(new_name, caller.name, unusual_names = caller.db.species.unusual_names)
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


    valid, err_msg = name_validate(new_name, caller.name, unusual_names = caller.db.species.unusual_names)
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

def _init_halfbreed(caller, species):
    # Reinitialize player's Human species.
    caller.db.species = Human()

    if species == "Carven":
        caller.db.halfbreed_family = "Carven"
        caller.db.species.has_horns = True
        caller.db.species.horns_optional = True

    elif species == "Sacrilite":
        caller.db.halfbreed_family = "Sacrilite"
        caller.db.species.has_fangs = True
        caller.db.species.fang_choice = True
        caller.db.species.fangs_optional = True
        caller.db.species.has_tail = True
        caller.db.species.tail_optional = True

    elif species == "Luum":
        caller.db.halfbreed_family = "Luum"
        caller.db.species.has_fangs = True
        caller.db.species.fangs_optional = True
        caller.db.species.has_bioluminescence = True
        caller.db.species.can_eat_anything = True

def anatomy_selection(caller, **kwargs):
    anatomy = kwargs.get("anatomy")

    if anatomy == "breasts":
        caller.db.has_breasts = not caller.db.has_breasts
    elif anatomy == "halfbreed":
        caller.db.is_halfbreed = not caller.db.is_halfbreed
        if caller.db.is_halfbreed == False:
            caller.db.species = Human()
        else:
            _init_halfbreed(caller, "Carven")
    elif anatomy == "halfbreed_family":
        if not caller.db.halfbreed_family:
            _init_halfbreed(caller, "Carven")

        f = caller.db.halfbreed_family
        if f == "Carven":
            _init_halfbreed(caller, "Sacrilite")

        if f == "Sacrilite":
            _init_halfbreed(caller, "Luum")
        if f == "Luum":
            _init_halfbreed(caller, "Carven")
    elif anatomy == "pregnancy":
        caller.db.can_carry_child = not caller.db.can_carry_child
    elif anatomy == "four_arms":
        caller.db.has_four_arms = not caller.db.has_four_arms
    elif anatomy == "horns":
        caller.db.has_horns = not caller.db.has_horns
    elif anatomy == "fangs_toggle":
        caller.db.has_fangs = not caller.db.has_fangs
    elif anatomy == "fangs_style":
        caller.db.fang_desc = "tusks" if caller.db.fang_desc == "fangs" else "fangs"
    elif anatomy == "tail":
        caller.db.has_tail = not caller.db.has_tail
    elif anatomy == "bioluminescence":
        c = caller.db.bioluminescence_desc
        if c == "white":
            caller.db.bioluminescence_desc = "blue"
        elif c == "blue":
            caller.db.bioluminescence_desc = "green"
        elif c == "green":
            caller.db.bioluminescence_desc = "gold"
        elif c == "gold":
            caller.db.bioluminescence_desc = "violet"
        elif c == "violet":
            caller.db.bioluminescence_desc = "red"
        elif c == "red":
            caller.db.bioluminescence_desc = "white"

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
    elif input_string == "blackbird" or input_string == "blackbirds" and caller.check_permstring("Admin"):
        species = Blackbird()

    if species:
        # Basic information.
        caller.echo(species.chargen_documentation["synopsis"])
        caller.echo("\n")

        # Age and height.
        minh_width = len(str(species.min_height)) + 2
        caller.echo(f"  |xHeight |c|||n |W{species.min_height}|ncm |c-|n |W{species.max_height}|ncm |c(|W{cm_to_ft(species.min_height):.0f}|nft |c-|n |W{cm_to_ft(species.max_height):.0f}|nft|c)|n")
        caller.echo(f"     |xAge |c|||n |W{jright(species.min_age, minh_width)}|n |c-|n |W{species.max_age}|n")
        caller.echo("\n")

        qualities = []

        # Add automatically-generated qualities based on species data.
        if species.max_neon > 0:
            qualities.append(f"{'Can survive considerably well' if species.max_neon >= 50 else 'Can survive briefly'} in Neon-rich environments.")
        if species.can_reproduce_asexually:
            qualities.append("Can reproduce asexually.")
        if species.has_horns:
            qualities.append(f"{'Can choose a variety of' if species.horns_optional else 'Has long, powerful'} horns.")
        if species.has_fangs:
            qualities.append(f"{'Can choose to have' if species.fangs_optional else 'Born with'} fangs{' or tusks' if species.fang_choice else ''}.")
        if species.has_tail:
            qualities.append(f"{'May or may not have' if species.tail_optional else 'Has'} a tail.")
        if species.has_claws:
            qualities.append("Their claws make versatile tools for hunting and climbing.")
        if species.has_exoskeleton:
            qualities.append("Gains exoskeletal growth based on age, which must be treated or worn away.")
        if species.can_be_fourarmed:
            qualities.append(f"Can be born either with two or four arms. Four-armed {species.plural_name} are cumbersome, but powerful.")
        if species.can_eat_anything:
            qualities.append("Can eat almost anything, but must eat far more often.")
        if species.precision_information:
            qualities.append("Receives detailed information when looking at things.")

        # Finally, pull from the handwritten quality list.
        for q in species.chargen_documentation["qualities"]:
            qualities.append(q)

        # Produce the quality list.
        for q in qualities:
            caller.echo(bullet(q, indent = 2))

        caller.echo("\n")
        caller.echo(bullet(species.chargen_documentation["difficulty"], indent = 2))

        caller.echo("\n")

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
        if caller.check_permstring("Developer"):
            caller.db.species = Idol()
        else:
            # caller.error_echo("The Idol species will be available to you upon purchasing it with Rubric. Please make another selection.")
            caller.error_echo("The Idol species is unfinished, and currently unavailable. Please make another selection.")
            return "chargen_base"
    elif species == "Blackbird":
        if caller.check_permstring("Admin"):
            caller.db.species = Blackbird()

    return "chargen_identity"

def pronoun_selection(caller, raw_string, **kwargs):
    sel = kwargs.get("pronoun_choice")
    they, them, their, theirs = "they", "them", "their", "theirs"

    if sel == 1:
        they, them, their, theirs = "he", "him", "his", "his"
    elif sel == 2:
        they, them, their, theirs = "she", "her", "her", "hers"
    elif sel == 3:
        they, them, their, theirs = "they", "them", "their", "theirs"
    elif sel == 4:
        they, them, their, theirs = "it", "it", "its", "its"

    caller.db.pronoun_they = they
    caller.db.pronoun_them = them
    caller.db.pronoun_their = their
    caller.db.pronoun_theirs = theirs

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

def chargen_anatomy(caller, raw_string, **kwargs):
    text = f"Here, you'll specify certain aspects of your character's anatomy. Your choices here are dependent on your character's species, and can affect various game mechanics, from the names of clothing slots, to ability use, to the ability to bear children. Please take care in selecting these, as none of these choices are easily altered.\n\nAs {an(caller.db.species.name)}, {caller.name}..."

    options = []

    if caller.db.species.can_halfbreed:
        options.append({"desc": anatomy_display("is a halfbreed.", caller.db.is_halfbreed), "goto": (anatomy_selection, {"anatomy": "halfbreed"})})

    if caller.db.species.can_halfbreed and caller.db.is_halfbreed:
        options.append({"desc": anatomy_display(f"halfbreed family: |W{caller.db.halfbreed_family}|n.", None, bool = False), "goto": (anatomy_selection, {"anatomy": "halfbreed_family"})})

    options.append({"desc": anatomy_display("has breasts.", caller.db.has_breasts), "goto": (anatomy_selection, {"anatomy": "breasts"})})

    if caller.db.species.can_reproduce:
        options.append({"desc": anatomy_display("can become pregnant.", caller.db.can_carry_child), "goto": (anatomy_selection, {"anatomy": "pregnancy"})})

    if caller.db.species.can_be_fourarmed:
        options.append({"desc": anatomy_display("has four arms.", caller.db.has_four_arms), "goto": (anatomy_selection, {"anatomy": "four_arms"})})

    if caller.db.species.has_horns and caller.db.species.horns_optional:
        options.append({"desc": anatomy_display("has horns.", caller.db.has_horns), "goto": (anatomy_selection, {"anatomy": "horns"})})

    if caller.db.species.has_fangs and caller.db.species.fangs_optional:
        options.append({"desc": anatomy_display("has fangs.", caller.db.has_fangs), "goto": (anatomy_selection, {"anatomy": "fangs_toggle"})})

    if caller.db.species.has_fangs and caller.db.species.fang_choice:
        options.append({"desc": anatomy_display(f"fang style: |W{caller.db.fang_desc}|n.", None, bool = False), "goto": (anatomy_selection, {"anatomy": "fangs_style"})})

    if caller.db.species.has_tail and caller.db.species.tail_optional:
        options.append({"desc": anatomy_display("has a tail.", caller.db.has_tail), "goto": (anatomy_selection, {"anatomy": "tail"})})

    if caller.db.species.has_bioluminescence:
        options.append({"desc": anatomy_display(f"has |{caller.bioluminescence_color_code}{caller.db.bioluminescence_desc}|n bioluminescence.", None, bool = False), "goto": (anatomy_selection, {"anatomy": "bioluminescence"})})

    options.append({"key": "n", "desc": "Continue to |RTBD|n.", "goto": "chargen_anatomy"})
    options.append({"key": "r", "desc": "Return to character identity.", "goto": "chargen_identity"})

    return text, options

def chargen_identity(caller, raw_string, **kwargs):
    text = "Next, we'll ask you to fill out some identifying information about your character. It's here that you'll choose a thematically appropriate name, an age, as well as some other details about yourself.\n\nTo change a field, simply type in the name of a |513field|n, along with the desired info. Type in a |513field|n by itself to see what information it will accept. This may change based on your chosen species.\n"

    text += f"\n     |513name|n |c|||n {caller.name}"
    text += f"\n  |513surname|n |c|||n {caller.db.surname}"
    text += f"\n      |513age|n |c|||n {caller.db.age}"
    text += f"\n |513pronouns|n |c|||n {caller.pronouns()}"

    options = (
        {"key": "n", "desc": "Continue to anatomical details.", "goto": identity_validate},
        {"key": "r", "desc": "Return to species selection.", "goto": "chargen_base"},
        {"key": "_default", "goto": (_chargen_identity_parse_input)},
    )

    return text, options

def chargen_base(caller, raw_string, **kwargs):
    text = "To begin, choose the species of your character. Enter the name of the species to read more about them. Enter the number to select the one you want.\n\n|RPlease note that this character generation process is in an unfinished state!|n"

    options = []
    for s in ["Human", "Carven", "Sacrilite", "Luum"]:
        options.append({"desc": s, "goto": (_chargen_select_species, {"species": s})})

    options.append({"desc": "|xIdol|n", "goto": (_chargen_select_species, {"species": "Idol"})})
    if caller.check_permstring("Admin"):
        options.append({"desc": "|415Blackbird|n", "goto": (_chargen_select_species, {"species": "Blackbird"})})

    options.append({"key": "_default", "goto": (_chargen_base_species_info)})

    return text, options