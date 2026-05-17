import random

from constants import Roles
from hint_requests import get_hint
from models import Player


def player_settings():
    players = []

    while True:
        try:
            no_players = int(input("How many players are playing?"))
            if no_players < 3:
                print("Minimum 3 players required")
                continue
            else:
                confirm = input(
                    f"There are going to be {no_players} playing. Is that correct?(y/n)"
                )

                if confirm in ("y", "Y"):
                    for i in range(1, no_players + 1):
                        player = Player(name=input(f"What is player {i}'s name? "))
                        players.append(player)
                    break

                else:
                    continue

        except ValueError:
            print("Please provide a valid whole number")

    return players


def settings(player_list, mode):
    no_imposter = 0
    imposter = None
    mr_n = None

    # Pre assigning special roles
    imposter = random.choice(player_list)
    mr_n = random.choice(player_list)

    while imposter == mr_n:
        mr_n = random.choice(player_list)

    if mode == 3:
        no_imposter = len(player_list)

    for player in player_list:
        if mode in (1, 2) and player == imposter:
            player.role = Roles.IMPOSTER

        elif mode == 2 and player == mr_n:
            player.role = Roles.MR_N

        elif mode == 3:
            player.role = Roles.IMPOSTER

        else:
            player.role = Roles.NORMAL

    return


def word(player_list, category):

    real_word = category
    hint_word = get_hint(real_word)

    for player in player_list:
        if player.role == Roles.IMPOSTER:
            player.word = hint_word

        elif player.role == Roles.MR_N:
            player.word = None

        else:
            player.word = real_word

    return


def main():

    player_list = player_settings()

    # Choose game mode
    print("1 - Normal")
    print("2 - Mysterious")

    mode = int(input("Choose game mode: "))
    # category = input("What category of word would you like?")
    category = input("Choose a word: ")

    # Apply settings/assign roles
    settings(player_list, mode)

    # Word settings
    word(player_list, category)

    # Print results for testing
    print("\n=== PLAYER ROLES ===")

    for player in player_list:
        print(player)


main()
