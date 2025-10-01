"""Multiplikationsspel med highscore och streak."""

from __future__ import annotations

import random


def play_highscore_game() -> None:
    """Spela tills användaren avbryter med Ctrl+C."""
    total_correct = 0
    streak = 0

    try:
        while True:
            factor_a = random.randint(1, 10)
            factor_b = random.randint(1, 10)
            correct_answer = factor_a * factor_b

            while True:
                try:
                    answer = int(input(f"Vad är {factor_a} * {factor_b}?: "))
                except ValueError:
                    print("Skriv ett heltal, tack.\n")
                    continue

                if answer == correct_answer:
                    total_correct += 1
                    streak += 1
                    print("Rätt svar!\n")
                    print(f"Highscore (totalt antal rätt): {total_correct}")
                    print(f"Antal rätt i rad: {streak}\n")
                    break

                print("Fel svar. Försök igen!\n")
                streak = 0
    except KeyboardInterrupt:
        print("\nTack för att du spelade!")


def main() -> None:
    """Starta spelet."""
    play_highscore_game()


if __name__ == "__main__":
    main()
