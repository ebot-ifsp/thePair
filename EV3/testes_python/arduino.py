#!/usr/bin/env python3
# -*- coding: latin-1 -*-
'''
Baseado na biblioteca pra i2c:
http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc

'''

import sys, os
import numpy as np

from smbus import SMBus

class Arduino():
    def __init__(self):
        self.address = 0x04
        self.canal = 6
        self.pedido = 1
        self.led_on = 2
        self.led_off = 3
        self.tamanho = 8
        self.buss = SMBus(self.canal)
        self.limiar = 40                

    def le_todos(self):
        resposta =  self.buss.read_i2c_block_data(
                    self.address, self.pedido, self.tamanho)
        return resposta
    
    def le(self, qual):
        valores = self.le_todos()
        return valores[qual]

    def liga_led(self):
        resposta = self.buss.read_i2c_block_data(
                    self.address, self.led_on, self.tamanho)

    def desliga_led(self):
        self.buss.read_i2c_block_data(
                    self.address, self.led_off, self.tamanho)

    def calibrar(self):
        self.buss.read_i2c_block_data(self.address, 4, self.tamanho)

    def sensores(self):
        return np.array(self.le_todos()) > self.limiar
