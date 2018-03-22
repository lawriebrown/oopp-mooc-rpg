""" Define Item and Inventory classes used in adventure game

Written for the Object-oriented Programming in Python (OOPP) MOOC
Code additions Copyright 2018 by Lawrie Brown, licence CC-BY-NC-SA 3.0.
"""

class Item():
    """ Some thing which may be present in a room or carried by a character. """

    def __init__(self, item_name, item_description = None):
        """Create item with the supplied name, and optional description"""
        self.name = item_name
        self.description = item_description

    def __str__(self):
        """return name as string representation of self"""
        return self.name
    
    # Getters and setters for Item attributes
    def get_name(self):
        """Returns the item name"""
        return self.name

    def get_description(self):
        """Returns the item description"""
        return self.description

    def set_description(self, item_description):
        """Sets the item description"""
        self.description = item_description

    # Methods to interact with item
    def describe(self):
        """Prints a description of the item"""
        print( self.name + " - " + self.description )


class Inventory():
    """ A collection of things (Items, strings) present in a room or carried by a character. """

    def __init__(self):
        """Create empty inventory disctionary"""
        self.contents = {}

    def __str__(self):
        """return string representation of contents"""
        if len(self.contents) == 0:
            return ""
        description = "["
        for i in self.contents:     # get all keys (names) form contents
            description += i + ", "
        return description[:-2] + "]"

    # Methods to interact with inventory

    def add(self, some_item):
        """add some_item to contents"""
        name = str(some_item)       # get name (as string version of item)
        self.contents[name] = some_item
 
    def remove(self, some_item):
        """remove some_item from contents"""
        name = str(some_item)       # get name (as string version of item)
        self.contents.pop(name)     # and pop value to remove item
 
    def find(self, item_name):
        """find item by name in contents, returning item if present or None if not"""
        if item_name in self.contents:
            return self.contents[item_name]
        return None
 
    def has(self, item_name):
        """return true/false if named item in contents"""
        return (item_name in self.contents)

    def describe(self):
        """Prints description of item's in contents"""
        for i in self.contents:
            print (" + ", end="")
            try:                    # try to use describe method for item/character
                self.contents[i].describe()
            except AttributeError:  # if fails, just go with str
                print(str(self.contents[i]))

    def is_empty(self):
        """return true if nothing in inventory, false if have contents"""
        return (len(self.contents) == 0)

    def size(self):
        """return number of items in contents"""
        return len(self.contents)



# Diagnostic main to test class
# "run this diagnostic test script if run file rather than importing it."
if __name__ == "__main__":
    print("Test Item and Inventory classes\n")

    # Some example items
    knife = Item("Carving Knife")
    knife.set_description("A long razor sharp knife with an elegantly carved handle")
    print("Created a " + knife.get_name())
    knife.describe()

    key = Item("Ornate Door Key")
    key.set_description("An ornate skeleton key")
    print("Created a " + key.get_name())
    key.describe()

    # An example inventory
    print("Create inventory my_stuff, add 2 items & 2 strings, print short & long")
    my_stuff = Inventory()
    print("Is newly created my_stuff empty? " + str(my_stuff.is_empty()))
    print("Size of my_stuff is: " + str(my_stuff.size()))
    my_stuff.add(knife)
    my_stuff.add("Some random text")
    my_stuff.add(key)
    my_stuff.add("Shhhh")
    print("my_stuff contains " + str(my_stuff))
    print("The contents of my_stuff are:")
    my_stuff.describe()
    print("Is my_stuff empty? " + str(my_stuff.is_empty()))
    print("Size of my_stuff is: " + str(my_stuff.size()))
    print("Try finding both item & string by name")
    print("find 'Carving Knife' gives: " + str(my_stuff.find("Carving Knife")))
    print("find 'No Such Thing' gives: " + str(my_stuff.find("No Such Thing")))
    print("find 'Shhhh' gives: " + str(my_stuff.find("Shhhh")))
    print("has 'Carving Knife' gives: " + str(my_stuff.has("Carving Knife")))
    print("has 'No Such Thing' gives: " + str(my_stuff.has("No Such Thing")))
    print("Remove knife & 'Shhhh' results in list:")
    my_stuff.remove(knife)
    my_stuff.remove("Shhhh")
    my_stuff.describe()
    print("Size of my_stuff is: " + str(my_stuff.size()))

    # empty inventory
    print("Create empty inventory, print short & long")
    no_stuff = Inventory()
    print("Is newly created no_stuff empty? " + str(no_stuff.is_empty()))
    print("no_stuff contains " + str(no_stuff))
    print("The contents of no_stuff are:")
    no_stuff.describe()
    

    



