#!/usr/bin/env python3
import time
import smbus2

# ===== Config =====
I2C_BUS = 2                 # /dev/i2c-2 (change if needed)
SHT3X_ADDRESS = 0x45        # Grove SHT35 often uses 0x45; can also be 0x44

# Single shot, no clock stretching, high repeatability command for SHT3x
# (see Sensirion datasheet)
CMD_SINGLE_SHOT_HIGH = (0x24, 0x00)

def _crc8_sht(data: bytes) -> int:
    """
    Sensirion CRC-8 for SHT3x (poly 0x31, init 0xFF).
    """
    poly = 0x31
    crc = 0xFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def read_sht35():
    """
    Returns a dict with 'temperature' (°C) and 'humidity' (%RH).
    Raises OSError on I2C errors and ValueError on CRC mismatch.
    """
    with smbus2.SMBus(I2C_BUS) as bus:
        # Trigger single-shot high repeatability measurement (no clock stretching)
        bus.write_i2c_block_data(SHT3X_ADDRESS, CMD_SINGLE_SHOT_HIGH[0], [CMD_SINGLE_SHOT_HIGH[1]])

        # Measurement time: high repeatability ~15ms; add margin
        time.sleep(0.02)

        # Read 6 bytes: T_MSB, T_LSB, T_CRC, RH_MSB, RH_LSB, RH_CRC
        data = bus.read_i2c_block_data(SHT3X_ADDRESS, 0x00, 6)
        t_raw = bytes(data[0:2])
        t_crc = data[2]
        rh_raw = bytes(data[3:5])
        rh_crc = data[5]

        if _crc8_sht(t_raw) != t_crc or _crc8_sht(rh_raw) != rh_crc:
            raise ValueError("CRC check failed reading SHT35")

        t_ticks = (t_raw[0] << 8) | t_raw[1]
        rh_ticks = (rh_raw[0] << 8) | rh_raw[1]

        # Convert per datasheet
        temperature_c = -45.0 + (175.0 * (t_ticks / 65535.0))
        humidity_rh = 100.0 * (rh_ticks / 65535.0)
        # Clamp humidity to [0, 100]
        humidity_rh = max(0.0, min(100.0, humidity_rh))

        return {
            "temperature": temperature_c,
            "humidity": humidity_rh
        }

def main():
    try:
        while True:
            try:
                data = read_sht35()
                print(f"Temperature: {data['temperature']:.2f} °C")
                print(f"Humidity:    {data['humidity']:.2f} %RH")
                print()  # blank line
            except (OSError, ValueError) as e:
                # transient I2C or CRC issues—log and keep going
                print(f"Read error: {e}")
            time.sleep(2)  # delay between readings
    except KeyboardInterrupt:
        print("Measurement stopped by user")

if __name__ == "__main__":
    main()
