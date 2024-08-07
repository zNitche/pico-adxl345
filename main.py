import machine
import time
from adxl345 import ADXL345, RANGE_4G


def main():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
    sensor = ADXL345(i2c, range=RANGE_4G)

    if sensor.check_connection():
        sensor.start_measurements()

        for _ in range(100):
            x, y, z = sensor.get_readings()
            print(f"X:{x} | Y:{y} | Z:{z}")

            time.sleep(0.5)

        sensor.stop_measurements()


if __name__ == '__main__':
    main()
