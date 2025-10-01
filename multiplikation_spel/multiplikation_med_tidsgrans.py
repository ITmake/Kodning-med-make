"""Multiplikationsspel med tidsgräns."""

from __future__ import annotations

import random
import time


def play_time_limited_game(time_limit: int = 30) -> None:
    """Spela så många uppgifter som möjligt innan tiden tar slut."""
    total_correct = 0
    streak = 0

    print(f"Du har {time_limit} sekunder på dig att svara på så många som möjligt!")
    start_time = time.time()

    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                break

            factor_a = random.randint(1, 10)
            factor_b = random.randint(1, 10)
            correct_answer = factor_a * factor_b

            while True:
                elapsed = time.time() - start_time
                if elapsed > time_limit:
                    print("\nTiden är slut!")
                    print(f"Highscore (totalt antal rätt): {total_correct}")
                    print(f"Antal rätt i rad: {streak}")
                    return

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
        print("\nSpelet avbröts.")
        return

    print("\nTiden är slut!")
    print(f"Highscore (totalt antal rätt): {total_correct}")
    print(f"Antal rätt i rad: {streak}")


def main() -> None:
    """Starta spelet."""
    play_time_limited_game()


if __name__ == "__main__":
    main()
