from utilities.utils_string import RPFormat
from typeclasses.colors import GameColors

def ProcessSpeech(self, message, msg_self = None, msg_location = None, receivers = None, msg_receivers = None, **kwargs):
    """
    Display the actual say (or whisper) of self.

    This hook should display the actual say/whisper of the object in its
    location.  It should both alert the object (self) and its
    location that some text is spoken.  The overriding of messages or
    |mapping` allows for simple customization of the hook without
    re-writing it completely.

    Args:
        message (str): The message to convey.
        msg_self (bool or str, optional): If boolean True, echo |message` to self. If a string,
            return that message. If False or unset, don't echo to self.
        msg_location (str, optional): The message to echo to self's location.
        receivers (Object or iterable, optional): An eventual receiver or receivers of the message
            (by default only used by whispers).
        msg_receivers(str): Specific message to pass to the receiver(s). This will parsed
            with the {receiver} placeholder replaced with the given receiver.
    Kwargs:
        whisper (bool): If this is a whisper rather than a say. Kwargs
            can be used by other verbal commands in a similar way.
        mapping (dict): Pass an additional mapping to the message.

    Notes:


        Messages can contain {} markers. These are substituted against the values
        passed in the |mapping` argument.

            msg_self = 'You say: "{speech}"'
            msg_location = '{object} says: "{speech}"'
            msg_receivers = '{object} whispers: "{speech}"'

        Supported markers by default:
            {self}: text to self-reference with (default 'You')
            {speech}: the text spoken/whispered by self.
            {object}: the object speaking.
            {receiver}: replaced with a single receiver only for strings meant for a specific
                receiver (otherwise 'None').
            {all_receivers}: comma-separated list of all receivers,
                                if more than one, otherwise same as receiver
            {location}: the location where object is.
    """

    message = RPFormat(message)
    msg_type = "say"
    colors = GameColors()
    light, dark = colors.SPEECH_LIGHT, colors.SPEECH_DARK

    if kwargs.get("whisper", False):
        # Player is whispering.
        msg_type = "whisper"
        msg_self = '{self} whisper to {all_receivers}, "{speech}"' if msg_self is True else msg_self
        msg_receivers = '{object} whispers: "{speech}"'
        msg_receivers = msg_receivers or '{object} whispers: "{speech}"'
        msg_location = None
    else:
        msg_self = '{self} say, "{speech}"' if msg_self is True else msg_self
        msg_location = msg_location or '{object} says, "{speech}"'
        msg_receivers = msg_receivers or message

    # Custom mapping is passed through arbitrary additional arguments.
    custom_mapping = kwargs.get('mapping', {})
    receivers = make_iter(receivers) if receivers else None
    location = self.location

    if msg_self:
        self_mapping = {"self": "You",
                        "object": self.get_display_name(self),
                        "location": location.get_display_name(self) if location else None,
                        "receiver": None,
                        "all_receivers": ", ".join(
                            recv.get_display_name(self)
                            for recv in receivers) if receivers else None,
                        "speech": message}
        # If we added more mapping, inject it now
        self_mapping.update(custom_mapping)
        self.msg(text = (msg_self.format(**self_mapping), {"type": msg_type}), from_obj = self)

    if receivers and msg_receivers:
        receiver_mapping = {"self": "You",
                            "object": None,
                            "location": None,
                            "receiver": None,
                            "all_receivers": None,
                            "speech": message}
        for receiver in make_iter(receivers):
            individual_mapping = {"object": self.get_display_name(receiver),
                                    "location": location.get_display_name(receiver),
                                    "receiver": receiver.get_display_name(receiver),
                                    "all_receivers": ", ".join(
                                        recv.get_display_name(recv)
                                        for recv in receivers) if receivers else None}
            receiver_mapping.update(individual_mapping)
            receiver_mapping.update(custom_mapping)
            receiver.msg(text=(msg_receivers.format(**receiver_mapping),
                            {"type": msg_type}), from_obj=self)

    if self.location and msg_location:
        location_mapping = {"self": "You",
                            "object": self,
                            "location": location,
                            "all_receivers": ", ".join(str(recv) for recv in receivers) if receivers else None,
                            "receiver": None,
                            "speech": message}
        location_mapping.update(custom_mapping)
        exclude = []
        if msg_self:
            exclude.append(self)
        if receivers:
            exclude.extend(receivers)
        self.location.msg_contents(text=(msg_location, {"type": msg_type}),
                                    from_obj=self,
                                    exclude=exclude,
                                    mapping=location_mapping)