#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
from controle import *
from arduino import *
import numpy as np
import time

ard = Arduino()
estado = 1

while 1:
    if ir.value() < minimo_if:                     # caso chegue no obstaculo
        desvia_bloco()
    sensores = ard.sensores()
    qt_preto = np.count_nonzero(sensores)
    if qt_preto == 0 or qt_preto == 8:      # tudo branco (sem linha) ou encruzilhada
        if qt_preto == 8:
            print('8')
        anda(v_reta + 200, 0)
    elif qt_preto > 3:                      # encruzilhada ou virada (verde)
        print('>3 antes', qt_preto)
        parar()
        anda_posicao(5, velocidade=50)
        sensores = ard.sensores()
        qt_preto = np.count_nonzero(sensores)
        if qt_preto == 4 or qt_preto == 5:                     # cor para virar - descobrir para onde
            print("4", qt_preto)
            if sensoresEsquerda(sensores):
                print('curva esquerda')
                curvaVerde('esquerda', ard)
                estado=1
            elif sensoresDireita(sensores):
                print('curva direita')
                curvaVerde('direita', ard)
                estado=2
            else:
                print('Arrumar !')
            estado = segue_linha(sensores, estado)
        elif qt_preto == 6 or qt_preto == 7:                     # fim de curso - Voltar
            print("6-7", qt_preto)
            gira_angulo(120)
            gira('direita')
            sensores = ard.sensores()
            while not sensoresMeio(sensores):
                sensores = ard.sensores()
                time.sleep(0.01)
            estado = 1
        elif qt_preto == 8:
            anda(v_reta + 200, 0)
        else:
            estado = segue_linha(sensores, estado)
    elif qt_preto < 4 and  qt_preto > 0:
        estado = segue_linha(sensores, estado)
    else:
        anda(v_reta, 0)

