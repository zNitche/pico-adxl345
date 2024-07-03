import time
import struct
from micropython import const
import machine


DEVICE_ID_REGISTER_ADDR = const(0x00)
DEVICE_ID = const(0xE5)
POWER_CONTROL_REGISTER_ADDR = const(0x2D)
DATA_REGISTER_ADDR = const(0x32)

ACTIVE_MODE = const(0x28)
STANDBY_MODE = const(0x24)


class ADXL345:
    def __init__(self, i2c: machine.I2C, address=0x53):
        self.i2c = i2c
        self.address = address

        self.__compensation_value = 0.039228

    def is_device_accessible(self) -> bool:
        return True if self.address in self.i2c.scan() else False

    def check_connection(self) -> bool:
        data = self.i2c.readfrom_mem(self.address, DEVICE_ID_REGISTER_ADDR, 1)
        time.sleep_ms(20)

        return True if data == bytearray((DEVICE_ID,)) else False

    def start_measurements(self):
        self.i2c.writeto_mem(self.address, POWER_CONTROL_REGISTER_ADDR, bytearray([ACTIVE_MODE]))
        time.sleep_ms(50)

    def stop_measurements(self):
        self.i2c.writeto_mem(self.address, POWER_CONTROL_REGISTER_ADDR, bytearray([STANDBY_MODE]))

    def get_xyz(self) -> tuple[float, float, float]:
        data = self.i2c.readfrom_mem(self.address, DATA_REGISTER_ADDR, 6)
        raw_data_struct = struct.unpack("<hhh", data)

        x_acceleration = raw_data_struct[0] * self.__compensation_value
        y_acceleration = raw_data_struct[1] * self.__compensation_value
        z_acceleration = raw_data_struct[2] * self.__compensation_value

        return x_acceleration, y_acceleration, z_acceleration
