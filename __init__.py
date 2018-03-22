""" Lawrie's Simple Text Adventure Game package.

Contains a set of classes to implement a text-based adventure game.
To play a new instance of the game, create a new `World` instance
(optionally passing in a customized game_config data structure),
and then call the play method on that instance. eg.

  import rpg
  game_world = rpg.World()
  game_world.play()

Written for the Object-oriented Programming in Python (OOPP) MOOC
Code additions Copyright 2018 by Lawrie Brown, licence CC-BY-NC-SA 3.0.
"""

from .character import Character, Enemy, Friend, Player
from .game_config import default_config
from .item import Item, Inventory
from .room import Room
from .world import World

