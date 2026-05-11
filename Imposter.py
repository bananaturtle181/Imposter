import random as rd

def players(mode=1):
    players = []

    while True:
        try:
            no_players = int(input("How many players are playing?"))
            if no_players < 3:
                print("Minimum 3 players required")
                break
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
            
    if mode == 1:


    return

# def word():



#     return


players()
