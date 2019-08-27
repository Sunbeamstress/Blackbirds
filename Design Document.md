# Core Functionality

## Behind the Scenes

### Display Features

- [ ] Override all use of msg() with proprietary method - implementation TBD.
   - "echo" class, defining all ways to display messages to players (read: unidirectional, room, gamewide, etc.)
   - Just make a bunch of functions. Not Python friendly!

- [ ] Standardize prompt, ensure it displays after literally everything.

- [ ] GMCP! But let's not be in a rush.

## Creation

### Characters

- [ ] Need to implement at least a basic chargen and determine what properties a character has.
   - [ ] First and last name.
      - Freeform: Type almost anything you want, 32 characters in both fields.
   - [ ] Age.
   - [ ] Age of appearance, in case you take good or bad care of yourself.
   - [ ] An "identity" ("intro" in other RPIs). The string we see if we don't know your name.
   - [ ] **Big Decision**: Haven-style descriptions, with body parts, etc.?
      - [ ] Fields for each body part (lower face, stomach, groin, etc.).
      - [ ] Ability to describe each, freely and on the fly.
   - [ ] No coded sex/gender (sorry, chuds). You determine your biology.
      - [ ] Pronouns. As much as I'd love to make them freeform, for grammatical purposes, limited to he/she/they.
         * This will be given the name of "sex" or "gender" in the code to make it easy to remember.
      - [ ] Detector in our echo class that looks for verbs after "they" pronouns and depluralizes them.
         * Will likely have to hand-code a big dictionary of depluralizations; and try to rely on a generic fallback if the word isn't found.
      - [ ] Specify body parts, such as breasts, that might appear in a slot-based description system.
         * This isn't Haven, no need to code in penises or vaginas. Just write whatever's there.
      - [ ] HIGHLY doubt it will ever be a thing, but possibly specify: can get pregnant?
         * If at all implemented, it would be specifically for establishing who's the mother in any kind of command that allows you to see someone's bloodline. Maybe. I dunno, it's messy.
   - [ ] Species. Choices pending establishment of setting. Tempted to go human-only, probably won't.
   - [ ] Archetype, a la Haven. Not quite a "class" but serves the same purpose.
   - [ ] Background - poverty, child of politician, that sort of thing.
      * Could influence starting money, allow/deny certain skills at chargen.

- [ ] Make a nice little tour for them to get acquainted.

### Abilities

- [x] Define ability and ability tree classes.
- [ ] Describe core ability trees and the individual abilities beneath them.
   - [ ] Implement logic to tally up total level in a tree, based on which abilities belong to it.

### Rooms

- [ ] Implement IRE-style building. yeah lmao it won't be that easy

- [ ] Determine what properties rooms need. Obvious ones: Environment, area, indoors/outdoors, water, etc.

### Items

----

# Setting

## General

High fantasy with anachronistic modern touches; the world Aetolia tried to be but couldn't. Think *Romeo + Juliet*, 2018's *Robin Hood*, or *Final Fantasy XV*.

### Culture

* Classic high-fantasy mish-mash of dominant European influences, with little Tolkeinisms and whatnot for flavor.

* Castles and palaces such as you'd find in Germany or France.

* People of all colors mingle. This isn't to say there's no racism in Blackbirds, but it never informed an avoidance of race-mixing, or kept people of a certain color from certain places. Much like the real world, skin color can often be used to determine a person's origin: brown-skinned people from hotter climes, white-skinned people from colder places, yellow-skinned, olive-skinned, etc. etc.

   * This isn't just a lazy 1:1 transfer of real world humans to Blackbirds humans. This goes for the other species, as well. Mary Sue the Wolfgirl has bluish, silvery fur, so you know she's from up north.

* Officially, language is formal and archaic:

        Standing atop the dead, Ashlar ejects the clip from his weapon, the gun
        smoking in his tightly-gripped fist. "Behold, the new way of things," he
        announces to the assembly.

        "You call this money?" The trader asks, biting at the coin's edge. "You insult
        me with this trifle - but I tell you plainly, I would derive a full MONEY's
        worth of pleasure from placing this dog-eared pig iron into the weaver's palm.
        I'll take it!"

   In practice the players can decide how they want to talk. It's up to us to build a world in which they want to do it the "correct" way - and if not, that's just fine.

* Music is unique to the game, but is depicated in a way that a player in today's society can understand - music might be performed in a tavern full of smelly peasants and the odd knight, but it's played on a modern-looking guitar, and might even include a drummer. That said, there are just as many people classically trained on harpsichords or shamisens.

* Language is used in another context: to speak directly to the player, and subliminally enforce the fantasy aspects of the world. If we were to simply go "you live in a castle and wear t-shirts" this setting would be a failure. It has to be immersive.

   - There are police, and peasants might even call them the same things you'd call police, but they're *prefects*, and respond to a *magistrate*, not a sheriff or captain or what have you.

   - The citizens are revolting? The prefects roll out a tank - but it's not a *tank*, it's an *iron coalhound*.

   - Guns are guns - but they come in various "classes" that determine their caliber, and these are named after blades: longsword, dagger, rapier, etc.

### Clothing Conventions

* **Formalwear:** Modern suits, fine dresses with contemporary cuts, but all with a baroque and ornate twist. The elite tend to wear an absolute shitload of jewelry, draped over everything, such that they jingle when they walk.

* **Armor:** Full-on high fantasy. Field plate, sabatons, greaves, the works. Politicians wear ringmail beneath their suits to fend away assassin's blades. Even peasants might own a nice leather jerkin.

* **Other anachronisms:** Aetolia-style: Kimonos, certain bits of lingerie (thongs, teddies, etc.). *Hard no* on trenchcoats, fedoras, or any other neckbeard crap.

### Architecture

There is one major city in which most of the gameplay occurs, so for the purposes of this heading we'll be describing that locale.

* The city's layout follows a quasi-medieval structure: built over rivers and on a coast, surrounded by a wall, and characterized by things such as a town square, a square around the biggest chapel, and a clear visual hierarchy of lofty palaces and nobles's quarters, and then the lower-slung buildings of trade industry and the odd citizen's home.

* The poor (and there *will* be poor, class disparity is a *huge* theme here) live in the shantytown outside the walls. This will also serve as the most likely area where players build their homes.

* **Neon**. Neon is something of particular importance. Neon lighting is used very heavily to signify opulence; in churches, along the baseboards of palace halls, or even in the signage of an especially rich merchant. More about Neon below.

### Neon

Neon is **a thing**, and though never specified, is implied to have great power. In typical use it functions just like the real-world gas (stick in a tube, give a little electrical impulse, watch the pretty glow), but carries the mystical qualities of Aetolia's ylem. It's so much more.

* Neon was discovered and studied originally by the Blackbirds. In a rare show of generosity, they made public several research journals detailing what they learned, determining that this technology would greatly improve life for all people.

* Our feeble and incomplete understanding of Neon is that its skeins exist in many alternate realities at once. Prevailing neonate theory is that a skein's dimension of origin can determine its purity and power.

* Things can be "infused" with Neon - in game terms, this is an enchantment system, with capabilities determined by the sort of Neon used.

### The Blackbirds

The hidden assassinocracy.

* The Blackbirds represent a special "endgame" goal for especially powerful players - where in Aetolia you'd become a special race, or in Haven you'd achieve Tier 5, the Blackbirds take that place.

* Lorewise, you are never actually part of the Blackbirds themselves. Rather, you're considered to be *in the know*, and are privy to their communiques.

### Specific Cool Things

* Hospitaliers in full regalia and armor standing sentinel over a chapel soaked in neon lights.

* Radio towers dotting the landscape, looking over towers, fortresses, and hamlets, spreading state propaganda.

* "Neon Mode": Name pending - some kind of otherworldly space. Mid-level players can move through it and it's the basis by which all stealth takes place. High-level players can even see into it from our plane.

----

# Game Policy

## Rules

