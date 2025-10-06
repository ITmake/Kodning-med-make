STYRA RELÉ MED BEAGLEBONE GREEN (BASIC KOD)

📦 Materiallista

-Komponent	Antal
-BeagleBone Green	1
-Relämodul (5V)	1
-Jumperkablar	4
-Strömkälla (5V)	1 (via BBB)

🔌 Kopplingar

-BeagleBone Pin	Funktion	Relämodul Pin	Kabelfärg
-P9_15 (GPIO 48)	Styrsignal	IN	🟡 Gul
-P9_01	Jord	GND	⚫ Svart
-P9_05	5V-ström	VCC	🔴 Röd
-(Reserv)	-	-	⚪ Vit

💻 skript för att styra relä

import gpiod
import time

chip = gpiod.Chip('gpiochip0')
line = chip.get_line(28)
line.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT)

while True:
    line.set_value(1)
    time.sleep(0.1)
    line.set_value(0)
    time.sleep(0.1)
