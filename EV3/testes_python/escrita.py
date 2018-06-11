import smbus
import time

bus = smbus.SMBus(6)        # i2c-canal6 -> entrada 4 do lego

while 1:
    data = raw_input("Pressione enter para pedir dados ") # 2 para ligar o led e 3 para desligar
    if len(data) == 1:
        data = int(data)
        bus.write_byte(0x04, data + 48)
