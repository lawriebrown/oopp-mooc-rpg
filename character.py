""" Define Character and related classes for use in adventure game.

Written for the Object-oriented Programming in Python (OOPP) MOOC
initial code from: https://github.com/raspberrypilearning/oop-course/blob/master/character.py
Code additions Copyright 2018 by Lawrie Brown, licence CC-BY-NC-SA 3.0.
"""

from item import Item, Inventory
from room import Room
import random

class Character():
    """Define Character class with basic functionality for all characters in game."""

    def __init__(self, char_name, char_description = None):
        """ Create a character with given name & (optional) description.
        Also has attributes for conversation, current location,
        and an inventory of what things they have.
        """
        self.name = char_name
        self.description = char_description
        self.conversation = None
        self.location = None
        self.prob_move = 0.5
        self.items = Inventory()

    def __str__(self):
        """return name as string representation of self"""
        return self.name

    def get_name(self):
        """Returns the character's name"""
        return self.name

    def set_description(self, item_description):
        """Sets the character's description"""
        self.description = item_description

    def get_description(self):
        """Returns the character's description"""
        return self.description

    def set_conversation(self, conversation):
        """ Set what this character will say when talked to """
        self.conversation = conversation

    def get_location(self):
        """Returns the character's location"""
        return self.location

    def set_prob_move(self, prob):
        """ Set probability (0.0 - 1.0) this character will randomly move after some interaction """
        self.prob_move = prob

    def describe(self):
        """ Describe this character """
        print( self.name + " is here! " + self.description )
        if not self.items.is_empty():
            print("  and has " + str(self.items))

    def talk(self):
        """ Talk to this character, displaying conversation if set """
        if self.conversation is not None:
            print("[" + self.name + " says]: " + self.conversation)
        else:
            print(self.name + " doesn't want to talk to you")
        self.random_move()       

    def add(self, some_item):
        """add some_item to character's inventory (used in setup)"""
        self.items.add(some_item)

    def give(self, some_item):
        """offer to give some_item to character (declined by default).
        Returns True if accepted, False otherwise."""
        print(self.name + " declines your offer of " + str(some_item))
        return False

    def find(self, item_name):
        """Return item with item_name in character's inventory."""
        return self.items.find(item_name)

    def has(self, item_name):
        """Return true if character has item_name in inventory, else false"""
        return self.items.has(item_name)

    def take(self, item_name):
        """Try to take item from charcter (rejected by default)"""
        the_item = self.items.find(item_name)
        if the_item != None:
            print(self.name + " rejects your attempt to take "+ item_name)
        else:
            print(self.name + " doesn't have "+ item_name)       
        return None

    def fight(self, combat_item):
        """ Fight with this character, by default wont.
        Returns True if attacker survives, False if not.
        """
        print(self.name + " doesn't want to fight with you")
        return True

    def move_to(self, new_room):
        """ Move character into specified room.

        Change details for both character's location and room's occupant.
        If the room is already occupied, a ValueError is thrown."""
        if isinstance(new_room, Room):
            # swap location from current to new room
            if self.location != None:
                self.location.set_occupant(None)
            self.location = new_room
            new_room.set_occupant(self)
            return True
        return False

    def random_move(self):
        """ Randomly move character after some interactions.

        With probability specified by self.prob_move will choose a
        random direction from self.location and try to move_to it."""
        if random.random() < self.prob_move and self.location != None:
            direction = self.location.random_direction()
            new_room = self.location.move(direction)
            if new_room != self.location and new_room.get_occupant() == None:
                print(self.name + " leaves the room.")
                if self.location != None:
                    self.location.set_occupant(None)
                self.location = new_room
                new_room.set_occupant(self)
                return True
        return False

class Enemy(Character):
    """Define Enemy sub-class with details for enemy NPCs."""
    
    num_vanquished = 0
    """Count of how many enemies the player has vanquised (game metric)."""

    def __init__(self, char_name, char_description = None):
        """ Create an enemy character with given name & optional description.
        Also has attributes for weakness, the message displayed when wins a fight,
        and a flag indicating whether has lost a fight (which allows items to be taken)."""       
        super().__init__(char_name, char_description)
        self.weakness = None
        self.vanquishes = "overpowers you, puny adventurer"
        self.vanquished = False

    def set_weakness(self, weakness, vanquishes = None):
        """ Set enemy's weakness in a fight, along with optional vanquishes message"""
        self.weakness = weakness
        if vanquishes != None:
            self.vanquishes = vanquishes

    def was_vanquished(self):
        """Returns whether character has been vanquished in a fight"""
        return self.vanquished

    def get_weakness(self):
        """ Get enemy's weakness in a fight """
        return self.weakness

    def fight(self, combat_item):
        """ Fight with this enemy, succeeds if combat_item is its weakness.
        Updates Enemy.num_vanquished if enemy defeated. 
        Returns True if attacker survives, False if not.
        """
        if combat_item == self.weakness:
            print("You fend " + self.name + " off with the " + str(combat_item) )
            if not self.vanquished:
                Enemy.num_vanquished += 1
                self.vanquished = True
            return True
        else:
            print(self.name + " " + self.vanquishes)
            return False

    def take(self, item_name):
        """Try to take item from enemy.
        Only succeeds if enemy has item and been vanquished, returing item.
        Otherwise print result & return None."""
        the_item = self.items.find(item_name)
        if the_item != None:
            if self.vanquished:
                print(self.name + " dejectedly hands over "+ item_name)
                self.items.remove(the_item)
                return the_item
            else:
                print(self.name + " says you must win a fight to get "+ item_name)
                self.random_move()       
        else:
            print(self.name + " doesn't have "+ item_name)       
        return None

class Friend(Character):
    """Define Friend sub-class with details for friend NPCs."""

    num_desires_met = 0
    """Count of how many friend's desires the player has met (game metric)."""

    def __init__(self, char_name, char_description = None):
        """ Create an friend character with given name & optional description.
        Also has attributes for item desires,
        and the message displayed this is given."""       
        super().__init__(char_name, char_description)
        self.desires = None
        self.thank_msg = "Thanks you warmly for such a desirable gift."
        self.desire_met = False

    def set_desires(self, desires, thank_msg = None):
        """ Set friend's desires in a fight, along with optional thank_msg if given desire"""
        self.desires = desires
        if thank_msg != None:
            self.thank_msg = thank_msg

    def get_desires(self):
        """ Get friend's desires"""
        return self.desires

    def get_desire_met(self):
        """Returns whether character's desired item has been gifted"""
        return self.desire_met

    def give(self, some_item):
        """offer to give some_item to friend, who always accepts.
        If the gift is the friend's desired item, display thank_msg
        and update self.desire_met and Friend.num_desires_met.
        Returns True if accepted, False otherwise."""
        if self.desires == None:
            print(self.name + " declines your offer of " + str(some_item))
            return False
        print(self.name + " gladly accepts your offer of "+ str(some_item))
        self.items.add(some_item)
        if self.desires == some_item:
            if not self.desire_met:
                Friend.num_desires_met += 1
                self.desire_met = True
            if self.thank_msg != None:
                print(self.thank_msg)
        return True

    def take(self, item_name):
        """Try to take item from friend.
        Only succeeds if friend has desired item, and you're not trying to take it.
        Returns item if ok, otherwise print result & return None."""
        the_item = self.items.find(item_name)
        if the_item != None:
            if self.desire_met:
                if the_item != self.desires:
                    print(self.name + " hands over "+ item_name)
                    self.items.remove(the_item)
                    return the_item
                else:
                    print(self.name + " says you can't have my precious " + item_name)                    
                    self.random_move()       
            else:
                print(self.name + " says you must gift my desire for me to keep to get "+ item_name)
                self.random_move()       
        else:
            print(self.name + " doesn't have "+ item_name)       
        return None

class Player(Character):
    """Define Player sub-class with details for the game player."""

    def __init__(self, char_name, char_description = None):
        """ Create the player character with given name & optional description.
        Used to represent the game player, for consistent character use."""       
        super().__init__(char_name, char_description)

    def remove(self, some_item):
        """remove some_item from character's inventory"""
        self.items.remove(some_item)

    def carries(self):
        """ List items player currently has """
        if not self.items.is_empty():
            print("You currently have " + str(self.items))
        else:
            print("You don't have any items on you.")

    def describe(self):
        """ Describe items player currently has """
        if not self.items.is_empty():
            print("You currently have:")
            self.items.describe()
        else:
            print("You don't have any items on you.")

    def move_to(self, new_room):
        """ Change player location to specified room.
        Override Character method since not changing room occupant details."""
        if isinstance(new_room, Room):
            self.location = new_room
            return True
        return False

# Diagnostic main to test class
# "run this diagnostic test script if run file rather than importing it."

if __name__ == "__main__":
    """Diagnostic main to test class."""

    print("Test Character & child classes\n")

    # Test an example generic character
    print("Create character Catrina with a watch, & try to describe, talk, fight")
    catrina = Character("Catrina", "A friendly skeleton with a purple hat & orange scarf")
    catrina.add("watch")
    catrina.describe()
    catrina.talk()
    catrina.fight("pen")

    print("Set conversation for catrina & try to talk again")
    catrina.set_conversation("Shake, rattle & roll!")
    catrina.talk()
    
    print("Try to give/has/take things with Catrina (all declined or invalid)")
    catrina.take("pen")
    catrina.take("watch")
    catrina.give("wine")
    print("Catrina find watch is " + str(catrina.find("watch")))
    print("Catrina has watch is " + str(catrina.has("watch")))
    print("Catrina has pen is " + str(catrina.has("pen")))
    
    kitchen = Room("Kitchen", "A clean and tidy room with no food in sight.")
    print("Move Catrina to kitchen gave: " + str(catrina.move_to(kitchen)))
    parlour = Room("Parlour", "A plush inviting room with comfortable chairs.")
    parlour.link_room(kitchen, "east", "west")
    catrina.set_prob_move(1.0)
    catrina.talk()
    print("Catrina is in the " + str(catrina.get_location()))
    print("")

    # Test an eneny
    print("Create enemy Dave, with a rattle & bones, then try to describe, talk")
    dave = Enemy("Dave", "A smelly zombie")
    dave.add("rattle")
    dave.add("bones")
    dave.describe()
    dave.talk()

    print("Set conversation for Dave & try to talk again")
    dave.set_conversation("Brains...I want braaaaiins!!")
    dave.talk()

    print("Set Dave's weakness as garlic, try to fight with sword then garlic, and to give/take things")
    dave.set_weakness("garlic", "eats your brains, puny adventurer")
    print(dave.get_name() + " weakness is " + dave.get_weakness())
    print("Show if Dave has been vanquished: " + str(dave.was_vanquished()))
    dave.give("wine")
    dave.take("bones")
    dave.fight("sword")
    dave.fight("garlic")
    print("Show if Dave has been vanquished: " + str(dave.was_vanquished()))
    dave.take("bones")
    dave.describe()
    print("Enemy.num_vanquished is " + str(Enemy.num_vanquished) )
    print("")

    # Test a friend
    print("Create friend Carlotta, with a fan, conversation, then describe, talk")
    carlotta = Friend("Carlotta", "A prima donna in a large ball-gown who seems nervous.")
    carlotta.add("fan")
    carlotta.set_conversation("I really need something to settle my nerves before I perform.")
    carlotta.describe()
    carlotta.talk()

    print("Set carlotta's desires as wine, and try to give/take things")
    carlotta.set_desires("wine", "She thanks you for this gift, and then comments that 'shazam' is the magic word, if you carry just the right things!")
    print(carlotta.get_name() + " desires is " + carlotta.get_desires())
    carlotta.take("fan")
    carlotta.give("hat")
    carlotta.give("wine")
    carlotta.take("fan")
    carlotta.take("wine")
    carlotta.describe()
    print("Friend.num_desires_met is " + str(Friend.num_desires_met) )
    print("")

    # Test a player character
    print("Create player me with a knife & watch, test add, carries, describe, remove")
    me = Player("Me", "That would be you!")
    me.add("knife")
    me.add("watch")
    me.carries()
    me.describe()
    me.remove("knife")
    me.carries()
    print("Me find watch is " + str(me.find("watch")))
    print("Me has watch is " + str(me.has("watch")))
    print("Me has pen is " + str(me.has("pen")))
    print("Move Me to kitchen gave: " + str(me.move_to(kitchen)))
    print("")
    
