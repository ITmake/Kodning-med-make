import random
import time

total_ratt = 0      # Highscore: totalt antal rätt
streak = 0          # Antal rätt i rad

print("Du har 30 sekunder på dig att svara på så många som möjligt!")
start_time = time.time()
time_limit = 30  # sekunder

while True:
    elapsed = time.time() - start_time
    if elapsed > time_limit:
        print("\nTiden är slut!")
        print(f"Highscore (totalt antal rätt): {total_ratt}")
        print(f"Antal rätt i rad: {streak}")
        break
    tal1 = random.randint(1, 10)
    tal2 = random.randint(1, 10)
    rätt_svar = tal1 * tal2
    while True:
        elapsed = time.time() - start_time
        if elapsed > time_limit:
            print("\nTiden är slut!")
            print(f"Highscore (totalt antal rätt): {total_ratt}")
            print(f"Antal rätt i rad: {streak}")
            exit()
        try:
            svar = int(input(f"Vad är {tal1} * {tal2}?: "))
            if svar == rätt_svar:
                print("Rätt svar!\n")
                total_ratt += 1
                streak += 1
                print(f"Highscore (totalt antal rätt): {total_ratt}")
                print(f"Antal rätt i rad: {streak}\n")
                break
            else:
                print("Fel svar. Försök igen!\n")
                streak = 0  # Nollställ streak vid fel svar
        except ValueError:
            print("Skriv ett heltal, tack.\n")