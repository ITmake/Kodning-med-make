# Kommunikation mellan två BeagleBones via RS232

Detta projekt demonstrerar seriell kommunikation mellan två BeagleBones med hjälp av Python och RS232. 
En BeagleBone skickar ljusdata och tar emot temperaturdata från den andra BeagleBone.

## Förutsättningar

1. **Python**  
   Skriptet kräver Python 3.
2. **PySerial**  
   Installera med:
   ```bash
   pip3 install pyserial

#installera

sudo apt install python3-serial

#Koden

import serial
import time
import random

# Open serial port
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

while True:
    # Simulate temperature reading
    temperature = 22.5 + random.uniform(-1, 1)
    temp_message = f"TEMP:{temperature:.2f}\n"
    ser.write(temp_message.encode('utf-8'))
    print("Skickat:", temp_message.strip())

    # Read incoming light data
    incoming = ser.readline().decode('utf-8').strip()
    if incoming:
        print("Mottaget:", incoming)

    time.sleep(2)


#Fysiska Kopplingar

-Anslut de två BeagleBones via J5-kontakten.
-Koppla TX på BeagleBone A till RX på BeagleBone B och vice versa.
-Se till att GND är gemensam mellan enheterna.
