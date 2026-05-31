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
            no_players = int(input("How many players are playing? "))
            if no_players < 3:
                print("Minimum 3 players required")
                continue
            else:
                confirm = input(
                    f"There are going to be {no_players} playing. Is that correct?(y/n) "
                ).lower().strip()

                if confirm != "y":
                    continue
                for i in range(1,no_players + 1):
                    while True: 
                        name = input(f"What is player {i}'s name? ").strip()

                        if not name: 
                            print("Name cannot be empty.")
                        if any(p.name.lower() == name.lower() for p in players):
                            print("Name already taken. Choose a different name.")
                            continue
                        players.append(Player(name = name))
                        break
                    return players
        except ValueError:
        

def game_setting(player_list: list[Player]) -> tuple[GameSettings, str]:
    #Choose game mode
    while True:
        try:
            mode = int(input("1 - Normal\n2 - Mysterious\nChoose game mode: "))
        except ValueError:
            print("Please provide an integer")
            continue
        if mode not in (1, 2, 3, 4):
            print("Invalid mode. Choose 1-4.")
            continue

        if mode == 2 and len(player_list) <= 3:
            print("Not enough players to run Mysterious mode!")
            continue
        break

#-----------------------------------------------------------------------------
  #Choose imposters
    imposters = 0
    if mode == 4: 
        imposters = 0
    if mode in (1, 2):
        #Set rule for maximum allowed imposters as imposters = max no.players divided by 4, round down
        max_imposters = max(1, len(player_list) // 4)

        while True:
            try:
                imposters = int(input("How many Imposters? "))
            except ValueError:
                print("Please provide a valid whole number for imposters")
                continue

            if imposters > max_imposters:
                print(
                    f"Too many imposters for number of players. Max imposters is {max_imposters}"
                )
                continue
            if imposters <1: 
                print("Must have at least 1 imposter")
                continue
            break
    elif mode == 3:
        imposters = len(player_list)
    
#---------------------------------------------------------------------------------
# Category selection   
    category = input("What category of word would you like?").strip()

#---------------------------------------------------------------------------------
#Build settings
    settings = GameSettings(
                mode = mode,
                imposters = imposters
    )

    return settings, category


def assign_roles(player_list: list[Player], settings) -> None:      #Need to refactor as imposters has changed to a list
   
    if settings.mode == 4:
        return

    if settings.mode == 3:
        for player in player_list:
            player.role = Roles.IMPOSTER
        return
            
    imposter = random.sample(player_list, settings.imposters)
    mr_n = random.choice(player_list)

    eligible_players = [
        player for player in player_list if player not in imposter
    ]
    
    mr_n = random.choice(eligible_players)

    imposter.role = Roles.IMPOSTER
    
    if settings.mode == 2:
    # select imposters (may be more than one)
        imposter = random.sample(player_list, settings.imposters)

    # pick mr_n from players not imposters
    eligible_players = [player for player in player_list if player not in imposter]
    mr_n = random.choice(eligible_players) if eligible_players else None

    # assign imposter roles
    for p in imposter:
        p.role = Roles.IMPOSTER

    if settings.mode == 2 and mr_n:

        mr_n.role = Roles.MR_N

    return


def assign_word(player_list: list[Player], category: str) -> None:

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
    os.system("cls" if os.name == "nt" else "clear")


def order(player_list: list[Player]) -> None:

    for player in player_list:
        _clear_screen()
        print(f"{player.name}'s turn to see their word")

        while True:
            ready = input("Ready to see your word? (y/n)").lower()
            if ready == "y":
                print(f"Your word is {player.word}")
                player.view = True
                input(
                    "\nPress Enter when you have memorised your word to clear the screen..."
                )
                _clear_screen()
                break

            elif ready == "n":
                continue

    player_list = player_settings()
    settings, category = game_setting(player_list)

    # Choose game mode
    print("1 - Normal")
    print("2 - Mysterious")

    # Apply settings/assign roles
    assign_roles(player_list, settings)

    # Word settings

def run_game(player_list, settings, category):
    # using existing helpers
    assign_roles(player_list, settings)

    assign_word(player_list, category)
    order(player_list)
    for p in player_list:
        print(p)


def main():
    players = player_settings()
    settings, category = game_setting(players)
    run_game(players, settings, category)


if __name__ == "__main__":
    main()
