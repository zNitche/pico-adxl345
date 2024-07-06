### pico-adxl345

MicroPython module for performing measurements using ADXL345 accelerometer.

#### Usage
```
import machine
import time
from adxl345 import ADXL345


def main():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
    sensor = ADXL345(i2c)

    if sensor.check_connection():
        sensor.start_measurements()

        for _ in range(10):
            x, y, z = sensor.get_readings()
            print(f"X:{x} | Y:{y} | Z:{z}")

            time.sleep(0.5)

        sensor.stop_measurements()


if __name__ == '__main__':
    main()
```

#### Resources
- [Datasheet](https://www.sparkfun.com/datasheets/Sensors/Accelerometer/ADXL345.pdf)
