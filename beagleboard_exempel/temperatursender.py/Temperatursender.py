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
