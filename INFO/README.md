📦 Materiallista

BeagleBone Green – 1 st
Relämodul (5V) – 1 st
Jumperkablar – 4 st
Strömkälla (5V) – 1 st (via BBB)

🔌 Kopplingar

P9_15 (GPIO48) → Relä IN → 🟡 Gul kabel (styrsignal)
P9_01 → Relä GND → ⚫ Svart kabel (jord)
P9_05 → Relä VCC → 🔴 Röd kabel (5V)
(Reserv) → ⚪ Vit kabel
Tips: Kontrollera att kablarna sitter ordentligt och att relämodulen klarar 5V-logik från BBB.

💻 Python-skript (förklaring i punkter)

import gpiod → Bibliotek för GPIO-styrning på Linux
import time → Bibliotek för paus/fördröjning
chip = gpiod.Chip('gpiochip0') → Initierar GPIO-chip
line = chip.get_line(28) → Väljer linje 28 (motsvarar P9_15/GPIO48)
line.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT) → Sätter linjen som utgång

Loop som styr reläet
while True: → Skapar en oändlig loop
line.set_value(1) → Sätter GPIO HIGH, reläet slås på
time.sleep(0.1) → Pausar 0,1 s
line.set_value(0) → Sätter GPIO LOW, reläet slås av
time.sleep(0.1) → Pausar 0,1 s
Resultat: Reläet blinkar med 0,1 sekunders intervall.

⚠️ Säkerhetstips

Kontrollera att reläets spänning matchar BBB:s 5V-utgång
Använd alltid GND för att undvika skador
Vid styrning av högspänningsenheter (t.ex. 230V) använd separata skyddskretsar

📖 Nyckelpunkter för provet

GPIO48 (P9_15) styr reläet
VCC = 5V, GND = jord
while True = oändlig loop
line.set_value(1) = relä på, line.set_value(0) = relä av
time.sleep(x) = paus i x sekunder

---------------------------------

I det här projektet använder vi en BeagleBone Green (BBG) för att styra ett 5V-relä via GPIO. 
Material som behövs är: en BeagleBone Green, en 5V-relämodul, fyra jumperkablar och ström, som vi kan ta från BBB:s 5V-utgång.

Kopplingarna görs på följande sätt: P9_15 (GPIO48) på BBB kopplas till relämodulens IN-pin med en gul kabel, 
P9_01 kopplas till reläets GND med svart kabel, och P9_05 kopplas till reläets VCC med röd kabel. 
Det går även att ha en reservkabel (vit) om man vill. 
Det är viktigt att kablarna sitter ordentligt och att relämodulen klarar 5V-logik från BBB.

För att styra reläet använder vi ett Python-skript med biblioteken gpiod och time. 
gpiod används för att styra GPIO-pinnar på Linux, och time används för att göra pauser. 
Först initierar vi GPIO-chipet med chip = gpiod.Chip('gpiochip0') och väljer linje 28 (motsvarande GPIO48) med line = chip.get_line(28). 
Linjen konfigureras som utgång med line.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT).

I skriptet används sedan en evig loop med while True:. 
Inuti loopen slår line.set_value(1) på reläet genom att sätta GPIO-linjen HIGH, sedan pausas programmet i 0,1 sekunder med time.sleep(0.1). 
Efter det slår line.set_value(0) av reläet (GPIO LOW) och programmet pausar igen i 0,1 sekunder. 
Resultatet blir att reläet blinkar med 0,1 sekunders intervaller.

Det är viktigt att alltid koppla GND, och att kontrollera att reläets spänning matchar BBB:s 5V-utgång. 
Om man ska styra externa enheter med högre spänning, t.ex. 230V, måste man alltid använda separata skyddskretsar.

Sammanfattningsvis: GPIO48 (P9_15) styr reläet, VCC ger 5V och GND jord, 
while True skapar en oändlig loop, line.set_value(1) slår på reläet, line.set_value(0) slår av det, och time.sleep() 
pausar programmet för att skapa blinkande effekt.
