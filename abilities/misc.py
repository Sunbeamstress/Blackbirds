from typeclasses.abilities import Ability

class TestAbility(Ability):
    def __init__(self):
        super().__init__()
        self.key = "test_ability"
        self.name = "The Super Neat Test Ability"
        self._description = "A super cool test ability you'll use to see if any of this nonsense works."
        self.tiers = {
            1: "This is the first level of your ability. It's a really cool and versatile ability, not too flashy, but you're sure glad you dumped the AP into it.",
            2: ("This is the second level of your ability.", "It also does this neato thing."),
            3: "This is the third level of your ability. This is often the really superfluous one that nonetheless is worthwhile, since it almost always unlocks a new hidden tree."
        }