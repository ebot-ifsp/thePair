#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
from controle import *
from arduino import *
import numpy as np
import time

ard = Arduino()
estado = 1

sequencia = ['dir', 'vol', 'esq', 'reto']

while 1:
    if ir.value() < 25:                     # caso chegue no obstaculo
        desvia_bloco()
    sensores = ard.sensores()
    qt_preto = np.count_nonzero(sensores)
    if qt_preto == 0:
        anda(v_reta + 200, 0)
    elif qt_preto > 3:                      # encruzilhada ou virada (verde)
        print('>3', qt_preto)
        acao = sequencia[0]
        sequencia.pop(0)
        if acao == 'esq':
            print('esq')
            curvaVerde('esquerda', ard)
        elif acao == 'dir':
            print('dir')
            curvaVerde('direita', ard)
        elif acao == 'vol':
            print('vol')
            voltar(ard)
        else:
            anda_posicao(80)
            estado = segue_linha(sensores, estado)
        estado = 1
    elif qt_preto < 4:
        estado = segue_linha(sensores, estado)

