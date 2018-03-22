""" Define the default world configuration for the adventure.

The game configuration is detailed in a dictionary of the following form:

config = {
    'title': "title for game world",
    'rooms': [ (name, description, key_item, used_msg)* ],
    'links': [ (room1, direction1, room2, direction2)* ],
    'items': [ (name, description, location)* ],
    'enemies': [ (name, description, conversation, location, weakness, defeat_msg)* ],
    'friends': [ (name, description, conversation, location, desire, thank_msg)* ],
    'players': [ (name, description, location)* ],
    'messages': { name: text },
    'success': (magic_word, item_needed, item_not_have, num_enemies, num_friends, num_rooms)
}
"""

import sys

# specify default game world configuration

default_config = {
### Set the title of the game ###
'title': "Lawrie's Haunted House Adventure Game",

## Describe each room in the game ###
'rooms': [
  # (name, description, key_item, used_msg)*
  ("Ballroom",
   "A vast room with a shiny wooden floor. Huge wooden statues guard the entrance",
   None, None),
  ("Bathroom",
   "A rather dingy looking room with a large stained bath that has seen better days!",
   None, None),
  ("Cellar",
   "A cool dimly lit room with a large well-stocked wine rack!",
   "torch", 
   "You see written on the wall:\n    'The enchanted sword will vanquish armour, but is cursed to never leave the house!'"),
  ("Dining Hall",
   "A large ornate room with polished wooden walls and a plush carpeted floor.",
   None, None),
  ("Entry Hall",
   "A marble lined formal entry hall, with suits of armour standing by the walls.\nThe main doors to the south appear to be barred shut!",
   None, None),
  ("Grand Staircase",
   "An elegant marble staircase leads up to the landing you are on, and then continues either side to the upper floor.",
   None, None),
  ("Guest Room",
   "A darkened room with a collapsing bed and a ramshakle wardrobe.",
   None, None),
  ("Kitchen",
   "A warm and cozy room with a large cast iron stove.",
   "knife", "You gag on the smell as you slice open the roast!"),
  ("Library",
   "A musty smell pervades this room, packed with bookcase filled with ancient tomes. In the centre are a couple of collapsing armchairs around a small table.",
   "steps", "You use the steps to reach for a volume on the top shelf, and almost knock yourself out when it falls on you!"),
  ("Master Bedroom",
   "A large poster bed dominates the room, with dark wood pannelling on the walls.",
   None, None),
  ("Parlour",
   "A plush inviting room with comfortable lounges & small tables.",
   "cards", "You try to make a move in the card game, but the cards rearrange themselves back to how they were, and you hear a faint whisper of laughter behind you!"),
  ("Upstairs Hall",
   "A large square hallway links the stairs to the upper rooms.",
   None, None)
],

### Describe links between the rooms
'links': [
  # (room1, direction1, room2, direction2)*
  ("Ballroom", "north", "Parlour", "south" ),
  ("Entry Hall", "east", "Dining Hall", "west"),
  ("Entry Hall", "west", "Ballroom", "east" ),
  ("Entry Hall", "up", "Grand Staircase", "down" ),
  ("Entry Hall", "ne", "Kitchen", "sw" ),
  ("Entry Hall", "nw", "Parlour", "se" ),
  ("Grand Staircase", "up", "Upstairs Hall", "down"),
  ("Kitchen", "south", "Dining Hall", "north"),
  ("Kitchen", "down", "Cellar", "up"),
  ("Parlour", "east", "Kitchen", "west"),
  ("Upstairs Hall", "east", "Library", "west"),
  ("Upstairs Hall", "west", "Master Bedroom", "east"),
  ("Upstairs Hall", "nw", "Bathroom", "se"),
  ("Upstairs Hall", "ne", "Guest Room", "sw")
],

## Describe each item in the game ###
'items': [
  # (name, description, location)*
  ("book", "A large leather bound volume lies open on the table.\n    You see a page on zombies that notes they are repelled by garlic.", "Library"),
  ("cards", "A set of playing cards is laid out on the table.", "Parlour"),
  ("fan", "An elegantly decorated bamboo fan", "Carlotta"),
  ("garlic", "A fresh looking garlic bulb", "Kitchen"),
  ("key", "An ornate skeleton key", "Rusty"),
  ("knife", "A long narrow razor sharp knife with an elegantly carved handle", "Dining Hall"),
  ("roast", "A rather smelly and moldy side of roast sits on the bench.", "Kitchen"),
  ("steps", "A small set of steps would help to reach the upper shelves.", "Library"),
  ("sword", "A shiny sharp sword with some strange symbols etched into the blade", "Dave"),
  ("torch", "A compact but powerful torch", "Me"),
  ("wine", "A nice drop of dessert wine", "Cellar"),
],

## Describe each character in the game: enemies, friends, player(s) ###
'enemies': [
  # (name, description, conversation, location, weakness, defeat_msg)*
  ("Dave", "A smelly zombie who starts shambling towards you",
   "Brains...I want braaaaiins!!",
   "Master Bedroom",
   "garlic", "eats your brains, puny adventurer"),
  ("Rusty", "A somewhat tarnished suit of armour clanks to life",
   "Intruders must be repulsed",
   "Entry Hall",
   "sword", "slices & dices & thats the end of you!")
],

'friends': [
  # (name, description, conversation, location, desire, thank_msg)* 
  ("Carlotta", "A prima donna in a large ball-gown who seems nervous.",
   "I really need something to settle my nerves before I perform.",
   "Ballroom",
   "wine", "She thanks you for this gift, and then comments that 'shazam' is the magic word, if you have been a good person and carry just the right things!"),
  ("Mona", "You feel a sudden chill as you glimpse a ghostly apparition passing by",
   "Noooooooo",
   "Bathroom",
   None, None),
  ("Norm", "A rather sad looking, sliced and diced, former adventurer.",
   "I seem to be stuck in here ...",
   "Parlour",
   "knife", "Thankyou, at least I have something to end it all with now!")
],

'players': [
  # (name, description, location)*
  ("Me", "That would be you!", "Entry Hall")
],

  # Provide a dictionary of messages used in the game
  #   need: help, intro, exit_success, exit_fail
  'messages': {
  # { name: text },
'help': """Enter one of the following commands:
exit\t\t- abandon all hope and leave the game
fight with_item\t- fight room inhabitant with item
give some_item\t- offer item to room inhabitant
go direction\t- move in named direction (eg. north, south etc) if possible
help\t\t- display this help list
leave item\t- leave (or drop) item in current room
list\t\t- list (or have) items you are carrying
look\t\t- describe current room and what you carry
look direction\t- look at room in given direction
look item\t- look at some item you have, or in current room, or on occupant
look occupant\t- look at room occupant
take item\t- take an item from the current room
talk\t\t- talk to inhabitant of room (if present)
use item\t- use an item you have or here in current room
""",
'intro': """
You suddenly find yourself standing inside a rather dark and musty mansion,
and a shiver runs down your spine. Can you find your way out of here???

Enter a command at the '>' prompt. 'help' lists (most) available commands.
""",
'exit_success': "Congratulations, you've managed to escape from the haunted house!",
'exit_fail': "So it looks like you're joining the house's inhabitants ... forever!"
},

  # Detail the success criteria for the game
  # with: magic_word, item_needed, item_not_have, num_enemies, num_friends, num_rooms
  'success': ("shazam", "key", "sword", 2, 1, 3)
}

import json

# Diagnostic main to test class
# "run this diagnostic test script if run file rather than importing it."
if __name__ == "__main__":

    print ("Default game configuration is:")
    print (default_config)
    print

    outfile = "game_config.json"
    print ("Writing config as json file: " + outfile)
    with open(outfile, 'w') as f:
        json_data = json.dumps(default_config, indent=4)
        f.write(json_data)

    print ("Reading config back from json file: " + outfile)
    with open(outfile, 'r') as f2:
        json_data = f2.read()
        new_config = json.loads(json_data)

    print("Loaded config is:")
    print(new_config)
    res = (default_config == new_config)
    print("Comparing original & loaded configs gives: " + str(res))


