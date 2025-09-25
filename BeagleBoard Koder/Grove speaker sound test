import Adafruit_BBIO.PWM as PWM
import time

# PWM pin connected to Grove Speaker
speaker_pin = "P9_14"

# Function to play a tone
def play_tone(frequency, duration):
    PWM.start(speaker_pin, 50, frequency)  # 50% duty cycle
    time.sleep(duration)
    PWM.stop(speaker_pin)

# Play a simple scale
notes = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
duration = 0.5  # seconds

for note in notes:
    play_tone(note, duration)
    time.sleep(0.1)  # short pause between notes

PWM.cleanup() 
