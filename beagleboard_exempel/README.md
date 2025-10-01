# BeagleBoard-exempel

Den här mappen innehåller anteckningar och skript för att komma igång med Grove-sensorer och BeagleBone Black.

## Installation

```bash
sudo apt update
sudo apt install python3-smbus python3-pip python3-bme280 i2c-tools
```

## Skript

- `gpio_blink.py`, `gpio_bilblink.py`, `gpio_snabbblink.py` – olika varianter av blinkande LED:er.
- `grove_speaker_sound_test.py` – spelar en enkel skala på en Grove-högtalare.
- `import_smbus2.py` – läser data från en BME280-sensor.
- `sht35.py` – kommunicerar med en SHT35-sensor.

Textfilerna `bme280.txt` och `sht35_install.txt` innehåller ytterligare instruktioner.

## Exempel: läsa av BME280

```python
import smbus2
import bme280
import time

ADDRESS = 0x76
BUS = smbus2.SMBus(2)
CALIBRATION_PARAMS = bme280.load_calibration_params(BUS, ADDRESS)

while True:
    data = bme280.sample(BUS, ADDRESS, CALIBRATION_PARAMS)
    print(f"Temperature: {data.temperature:.1f} °C")
    print(f"Humidity: {data.humidity:.1f} %")
    print(f"Pressure: {data.pressure:.1f} hPa")
    time.sleep(2)
```

Kör skriptet med `python import_smbus2.py` när hårdvaran är ansluten.

