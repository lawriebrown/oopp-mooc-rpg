""" World contains all the details used in the adventure game.

This includes all rooms and their links, characters, and items.
It also has the main game loop in the play method used to run the game.

When created, a configuration dictionary is used. This can be passed
to the constructor, otherwise the default_config in game_config.py is used.
That file describes the configuration dictionary format.

Written for the Object-oriented Programming in Python (OOPP) MOOC
Code additions Copyright 2018 by Lawrie Brown, licence CC-BY-NC-SA 3.0.
"""

from character import Character, Enemy, Friend, Player
from game_config import default_config
from item import Item, Inventory
from room import Room
import sys

class World():
    """ Contains all the details used in the adventure game.
    This includes all rooms and their links, characters, and items.
    It also has the main game loop in the play method used to run the game.
    """

    def __init__(self, config = None):
        """Create a game world using the supplied configuration details.
        If no config specified, then use default_config world configuration.
        The game world has: title, rooms, characters, items, messages,
        and the success criteria.
        """
        # use default_config is none supplied
        if config == None:
            config = default_config

        # instance variables for a world
        self.title = config['title']
        self.rooms = {}
        self.items = {}
        self.characters = {}
        self.player = None
        self.messages = config['messages']
        self.success = config['success']

        # populate the world using the configuration details
        try:
            # configure rooms
            doing = "rooms"
            # room config has: (name, description, key_item, used_msg)*
            keyitems = []               # list of key items to config later
            for conf in config['rooms']:
                self.rooms[conf[0]] = Room(conf[0], conf[1])
                if conf[3] != None:     # key items to be set when have items
                    keyitems.append((conf[0], conf[2], conf[3]))        # (room, item, msg)

            # configure links between rooms
            doing = "links"
            # links config has: (room1, direction1, room2, direction2)*
            for conf in config['links']:
                self.rooms[conf[0]].link_room(self.rooms[conf[2]], conf[1], conf[3] )
            # configure items
            doing = "items"
            # items config has: (name, description, location)
            player_items = []           # list of player items to config later
            for conf in config['items']:
                self.items[conf[0]] = Item(conf[0], conf[1])
                if conf[2] in self.rooms:     # place item in room
                    self.rooms[conf[2]].leave(self.items[conf[0]])
                else:                   # item on character to add later
                    player_items.append((conf[0], conf[2]))

            # now configure key_items in rooms - has (room, item, msg)
            doing = "key_items"
            for conf in keyitems:
                self.rooms[conf[0]].set_key_item(self.items[conf[1]], conf[2])

            # configure characters (enemies, friends, player)
            doing = "enemies"
            # links config has: (name, description, conversation, location, weakness, defeat_msg)*
            for conf in config['enemies']:
                self.characters[conf[0]] = Enemy(conf[0], conf[1])
                self.characters[conf[0]].set_conversation(conf[2])
                self.characters[conf[0]].move_to(self.rooms[conf[3]])
                if conf[4] != None:
                    self.characters[conf[0]].set_weakness(self.items[conf[4]], conf[5])

            doing = "friends"
            # friends config has: (name, description, conversation, location, desire, thank_msg)*
            for conf in config['friends']:
                self.characters[conf[0]] = Friend(conf[0], conf[1])
                self.characters[conf[0]].set_conversation(conf[2])
                self.characters[conf[0]].move_to(self.rooms[conf[3]])
                if conf[4] != None:
                    self.characters[conf[0]].set_desires(self.items[conf[4]], conf[5])

            doing = "players"
            # players config has: (name, description, location)*
            num_players = 0
            for conf in config['players']:
                self.characters[conf[0]] = Player(conf[0], conf[1])
                self.characters[conf[0]].move_to(self.rooms[conf[2]])
                self.player = self.characters[conf[0]]
                num_players += 1
            if num_players != 1:
                print ("You can only have 1 player character in the game!")

            # now configure player_items on characters - has (item, character)
            doing = "player_items"
            for conf in player_items:
                self.characters[conf[1]].add(self.items[conf[0]])

        except (IndexError, KeyError, ValueError) as msg:
            print ("### Error: Incorrect format or values in " + doing + " config: " + str(conf))
            print(str(msg))
            raise

    def __str__(self):
        """return name as string representation of this world."""
        return (self.title + " has " + str(len(self.rooms)) + " rooms, " +
            str(len(self.characters)) + " characters, and " +
            str(len(self.items)) + " items.")

    def __check_success(self):
        """Check whether player has met success criteria for game on exit."""
        item_needed = self.player.find(self.success[1])
        item_not_have = self.player.find(self.success[2])
        if ((item_needed != None) and (item_not_have == None) and
            (Enemy.num_vanquished >= self.success[3]) and
            (Friend.num_desires_met >= self.success[4]) and
            (Room.num_rooms_visited >= self.success[5])):
            return True
        else:
            return False

    def play(self):
        """Play adventure in this world.
        
        Will repeatedly prompt user for command, and execute it.
        (Most) available commands are shown by 'help'.
        """

        # initial consistency checks
        if self.player == None:
            print("You must define a player in the game config in order to play!")
            return False

        #setup details for main loop
        current_room = self.player.get_location()       # starting room
        escaped = False         # whether have met conditions to escape
        keep_playing = True     # whether game continues
        last_described = None   # room last described so describe on entry
        magic_word = self.success[0]    # magic word to escape
        print("Welcome to " + self.title)
        print(self.messages['intro'])
        self.player.carries()

        # main game loop to get command from player and respond to it
        while keep_playing:

            # give details about current location if new room
            if current_room != last_described:
                print("You are in the:")
                current_room.describe()
                last_described = current_room

            # get input from user & split into words
            inp = input("> ")
            cmd_words = inp.split()
            if len(cmd_words) == 0:
                continue
            command = cmd_words[0]

            # process requested command
            if command == "exit":
                keep_playing = False

            # fight current room occupant
            elif command == "fight":
                occupant = current_room.get_occupant()
                if occupant == None:
                    print( "Fight who? There's no-one here!" )
                    continue
                if len(cmd_words) < 2:
                    print("You need to say what you want to fight with!")
                    continue
                what = cmd_words[1]
                weapon = self.player.find(what)
                if weapon != None:
                    if not occupant.fight(weapon):
                        keep_playing = False
                else:
                    print("You don't have " + what + " to fight with!")

            # give item to current room occupant
            elif command == "give":
                if len(cmd_words) < 2:
                    print("You need to say what item you want to give!")
                    continue
                what = cmd_words[1]
                if not self.player.has(what):
                    print("You don't have " + what + " to give!")
                    continue
                occupant = current_room.get_occupant()
                if occupant == None:
                    print("There is no-one here to give " + what + " to!")
                    continue
                item = self.player.find(what)
                if occupant.give(item):
                    self.player.remove(item)

            # go to room in specified direction
            elif command == "go":
                if len(cmd_words) < 2:
                    print("You need to say what direction you want to go in!")
                    continue
                direction = cmd_words[1]
                current_room = current_room.move(direction)
                self.player.move_to(current_room)

            # display help text
            elif command == "help":
                print (self.messages['help'])

            # leave item in current room
            elif command == "leave" or command == "drop":
                if len(cmd_words) < 2:
                    print("You need to say what item you want to leave!")
                    continue
                what = cmd_words[1]
                if not self.player.has(what):
                    print("You don't have " + what + " to leave!")
                    continue
                item = self.player.find(what)
                self.player.remove(item)
                current_room.leave(item)

            # list items player currently has
            elif command == "list" or command == "have":
                self.player.describe()

            # describe current room
            elif command == "look":
                if len(cmd_words) >= 2:     # get description of some item or room
                    what = cmd_words[1]
                    occupant = current_room.get_occupant()
                    item = self.player.find(what)    # see if player has item
                    if item != None:
                        item.describe()
                    elif occupant != None and what == occupant.get_name():    # occupant
                        occupant.describe()
                    elif current_room.has(what):    # or item in room
                        item = current_room.find(what)
                        if item != None:
                            item.describe()
                    elif occupant != None and occupant.has(what):   # or on occupant
                        item = occupant.find(what)
                        if item != None:
                            item.describe()
                    elif what in current_room.linked_rooms:
                        current_room.linked_rooms[what].describe()
                    else:                   # invalid item or room direction
                        print("There is no " + what + " here to look at!")                
                    continue
                # otherwise just describe what you carry & current room
                self.player.carries()
                print("You are in the:")
                current_room.describe()

            # take item from current room occupant
            elif command == "take":
                if len(cmd_words) < 2:
                    print("You need to say what item you want to take!")
                    continue
                what = cmd_words[1]
                occupant = current_room.get_occupant()
                if occupant != None and occupant.has(what):
                    took = occupant.take(what)
                    if took != None:
                        self.player.add(took)
                elif current_room.has(what):           
                    took = current_room.take(what)
                    if took != None:
                        print("You take the " + what)
                        self.player.add(took)
                else:
                    print(what + " is not here to take!")

            # talk to current room occupant
            elif command == "talk":
                occupant = current_room.get_occupant()
                if occupant == None:
                    print( "Talk to who? There's no-one here!" )
                else:
                    occupant.talk()

            # use item in current room
            elif command == "use":
                if len(cmd_words) < 2:
                    print("You need to say what item you want to use!")
                    continue
                what = cmd_words[1]
                item = self.player.find(what)           # see it player has item
                if item == None:
                    item = current_room.find(what)      # or if item in room
                if item != None:
                    if not current_room.use(item):
                        print("Nothing much seems to happen.")
                else:
                    print("You don't have " + what + " to use!")

            # command is magic word to escape, check if successful or not!
            elif command == magic_word:
                escaped = self.__check_success()
                if escaped:
                    keep_playing = False
                    print("There is a blinding flash of light ... and you are elsewheresville!")
                else:
                    print("The word echoes around the room ... but nothing else happens")

            # unrecognized command
            else:
                print("Unknown command. 'help' lists (most) available commands.")

        # leaving game, see if escaped or not
        print("You have vanquished " + str(Enemy.num_vanquished) + " enemies.")
        print("You have met " + str(Friend.num_desires_met) + " friend's desires.")
        print("You have visited " + str(Room.num_rooms_visited) + " rooms.")
        self.player.carries()
        if escaped:
            print(self.messages['exit_success'])
            return True
        else:
            print(self.messages['exit_fail'])
            return False


# Diagnostic main to test class
# "run this diagnostic test script if run file rather than importing it."
if __name__ == "__main__":

    test_world = World()
    print ("\nTesting " + test_world.title)
    print (str(test_world))

    if len(sys.argv) > 1:       # more details if give arg on command-line
        print ("\nwith rooms:")
        for name in test_world.rooms:
            test_world.rooms[name].describe()
        print ("\nand characters:")
        for name in test_world.characters:
            print(name + ": ", end="")
            test_world.characters[name].describe()
            print("  with conversation: " + 
                  str(test_world.characters[name].conversation))
        print ("\nand items:")
        for name in test_world.items:
            test_world.items[name].describe()
        print ("\nwith player: " + str(test_world.player))
        print ("\nmessages: " + str(test_world.messages))
        print ("\nsuccess: " + str(test_world.success))

