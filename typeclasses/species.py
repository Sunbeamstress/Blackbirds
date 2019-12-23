class Species():
    def __init__(self):
        # Species-specific naming info.
        self.name = None
        self.plural_name = None
        self.society = None

        # Physical characteristics.
        self.min_age = 0
        self.max_age = 0
        self.min_height = 0
        self.max_height = 0
        self.min_temp = 0
        self.max_temp = 0
        self.max_neon = 0

        # Naming conventions.
        self.requires_surname = True
        self.unusual_names = False

        # Anatomy.
        self.can_halfbreed = False
        self.can_eat = True
        self.can_drink = True
        self.can_sleep = True
        self.can_reproduce = True
        self.can_reproduce_asexually = False
        self.has_horns = False
        self.horns_optional = False
        self.has_exoskeleton = False
        self.can_be_fourarmed = False
        self.has_fangs = False
        self.fang_choice = False
        self.fangs_optional = False
        self.has_tail = False
        self.tail_optional = False
        self.has_claws = False
        self.has_bioluminescence = False
        self.has_plant_appendages = False
        self.can_eat_anything = False

        # Other conventions.
        self.precision_information = False

        # Misc.
        self.playable = True
        self.chargen_documentation = None

    def update(self):
        pass

    def at_look(self):
        return False

    def age_description(self, a):
        low, high = self.min_age, self.max_age
        a_perc = (a * 100) / high

        if a < low:
            return "juvenile"
        if a_perc >= 85:
            return "ancient"
        if a_perc >= 60:
            return "elderly"
        if a_perc >= 41:
            return "middle-aged"
        if a_perc >= 30:
            return "adult"
        if a_perc >= 21:
            return "young adult"
        return "young"

    def height_description(self, h):
        low, high = self.min_height, self.max_height
        h_perc = ((h - low) * high) / (high - low)

        if h < low:
            return "stunted"
        if h > high:
            return "unnatural"
        if h_perc >= 95:
            return "incredibly tall"
        if h_perc >= 85:
            return "very tall"
        if h_perc >= 70:
            return "tall"
        if h_perc >= 50:
            return "average"
        if h_perc >= 30:
            return "sub-average"
        if h_perc >= 15:
            return "short"
        if h_perc >= 5:
            return "diminutive"

class Human(Species):
    def __init__(self):
        super().__init__()

        self.name = "Human"
        self.plural_name = "Humans"
        self.society = "Humanity"
        self.min_age = 18
        self.max_age = 100
        self.min_height = 120
        self.max_height = 215
        self.min_temp = 10
        self.max_temp = 43
        self.can_halfbreed = True
        self.chargen_documentation = {
            "synopsis": "Humans, sometimes archaically referred to as Man, are a prolific, versatile people, the very species which gave rise to the term 'humanoid'. Though they are found predominantly along coastlines, mountains, woods, and plains, they are comfortable in a wide variety of temperatures and environments, and can be found living almost anywhere.",
            "qualities": [
                "Can survive in a broad range of temperatures, but suffers greatly at either extreme.",
                "Can start as a half-breed, choosing another species from which to draw minor features.",
                "A half-breed Human counts as either species for the purposes of some ability checks.",
                "Are not subject to certain prejudices common in the State of Brillante."
            ],
            "difficulty": "Excellent for beginners, or for testing character builds."
        }

class Carven(Species):
    def __init__(self):
        super().__init__()

        self.name = "Carven"
        self.plural_name = "Carven"
        self.society = "Carvendom"
        self.min_age = 18
        self.max_age = 170
        self.min_height = 150
        self.max_height = 215
        self.min_temp = 20
        self.max_temp = 60
        self.requires_surname = False
        self.has_horns = True
        self.has_exoskeleton = True
        self.can_be_fourarmed = True
        self.chargen_documentation = {
            "synopsis": "Carven are a people spawned from Ninesilver's great deserts, adapted to hot climates, and were the predominant species in the state of Brillante before its occupation. They are characterized by the rapid mutant growth of their bone and chitin, leading to horns, spines, and other appendages in their young teen years, and encrustations of sharp bone over their limbs in middle adulthood.",
            "qualities": [
                "Comfortable in warm weather, and can never feel too hot.",
                "Cannot move as quickly in cold weather, and will suffer greatly.",
            ],
            "difficulty": "A good choice for seasoned players, especially those who enjoy battle."
        }

class Sacrilite(Species):
    def __init__(self):
        super().__init__()

        self.name = "Sacrilite"
        self.plural_name = "Sacrilites"
        self.society = "Sacrility"
        self.min_age = 18
        self.max_age = 65
        self.min_height = 150
        self.max_height = 245
        self.min_temp = -40
        self.max_temp = 32
        self.has_fangs = True
        self.fang_choice = True
        self.has_tail = True
        self.has_claws = True
        self.chargen_documentation = {
            "synopsis": "Originating from the taigas of Lightningshield, the Sacrilites are a hardy and cunning people, with thick, furry body hair. They are often likened to predatory cats, for their claws, fur, and elongated ears. Though they can live comfortably indoors or in the shade of Brillante, their homes are in the mountains, and they can roam nude in the snow without a hint of discomfort.",
            "qualities": [
                "Comfortable in cool weather, and can never feel too cold.",
                "Can choose heat-, motion-, or night-vision, each with their own benefits and drawbacks.",
            ],
            "difficulty": "Recommended for players with a little experience."
        }

class Luum(Species):
    def __init__(self):
        super().__init__()

        self.name = "Luum"
        self.plural_name = "Luumi"
        self.society = "Luumdom"
        self.min_age = 18
        self.max_age = 1000
        self.min_height = 60
        self.max_height = 335
        self.min_temp = -30
        self.max_temp = 50
        self.max_neon = 5
        self.requires_surname = False
        self.can_reproduce_asexually = True
        self.has_fangs = True
        self.fangs_optional = True
        self.has_bioluminescence = True
        self.has_plant_appendages = True
        self.can_eat_anything = True
        self.chargen_documentation = {
            "synopsis": "The people of Colossus Grove, the seaforest. The Luum have coal-colored flesh, set aglow with bioluminescence. Draped in naturally-occuring blossoms and vines, they are like nothing so much as spirits of the deepest woods, brought into humanoid shape. Owing to the peculiar biome from which they evolved, they are incidentally quite comfortable in water, as well.",
            "qualities": [
                "Too delicate for certain intensely physical abilities.",
                "Can choose certain extraneous appendages, such as vines or thorns.",
                "Can briefly survive Neon-rich environs.",
            ],
            "difficulty": "Good for players who want a challenge and don't mind limited options."
        }

class Idol(Species):
    def __init__(self):
        super().__init__()

        self.name = "Idol"
        self.plural_name = "Idols"
        self.society = "Synthesis"
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
        self.precision_information = True
        self.chargen_documentation = {
            "synopsis": "A warhost of Humanlike automata, numerous enough to comprise a race of their own. With shells of stone, steel, and/or false flesh, no two Idols are the same. Though the great majority of activated Idols were built for killing, the softer, more graceful shapes of others suggest that they may have once belonged to a noble social strata, in an era that time forgot.",
            "qualities": [
                "Were built in another time and age, and cannot utilize many common abilities - but make up for it with capabilities of their own.",
                "Do not need to eat, drink, or sleep, but must maintain their energy levels.",
                "Do not suffer any fatigue-based penalties, so long as their energy levels are maintained.",
                "Can obtain and swap components."
            ],
            "difficulty": "A difficult species to play; must be unlocked with Rubric."
        }

class Blackbird(Species):
    def __init__(self):
        super().__init__()
        self.name = "Blackbird"
        self.plural_name = "Blackbirds"
        self.society = "the Assassinocracy"
        self.min_age = 18
        self.max_age = 9999
        self.min_height = 1
        self.max_height = 9999
        self.min_temp = -273
        self.max_temp = 9999
        self.max_neon = 9999
        self.requires_surname = False
        self.unusual_names = True
        self.can_reproduce_asexually = True
        self.has_horns = True
        self.horns_optional = True
        self.has_exoskeleton = True
        self.can_be_fourarmed = True
        self.has_fangs = True
        self.fang_choice = True
        self.fangs_optional = True
        self.has_tail = True
        self.tail_optional = True
        self.has_claws = True
        self.has_bioluminescence = True
        self.has_plant_appendages = True
        self.can_eat_anything = True
        self.precision_information = True
        self.playable = False
        self.chargen_documentation = {
            "synopsis": "A coven of mysterious ageless beings. In accordance with folklore, they were once mercenaries, scientists, capitalists, and thieves, the very first to strike it rich in the Neon Drive. What they did with that Neon, and why it did it to them, will likely never be known. Each of them is a terrifying force of nature, a living planetary will; they do as they please and are not beholden to laws, social mores, or even physical force.",
            "qualities": [
                "Stricken with ghost-white skin and black hair.",
                "Linked, somehow, to the stream of time itself.",
                "In all places and at all times.",
                "Invisible and impossible to touch.",
                "Never without a blade.",
            ],
            "difficulty": "The world will bend easily beneath your talons, but keeping your mind intact will prove to be a nightmare."
        }