# Python modules.
import re

# Blackbirds modules.
from utilities.utils_string import jleft, jright, sanitize

# Gotta move these to a dedicated file later!
_HUMAN_FILE = """
Humans, sometimes archaically referred to as Man, are a prolific, versatile people, the very species which gave rise to the term 'humanoid'. Though they are found predominantly along coastlines, mountains, woods, and plains, they are comfortable in a wide variety of temperatures and environments, and can be found living almost anywhere.

  |xHeight |c|||n |W120|ncm |c-|n |W215|ncm |c(|W4|n ft |c-|n |W7|n ft|c)|n
     |xAge |c|||n    |W18|n |c-|n |W100|n

  |c-|n Can select almost any archetype, and all but the most exotic abilities.
  |c-|n Can survive in a broad range of temperatures, but suffer greatly at either
    extreme.
  |c-|n Can start as a half-breed, choosing another species from which to draw
    minor benefits.
  |c-|n A half-breed Human counts as either species for the purposes of some
    ability checks.
  |c-|n Are not subject to certain prejudices amidst the state of Brillante.

  |c-|n Excellent for beginners, or for testing character builds.
"""

_CARVEN_FILE = """
Carven are a people spawned from Ninesilver's great deserts, adapted to hot climates, and were the predominant species in the state of Brillante before its occupation. They are characterized by the rapid mutant growth of their bone and chitin, leading to horns, spines, and other appendages in their young teen years, and encrustations of sharp bone over their limbs in middle adulthood.

  |xHeight |c|||n |W150|ncm |c-|n |W215|ncm |c(|W5|n ft |c-|n |W7|n ft|c)|n
     |xAge |c|||n    |W18|n |c-|n |W170|n

  |c-|n Can choose a variety of horns.
  |c-|n Gains exoskeletal growth based on age, which must be treated or worn away.
  |c-|n Comfortable in warm weather, and can never feel too hot.
  |c-|n Cannot move as quickly in cold weather, and will suffer greatly.
  |c-|n Can be given two or four arms.
  |c-|n Four-armed Carven are cumbersone, but fearsomely strong.

  |c-|n A good choice for seasoned players, especially those who enjoy battle.
"""

_SACRILITE_FILE = """
Originating from the taigas of Lightningshield, the Sacrilites are a hardy and cunning people, with thick, furry body hair. They are often likened to predatory cats, for their claws, fur, and elongated ears. Though they can live comfortably indoors or in the shade of Brillante, their homes are in the mountains, and they can roam nude in the snow without a hint of discomfort.

  |xHeight |c|||n |W150|ncm |c-|n |W245|ncm |c(|W5|n ft |c-|n |W9|n ft|c)|n
     |xAge |c|||n    |W18|n |c-|n |W65|n

  |c-|n Can be given fangs or tusks.
  |c-|n Their claws make versatile tools for hunting and rending.
  |c-|n Can climb trees and scale buildings.
  |c-|n Comfortable in cool weather, and can never feel too cold.
  |c-|n Can choose heat-, motion-, or night-vision, each with their own benefits
    and drawbacks.

  |c-|n Recommended for players with a little experience.
"""

_LUUM_FILE = """
The people of Colossus Grove, the seaforest. The Luum have coal-colored flesh, set aglow with bioluminescence. Draped in naturally-occuring blossoms and vines, they are like nothing so much as spirits of the deepest woods, brought into humanoid shape. Owing to the peculiar biome from which they evolved, they are incidentally quite comfortable in real oceanic environs.

  |xHeight |c|||n |W60|ncm |c-|n |W335|ncm |c(|W2|n ft |c-|n |W11|n ft|c)|n
     |xAge |c|||n   |W18|n |c-|n |W1000|n

  |c-|n Restricted from certain intensely physical archetypes and abilities.
  |c-|n Can choose the color and vibrance of their biolight.
  |c-|n Can choose certain extraneous appendages, such as vines or thorns.
  |c-|n Can see perfectly in the dark.
  |c-|n Can briefly survive Neon-rich environs.
  |c-|n Can reproduce asexually.
  |c-|n Can eat almost anything, but must eat often.

  |c-|n Good for players who want a challenge and don't mind limited options.
"""

_IDOL_FILE = """
A warhost of Humanlike automata, numerous enough to comprise a race of their own. With shells of stone, steel, and/or false flesh, no two Idols are the same. Though the great majority of activated Idols were built for killing, the softer, more graceful shapes of others suggest that they may have once belonged to a noble social strata, in an era that time forgot.

  |xHeight |c|||n |W120|ncm |c-|n |W300|ncm |c(|W4|n ft |c-|n |W10|n ft|c)|n
     |xAge |c|||n     |W1|n |c-|n |W1000|n

  |c-|n Suffer numerous archetypal restrictions, but gain access to exclusive
    Idol-based archetypes.
  |c-|n Receive much more detailed information when looking at things.
  |c-|n Do not need to eat, drink, or sleep, but must maintain their fuel levels.
  |c-|n Can passively regenerate fuel with the right parts, albeit slowly.
  |c-|n Do not suffer any fatigue-based penalties, so long as their energy levels
    are maintained.
  |c-|n Can obtain and swap components.
  |c-|n May or may not be anatomically correct.

  |c-|n A difficult species to play; must be unlocked after 200 hours of play time.
"""

def _chargen_base_species_info(caller, raw_string, **kwargs):
    input_string = sanitize(raw_string).lower()

    if input_string == "human" or input_string == "humans":
        caller.echo(_HUMAN_FILE)
        return "chargen_base"
    elif input_string == "carven" or input_string == "carvens":
        caller.echo(_CARVEN_FILE)
        return "chargen_base"
    elif input_string == "sacrilite" or input_string == "sacrilites":
        caller.echo(_SACRILITE_FILE)
        return "chargen_base"
    elif input_string == "luum" or input_string == "luums" or input_string == "loom" or input_string == "looms":
        caller.echo(_LUUM_FILE)
        return "chargen_base"
    elif input_string == "idol" or input_string == "idols":
        caller.echo(_IDOL_FILE)
        return "chargen_base"

def _chargen_select_species(caller, raw_string, **kwargs):
    species = kwargs.get("species", None)

    if not species:
        caller.error_echo("Something went wrong with species selection! Please notify the admin.")
        return "chargen_base"

    caller.db.species = species
    return "chargen_identity"

def _chargen_identity_parse_input(caller, raw_string, **kwargs):
    input_string = sanitize(raw_string)
    input_list = input_string.split()

    sub_cmd = input_list[0]
    no_args = True if len(input_list) <= 1 else False

    if sub_cmd == "name":
        if no_args:
            caller.error_echo("You must specify a name. This can be from 3 to 24 characters.")
            return "chargen_base"

        new_name = input_list[1]
        if len(new_name) < 3 or len(new_name) > 24:
            caller.error_echo(f"Your name must be no fewer than 3 and no greater than 24 characters. You attempted to use {len(new_name)} character(s).")
            return "chargen_base"

        if not new_name.isalpha():
            caller.error_echo("For your first name, you may only use the characters A-Z.")
            return "chargen_base"

        caller.name = new_name

    elif sub_cmd == "surname":
        if no_args:
            caller.error_echo("You must specify a surname. This can be from 3 to 24 characters.")
            return "chargen_base"

        new_name = " ".join(input_list[1:])
        if len(new_name) < 3 or len(new_name) > 24:
            caller.error_echo(f"Your surname must be no fewer than 3 and no greater than 24 characters. You attempted to use {len(new_name)} character(s).")
            return "chargen_base"

        if any(char.isdigit() for char in new_name):
            caller.error_echo("You may not use numbers in your surname.")
            return "chargen_base"

        caller.db.surname = new_name

    return "chargen_base"

def chargen_identity(caller, raw_string, **kwargs):
    text = None

    options = (
        {"key": "_default", "goto": (_chargen_identity_parse_input)},
        {"key": "r", "desc": "Return to species selection.", "goto": "chargen_base"}
    )

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