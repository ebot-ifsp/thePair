#!/usr/bin/env python3

# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
import numpy as np
import time
from movimento import *
from controle import *
from arduino import *
import movimento as mov

ard = Arduino()
estado = 1
estado_ant = 1

try:
   while 1:
        print('1')
        sensores = ard.sensores()
        print('2')
        estado = segue_linha(sensores, estado)
        print('3')
        if estado_ant != estado:
            print('4')
            print('5: ', sensores)
            estado_ant = estado
except Exception as e:# (KeyboardInterrupt, SystemExit):
    mov.parar()
    print('fim: ', e)

mov.parar()
print('fim')