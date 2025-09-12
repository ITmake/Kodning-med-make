import random

try:
    # Get player names
    player1 = input("Ange namn för spelare 1: ").strip()
    player2 = input("Ange namn för spelare 2: ").strip()
    players = [player1, player2]

    while True:
        goal = random.randint(20, 50)  # Slutmål
        print(f"\nMålet är att nå {goal} poäng utan att gå över\n")
        scores = {player1: 0, player2: 0}
        stopped = {player1: False, player2: False}
        turn = 0  # 0 for player1, 1 for player2

        while True:
            # Hitta nästa spelare som inte har stannat
            while stopped[players[turn % 2]]:
                turn += 1
                # Om båda har stannat, bryt loopen
                if all(stopped.values()):
                    break
            if all(stopped.values()):
                # Determine winner
                diff1 = goal - scores[player1] if scores[player1] <= goal else float('inf')
                diff2 = goal - scores[player2] if scores[player2] <= goal else float('inf')
                if diff1 < diff2:
                    print(f"\n{player1} vinner med {scores[player1]} poäng, närmast målet {goal}!\n")
                elif diff2 < diff1:
                    print(f"\n{player2} vinner med {scores[player2]} poäng, närmast målet {goal}!\n")
                else:
                    print(f"\nOavgjort! Båda är lika nära målet {goal}.\n")
                break

            current_player = players[turn % 2]
            print(f"{current_player}s tur. Du har nu {scores[current_player]} poäng och målet är {goal}.")
            val = input("skriv '+' för att kasta på nytt eller '-' för att stanna: ").strip()
            val = val.lower()
            if val == "+":
                num = random.randint(1, 15)  # "tärningen"
                print(f"Du kastade {num} och har nu totalt {scores[current_player] + num} poäng\n")
                scores[current_player] += num
                if scores[current_player] > goal:
                    print(f"BUST! {current_player} har {scores[current_player]} vilket gick över \n")
                    scores[current_player] = 0
                    stopped[current_player] = True
            elif val == "-":
                print(f"{current_player} har stannat på {scores[current_player]} poäng!")
                stopped[current_player] = True
            elif val == "nej":
                print(f"{current_player} vill inte fortsätta. Hoppar över {current_player} resten av rundan.")
                stopped[current_player] = True
            else:
                print("ogiltigt val, försök igen")
                continue

            turn += 1  # Nästa spelares tur

        play_again = input("Vill ni spela igen? (j/n): ")
        if play_again.lower() != 'j':
        
            print("Tack för att ni spelade!")
            break
except KeyboardInterrupt:
    print("\nSpelet avslutat. Tack för att ni spelade!")
