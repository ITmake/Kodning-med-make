# Kodning med make – repo fix

Detta repo innehåller små Python-projekt och exempel skrivna under kursmoment i programmering. Strukturen var tidigare svår att navigera på grund av mellanslag i filnamn och avsaknad av dokumentation. Den har nu städats upp så att varje kategori ligger i en tydligt namngiven mapp med snake_case-filer.

## Innehåll

| Katalog | Beskrivning |
| --- | --- |
| `beagleboard_examples/` | Skript och anteckningar för experiment med BeagleBone Black och Grove-sensorer. |
| `dictionary_examples/` | Uppgifter som använder Python-dictionaries. |
| `mini_games/` | Små spel i terminalen, bland annat varianter av tärnings- och gissningsspel. |
| `multiplication_games/` | Multiplikationsövningar med olika regler. |
| `type_conversion/` | Exempel på typkonverteringar i Python. |
| `weekday_examples/` | Övningar relaterade till listor över veckodagar. |
| `integer_test.py` | Enkel funktion som ber användaren om ett tal och adderar 5. |
| `random_guess.py` | Terminalspel där användaren gissar ett slumpmässigt nummer. |
| `random_name_list.py` | Hälsar på namn i en lista. |

## Komma igång

Repo:t kräver endast Python 3.11 eller senare.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # om du behöver externa beroenden
```

Det finns inga externa beroenden för de enklare skripten. Vissa projekt under `beagleboard_examples` kräver hårdvara och bibliotek för BeagleBone Black.

## Köra skript

Exempel: starta gissningsspelet

```bash
python random_guess.py
```

Eller kör ett multiplikationsspel:

```bash
python multiplication_games/multiplikation_med_highscore.py
```

De flesta interaktiva skripten har en `main()`-funktion som körs när filen startas direkt.

## Testa att koden kompilerar

```bash
python -m compileall .
```

Kommandot ovan säkerställer att alla Python-filer har giltig syntax.

