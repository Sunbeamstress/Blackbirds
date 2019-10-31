"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia import DefaultObject
from evennia.utils import logger

class Object(DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved to
                           database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
                                  back to this class
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     sessions (list of Sessions, read-only) - returns all sessions connected
                       to this object
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this
                             self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
                             a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_before_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_after_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_after_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

     """

    def at_object_creation(self):
        self.db.long_desc = "An object lies here."
        self.db.short_desc = "a nondescript object"

    def update(self):
        pass

    def echo(self, string, prompt = False):
        # At this moment, simply a lazy method wrapper that sends a message to the object,
        # then displays a prompt.
        self.msg(string)
        if prompt == True:
            self.msg(prompt = self.prompt())

    def prompt(self):
        "Returns the object's prompt, if applicable."
        # Placeholder for now - replace with real one later.
        HP, MP, END, WIL = 500, 500, 1500, 1500
        p_string = f"|cH:|n{HP} |cM:|n{MP} |cE:|n{END} |cW:|n{END} |x-|n "
        return p_string

    def move_to(self, destination, quiet = False, move_hooks = True, **kwargs):
        # self: obvious.
        # destination: handled by dir-based move method
        # quiet: if true, won't display enter/exit messages
        # move_hooks: if False, bypasses at_move/before_move on objects

        # should return True if move was successful, and False if not

        # all access/ability checks should be handled before this method!
        # if we've gotten to move_to, everything is green and we are ready
        # to move the object.

        def error_msg(string = "", err = None):
            """Simple log helper method"""
            logger.log_trace()
            self.echo("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        errtxt = _("Couldn't perform move ('%s'). Contact an admin.")

        if not destination:
            self.echo("|xYou can't seem to figure out how to get there.|n")
            return False

        if move_hooks:
            try:
                if not self.at_before_move(destination):
                    return False
            except Exception as err:
                error_msg(errtxt % "at_before_move()", err)
                return False

        source_location = self.location
        if move_hooks and source_location:
            try:
                source_location.at_object_leave(self, destination)
            except Exception as err:
                error_msg(errtxt % "at_object_leave()", err)
                return False

        if not quiet:
            try:
                self.announce_move_from(destination, **kwargs)
            except Exception as err:
                error_msg(errtxt % "at_announce_move()", err)
                return False

        try:
            self.location = destination
        except Exception as err:
            error_msg(errtxt % "location change", err)
            return False

        if not quiet:
            # Tell the new room we are there.
            try:
                self.announce_move_to(source_location, **kwargs)
            except Exception as err:
                error_msg(errtxt % "announce_move_to()", err)
                return False

        if move_hooks:
            # Perform eventual extra commands on the receiving location
            # (the object has already arrived at this point)
            try:
                destination.at_object_receive(self, source_location)
            except Exception as err:
                error_msg(errtxt % "at_object_receive()", err)
                return False

        # Execute eventual extra commands on this object after moving it
        # (usually calling 'look')
        if move_hooks:
            try:
                self.at_after_move(source_location)
            except Exception as err:
                error_msg(errtxt % "at_after_move", err)
                return False
        return True