## Typeclasses in Blackbirds
This guide will briefly go over the various typeclasses defined in the game, what they're for, and what they can/cannot do. If you are adding a new typeclass to the game, your code will not be approved until it is documented here.

### Abilities
**NOTE: Abilities are in a heavily unfinished prototype state!**

The Ability class defines information for the game's various abilities. This is not how abilities are created and defined - those are found in the `blackbirds\abilities` folder.

As of right now there is only one class - `Ability`. This stores the ability's name, whether it costs Rubric, and other such information.

### Accounts
Accounts is an incredibly important object that stores all of the player's account information. It is important to realize that when you are connected to the game, you are not represented as your Character, but as your Account.

A Character is something "puppeted" by an Account, and acts as a proxy for the Account's interaction with the game world. The Account stores information such as which characters the player has access to, what to do when they log in or out, and more. It also contains account-level saved data, such as Rubric and total time played.

Because the game needs to display messages to the player even when they're not playing as a character, it has its own implementation of the `echo()`, `prompt()`, and other methods.

### Areas
**NOTE: Areas are in a heavily unfinished prototype state!**

Think of an Area as a container for Zones. If Zones are collections of rooms in the same geographical area, an Area is a collection of Zones, and thus represents a much larger space. They are manipulated in-game through the `AREA` command.

For instance, the City of Brillante Area contains all of the relevant Zones that belong to the city: Cruzar Riding District, the Palatial Circle, the Jawline, and more.

Weather will be implemented on the Area level, with each Area having its own climate. The climate acts as a template, and will exert influence over any climate defined on the Zone level. For instance, the Gorgon Desert Area might have a `base_temperature` of `40`, but the particularly arid Zone of Catoblepas has a `base_temperature_mod` of `5`. This means that on average, Catoblepas will be 5 C hotter than the rest of the desert.

### Channels
Channels are not yet implemented.

### Characters
Characters are self-explanatory - they're objects representing a person or some other sentient thing in the game world. They contain names, body parts with descriptions, health and endurance pools, accounts, and more. They have methods to `echo()` information to them - as of course you need to be able to see what the game is telling you.

NPCs are not yet implemented but will function identically to characters, the only crucial difference being that they are not linked to an account.

#### Significant Attributes
**Body**: Body represents the player's limbs and other anatomical features.

 - Body is stored as a dictionary with numerous strings and flags.
 - The contents of the Body are polled to build the Character's description.
 - Body parts can be damaged, removed, or replaced with prosthetics.

**Species**: The player's Species is stored in `character.db.species` and is an instance of the Species class object. In the future, this may be changed to a dictionary whose data is derived from the Species class.

 - Evennia does not store data in classes like this, so editing the Character's Species instance will not survive a game reload.
 - Instead, certain flags are stored in the Character's own attributes, such as `has_horns` and `bioluminescence_color`.
 - This allows Species 'edits' to persist, and is also required to allow halfbreed Humans to retain the properties of their halfbred Species.

### Environments
**NOTE: Environments are in a heavily unfinished prototype state!**

Environments represent different types of terrain and surroundings in the game. They are manipulated in-game through the `ENV` or `ENVIRONMENT` command.

Currently, environments have only a name, a full name, a color, and can store whether or not they are natural, in the `natural` attribute. Changes to environments will come as ideas and features are implemented in the game. As of this moment, their most important feature is that they affect the color of room nodes on the game map.

### Exits
*Exits are an unused class in Blackbirds - the Object is required for Evennia to function.*

To see how Blackbirds implements exits, check the Room class.

### Objects
**NOTE: Objects are in a heavily unfinished prototype state!**

Objects are anything that isn't one of the other typeclasses, and represent inanimate things - anything from a vase, to a longsword, to a crackling electrical haze in the sky. They are currently non-functional, as development is focused on more fundamental things. As there will be countless applications for objects, right now it's not useful to talk about them here.

### Rooms
Rooms are the abstract spaces through which players move. They can be a closet, a meadow, or a spot of water deep under the ocean, with no upper or lower size limit.

Being one of the most important types of objects in the game, Rooms have a lot of attributes. They have a Zone and Environment (see below and above, respectively), they act as a container for Characters and Objects, and can represent other things, such as shops or libraries. Rooms also have a concept of electrical power, and pending implementation, will look for power storage units to keep lights and machinery running.

#### Significant Attributes
**Exits:** Unlike most Evennia games, Exits are not implemented through classes but are instead an abstract part of Rooms, existing in the `room.db.exits` dictionary.

 - In the dictionary, the exits contain flags for hidden, locked, and one-way status. More will come as features are implemented.

### Scripts
*Scripts are currently not implemented but will be incredibly important to the game. See https://github.com/evennia/evennia/wiki/Scripts for more details.*

### Species
Species are objects representing the playable races of Blackbirds. The parent Species object contains loads of structured data, such as name, plural name, whether or not the species has horns or claws, and more.

Although Species take the backseat to Abilities in determining what characters can and cannot do, they still have certain mechanical consequences, from a Sacrilite being able to climb trees (`has_claws`) to an Idol taking damage from electromagnetic pulses (`is_synthetic`).

### Zones
Zones are a collection of rooms, and are instrumental in keeping the game world sensible and organized. Every Room in the game should belong to a Zone, and inherits certain information from that Zone, such as whether or not the room disallows open PVP (read: has guards).

Zones also directly influence the game map - the map only displays rooms in the current Zone.