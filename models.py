from dataclasses import dataclass
from constants import Roles

"""
I have named this file models for clarity
Why do we use dataclasses?
Dataclasses are a convenient way to define classes that primarily store data. 
They can save time and also provide a clear structure for your data. 
In your case, you were using a dictionary to represent players, which can be less clear and more error prone than using a dataclass.
For example, if you were to assign a role but misspelled the key it would lead to a bug.
I also expect as you work on larger projects that you will be expected to use dataclasses in complex projects.
In this case, we use a dataclass to represent a player in the game, making it easier to manage player attributes 
(by attributes i mean name or any other fields) and roles.
Delete this docstring when you have read it and understand the purpose.
"""


@dataclass
class Player:
    """
    A class to represent a player in the game
    """

    # name of the player
    name: str

    # default role is normal, can be changed to imposter or mr_n
    # We assign imposter, see my comment in settings() function in Imposter.py
    role: Roles = Roles.NORMAL

    # Word assigned to player
    word: str = None  # None is default value

    # cross check for if player has seen their word
    view: bool = False  # False for no is the default value


@dataclass
class GameSettings:
    # What are the possibel game modes with the number of players
    mode: int

    # The max number of imposters in the game
    imposters: int
