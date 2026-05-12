import random as rd
from wonderwords import RandomWord

def players():
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
    
    #implementation of game modes. 1 = normal (default), 2 = mysterious, 3 = chaos
    if mode == 1:
        imposter = rd.choice(player_list)
    
    elif mode == 2:
        imposter = rd.choice(player_list)
        mr_n = rd.choice(player_list)

        while imposter == mr_n:
            mr_n = rd.choice(player_list)

    elif mode == 3:
        for player in player_list:

    else:
        print("Please choose a number between 1-3")


    return imposter, mr_n

# def word():
#     return


def main():

    players()

    mode = input("Which game mode would you like to play? 1- Normal mode, 2- Mysterious mode, 3- Chaos mode")


    return

#Example player list structure: 
    #player_list = [{"name":"Law",
#                    "role":"Imposter"
#}
#] Up to assigning role if mode == 1, then loop through list of dicts to assign everyone imposter for mode == 3