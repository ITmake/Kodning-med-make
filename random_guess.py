"""Enkel gissningslek i terminalen."""

from __future__ import annotations

import random
from typing import Callable, Iterable


MESSAGES: tuple[str, ...] = (
    "Grattis, du gissade rätt!",
    "Rätt gissat, bra jobbat!",
    "Fantastiskt, du hittade det rätta numret!",
    "Wow, vilken träffsäkerhet!",
    "Snyggt! Du prickade in rätt siffra!",
    "Imponerande, du klarade det!",
    "Du har verkligen tur idag!",
    "Otroligt, du valde rätt!",
    "Perfekt gissning!",
    "Du är en riktig mästare på att gissa!",
)


def guess(
    lower: int = 1,
    upper: int = 100,
    input_func: Callable[[str], str] | None = None,
    output_func: Callable[[str], None] | None = None,
    congratulation_messages: Iterable[str] = MESSAGES,
) -> int:
    """Spela en gissningslek och returnera antalet försök."""
    if lower >= upper:
        raise ValueError("'lower' måste vara mindre än 'upper'.")

    prompt = input_func or input
    say = output_func or print

    target = random.randint(lower, upper)
    attempts = 0

    while True:
        attempts += 1
        user_input = prompt(f"Gissa på ett nummer mellan {lower} och {upper}: ")
        try:
            guess_value = int(user_input)
        except ValueError:
            say("Ange tal, inte bokstäver.")
            attempts -= 1  # ogiltigt försök räknas inte
            continue

        if guess_value > target:
            say("Ditt nummer var för stort.")
        elif guess_value < target:
            say("Ditt nummer var för litet.")
        else:
            message = random.choice(tuple(congratulation_messages))
            say(f"{message} Du gissade rätt på {attempts} försök.")
            return attempts


def main() -> None:
    """Kör spelet i terminalen."""
    guess()


if __name__ == "__main__":
    main()
