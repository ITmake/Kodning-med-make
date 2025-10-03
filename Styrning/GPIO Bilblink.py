import gpiod
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
    time.sleep(0.5)   # 0.5 sekunder av