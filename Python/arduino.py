#!/usr/bin/env python3
# -*- coding: latin-1 -*-
'''
Baseado na biblioteca pra i2c:
http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc

'''
import sys, os
from movimento import limiar_if
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
        self.limiar = limiar_if

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
        resposta = []
        Sensores = self.le_todos()
        for sensor in Sensores:
            resposta.append(sensor > self.limiar)
        return resposta

    def posicao(self, sensores):
        acom_inf = 0.0
        acom_sup = 0.0
        for indice, sensor in enumerate(sensores):
            acom_inf += sensor
            acom_sup += indice*1000*sensor
        return float(acom_sup/acom_inf)

    def quantidade(self, Sensores):
        q = 0
        for sensor in Sensores:
            if sensor != 0:
                q += 1
        return q
