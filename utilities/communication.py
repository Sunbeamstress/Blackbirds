from utilities.string import autoformat

def process_speech(self, message, msg_self = None, msg_location = None, receivers = None, msg_receivers = None, **kwargs):
    message = autoformat(message)
    msg_type = "say"
    light, dark = "C", "c"

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