"""Hälsa på en lista av namn."""

from typing import Iterable


def greet_names(names: Iterable[str]) -> None:
    """Print a friendly greeting for each name in ``names``."""
    for name in names:
        print(f"Hej {name.title()}!")


def main() -> None:
    """Visa en standardlista med namn att hälsa på."""
    default_names = ["johan", "jörgen", "make"]
    greet_names(default_names)


if __name__ == "__main__":
    main()
