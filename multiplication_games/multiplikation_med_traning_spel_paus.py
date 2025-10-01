"""Multiplikationsövning med tränings- och tidsläge."""

from __future__ import annotations

import random
import time


def _ask_table_choice() -> tuple[str, int | None]:
    """Returnera ('val', nummer), ('random', None) eller ('sluta', None)."""
    while True:
        choice = input(
            "Vill du välja tabell eller slumpmässigt valt? (skriv 'val', 'random' eller 'sluta'): "
        ).strip().lower()
        if choice == "val":
            while True:
                try:
                    number = int(input("Skriv ett nummer mellan 1 och 10: "))
                except ValueError:
                    print("Det är inte ett heltal. Försök på nytt!")
                    continue

                if 1 <= number <= 10:
                    print(f"Du valde: {number}")
                    return "val", number
                print("Skriv ett nummer mellan 1 och 10.")
        elif choice == "random":
            return "random", None
        elif choice == "sluta":
            return "sluta", None
        else:
            print("Ogiltigt svar.")


def training_mode() -> None:
    """Obegränsad träning tills användaren skriver 'sluta'."""
    selection, number = _ask_table_choice()
    if selection == "sluta":
        return

    fixed_number = number if selection == "val" else None

    while True:
        factor_a = fixed_number or random.randint(1, 10)
        factor_b = random.randint(1, 10)
        correct_answer = factor_a * factor_b
        answer = input(f"Vad är {factor_a} * {factor_b}? (eller skriv 'sluta'): ")
        if answer.strip().lower() == "sluta":
            break
        try:
            if int(answer) == correct_answer:
                print("Rätt svar!\n")
            else:
                print("Fel svar. Försök igen!\n")
        except ValueError:
            print("Skriv ett heltal, tack.\n")


def timed_mode(time_limit: int = 30) -> None:
    """Spela mot klockan."""
    print(f"Du har {time_limit} sekunder på dig att svara på så många som möjligt!")
    start_time = time.time()
    total_correct = 0
    streak = 0

    while True:
        if time.time() - start_time > time_limit:
            break

        factor_a = random.randint(1, 10)
        factor_b = random.randint(1, 10)
        correct_answer = factor_a * factor_b
        answer = input(f"Vad är {factor_a} * {factor_b}? (eller skriv 'sluta'): ")

        if answer.strip().lower() == "sluta":
            break

        try:
            if int(answer) == correct_answer:
                total_correct += 1
                streak += 1
                print("Rätt svar!\n")
                print(f"Highscore (totalt antal rätt): {total_correct}")
                print(f"Antal rätt i rad: {streak}\n")
            else:
                print("Fel svar. Försök igen!\n")
                streak = 0
        except ValueError:
            print("Skriv ett heltal, tack.\n")

    print("\nTiden är slut!")
    print(f"Highscore (totalt antal rätt): {total_correct}")
    print(f"Antal rätt i rad: {streak}")


def main() -> None:
    """Hantera meny och välj spelläge."""
    while True:
        mode = input(
            "Vill du träna eller spela på tid? (skriv 'träna', 'spela' eller 'sluta'): "
        ).strip().lower()
        if mode == "träna":
            training_mode()
        elif mode == "spela":
            timed_mode()
        elif mode == "sluta":
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val.")


if __name__ == "__main__":
    main()
