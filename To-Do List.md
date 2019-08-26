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
      - [ ] Detector in our echo class that looks for verbs after "they" pronouns and depluralizes them.
      - [ ] Specify body parts, such as breasts, that might appear in a slot-based description system.
         * This isn't Haven, no need to code in penises or vaginas. Just write whatever's there.
      - [ ] HIGHLY doubt it will ever be a thing, but possibly specify: can get pregnant?
         * If at all implemented, it would be specifically for establishing who's the mother in any kind of command that allows you to see someone's bloodline. Maybe. I dunno, it's messy.
   - [ ] Species. Choices pending establishment of setting. Tempted to go human-only, probably won't.
   - [ ] Archetype, a la Haven. Not quite a "class" but serves the same purpose.
   - [ ] Background - poverty, child of politician, that sort of thing.
      * Could influence starting money, allow/deny certain skills at chargen.

- [ ] Make a nice little tour for them to get acquainted.

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

   In practice the players can decide how they want to talk. It's up to us to build a world in which they want to do it the "correct" way.

* Music is unique to the game, but is depicated in a way that a player in today's society can understand - music might be performed in a tavern full of smelly peasants and the odd knight, but it's played on a modern-looking guitar, and might even include a drummer. That said, there are just as many people classically trained on harpsichords or shamisens.

### Clothing Conventions

* **Formalwear:** Modern suits, fine dresses with contemporary cuts, but all with a baroque and ornate twist. The elite tend to wear an absolute shitload of jewelry, draped over everything, such that they jingle when they walk.

* **Armor:** Full-on high fantasy. Field plate, sabatons, greaves, the works. Politicians wear ringmail beneath their suits to fend away assassin's blades. Even peasants might own a nice leather jerkin.

* **Other anachronisms:** Aetolia-style: Kimonos, certain bits of lingerie (thongs, teddies, etc.). *Hard no* on trenchcoats, fedoras, or any other neckbeard crap.

### Specific Cool Things

* Hospitaliers in full regalia and armor standing sentinel over a chapel soaked in neon lights.

* Radio towers dotting the landscape, looking over towers, fortresses, and hamlets, spreading state propaganda.

* "Neon Mode": Name pending - some kind of otherworldly space. Mid-level players can move through it and it's the basis by which all stealth takes place. High-level players can even see into it from our plane.

----

# Game Policy

## Rules