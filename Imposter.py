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
                )

                if confirm in ("y", "Y"):
                    for i in range(1, no_players + 1):
                        name = input(f"What is player {i}'s name? ").strip()

                        # extra check to make sure not the same name
                        while not name or any(
                            p.name.lower() == name.lower() for p in players
                        ):
                            name = input(
                                "Name already taken or invalid. Choose a different name: "
                            ).strip()

                        players.append(Player(name=name))
                    break

                else:
                    continue

        except ValueError:
            print("Please provide a valid whole number")

    return players


def game_setting(player_list: list[Player]) -> tuple[int, str]:

    while True:
        try:
            mode = int(input("1 - Normal\n2 - Mysterious\nChoose game mode: "))
        except ValueError:
            print("Please provide an integer")
            continue
        if len(player_list) <= 3 and mode == 2:
            print("Not enough players to run game mode!")
            continue

        elif mode in (1, 2, 3, 4):
            break
        else:
            continue

    if mode in (1, 2):
        while True:
            # Set rule for maximum allowed imposters = players/4, round down
            max_imposters = max(1, len(player_list) // 4)
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
            else:
                break

    category = input("What category of word would you like?")

    return mode, category


def assign_roles(player_list: list[Player], mode: int) -> None:

    if mode == 4:
        return

    if mode == 3:
        for player in player_list:
            player.role = Roles.IMPOSTER
        return

    imposter = random.choice(
        player_list
    )  # NEED TO FACTOR IN NUMBER OF IMPOSTERS TO ASSIGN MORE THAN 1
    mr_n = random.choice(player_list)

    while imposter == mr_n:  # Apparently this can be done without a loop?
        mr_n = random.choice(player_list)

    imposter.role = Roles.IMPOSTER

    if mode == 2:
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


def run_game(player_list, mode, category):
    # using existing helpers
    assign_roles(player_list, mode)
    assign_word(player_list, category)
    order(player_list)
    for p in player_list:
        print(p)


def main():
    players = player_settings()
    mode, category = game_setting(players)
    run_game(players, mode, category)


if __name__ == "__main__":
    main()
