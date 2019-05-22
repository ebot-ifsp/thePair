import serial, time
from movimento import limiar_if

class Arduino():
    def __init__(self, port='/dev/ttyUSB0', baud=9600):
        self.init_data = 'I'
        self.end_data = '\r\n'
        self.s = serial.Serial(port, baud, timeout=0)
        self.s.open()

    def move_servo(self, qual, posicao):
        if qual == 'A':
            self.s.write('SA' + str(posicao))
        elif qual == 'B':
            self.s.write('SB' + str(posicao))

    def le_linha(self):
        self.s.read(50)         # limpa buffer com possíveis dados anteriores
        self.s.write('3\n')     # envia pedido de leitura
        time.sleep(0.05)
        leitura = self.s.read(50)
        if self.valida_leitura(leitura):
            leitura = leitura[1:-2].decode()
            sensores, posicao = leitura.split('-')
            return sensores, posicao
        return None 

    def valida_leitura(self, dado):
        if dado[0] == ord(self.init_data) and dado[-2] == ord(self.end_data[0]) and dado[-1] == ord(self.end_data[1]):
            return True
        return False

    def __dell__(self):
        self.s.close()

    
