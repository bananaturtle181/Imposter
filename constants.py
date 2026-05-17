from enum import Enum


class Roles(Enum):
    """
    Player roles for the game
    """

    IMPOSTER = "imposter"
    MR_N = "mr_n"
    NORMAL = "normal"


class WordCategories(Enum):
    """
    Word categories for the game
    """

    ANIMALS = "animals"
    FOOD = "food"
    SPORTS = "sports"
