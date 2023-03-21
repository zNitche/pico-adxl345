# https://www.digikey.com/en/maker/projects/raspberry-pi-pico-rp2040-i2c-example-with-micropython-and-cc/47d0c922b79342779cdbd4b37b7eb7e2

import utime
import ustruct
from micropython import const


REG_DEVICE_ID = const(0x00)
REG_POWER_CTL = const(0x2D)
REG_DATAX0 = const(0x32)

DEVICE_ID = const(0xE5)
MG2G_MULTIPLIER = const(0.004)
EARTH_GRAVITY = const(9.807)


class ADXL345:
    def __init__(self, i2c, address=0x53):
        self.i2c = i2c
        self.address = address

    def reg_write(self, addr, reg, data):
        data_struct = bytearray()
        data_struct.append(data)

        self.i2c.writeto_mem(addr, reg, data_struct)

        utime.sleep(0.5)

    def reg_read(self, addr, reg, nbytes=1):
        return self.i2c.readfrom_mem(addr, reg, nbytes) if nbytes > 1 else bytearray()

    def check_connection(self):
        data = self.reg_read(self.address, REG_DEVICE_ID)

        return True if data != bytearray((DEVICE_ID,)) else False

    def read_power_control_register(self):
        return self.reg_read(self.address, REG_POWER_CTL)

    def start_measurements(self):
        pwc = self.read_power_control_register()

        self.reg_write(self.address, REG_POWER_CTL, (int.from_bytes(pwc, "big") | (1 << 3)))

    def init(self):
        self.start_measurements()

    def get_xyz(self):
        data = self.reg_read(self.address, REG_DATAX0, 6)

        x_acceleration = ustruct.unpack_from("<h", data, 0)[0] * MG2G_MULTIPLIER * EARTH_GRAVITY
        y_acceleration = ustruct.unpack_from("<h", data, 2)[0] * MG2G_MULTIPLIER * EARTH_GRAVITY
        z_acceleration = ustruct.unpack_from("<h", data, 4)[0] * MG2G_MULTIPLIER * EARTH_GRAVITY

        return [x_acceleration, y_acceleration, z_acceleration]
