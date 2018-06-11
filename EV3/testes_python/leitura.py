import smbus
import time
import threading

bus = smbus.SMBus(6)        # i2c-canal6 -> entrada 4 do lego
address = 0x04
pedido = 49
liga_led = 50
desliga_led = 51

def worker():
    while 1:
        print bus.read_i2c_block_data(address, pedido, 8)
        time.sleep(1)

t = threading.Thread(target=worker)
t.start()

while 1:
    time.sleep(0.5)

