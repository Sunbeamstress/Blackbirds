## Urgent!
- [ ] Look at https://github.com/evennia/evennia/wiki/TickerHandler !

## Displays
- [x] Implement standardized "echo()" methods on player class object.
- [x] Add echo() support for:
   - [x] Commands (shortcut to player/account)
   - [x] Players
   - [x] Accounts
   - [x] Rooms
   - [x] All sessions (game-wide emotes)
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
- [x] Exit standardizing and room displaying.
   - [x] ~~Rewrite of Exit class from the ground up.~~
   - [x] Commands to create/delete exits.
   - [x] Determine whether or not to continue using actual exit class - all required use cases might be covered by simple dictionary.
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
         - [x] Room color varies based on environment.
      - [x] Draws exit links between applicable rooms.
         - [ ] Determine how to display one-way exits.
         - [ ] Conceal secret exits.
      - [x] Displays header and footer with ~~room name, zone name, and~~ coordinate data.
   - [ ] Submapping and partitioning.
   - [ ] Background and texturing.
      - [ ] Background color can be defined by and vary from zone to zone.
      - [ ] Allow zones to define texture characters (".", ",", "`", etc.) to add visual appeal to the map.
   - [ ] Abilities may allow you to passively see other players on map within range.
   - [ ] Edge case handling for when no map should be drawn ("you're lost").
   - [ ] Map overriding (neon mode, blindness, etc.)!

## Cleanup, Maintenance
- [x] Fix dumb, inconsistent method name casing (AutoPunc, etc.)
- [x] Look up how database migration works.

## Evennia System Message Replacements
- [ ] Invalid commands.
- [x] System reloads.

## Characters

- [x] Need to implement at least a basic chargen and determine what properties a character has.
   - [x] First and last name.
   - [x] Age.
   - [x] ~~Age of appearance, in case you take good or bad care of yourself.~~ (will be handled by mechanics)
   - [x] An "identity" ("intro" in other RPIs). The string we see if we don't know your name.
   - [x] **Big Decision**: Haven-style descriptions, with body parts, etc.?
      - [x] Fields for each body part (lower face, stomach, groin, etc.).
      - [x] Ability to describe each, freely and on the fly.
   - [x] No coded sex/gender (sorry, chuds). You determine your biology.
      - [x] Pronouns. As much as I'd love to make them freeform, for grammatical purposes, limited to he/she/they.
         * This will be given the name of "sex" or "gender" in the code to make it easy to remember.
      - [x] Detector in our echo class that looks for verbs after "they" pronouns and depluralizes them.
         * ~~Will likely have to hand-code a big dictionary of depluralizations; and try to rely on a generic fallback if the word isn't found.~~
         * lmao nevermind python rules
      - [x] Specify body parts, such as breasts, that might appear in a slot-based description system.
         * This isn't Haven, no need to code in penises or vaginas. Just write whatever's there.
   - [x] Species. Choices pending establishment of setting. ~~Tempted to go human-only, probably won't.~~
   - [x] Species-based anatomy.
      - [x] ~~Reproductive ability.~~
      - [x] Two or four arms.
      - [ ] Idol treads/traction.
   - [x] ~~Archetype, a la Haven. Not quite a "class" but serves the same purpose.~~ Not needed at this time.
   - [x] ~~Background - poverty, child of politician, that sort of thing.~~
      * Could influence starting money, allow/deny certain skills at chargen.

### Character Generation
- [ ] Create a simple and effective tour to work players through the character creation process.
   - [x] Species selection.
   - [ ] Personal information - name, age, pronouns, etc.
      - [x] Check for duplicate names.
      - [x] Check for invalid names.
      - [x] Forbid ages/heights out of species-based ranges.
      - [ ] Make sure to check for validity again if the player returns to the first menu and changes their species.
   - [ ] Anatomical selection.
      - [x] Breasts - cosmetic option that changes the name of your "upper chest" slot.
      - [x] ~~Reproduction?~~ Discarded as we won't be doing succession/child rearing mechanics
      - [x] Species features: horns, extra arms, etc.
      - [x] Human half-breed support for species features.
   - [ ] Introduction to identities and descriptions.
      - [ ] Allow the player to define their identity (intro).
      - [ ] Give the player fields to define their body part descriptions.
   - [ ] Primer to abilities, and a leeway period of free learning/unlearning.
   - [ ] Dump the player out into the wild to fend for themselves like a shaky newborn foal.

### Abilities

- [ ] Implement abilities.
   - [x] Define ability and ability tree classes.
      - [x] Implementation question: store each player's individual ability as its own object, or use a dictionary stored on the player? (We went with dictionary)
   - [ ] Describe core ability trees and the individual abilities beneath them.
      - [ ] Implement logic to tally up total level in a tree, based on which abilities belong to it.

### Employment

- [ ] Create job system.
   - [ ] Implement JOB command to take/manage jobs. Current idea is you put in a request at a business and its owner is notified that you want a job. From there they can JOB HIRE you.
   - [ ] Implement WORK command. Flags the player as being at work. As long as they don't leave the business premises for five minutes they'll get their pay for the day.
   - [ ] Payment is handled daily - you can work once a day, seven days a week. If you miss three or more days in a row, your pay for that day is docked (based on how many you missed), with an explanation given that you weren't working enough. The next day worked will give you full pay again.

## Objects

- [ ] Object system.
   - [ ] Master structure.
      - [ ] Implement "master" objects that serve as a template for all children. Changing the qualities of the master should change all children in real time.
      - [ ] Changing the quality of a child object will enforce an "override," meaning that field won't be changed should the master change. Very standard stuff.
      - [ ] Children can be given *additional* aliases.
      - [ ] Ability to filter/search through the master list.
   - [ ] Creation commands.
      - [x] Simple CREATE verb.
      - [ ] CREATE argument to create a new object by master reference.
      - [ ] Ability to alter the master of an existing object.
   - [ ] Manipulation commands.
   - [ ] Interactivity.
      - [ ] Settable flags that allow the object to react to given standard verbs (e.g. USE, PUSH, HACK, etc.).
      - [ ] Generic "portal" flag that links the object to a room - useful for quick and dirty windows, elevators, or other non-room-based exits.
      - [ ] Power system.
         - [ ] Flagging on the power system means that the object interacts with power in any way, whether to use it, generate it, or more.
            - [ ] Allows the object to be affected by EMP.
            - [ ] Allows the object to accept circuitry, batteries, neon cells, and more.
         - [ ] Power interactivity flags:
            - [ ] Radio channels.
            - [ ] Remote controlling.
            - [ ] "Trap" systems (tripwires, lasers, etc.).
         - [ ] Powernets.
            - [ ] Divide zones into powernets and allow objects to subscribe to them.
            - [ ] Allow further subdivision for buildings or other partitions.
            - [ ] Allow generated power to charge the batteries of validly connected objects in the powernet.
         - [ ] Power generation.
            - [ ] Implement generator object that dumps power into a powernet at a certain rate.
            - [ ] Generator types:
               - [ ] Infinite "neon well" power gen for testing purposes.
               - [ ] Solar/lunar.
               - [ ] Conventional fuel-based generation that accepts a given object as fuel.
               - [ ] Possibility: heat-based (think TEG)?
         - [ ] Power storage.
         - [ ] Wiring.
         - [ ] Wireless systems.
      - [ ] Media
         - [ ] Media consists of a filename, origin (usually the person who produced it via phone or w/e), and a fake-ass filesize.
         - [ ] Allow the filesize to change to hint at certain *nefarious aspects* of the media.
         - [ ] Media types:
            - [ ] Images: consists of a description of the image as a whole (this is a low-quality snapshot of a dog drinking from a puddle); if containing players or objects, they are included as additional elements that can be looked at individually. Their descriptions are stored *in* the media (in case they change later).
            - [ ] Video: literally a recorded segment of RP playing out for your benefit. If recorded by a player, you see none of their actions but can hear their speech.
            - [ ] Audio: almost identical to audio but with no visual component.
      - [ ] Scripting language.
         - [ ] hahaha this will never get done