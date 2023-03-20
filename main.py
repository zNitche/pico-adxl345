from machine import Pin, I2C
from adxl345 import ADXL345
import time


def main():
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
    adx = ADXL345(i2c)

    if adx.check_connection():
        adx.init()

        while True:
            x, y, z = adx.get_xyz()
            print(f"X:{x} | Y:{y} | Z:{z}")

            time.sleep(0.5)


if __name__ == '__main__':
    main()
