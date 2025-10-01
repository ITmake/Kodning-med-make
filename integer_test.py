"""Utility for adding an offset to a favourite number input."""

def favourite_number(offset: int = 5) -> int:
    """Ask the user for a number, add ``offset`` and return the result."""
    while True:
        user_input = input("Ange ett heltal: ")
        try:
            number = int(user_input)
        except ValueError:
            print("Du måste skriva en siffra. Försök igen!")
            continue
        result = number + offset
        print(f"Ditt favoritnummer plus {offset} är: {result}")
        return result


def main() -> None:
    """Kör en enkel interaktiv demonstration."""
    favourite_number()


if __name__ == "__main__":
    main()
