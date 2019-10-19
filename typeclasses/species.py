class Species():
    def __init__(self):
        # Species-specific naming info.
        self.name = None
        self.plural_name = None

        # Physical characteristics.
        self.min_age = 0
        self.max_age = 0
        self.min_height = 0
        self.max_height = 0
        self.min_temp = 0
        self.max_temp = 0
        self.max_neon = 0

        # Naming conventions.
        self.requires_surname = None
        self.unusual_names = None

        # Anatomy.
        self.can_eat = True
        self.can_drink = True
        self.can_sleep = True
        self.can_reproduce = True
        self.can_reproduce_asexually = False
        self.has_horns = False
        self.has_exoskeleton = False
        self.can_be_fourarmed = False
        self.has_fangs = False
        self.has_tail = False
        self.has_claws = False
        self.has_bioluminescence = False
        self.has_plant_appendages = False
        self.can_eat_anything = False

        # Misc.
        self.chargen_documentation = None

    def at_look(self):
        return False

class Human(Species):
    def __init__(self):
        super().__init__()

        self.name = "Human"
        self.plural_name = "Humans"
        self.min_age = 18
        self.max_age = 100
        self.min_height = 120
        self.max_height = 215
        self.min_temp = 10
        self.max_temp = 43
        self.requires_surname = True
        self.unusual_names = False
        self.chargen_documentation = "Humans, sometimes archaically referred to as Man, are a prolific, versatile people, the very species which gave rise to the term 'humanoid'. Though they are found predominantly along coastlines, mountains, woods, and plains, they are comfortable in a wide variety of temperatures and environments, and can be found living almost anywhere.\n\n  |xHeight |c|||n |W120|ncm |c-|n |W215|ncm |c(|W4|n ft |c-|n |W7|n ft|c)|n\n     |xAge |c|||n    |W18|n |c-|n |W100|n\n\n  |c-|n Can select almost any archetype, and all but the most exotic abilities.\n  |c-|n Can survive in a broad range of temperatures, but suffer greatly at either\n    extreme.\n  |c-|n Can start as a half-breed, choosing another species from which to draw\n    minor benefits.\n  |c-|n A half-breed Human counts as either species for the purposes of some\n    ability checks.\n  |c-|n Are not subject to certain prejudices amidst the state of Brillante.\n\n  |c-|n Excellent for beginners, or for testing character builds."

class Carven(Species):
    def __init__(self):
        super().__init__()

        self.name = "Carven"
        self.plural_name = "Carven"
        self.min_age = 18
        self.max_age = 170
        self.min_height = 150
        self.max_height = 215
        self.min_temp = 20
        self.max_temp = 60
        self.requires_surname = False
        self.unusual_names = False
        self.has_horns = True
        self.has_exoskeleton = True
        self.can_be_fourarmed = True
        self.chargen_documentation = "Carven are a people spawned from Ninesilver's great deserts, adapted to hot climates, and were the predominant species in the state of Brillante before its occupation. They are characterized by the rapid mutant growth of their bone and chitin, leading to horns, spines, and other appendages in their young teen years, and encrustations of sharp bone over their limbs in middle adulthood.\n\n  |xHeight |c|||n |W150|ncm |c-|n |W215|ncm |c(|W5|n ft |c-|n |W7|n ft|c)|n\n     |xAge |c|||n    |W18|n |c-|n |W170|n\n\n  |c-|n Can choose a variety of horns.\n  |c-|n Gains exoskeletal growth based on age, which must be treated or worn away.\n  |c-|n Comfortable in warm weather, and can never feel too hot.\n  |c-|n Cannot move as quickly in cold weather, and will suffer greatly.\n  |c-|n Can be given two or four arms.\n  |c-|n Four-armed Carven are cumbersone, but fearsomely strong.\n\n  |c-|n A good choice for seasoned players, especially those who enjoy battle."

class Sacrilite(Species):
    def __init__(self):
        super().__init__()

        self.name = "Sacrilite"
        self.plural_name = "Sacrilites"
        self.min_age = 18
        self.max_age = 65
        self.min_height = 150
        self.max_height = 245
        self.min_temp = -40
        self.max_temp = 32
        self.requires_surname = True
        self.unusual_names = False
        self.has_fangs = True
        self.has_tail = True
        self.has_claws = True
        self.chargen_documentation = "Originating from the taigas of Lightningshield, the Sacrilites are a hardy and cunning people, with thick, furry body hair. They are often likened to predatory cats, for their claws, fur, and elongated ears. Though they can live comfortably indoors or in the shade of Brillante, their homes are in the mountains, and they can roam nude in the snow without a hint of discomfort.\n\n  |xHeight |c|||n |W150|ncm |c-|n |W245|ncm |c(|W5|n ft |c-|n |W9|n ft|c)|n\n     |xAge |c|||n    |W18|n |c-|n |W65|n\n\n  |c-|n Can be given fangs or tusks.\n  |c-|n Their claws make versatile tools for hunting and rending.\n  |c-|n Can climb trees and scale buildings.\n  |c-|n Comfortable in cool weather, and can never feel too cold.\n  |c-|n Can choose heat-, motion-, or night-vision, each with their own benefits\n    and drawbacks.\n\n  |c-|n Recommended for players with a little experience."

class Luum(Species):
    def __init__(self):
        super().__init__()

        self.name = "Luum"
        self.plural_name = "Luumi"
        self.min_age = 18
        self.max_age = 1000
        self.min_height = 60
        self.max_height = 335
        self.min_temp = -30
        self.max_temp = 50
        self.max_neon = 5
        self.requires_surname = False
        self.unusual_names = False
        self.can_reproduce_asexually = True
        self.has_fangs = True
        self.has_bioluminescence = True
        self.has_plant_appendages = True
        self.can_eat_anything = True
        self.chargen_documentation = "The people of Colossus Grove, the seaforest. The Luum have coal-colored flesh, set aglow with bioluminescence. Draped in naturally-occuring blossoms and vines, they are like nothing so much as spirits of the deepest woods, brought into humanoid shape. Owing to the peculiar biome from which they evolved, they are incidentally quite comfortable in real oceanic environs.\n\n  |xHeight |c|||n |W60|ncm |c-|n |W335|ncm |c(|W2|n ft |c-|n |W11|n ft|c)|n\n     |xAge |c|||n   |W18|n |c-|n |W1000|n\n\n  |c-|n Restricted from certain intensely physical archetypes and abilities.\n  |c-|n Can choose the color and vibrance of their biolight.\n  |c-|n Can choose certain extraneous appendages, such as vines or thorns.\n  |c-|n Can see perfectly in the dark.\n  |c-|n Can briefly survive Neon-rich environs.\n  |c-|n Can reproduce asexually.\n  |c-|n Can eat almost anything, but must eat often.\n\n  |c-|n Good for players who want a challenge and don't mind limited options."

class Idol(Species):
    def __init__(self):
        super().__init__()

        self.name = "Idol"
        self.plural_name = "Idols"
        self.min_age = 1
        self.max_age = 1000
        self.min_height = 100
        self.max_height = 300
        self.min_temp = -273
        self.max_temp = 80
        self.max_neon = 50
        self.requires_surname = False
        self.unusual_names = True
        self.can_eat = False
        self.can_drink = False
        self.can_sleep = False
        self.can_reproduce = False
        self.can_be_fourarmed = True
        self.chargen_documentation = "A warhost of Humanlike automata, numerous enough to comprise a race of their own. With shells of stone, steel, and/or false flesh, no two Idols are the same. Though the great majority of activated Idols were built for killing, the softer, more graceful shapes of others suggest that they may have once belonged to a noble social strata, in an era that time forgot.\n\n  |xHeight |c|||n |W120|ncm |c-|n |W300|ncm |c(|W4|n ft |c-|n |W10|n ft|c)|n\n     |xAge |c|||n     |W1|n |c-|n |W1000|n\n\n  |c-|n Suffer numerous archetypal restrictions, but gain access to exclusive\n    Idol-based archetypes.\n  |c-|n Receive much more detailed information when looking at things.\n  |c-|n Do not need to eat, drink, or sleep, but must maintain their fuel levels.\n  |c-|n Can passively regenerate fuel with the right parts, albeit slowly.\n  |c-|n Do not suffer any fatigue-based penalties, so long as their energy levels\n    are maintained.\n  |c-|n Can obtain and swap components.\n  |c-|n May or may not be anatomically correct.\n\n  |c-|n A difficult species to play; must be unlocked after 200 hours of play time."

    def at_look(ply, target = None, **kwargs):
        if not target.access(self, "view"):
            try:
                return "Could not view '%s'." % target.get_display_name(self, **kwargs)
            except AttributeError:
                return "Could not view '%s'." % target.key

        description = target.return_appearance(self, **kwargs)

        # the target's at_desc() method.
        # this must be the last reference to target so it may delete itself when acted on.
        target.at_desc(looker = self, **kwargs)

        return description