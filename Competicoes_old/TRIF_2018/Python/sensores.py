#!/usr/bin/env python3
# -*- coding: latin-1 -*-
'''
Baseado na biblioteca pra i2c:
http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc

'''
import sys, os
from smbus import SMBus
import ev3dev.ev3 as ev3
from movimento import *

btn = ev3.Button()

corE = ev3.ColorSensor(pino_corE)
corD = ev3.ColorSensor(pino_corD)
corE.mode = 'RGB-RAW'
corD.mode = 'RGB-RAW'

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

    def sensores(self, Sensores=None):
        resposta = []
        if not Sensores:
            Sensores = self.le_todos()
        for sensor in Sensores:
            resposta.append(sensor > self.limiar)
        return resposta

    def quantidade(self, Sensores=None):
        q = 0
        if not Sensores:
            Sensores = self.sensores()
        for sensor in Sensores:
            if sensor != 0:
                q += 1
        return q

    def pos_linha(self, Sensores=None):
        if not Sensores:
            Sensores = self.le_todos()
        resposta_sup, resposta_inf = 0, 0
        for i, sensor in enumerate(Sensores):
            if sensor > self.limiar:
                resposta_sup += 1000*(i+1)*sensor
                resposta_inf += sensor
        if resposta_inf > 0:
            return resposta_sup/resposta_inf
        else:
            return 0

ard = Arduino()