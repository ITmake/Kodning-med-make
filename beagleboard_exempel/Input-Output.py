#!/usr/bin/env python3
"""
sht35_fan_control.py
 
Reads SHT35 temperature/humidity and enables a relay (fan) when temperature
exceeds a threshold. Uses libgpiod for relay control.
 
Configurable constants are near the top of the file.
"""
 
import time
import signal
import sys
import smbus2
import gpiod
 
# ===== Config =====
I2C_BUS = 2                 # /dev/i2c-2 (change if needed)
SHT3X_ADDRESS = 0x45        # SHT35 address (0x45 or 0x44)
CMD_SINGLE_SHOT_HIGH = (0x24, 0x00)
 
# Relay / fan GPIO (using libgpiod). Example used line 28 in your relay script.
GPIOCHIP = "gpiochip0"
RELAY_LINE_NUM = 28        # change if your relay is on a different line
 
# Temperature control parameters
TEMP_THRESHOLD_C = 25.0    # turn fan ON when temperature >= this (°C)
HYSTERESIS_C = 0.5         # require temp to fall below (threshold - hysteresis) to turn OFF
READ_INTERVAL = 2.0        # seconds between sensor reads
 
# ===== SHT3x CRC helper =====
def _crc8_sht(data: bytes) -> int:
    """
    Sensirion CRC-8 (poly 0x31, init 0xFF).
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
        humidity_rh = max(0.0, min(100.0, humidity_rh))
 
        return {
            "temperature": temperature_c,
            "humidity": humidity_rh
        }
 
# ===== Relay (fan) control wrapper =====
class RelayFan:
    def __init__(self, chip_name: str, line_num: int, active_high: bool = True):
        """
        chip_name: e.g. "gpiochip0"
        line_num: line offset (int)
        active_high: if True, set line value 1 to enable relay. If False, invert logic.
        """
        self.chip_name = chip_name
        self.line_num = line_num
        self.active_high = active_high
        self.chip = None
        self.line = None
        self._state = False
 
        # request line
        try:
            self.chip = gpiod.Chip(self.chip_name)
            self.line = self.chip.get_line(self.line_num)
            self.line.request(consumer="sht35-fan", type=gpiod.LINE_REQ_DIR_OUT)
            # make sure relay is off at startup
            self.set(False)
            print(f"[RelayFan] Requested line {self.line_num} on {self.chip_name}")
        except Exception as e:
            # propagate so caller can handle; device may not have gpio access
            raise RuntimeError(f"Failed to request GPIO line {self.line_num} on {self.chip_name}: {e}")
 
    def set(self, enable: bool):
        """Set fan/relay on (True) or off (False)."""
        if self.line is None:
            raise RuntimeError("GPIO line not initialized")
        value = 1 if (enable and self.active_high) or (not enable and not self.active_high) else 0
        try:
            self.line.set_value(value)
            self._state = bool(enable)
        except Exception as e:
            print(f"[RelayFan] Failed to set GPIO line: {e}")
 
    def is_on(self) -> bool:
        return bool(self._state)
 
    def cleanup(self):
        try:
            if self.line is not None:
                # ensure off
                self.set(False)
                self.line.release()
            if self.chip is not None:
                self.chip.close()
        except Exception:
            pass
 
# ===== Main control loop =====
should_exit = False
 
def signal_handler(signum, frame):
    global should_exit
    print(f"\n[Main] Signal {signum} received, shutting down...")
    should_exit = True
 
def main():
    global should_exit
 
    # install signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
 
    # Initialize relay/fan controller
    try:
        fan = RelayFan(GPIOCHIP, RELAY_LINE_NUM, active_high=True)
    except Exception as e:
        print(f"[Main] ERROR initializing RelayFan: {e}")
        sys.exit(1)
 
    # Derived thresholds for hysteresis
    on_threshold = TEMP_THRESHOLD_C
    off_threshold = TEMP_THRESHOLD_C - HYSTERESIS_C
 
    print(f"[Main] Starting loop: ON >= {on_threshold:.2f} °C, OFF <= {off_threshold:.2f} °C, read every {READ_INTERVAL}s")
    try:
        while not should_exit:
            try:
                data = read_sht35()
                temp = data['temperature']
                rh = data['humidity']
                print(f"[Sensor] Temperature: {temp:.2f} °C, Humidity: {rh:.2f} %RH")
 
                # Hysteresis control
                if not fan.is_on() and temp >= on_threshold:
                    fan.set(True)
                    print(f"[Control] Temperature {temp:.2f} >= {on_threshold:.2f} -> FAN ON")
                elif fan.is_on() and temp <= off_threshold:
                    fan.set(False)
                    print(f"[Control] Temperature {temp:.2f} <= {off_threshold:.2f} -> FAN OFF")
                else:
                    # no change; optionally print current state
                    print(f"[Control] Fan is {'ON' if fan.is_on() else 'OFF'}. No state change.")
 
            except (OSError, ValueError) as e:
                # Transient I2C or CRC issues — log and keep going
                print(f"[Sensor] Read error: {e}")
 
            # Sleep until next read or until exit requested
            for _ in range(int(max(1, READ_INTERVAL))):
                if should_exit:
                    break
                time.sleep(1)
            # If READ_INTERVAL isn't an integer, sleep remaining fractional part
            frac = READ_INTERVAL - int(READ_INTERVAL)
            if frac and not should_exit:
                time.sleep(frac)
 
    except KeyboardInterrupt:
        print("[Main] KeyboardInterrupt received")
 
    finally:
        print("[Main] Cleaning up: turning fan off and releasing GPIO")
        try:
            fan.cleanup()
        except Exception:
            pass
        print("[Main] Goodbye")
 
if __name__ == "__main__":
    main()
 