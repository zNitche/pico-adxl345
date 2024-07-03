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

        while True:
            x, y, z = sensor.get_xyz()
            print(f"X:{x} | Y:{y} | Z:{z}")

            time.sleep(1)


if __name__ == '__main__':
    main()

```

#### Resources
- [Datasheet](https://www.sparkfun.com/datasheets/Sensors/Accelerometer/ADXL345.pdf)
