import gpiod
import time
import threading

chip = gpiod.Chip('gpiochip0')
line = chip.get_line(28)
line.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT)

state = 0
interval = 0.1  # blinkintervall
running = True
paused = False

def input_thread():
    global running, paused
    while running:
        cmd = input("Skriv 'p' för pausa, 'r' för fortsätt, 'q' för avsluta: ").strip().lower()
        if cmd == 'p':
            paused = True
        elif cmd == 'r':
            paused = False
        elif cmd == 'q':
            running = False
            break

# Starta tråd som lyssnar på tangentbord
threading.Thread(target=input_thread, daemon=True).start()

while running:
    if not paused:
        state ^= 1
        line.set_value(state)
    time.sleep(interval)

# Släpp GPIO-linjen när vi avslutar
line.set_value(0)
line.release()
print("Programmet avslutat.")
