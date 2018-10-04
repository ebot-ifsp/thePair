#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
import time
from movimento import *
from arduino import *
ard = Arduino()
from controle import *

estado = 1
btn = ev3.Button()

while not btn.any():                                    # esperando botao para
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)  # iniciar
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
    time.sleep(0.05)
time.sleep(1)
ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)       # ready go
ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)      # go go go

def change(bt):
    print('change')
    bt_pressionado = True
    time.sleep(1)

try:
    while not btn.any():
        #verifica se tem obstaculo para desviar
        if ir.value() < minimo_if:                     # caso chegue no obstaculo
            print('devia bloco')
            desvia_bloco()
        # verificar se alguma linha verde foi encotrada
        #
        #
        sensores = ard.sensores()
        qt_preto = ard.quantidade(sensores)
        if qt_preto > 0 and qt_preto < 3:               # linha normal
            estado = segue_linha(sensores, estado)
            print(estado, 'maquina estado')
        elif qt_preto == 0:                             # sem linha
            anda(v_reta, 0)
            estado = 1
            print(qt_preto, 'reta')
        elif qt_preto > 6:                              # encruzilhada
            print(qt_preto, 'cruzamento')
            parar()
            time.sleep(0.1)
            gira_angulo(90)                             # gira 90 graus
            time.sleep(0.1)
            gira('direita', v_gira/2)                   # continua girando
            while not sensoresMeio(ard.sensores()):     # ate linha chegar nomeio do
                time.sleep(0.1)                         # sensor
            parar()
            estado = 1
        elif qt_preto > 3:                              # virar 90 graus
            print(sensores)
            if sensoresDireita(sensores) and sensoresEsquerda(sensores):
                print('esquerda e direita')
            elif sensoresDireita(sensores):
                print('Direita')
                curva_alinhar('direita')                        # sensor
            elif sensoresEsquerda(sensores):
                print('Esquerda')
                curva_alinhar('esquerda')
        else:
            print('else', sensores, qt_preto)
    parar()
    time.sleep(1)

except Exception as e:
    parar()
    print('except', e)
    time.sleep(1)
