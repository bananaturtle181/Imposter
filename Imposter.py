import random as rd
from wonderwords import RandomWord

def player_settings():
    players = []

    while True:
        try:
            no_players = int(input("How many players are playing?"))
            if no_players < 3:
                print("Minimum 3 players required")
                continue
            else:
                confirm = input(f"There are going to be {no_players} playing. Is that correct?(y/n)")

                if confirm in ("y", "Y"):
                    for i in range(1,no_players + 1):
                        player = {'name': input(f"What is player {i}'s name? ")
                        }
                        players.append(player)
                    break

                else: continue

        except ValueError:
            print("Please provide a valid whole number")

    return players

def settings(player_list ,mode):
    no_imposter = 0
    imposter = None
    mr_n = None

    #Pre assigning special roles
    imposter = rd.choice(player_list)
    mr_n = rd.choice(player_list)

    while imposter == mr_n:
            mr_n = rd.choice(player_list)
    
    if mode == 3:
        no_imposter = len(player_list)
    
    for player in player_list:

        if mode in (1,2) and player == imposter:
            player["role"] = "imposter"
        
        elif mode == 2 and player == mr_n:
            player["role"] = "mr n"
        
        elif mode == 3:
            player["role"] = "imposter"
        
        else:
            player["role"] = "normal"


    return imposter, mr_n, no_imposter

# def word():
#     return


def main():

    player_list = player_settings()

    #Choose game mode
    print("1 - Normal")
    print("2 - Mysterious")

    mode = int(input("Choose game mode: "))

    #Apply settings / assign roles
    settings(player_list, mode)

    #Print results for testing
    print("\n=== PLAYER ROLES ===")

    for player in player_list:
        print(player)

main()


#example structure
#player_list = [
#     {"name": "Law", "role": "imposter"},
#     {"name": "Sarah", "role": "normal"},
#     {"name": "John", "role": "normal"}
# ]
