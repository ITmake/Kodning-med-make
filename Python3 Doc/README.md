# Python3 DOC

1️⃣#Anslut till BeagleBone via PuTTY

-Starta PuTTY på din dator.
-Ange BeagleBones IP-adress i fältet Host Name (or IP address). 192.168.7.2
-Klicka på Open.
-Logga in med användarnamn och lösenord (debian & Temppwd eller By8Hq2Ze)

2️⃣#Skapa en ny fil med Nano

-Nano "t.ex" (blinkled.py)

#Nu är du i Nano-editor. Skriv ditt program här. Exempel på en enkel C-kod som blinkar en LED (pseudo-exempel, du behöver justera GPIO-numren för BeagleBone):

#exempel kod 
"import gpiod
import time

chip = gpiod.Chip('gpiochip0')
line = chip.get_line(28)
line.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT)

while True:
    # Blink på (lite längre än "snabbblink")
    line.set_value(1)
    time.sleep(0.5)   # 0.5 sekunder på
    
    # Blink av (lite kortare paus)
    line.set_value(0)
    time.sleep(0.5)   # 0.5 sekunder av"

3️⃣#Spara filen i Nano

-Tryck Ctrl + O → Enter (sparar filen)
-Tryck Ctrl + X (stänger Nano)

4️⃣#Kör koden med följande

-Python3 "t.ex" (blinkled.py)

5️⃣#Tips

-Nano: Ctrl + K = klipp, Ctrl + U = klistra in.
-För GPIO-styrning på BeagleBone, använd /sys/class/gpio eller bibliotek som Adafruit_BBIO för Python.

1️⃣#Uppdatera systemet

-sudo apt-get update     # Uppdaterar paketlistan
-sudo apt-get upgrade    # Uppgraderar installerade paket
-sudo apt-get dist-upgrade  # (valfritt) Uppgraderar större paket och kärnan

2️⃣#Installera grundläggande utvecklingsverktyg

-sudo apt-get install build-essential   # Innehåller gcc, g++ och make
-sudo apt-get install git               # För att ladda ner projekt från GitHub
-sudo apt-get install cmake             # Byggsystem (om du behöver det)

3️⃣#Installera Python och nödvändiga bibliotek

-sudo apt-get install python3           # Python 3
-sudo apt-get install python3-pip       # Paketverktyg
-sudo pip3 install Adafruit_BBIO        # Bibliotek för GPIO på BeagleBone
-sudo pip3 install RPi.GPIO             # Kan också fungera på vissa BeagleBone-varianter

4️⃣#Uppdatera firmware och kernel (valfritt men rekommenderat)

-sudo apt-get install bbb-update        # Om tillgängligt
-sudo bbb-update                         # Kör firmware-uppdatering

5️⃣#Kontrollera att GPIO fungerar

-import Adafruit_BBIO.GPIO as GPIO
-GPIO.setup("P9_14", GPIO.OUT)
-GPIO.output("P9_14", GPIO.HIGH)

1️⃣#Extra utvecklingsverktyg

-sudo apt-get install gdb

-sudo apt-get install vim
-sudo apt-get install emacs

-sudo apt-get install screen
-sudo apt-get install minicom

2️⃣#Extra Python-bibliotek

numpy & scipy – matematiska beräkningar:
-sudo pip3 install numpy scipy

matplotlib – för att plotta data:
-sudo pip3 install matplotlib

pyserial – kommunikation via seriell port:
-sudo pip3 install pyserial

Adafruit_BBIO.PWM – för PWM-styrning av motorer/LED:
-sudo pip3 install Adafruit_BBIO

3️⃣#Verktyg för nätverk och debugging

curl och wget – för att ladda filer från internet:
-sudo apt-get install curl wget

htop – för att övervaka systemresurser:
-sudo apt-get install htop

net-tools – för nätverksdiagnostik (ifconfig, netstat):
-sudo apt-get install net-tools

4️⃣#GUI-relaterade saker (om du använder desktop)

Python Tkinter – för grafiska fönster:
-sudo apt-get install python3-tk

X11 forwarding – om du vill köra GUI-program över SSH:
-sudo apt-get install xauth x11-apps

5️⃣#Säkerhetskopiering & uppdatering

Skapa en lista över installerade paket innan stora uppdateringar:
-dpkg --get-selections > paketlista.txt

1️⃣#Versionskontroll och projektstruktur

Git – för att hantera kodversioner:
-sudo apt-get install git

Make / CMake – för att automatisera byggprocesser:
-sudo apt-get install make cmake

2️⃣#Hårdvarunära bibliotek

libi2c-dev – för I²C-kommunikation:
-sudo apt-get install libi2c-dev i2c-tools

SPI-stöd – för SPI-kommunikation:
-sudo apt-get install python3-spidev

🧰#BeagleBone Green – P8 Header

| Pin   | Funktion  | Användning                         |
| ----- | --------- | ---------------------------------- |
| P8_3  | GPIO1_6   | Digital I/O, t.ex. LED eller knapp |
| P8_4  | GPIO1_7   | Digital I/O                        |
| P8_5  | GPIO1_2   | Digital I/O                        |
| P8_6  | GPIO1_3   | Digital I/O                        |
| P8_13 | EHRPWM2B  | PWM, styr motor eller LED          |
| P8_19 | I2C2_SCL  | I2C klocka, sensorer               |
| P8_20 | I2C2_SDA  | I2C data, sensorer                 |
| P8_21 | UART2_TXD | Seriell sändning                   |
| P8_22 | UART2_RXD | Seriell mottagning                 |
| P8_23 | UART1_TXD | Seriell sändning                   |
| P8_24 | UART1_RXD | Seriell mottagning                 |

🧰#BeagleBone Green – P9 Header

| Pin   | Funktion  | Användning                      |
| ----- | --------- | ------------------------------- |
| P9_11 | I2C2_SCL  | I2C klocka, sensorer            |
| P9_12 | I2C2_SDA  | I2C data, sensorer              |
| P9_13 | EHRPWM0B  | PWM output, t.ex. motorstyrning |
| P9_14 | EHRPWM1A  | PWM output                      |
| P9_15 | GPIO1_16  | Digital I/O                     |
| P9_16 | EHRPWM1B  | PWM output                      |
| P9_17 | I2C1_SCL  | Alternativ I2C klocka           |
| P9_18 | I2C1_SDA  | Alternativ I2C data             |
| P9_19 | SPI0_CS0  | SPI chip select                 |
| P9_20 | SPI0_D0   | SPI data out                    |
| P9_21 | SPI0_D1   | SPI data in                     |
| P9_22 | SPI0_SCLK | SPI klocka                      |
| P9_33 | AIN4      | Analog input, t.ex. sensor      |
| P9_35 | AIN6      | Analog input                    |
| P9_36 | AIN5      | Analog input                    |
| P9_39 | AIN0      | Analog input                    |
| P9_40 | AIN1      | Analog input                    |

#Kortfattat användningsområde

-GPIO: LED, knappar, reläer, enkla digitala signaler.

-PWM: Motorer, servon, LED-dimmer.

-I2C: Sensorer och Grove-moduler.

-SPI: Snabb kommunikation med externa ICs (t.ex. SD-kort, displayer).

-UART: Seriell kommunikation (t.ex. med GPS, moduler, dator).

-Analog (AIN): Sensorer som mäter spänning (0–1.8V).
