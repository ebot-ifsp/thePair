#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
from movimento import *

def sensoresEsquerda(s):
    return s[0] or s[1]

def sensoresDireita(sensores):
    return s[6] or s[7]

def sensoresMeio(sensores):
    return s[3] or s[4]

def segue_linha(sensores,estado):
    if estado == 1:
        if not sensoresMeio(sensores):
            anda_posicao(50)
            return 1
        if sensoresDireta(sensores):
            gira_angulo_gyro(-80)
            return 2
        if sensoresEsquerda(sensores):
            gira_angulo_gyro(80)
            return 3
    if estado == 2:
        if sensoresMeio(sensores):
            anda_posicao(50)
            return 1
    if estado == 3:
        if sensoresMeio(sensores):
            anda_posicao(50)
            return 1

def desvia_bloco():
    gira_angulo_gyro(90)
    anda_posicao(200)
    gira_angulo_gyro(-90)
    anda_posicao(400)
    gira_angulo_gyro(-90)
    anda_posicao(200)
    gira_angulo_gyro(90)
