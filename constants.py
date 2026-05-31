from enum import Enum


class Roles(Enum):
    """
    Player roles for the game
    """

    IMPOSTER = "imposter"
    MR_N = "mr_n"
    NORMAL = "normal"


class GameModes(Enum):
    """
    Possibel game modes for the given number of players
    """

    NORMAL = 1
    MYSTERIOUS = 2
    CHAOS = 3
    TROLL = 4
