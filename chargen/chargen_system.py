from utilities.display import header
from utilities.string import jleft, jright

def column_data(field, result):
    return "|m%s |c|| |w%s|n" % (jright(field, 14), result)

def ChargenStage1(ply):
    string = header(col_string = "|035", label = "Character Creation", col_label = "|055")
    string += "\nMake yourself, so long as you make yourself free!"

    string += "\n"
    string += "\n" + column_data("Name", ply.name)
    string += "\n" + column_data("Surname", ply.db.surname)
    string += "\n" + column_data("Age", ply.db.age)
    string += "\n" + column_data("Apparent Age", ply.db.app_age)
    string += "\n" + column_data("Identity", ply.db.intro)
    string += "\n" + column_data("Pronouns", f"{ply.db.pronoun_he}, {ply.db.pronoun_him}, {ply.db.pronoun_his}, {ply.db.pronoun_hiss}")

    string += "\n"
    string += "\n" + column_data("Species", ply.db.species)
    string += "\n" + column_data("Archetype", ply.db.archetype)
    string += "\n" + column_data("Background", ply.db.background)

    string += "\n\nUse the command |Rchar change <field> <value>|n to alter your character's information."

    return string

def ChargenStageDescription(ply, stage):
    if stage == 1:
        return ChargenStage1(ply)

    return ""