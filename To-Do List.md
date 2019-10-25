## Urgent!
- [ ] Look at https://github.com/evennia/evennia/wiki/TickerHandler !

## Displays
- [x] Implement standardized "echo()" methods on player class object.
- [ ] Add echo() support for:
   - [x] Commands (shortcut to player/account)
   - [x] Players
   - [x] Accounts
   - [ ] Rooms
   - [ ] All sessions (game-wide emotes)
- [ ] Standardize prompt, ensure it displays after literally everything.
   - [x] Make the prompt display actual useful data once character creation is fleshed out.

## Room Data
- [x] Determine what properties rooms need. Obvious ones: Environment, area, indoors/outdoors, water, etc.
- [x] Modernize (read: add XTERM colors) room title display.
- [x] Display light, temperature, water level.
- [ ] Implement room echoes for remaining room attributes, where applicable.
- [x] ~~Area handling through JSON.~~
- [x] ~~Zone handling through JSON.~~
- [x] Environment handling through JSON.
- [ ] Exit standardizing and room displaying.
   - [x] Rewrite of Exit class from the ground up.
   - [x] Commands to create/delete exits.
   - [x] ~~Determine whether or not to continue using actual exit class - all required use cases might be covered by simple dictionary.~~
   - [ ] Support for:
      - [ ] One-way Exits
      - [ ] Secret Exits
      - [ ] Org/Class-access Restricted Exits
- [x] Implement actual room movement code.

## Zone Data
- [x] Implement Zone class.
- [x] Design menu to manipulate zones.

## Area Data
- [x] Implement Area class.
- [x] Design menu to manipulate areas.

## Mapping
- [ ] Feature-complete implementation of map system.
   - [x] Map class.
      - [x] Initializes the grid.
      - [x] Quickly obtains all rooms in current zone.
         - [x] Need to profile various methods for speed: gather all rooms whose zone value matches, store rooms in zone JSON, etc.
      - [x] Draws rooms within visible range.
         - [ ] Room color varies based on environment.
      - [ ] Draws exit links between applicable rooms.
         - [ ] Determine how to display one-way exits.
         - [ ] Conceal secret exits.
      - [ ] Displays header and footer with ~~room name, zone name, and~~ coordinate data.
   - [ ] Submapping and partitioning.
   - [ ] Background and texturing.
      - [ ] Background color can be defined by and vary from zone to zone.
      - [ ] Allow zones to define texture characters (".", ",", "`", etc.) to add visual appeal to the map.
   - [ ] Abilities may allow you to passively see other players on map within range.
   - [ ] Edge case handling for when no map should be drawn ("you're lost").
   - [ ] Map overriding (neon mode, blindness, etc.)!

## Cleanup, Maintenance
- [x] Fix dumb, inconsistent method name casing (AutoPunc, etc.)
- [ ] Look up how database migration works.

## Evennia System Message Replacements
- [ ] Invalid commands.
- [ ] System reloads.

## Characters

- [x] Need to implement at least a basic chargen and determine what properties a character has.
   - [x] First and last name.
   - [x] Age.
   - [x] ~~Age of appearance, in case you take good or bad care of yourself.~~ (will be handled by mechanics)
   - [ ] An "identity" ("intro" in other RPIs). The string we see if we don't know your name.
   - [ ] **Big Decision**: Haven-style descriptions, with body parts, etc.?
      - [ ] Fields for each body part (lower face, stomach, groin, etc.).
      - [ ] Ability to describe each, freely and on the fly.
   - [x] No coded sex/gender (sorry, chuds). You determine your biology.
      - [x] Pronouns. As much as I'd love to make them freeform, for grammatical purposes, limited to he/she/they.
         * This will be given the name of "sex" or "gender" in the code to make it easy to remember.
      - [ ] Detector in our echo class that looks for verbs after "they" pronouns and depluralizes them.
         * Will likely have to hand-code a big dictionary of depluralizations; and try to rely on a generic fallback if the word isn't found.
      - [ ] Specify body parts, such as breasts, that might appear in a slot-based description system.
         * This isn't Haven, no need to code in penises or vaginas. Just write whatever's there.
   - [x] Species. Choices pending establishment of setting. ~~Tempted to go human-only, probably won't.~~
   - [ ] Species-based anatomy.
      - [x] Reproductive ability.
      - [x] Two or four arms.
      - [ ] Idol treads/traction.
   - [ ] Archetype, a la Haven. Not quite a "class" but serves the same purpose.
   - [x] ~~Background - poverty, child of politician, that sort of thing.~~
      * Could influence starting money, allow/deny certain skills at chargen.

- [ ] Make a nice little tour for them to get acquainted.

### Abilities

- [x] Define ability and ability tree classes.
- [ ] Describe core ability trees and the individual abilities beneath them.
   - [ ] Implement logic to tally up total level in a tree, based on which abilities belong to it.

### Employment

- [ ] Create job system.
   - [ ] Implement JOB command to take/manage jobs. Current idea is you put in a request at a business and its owner is notified that you want a job. From there they can JOB HIRE you.
   - [ ] Implement WORK command. Flags the player as being at work. As long as they don't leave the business premises for five minutes they'll get their pay for the day.
   - [ ] Payment is handled daily - you can work once a day, seven days a week. If you miss three or more days in a row, your pay for that day is docked (based on how many you missed), with an explanation given that you weren't working enough. The next day worked will give you full pay again.

## Objects

### Misc. Object Stuff
- [ ] Flower language!