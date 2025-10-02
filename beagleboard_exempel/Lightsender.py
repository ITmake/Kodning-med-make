import serial
import time
import random

# Open serial port
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

while True:
    # Simulate light reading
    light = 300 + random.randint(-20, 20)
    light_message = f"LIGHT:{light}\n"
    ser.write(light_message.encode('utf-8'))
    print("Skickat:", light_message.strip())

    # Read incoming temperature data
    incoming = ser.readline().decode('utf-8').strip()
    if incoming:
        print("Mottaget:", incoming)

    time.sleep(2)
