""" Define Room class used in adventure game.

Written for the Object-oriented Programming in Python (OOPP) MOOC
Code additions Copyright 2018 by Lawrie Brown, licence CC-BY-NC-SA 3.0.
"""

from item import Item, Inventory
import random

class Room():

    num_rooms_visited = 0
    """Count of how many rooms the player has visited (game metric)."""

    def __init__(self, room_name, room_description = None):
        """Create a room with the supplied name & optional description
        A room also has a list of linked_rooms it connects to,
        a occupant who may be in the room, whether player has visited,
        a key item that may be used in the room, with message & flag if used,
        and the inventory of room contents
        """
        self.name = room_name
        self.description = room_description
        self.linked_rooms = {}
        self.occupant = None
        self.visited = False
        self.key_item = None
        self.item_used_msg = "Nothing much seems to happen."
        self.item_used = False
        self.contents = Inventory()

    def __str__(self):
        """return name as string representation of self"""
        return self.name

    # Getters and setters for Room attributes
    def set_description(self, room_description):
        """Sets the room description"""
        self.description = room_description

    def get_description(self):
        """Returns the room description"""
        return self.description

    def get_name(self):
        """Returns the room name"""
        return self.name

    def set_occupant(self, new_occupant):
        """Sets the room occupant, if not occupied"""
        if self.occupant == None or new_occupant == None:
            self.occupant = new_occupant
        else:
            raise ValueError('### Error: ' + str(new_occupant) +
                               ' trying to replace existing room occupant ' +
                               str(self.occupant) + ' in room ' + self.name)

    def get_occupant(self):
        """Returns the room occupant"""
        return self.occupant

    def set_key_item(self, key_item, item_used_msg = None):
        """ Set key_item that may be used in room, along with message to show if used."""
        self.key_item = key_item
        if item_used_msg != None:
            self.item_used_msg = item_used_msg

    def get_key_item(self):
        """ Get room's key item"""
        return self.key_item

    def get_item_used(self):
        """Returns whether room's key item has been used"""
        return self.item_used

    # Methods to interact with room
    def describe(self):
        """Prints a description of the room with:
        name, description, occupant, contents, linked rooms.
        Also updates the room visited flag and class counter.
        """
        print( self.name )
        print( "-" * len(self.name) )
        print( self.description )
        occupant = self.get_occupant()
        if occupant is not None:
            occupant.describe()
        if not self.contents.is_empty():
            print ("In the room you see:")
            self.contents.describe()
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print( "The " + room.get_name() + " is " + direction )
        print ("")
        if not self.visited:
            Room.num_rooms_visited += 1
            self.visited = True

    def link_room(self, room_to_link, direction, direction_back = None):
        """Link named room to self in given direction, adding link in direction_back if given"""
        if direction in self.linked_rooms:
            raise ValueError('### Error: ' + str(room_to_link) +
                               ' in direction ' + str(direction) +
                               ' trying to replace existing linked room ' +
                               str(self.linked_rooms[direction]) +
                               ' in room ' + self.name)
        self.linked_rooms[direction] = room_to_link
        if direction_back != None:
            room_to_link.link_room(self, direction_back)

    def move(self, direction):
        """Move between rooms returning the new room if direction valid, self if not"""
        if direction == None:
            return self
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def check_direction(self, direction):
        """Return room in specified direction if exists, None otherwise"""
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            return None

    def random_direction(self):
        """Return a random direction from those available in this room."""
        if len(self.linked_rooms) == 0:
            return None
        direction = random.choice(list(self.linked_rooms.keys()))
        return direction

    def find(self, item_name):
        """Return item with item_name in room contents"""
        return self.contents.find(item_name)

    def has(self, item_name):
        """Return true if item_name in in room contents, else false"""
        return self.contents.has(item_name)

    def leave(self, some_item):
        """leave some_item in room contents"""
        self.contents.add(some_item)
 
    def take(self, item_name):
        """Remove named item from room contents, returning item if present or None if not"""
        the_item = self.contents.find(item_name)
        if the_item != None:
            self.contents.remove(the_item)
            return the_item
        return None

    def use(self, some_item):
        """try to use some_item in this room.
        If the item is the room's key item, display item_used_msg & update flag.
        Returns True if successfully used, False otherwise."""
        if self.key_item == some_item:
            self.item_used = True
            if self.item_used_msg != None:
                print(self.item_used_msg)
            return True
        return False

# Diagnostic main to test class
# "run this diagnostic test script if run file rather than importing it."
if __name__ == "__main__":
    print("Test Room class\n")

    # Some example rooms
    print("Create and display some example rooms:\n")
    cellar = Room("Cellar")
    cellar.set_description("A cool dark room with a large well-stocked wine rack!")
    print("Created " + cellar.get_name())
    dining_hall = Room("Dining Hall", "A large ornate room with polished wooden walls and a plush carpeted floor.")
    print("Created " + dining_hall.get_name())
    ballroom = Room("Ballroom", "A vast room with a shiny wooden floor. Huge wooden statues guard the entrance")
    print("Created " + ballroom.get_name())
    print("Random direction from dining_hall (none exist): " + str(dining_hall.random_direction()))

    # link rooms together
    dining_hall.link_room(cellar, "downstairs")
    cellar.link_room(dining_hall, "upstairs")
    dining_hall.link_room(ballroom, "west", "east")

    # add some simple items
    dining_hall.leave("food")
    cellar.leave("wine")
    key = Item("key", "an ordinary looking house key")
    dining_hall.leave(key)

    # test display details
    ballroom.describe()
    dining_hall.describe()
    cellar.describe()
    print("dining_hall has watch is " + str(dining_hall.has("watch")))
    print("dining_hall find food is " + str(dining_hall.find("food")))
    print("dining_hall has food is " + str(dining_hall.has("food")))
    print("Number of Rooms visited is " + str(Room.num_rooms_visited) )

    #test key_item setting, display & use
    torch = Item("torch", "A compact but powerful torch")
    cellar.set_key_item(torch, "You see a powerful incantation on the wall!")
    print(cellar.get_name() + " key item is " + str(cellar.get_key_item()))
    print("Using key item gives: " + str(cellar.use(torch)))
    print("Using other item gives: " + str(cellar.use(key)))
    print("Item used flag is: " + str(cellar.get_item_used()))

    # test moving between rooms
    loc = cellar
    print("Try moving upstairs from " + loc.get_name())
    loc = loc.move("upstairs")
    print("Now in " + loc.get_name())
    print("Try moving south from " + loc.get_name())
    loc = loc.move("south")
    print("Now in " + loc.get_name())
    print("Random direction from dining_hall: " + dining_hall.random_direction())
