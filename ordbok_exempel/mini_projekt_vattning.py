from datetime import date, datetime

plants = [
    {
        "namn": "tomat",
        "typ": "grönsak",
        "temperaturintervall": (18, 25),
        "senaste_vattning": date(2025, 9, 18)
    },
    {
        "namn": "gurka",
        "typ": "grönsak",
        "temperaturintervall": (20, 28),
        "senaste_vattning": date(2025, 9, 18)
    },
    {
        "namn": "jordgubbe",
        "typ": "bär",
        "temperaturintervall": (15, 22),
        "senaste_vattning": date(2025, 9, 18)
    },
    {
        "namn": "eggplanta",
        "typ": "grönsak",
        "temperaturintervall": (22, 30),
        "senaste_vattning": date(2025, 9, 18)
    }
]

VATTNINGSINTERVALL = 3  # dagar

def skriv_vattningsbehov(plants, idag):
    behov = False
    for plant in plants:
        dagar_sedan_vattning = (idag - plant["senaste_vattning"]).days
        if dagar_sedan_vattning >= VATTNINGSINTERVALL:
            print(f"{plant['namn'].capitalize()} behöver vattnas idag.")
            behov = True
        else:
            print(f"{plant['namn'].capitalize()} behöver inte vattnas idag.")
    return behov

while True:
    datum_input = input("Ange dagens datum (MM-DD) eller tryck Enter för idag: ")
    if datum_input.strip():
        try:
            year = 2025  # Samma år som senaste_vattning
            idag = datetime.strptime(f"{year}-{datum_input}", "%Y-%m-%d").date()
        except ValueError:
            print("Fel format! Använd MM-DD, t.ex. 09-21.\n")
            continue
    else:
        idag = date.today().replace(year=2025)

    behov = skriv_vattningsbehov(plants, idag)
    if behov:
        print("Kom ihåg att vattna!")