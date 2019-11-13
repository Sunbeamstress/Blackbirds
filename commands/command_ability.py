"""
Commands to manipulate or learn about abilities.

The ability's commands themselves are not implemented here.
"""

from commands.command import Command
from typeclasses.abilities import Ability
from utilities.abilities import ability_list, ability_search, get_ability_name, get_ability_description, get_ability_tiers
from utilities.display import header, divider, column
from utilities.string import jleft, jright, wrap

def list_player_abilities(ply):
    ab_list = ability_list()

    string = header("Abilities", color = "m", title_color = "M")

    for ab, lvl in ply.db.abilities.items():
        # Skip over abilities that may have been removed from the game, or
        # are not accessible for whatever reason.
        if not ab in ab_list:
            continue

        lvl_string = f"|500{'||' * lvl}|100{'||' * (3 - lvl)}|n"
        ab_name = ab_list[ab]["name"]
        string += f"\n{' ' * 3}{lvl_string} {ab_name}"

    string += "\n" + divider(color = "m")
    ply.echo(string)

def display_ability_info(ply, ab):
    name = get_ability_name(ab)
    desc = get_ability_description(ab)
    tiers = get_ability_tiers(ab)
    lvl = ply.db.abilities[ab]

    string = header(f"{name} Lv. {lvl}", color = "m", title_color = "M")
    string += f"\n{desc}\n"

    for tier, info in tiers.items():
        info_list = []
        if type(info) is str:
            info_list.append(info)
        else:
            info_list = [i for i in info]

        for i, text in enumerate(info_list):
            prefix = "|_" * 4
            tier_color = "333" if lvl < tier else "W"
            color = "222" if lvl < tier else "w"

            if i == 0:
                prefix = f"  |{tier_color}{tier} |c|||n "

            formatted_text = None
            if text[:4].lower() == "cmd:":
                cmd_text = text[4:].strip()
                cmd_color = "300" if lvl < tier else "R"
                formatted_text = f"{prefix}|{color}Grants use of the |{cmd_color}{cmd_text.upper()}|{color} command."
            else:
                formatted_text = f"{prefix}|{color}{text}|n"


            string += "\n" + wrap(f"{formatted_text}", initial_indent = 2, subsequent_indent = 6)

    string += "\n" + divider(color = "m")

    ply.echo(string)

class CmdAbilities(Command):
    key = "abilities"
    aliases = ["ab", "skill", "skills", "sk", "ability"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        sub_cmd = self.words(1, self.word_count())

        if not sub_cmd:
            list_player_abilities(ply)

        else:
            ab = ability_search(sub_cmd)

            if not ab:
                ply.error_echo(f"There is no ability by the name '{sub_cmd}'.")
                return

            display_ability_info(ply, ab)