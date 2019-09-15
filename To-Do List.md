## Urgent!
- [ ] Look at https://github.com/evennia/evennia/wiki/TickerHandler !

## Displays
- [x] Implement standardized "echo()" methods on player class object.
- [ ] Add similar echo()s where needed for room objects, sessions, etc.
- [ ] Standardize prompt, ensure it displays after literally everything.
   - [ ] Make the prompt display actual useful data once character creation is fleshed out.

## Room Data
- [x] Determine what properties rooms need. Obvious ones: Environment, area, indoors/outdoors, water, etc.
- [x] Modernize (read: add XTERM colors) room title display.
- [x] Display light, temperature, water level.
- [ ] Implement room echoes for remaining room attributes, where applicable.
- [x] Area handling through JSON.
- [x] Zone handling through JSON.
- [x] Environment handling through JSON.
- [ ] Exit standardizing and room displaying.
   - [x] Rewrite of Exit class from the ground up.
   - [ ] Commands to create/delete exits. (half finished)
   - [ ] Support for:
      - [ ] One-way Exits
      - [ ] Secret Exits
      - [ ] Org/Class-access Restricted Exits
- [ ] Implement actual room movement code.

## Mapping
- [ ] hoo boy

## Cleanup, Maintenance
- [ ] Fix dumb, inconsistent method name casing (AutoPunc, etc.)
- [ ] Look up how database migration works.

## Evennia System Message Replacements
- [ ] Invalid commands.
- [ ] System reloads.

## Characters

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