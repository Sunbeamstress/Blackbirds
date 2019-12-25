## On Snowflake Code
One of the primary design paradigms for Blackbirds is the avoidance of "snowflake code." This refers to assigning special value to a specific class, a specific object, a specific instance of the two, or some other like element.

Objects in and of themselves are not special. They are not snowflakes. They are instead distinguished by their attributes.

### Example of Snowflakiness
The player is delving through some old ruins, and a long-dormant device activates, setting off a weak electromagnetic pulse. If the player is an Idol, this is very dangerous! It should hurt them, drain some of their energy, and scramble them for a bit. You might be tempted to design the attack like this:

```Python
class EMPBurst(Attack):
    @property
    def att_msg(self):
        return {
            "1P": "ATTACKER glows ominously and emits a low buzz."
            "1P_IDOL": "A crushing wave of force emanates from ATTACKER, striking you square in the gut.",
        }

    def func(self):
        attacker = self.caller
        tar = self.target

        if tar.db.species.name == "Idol":
            tar.echo(self.att_msg["1P_IDOL"])
            do_idol_stuff()
        else:
            tar.echo(self.att_msg["1P"])
```

Let's take a closer look here. We have attack messages clearly defined - a regular first-person message, and a special one for Idols. So how are we determining the player is an Idol?

```Python
if tar.db.species.name == "Idol":
    tar.echo(self.att_msg["1P_IDOL"])
    do_idol_stuff()
```

Here we are. If the player's species name matches "Idol", display a special message and add on a special attack, presumably located in `do_idol_stuff()`. Now what's the problem with this?

**This code assigns inherent value not to the Idol class object, but only its name. This means:**

 - The player will not be affected if an admin decides to change the name of their species instance, even though they are technically an Idol.
 - The player will not be affected if their species instance was given Idol-like qualities.
 - The player will not be affected if, for whatever reason, Idols begin to go by a different name.
 - The player *will* be affected even if they are called an Idol but do not represent a synthetic species.

### The Deflaking Process
Let's abstract what it is we want from this EMP attack example. We have an electromagnetic burst - it should affect machinery, synthetic life, or anything else that runs on electricity. What's a better way to implement this?

Let's assign an attribute to the Idol species. When we edit a Species class, we first add the attribute to its parent class, which is conveniently just called `Species`.

```Python
class Species():
    def __init__(self):
        # Species-specific naming info.
        self.name = None
        self.plural_name = None
        ...

        ...
        self.is_synthetic = False
```

We make the flag `False` - this is a reasonable default, as the other species are definitely not synthetic. Without having to edit their code, they now all report that they are non-synthetic - or more accurately, that their `is_synthetic` flag is `False`. If the majority of species in Blackbirds were various types of robot, we might default it to `True` and simply toggle it `False` for the non-synth ones, but in this case we're good.

Then, we alter Idols:

```Python
class Idol(Species):
    def __init__(self):
        super().__init__()

        self.name = "Idol"
        self.plural_name = "Idols"
        ...

        ...
        self.is_synthetic = True
```

So now, the Species objects have some sort of awareness of their synthetic status. How do we alter our EMP attack so that it looks for this information instead?

```Python
class EMPBurst(Attack):
    @property
    def att_msg(self):
        return {
            "1P": "ATTACKER glows ominously and emits a low buzz."
            "1P_SYNTH": "A crushing wave of force emanates from ATTACKER, striking you square in the gut.",
        }

    def func(self):
        attacker = self.caller
        tar = self.target

        if tar.db.species.is_synthetic:
            tar.echo(self.att_msg["1P_SYNTH"])
            do_synth_stuff()
        else:
            tar.echo(self.att_msg["1P"])
```

We'll make a number of subtle, but significant changes to the attack object.

 1. Check for the player's synthetic status: `if tar.db.species.is_synthetic`
 2. For our own reference, change the names of the attack entrY: `"1P_IDOL"` becomes `"1P_SYNTH"`

Now, the attack functions exactly the same, looking for synthetic status instead of checking for the name of the species. What are the advantages of doing things this way?

 - The status check remains accurate no matter what happens to the player's species instance. If they are a Carven and, through an event, an admin does something that makes them robotic, all they need to do is toggle their `is_synthetic` flag and now they're affected by EMP.
 - No change made to the Idol species will affect this check - unless `is_synthetic` is altered.
 - If another robotic species is added, presumably with the `is_synthetic` flag, this will affect them too with no additional work required.

### Advanced Deflaking
So now we can create an EMP attack that'll hurt any robot it affects. But what if we want to take it further? What if we want it to damage electronics in the room?

First, we're going to backtrack. Let's take a look at the Character object. What we're going to do is add a new method to this object, also called `is_synthetic`.

```Python
class Character(DefaultCharacter):
    def at_object_creation(self):
        self.db.surname = ""
        self.db.prefix = ""
        self.db.suffix = ""
        ...

    @property
    def is_synthetic(self):
        return self.db.species.is_synthetic
```

Because the method returns a simple `True` or `False` value, we make it a property, so that it can be referred to as `is_synthetic` and not `is_synthetic()`. So let's take a look at the main logic of our EMP attack again, and change it to use this new functionality.

```Python
def func(self):
    attacker = self.caller
    tar = self.target

    if tar.is_synthetic:
        tar.echo(self.att_msg["1P_SYNTH"])
        do_synth_stuff()
    else:
        tar.echo(self.att_msg["1P"])
```

As you can see, we changed the conditional check from `tar.db.species.is_synthetic` to `tar.is_synthetic`. We rely on the Character object itself to check for its own Species data. Not only does this cut down on a bit of typing and make the code a little more readable, but it comes with an advantage that may not be immediately apparent.

Now, the attack can easily affect things that aren't Characters - or to be more precise, things that don't have a species. Let's see what else is in the room. How is the machinery in the room receiving power? Maybe it's coming from the cell rack on the wall:

```Python
class BatteryRack(PoweredObject, PowerStorageUnit):
    def at_object_creation(self):
        self.db.name = "cellrack"
        self.db.aliases = ["rack", "batteryrack", "battery rack", "cell rack"]
        self.db.fullname = "cell rack PSU"
        self.db.desc = "A specially modified power storage unit, used as an auxiliary or emergency source of energy. Its stores and draws power from the numerous power cells slotted into its frame."
        self.db.charge_level = 3000

    @property
    def is_synthetic(self):
        return True
```

Let's make it synthetic. Because we know it's synthetic, and will always be synthetic, we only need its `is_synthetic` method to return `True`. Very easily done. Now, assuming the EMP cycles over every character and object in the room, the cell rack is also affected!

This can mean any number of things - maybe an EMP should reduce an object's `charge_level` by half. Not physically accurate, but fun and easy to understand from a gameplay standpoint. Maybe synthetic objects have an `is_operational` method that determines whether its doing its job. The EMP can force this to return `False` for a few seconds.

Hopefully, you can see how with a little careful planning, avoiding snowflake code makes the game far more flexible.