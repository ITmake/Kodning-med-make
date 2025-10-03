# Kodning-med-make

>>> import smbus2
>>> import bme280
>>> import time
>>>
>>> address = 0x76
>>> bus = smbus2.SMBus(2)
>>>
>>> calibration_params = bme280.load_calibration_params(bus, address
>>>
>>> def do():
...     while True:
...             data = bme280.sample(bus, address, calibration_params)
...             print(f"Temperature: {data.temperature:.1f} °C")
...             print(f"Humidity: {data.humidity:.1f} %")
...             print(f"Pressure: {data.pressure:.1f} hPa")
...             time.sleep(2)


jag updatera och ladda alla bibliotek 
sudo apt update
sudo apt install python3-smbus python3-pip python3-bme280 i2c-tools

sen böt jag "while true" i koden till "def do ():" while true istället så den det inte blir loop

sen tittade jag också att den hittar sensoren etc
