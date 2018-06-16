#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
import numpy as np
import time
from movimento import *
from controle import *
from arduino import *

ard = Arduino()
estado = 1

try:
    while 1:
        if ir.value() < minimo_if:                     # caso chegue no obstaculo
            desvia_bloco()
        sensores = ard.sensores()
        qt_preto = np.count_nonzero(sensores)
        if qt_preto == 0:
            anda(v_reta + 200, 0)
        elif qt_preto > 3:                      # encruzilhada ou virada (verde)
            print('>3', qt_preto)
            try:
                acao = sequencia[0]
                sequencia.pop(0)
            except:
                print('Fim do programa')
                m_esq.stop()
                m_esq.stop()
                break
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
            estado = 1
        elif qt_preto < 4:
            estado = segue_linha(sensores, estado)
except:# (KeyboardInterrupt, SystemExit):
    m_esq.stop()
    m_esq.stop()
    print('fim')

m_esq.stop()
m_esq.stop()
print('fim')
