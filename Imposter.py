from models import Player
import random
from olipy import corpora as co
from constants import Roles
from hint_requests import get_hint

def player_settings() -> list[Player]:
    players: list[Player] = []

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


def settings(player_list: list[Player], mode: int) -> None:

    if mode == 4: 
        return  #All players remain "normal" with mode 4
    
    if mode == 3:
        for player in player_list:
            player.role = Roles.IMPOSTER
        return
    
    imposter = random.choice(player_list)
    imposter.role = Roles.IMPOSTER
   

    if mode ==2:
        mr_n = random.choice(player_list)

        while imposter == mr_n:
            mr_n = random.choice(player_list)
    
        mr_n.role = Roles.MR_N

    return


def word(player_list: list[Player], category: str) -> None:

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

# def order(player_list):

    

#     return

def main():

    player_list = player_settings()

    # Choose game mode
    print("1 - Normal")
    print("2 - Mysterious")

    mode = int(input("Choose game mode: "))
    category = input("What category of word would you like?")

    # Apply settings/assign roles
    settings(player_list, mode)

    # Word settings
    word(player_list, category)

    # Print results for testing
    print("\n=== PLAYER ROLES ===")

    for player in player_list:
        print(player)

main()
