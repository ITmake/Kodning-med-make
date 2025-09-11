import random
import time

while True:
    mode = input("Vill du träna eller spela på tid? (skriv 'träna', 'spela' eller 'sluta'): ").strip().lower()
    if mode == 'träna':
        while True:
            val = input("Vill du välja tabell eller slumpmässigt valt? (skriv 'val', 'random' eller 'sluta'): ").strip().lower()
            if val == 'val':
                while True:
                    try:
                        number = int(input("Skriv ett nummer mellan 1 och 10: "))
                        if 1 <= number <= 10:
                            print(f"Du valde: {number}")
                            anvand_val = True
                            break
                        else:
                            print("Skriv ett nummer mellan 1 och 10.")
                    except ValueError:
                        print("Det är inte ett heltal. Försök på nytt!")
                break
            elif val == 'random':
                anvand_val = False
                break
            elif val == 'sluta':
                break
            else:
                print("Ogiltigt svar.")
        if val == 'sluta':
            continue
        # Träningsloop
        while True:
            tal1 = number if anvand_val else random.randint(1, 10)
            tal2 = random.randint(1, 10)
            rätt_svar = tal1 * tal2
            svar = input(f"Vad är {tal1} * {tal2}? (eller skriv 'sluta'): ")
            if svar.strip().lower() == 'sluta':
                break
            try:
                if int(svar) == rätt_svar:
                    print("Rätt svar!\n")
                else:
                    print("Fel svar. Försök igen!\n")
            except ValueError:
                print("Skriv ett heltal, tack.\n")
        continue

    elif mode == 'spela':
        print("Du har 30 sekunder på dig att svara på så många som möjligt!")
        start_time = time.time()
        time_limit = 30
        total_ratt = 0
        streak = 0
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
            svar = input(f"Vad är {tal1} * {tal2}? (eller skriv 'sluta'): ")
            if svar.strip().lower() == 'sluta':
                break
            try:
                if int(svar) == rätt_svar:
                    print("Rätt svar!\n")
                    total_ratt += 1
                    streak += 1
                    print(f"Highscore (totalt antal rätt): {total_ratt}")
                    print(f"Antal rätt i rad: {streak}\n")
                else:
                    print("Fel svar. Försök igen!\n")
                    streak = 0
            except ValueError:
                print("Skriv ett heltal, tack.\n")
        continue

    elif mode == 'sluta':
        print("Programmet avslutas.")
        break
    else:
        print("Ogiltigt val.")