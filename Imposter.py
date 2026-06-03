from models import Player, GameSettings
import random
from constants import Roles, GameModes
from hint_requests import get_hint, get_word_from_category
import os
from words import WORD_CATEGORIES


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
                            continue
                        if any(p.name.lower() == name.lower() for p in players):
                            print("Name already taken. Choose a different name.")
                            continue
                        players.append(Player(name = name))
                        break
                return players
        except ValueError:
            print("Please enter a valid number of players.")

def game_setting(player_list: list[Player]) -> tuple[GameSettings, str, str]: #Tuple of settings, real word, hint word
    #Choose game mode
    mode = random_game_mode(player_list)

    if mode is None:
        while True:
            try:
                mode = GameModes(int(input("1 - Normal\n2 - Mysterious\nChoose game mode: ")))
            except ValueError:
                print("Please provide a valid mode (1-4)")
                continue

            if mode == GameModes.MYSTERIOUS and len(player_list) <= 3:
                print("Not enough players to run Mysterious mode!")
                continue
            break

    #-----------------------------------------------------------------------------
    #Choose imposters
    if mode in (GameModes.NORMAL, GameModes.MYSTERIOUS):
        max_imposters = max(1, len(player_list) // 4)
        while True:
            try:
                imposters = int(input("How many Imposters? "))
            except ValueError:
                print("Please provide a valid whole number for imposters")
                continue
            if imposters > max_imposters:
                print(f"Too many imposters for number of players. Max imposters is {max_imposters}")
                continue
            if imposters < 1:
                print("Must have at least 1 imposter")
                continue
            break
    else:
        # Ask anyway to hide game mode from other players
        input("How many Imposters? ")
        imposters = 0 if mode == GameModes.TROLL else len(player_list)
    #---------------------------------------------------------------------------------
    # Category selection   
    while True:
        print("Available categories: " + ", ".join(WORD_CATEGORIES.keys()))
        category = input("What category of word would you like? ").strip()
        word = get_word_from_category(category)
        if word is None:
            print("Couldn't find words for that category, try a different one")
            continue
        hint_word = get_hint(word)
        if hint_word is None:
            print("Couldn't get a hint word, try a different category")
            continue
        break

    #---------------------------------------------------------------------------------
    #Build settings
    settings = GameSettings(
                mode = mode,
                imposters = imposters
    )

    return settings, word, hint_word


def assign_roles(player_list: list[Player], settings: GameSettings) -> None:    
    # No special roles
    if settings.mode == GameModes.TROLL:
        return

    # Everyone is imposter
    if settings.mode == GameModes.CHAOS:
        for player in player_list:
            player.role = Roles.IMPOSTER
        return

    # Normal and Mysterious modes
    # select imposters
    imposters = random.sample(player_list, settings.imposters)
    for p in imposters:
        p.role = Roles.IMPOSTER

    # In mysterious mode, pick one MR_N from non-imposters
    if settings.mode == GameModes.MYSTERIOUS:
        eligible = [p for p in player_list if p not in imposters]
        if eligible:
            mr_n = random.choice(eligible)
            mr_n.role = Roles.MR_N


def assign_word(player_list: list[Player], real_word: str, hint_word: str) -> None:
    for player in player_list:
        if player.role == Roles.IMPOSTER:
            player.word = hint_word
        elif player.role == Roles.MR_N:
            player.word = None
        else:
            player.word = real_word

def random_game_mode(player_list: list[Player]) -> GameModes | None:
    while True:
        choice = input("Do you want random or manual game mode? (r/m) ").lower().strip()
        if choice == "m":
            return None
        elif choice == "r":
            break
        else:
            print("Please enter r or m")

    while True:
        try:
            raw = input("Which modes do you want in the pool? (e.g. 1,2,3,4): ").strip()
            selected = [GameModes(int(x.strip())) for x in raw.split(",")]
            
            # Filter out Mysterious if not enough players
            if GameModes.MYSTERIOUS in selected and len(player_list) <= 3:
                print("Not enough players for Mysterious mode, removing it from the pool...")
                selected = [m for m in selected if m != GameModes.MYSTERIOUS]

            if len(selected) < 2:
                print("Please select at least 2 modes for random to make sense!")
                continue

            break
        except ValueError:
            print("Invalid input, please enter valid mode numbers separated by commas")

    chosen = random.choice(selected)
    # print(f"Randomly selected: {chosen.name}")
    return chosen

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
            else:
                print("Please enter y or n")

def end_game(settings: GameSettings, player_list: list[Player]) -> None:
    _clear_screen()
    input("Press Enter to reveal...")
    _clear_screen()

    if settings.mode == GameModes.CHAOS:
        print("Everyone was an imposter!")
        return
    
    if settings.mode == GameModes.TROLL:
        print("No one was an imposter!")
        return

    # Reveal words first
    for player in player_list:
        if player.role == Roles.NORMAL:
            print(f"The real word was: {player.word}")
            break
    
    for player in player_list:
        if player.role == Roles.IMPOSTER:
            print(f"The imposters word was: {player.word}")
            break

    # Reveal roles
    print("\nRoles:")
    for player in player_list:
        print(f"{player.name} was {player.role.value}")

def run_game(player_list: list[Player], settings: GameSettings, real_word: str, hint_word: str) -> None:
    assign_roles(player_list, settings)
    assign_word(player_list, real_word, hint_word)
    order(player_list)
    end_game(settings, player_list)

def main():
    players = player_settings()
    settings, real_word, hint_word = game_setting(players)
    run_game(players, settings, real_word, hint_word)


if __name__ == "__main__":
    main()
