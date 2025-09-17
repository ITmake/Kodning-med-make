import random

try:
    # Get player names
    antal_spelare = int(input("Hur många spelare vill du ha? ")) #alltså väljer huyr många spelare du vill ha i spelet
    spelare = []
    for i in range(antal_spelare):
        namn = input(f"Ange namn för spelare {i+1}: ").strip()
        spelare.append({"namn": namn, "poäng": 0})

    while True:
        goal = random.randint(20, 50)  # Slutmål
        print(f"\nMålet är att nå {goal} poäng utan att gå över\n")
        scores = {s["namn"]: s["poäng"] for s in spelare}
        stopped = {s["namn"]: False for s in spelare}
        quit_game = {s["namn"]: False for s in spelare}
        turn = 0  # 0 for player1, 1 for player2, 2 for player 3

        while True:
            #Find next player who hasn't quit or stopped
            active_players = [p for p in scores.keys() if not stopped[p] and not quit_game[p]]
            if not active_players:
                print("\nBåda spelarna har slutat eller stannat. Spelet avslutas.\n")
                break
            current_player = active_players[turn % len(active_players)]
            # Skip if player has quit or stopped
            if stopped[current_player] or quit_game[current_player]:
                turn += 1
                continue

            print(f"{current_player}s tur. Du har nu {scores[current_player]} poäng och målet är {goal}.")
            val = input("skriv '+' för att kasta på nytt eller '-' för att stanna, eller 'q' för att sluta: ").strip()
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
            elif val.lower() == "q":
                print(f"{current_player} har valt att sluta spelet.")
                quit_game[current_player] = True
                stopped[current_player] = True
            else:
                print("ogiltigt val, försök igen")
                continue

            # Check if both players have stopped
            if all(stopped.values()):
                # Determine winner
                diff = {s["namn"]: goal - s["poäng"] if s["poäng"] <= goal else float('inf') for s in spelare}
                min_diff = min(diff.values())
                winners = [name for name, difference in diff.items() if difference == min_diff]

                if len(winners) == 1:
                    print(f"\n{winners[0]} vinner med {scores[winners[0]]} poäng, närmast målet {goal}!\n")
                else:
                    winners_names = " och ".join(winners)
                    print(f"\nOavgjort mellan {winners_names}! Alla har lika nära målet {goal}.\n")
                break

            turn += 1  # Next player's turn

        play_again = input("Vill ni spela igen? (j/n): ")
        if play_again.lower() != 'j':
            print("Tack för att ni spelade!")
            break
except KeyboardInterrupt:
    print("\nSpelet avslutat. Tack för att ni spelade!")
