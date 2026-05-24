from models import Player, GameSettings
import random
from olipy import corpora as co
from constants import Roles, GameModes
from hint_requests import get_hint
import os

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

def game_setting(player_list: list[Player]) -> tuple[int,str]:

    while True:
        mode = int(input("Choose game mode: "))
        if player_list.len() <= 3 and mode == 2:
            print("Not enough players to run game mode")
            continue

        elif player_list.len() > 3 and mode == 2:
            break

    if mode in [1,2]:
        while True:
            max_imposters = 5 
            imposters = GameSettings.imposters(input("Choose a number of imposters"))
            if (player_list.len() - imposters) < 4:
    category = input("What category of word would you like?")
    
    return mode, category


def settings(player_list: list[Player], mode: int) -> None:

    if mode == 4: 
        return
    
    if mode == 3:
        for player in player_list:
            player.role = Roles.IMPOSTER
        return
    
    imposter = random.choice(player_list)
    mr_n = random.choice(player_list)

    while imposter == mr_n:
        mr_n = random.choice(player_list)
    
    imposter.role = Roles.IMPOSTER
    
    if mode == 2 and player_list.len() > 3:
        mr_n.role = Roles.MR_N
    
    elif mode == 2 and player_list.len() <= 3:
        print("Not enough players for chaos")


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

def _clear_screen() -> None:
    # Clears the terminal screen for Windows (nt) and Mac/Linux (posix)
    os.system('cls' if os.name == 'nt' else 'clear')


def order(player_list: list[Player]) -> None:

    for player in player_list:
        _clear_screen()
        print(f"{player.name}'s turn to see their word")

        while True:
            ready = input("Ready to see your word? (y/n)").lower()
            if ready == 'y':
                print(f"Your word is {player.word}")
                player.view = True
                input("\nPress Enter when you have memorised your word to clear the screen...")
                _clear_screen()
                break

            elif ready == 'n':
                continue
       

def main(mode: int,category: str) -> None:

    player_list = player_settings()
    mode , category = game_setting(player_list)

    # Choose game mode
    print("1 - Normal")
    print("2 - Mysterious")

    # Apply settings/assign roles
    settings(player_list, mode)

    # Word settings
    word(player_list, category)

    # Print results for testing
    print("\n=== PLAYER ROLES ===")

    #Order function
    order(player_list)

    for player in player_list:
        print(player)

main()

# 1. Need a statement to restrict game mode 2 if the number of imposters < 3
# 2. Need a if statement if game mode 2 is chosen to select the number of imposters
# 3. Need 