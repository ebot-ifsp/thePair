#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
from movimento import *
from arduino import *

def sensoresEsquerda(s):
    return s[1] or s[2]

def sensoresMeio(s):
    return s[3] or s[4]

def sensoresDireita(s):
    return s[5] or s[6]

def voltar(ard):
    gira_angulo(120)
    gira('direita')
    sensores = ard.sensores()
    while not sensoresMeio(sensores):
        sensores = ard.sensores()
        time.sleep(0.01)
    estado = 1
    anda_posicao(50)

def curvaVerde(direcao,ard):
    anda_posicao(70)
    if direcao == 'esquerda':
        gira_angulo(-60)
        gira('esquerda')
    else:
        gira_angulo(60)
        gira('direita')
    sensores = ard.sensores()
    while not sensoresMeio(sensores):
        sensores = ard.sensores()
        time.sleep(0.01)
    estado = 1
    anda(v_reta, 0)

def segue_linha(sensores,estado):
    if estado == 1:
        if not sensoresEsquerda(sensores) and not sensoresDireita(sensores):
            anda(v_reta, 0)
            return 1
        if sensoresDireita(sensores):
            gira('esquerda')
            return 2
        if sensoresEsquerda(sensores):
            gira('direita')
            return 3
    if estado == 2:
        if sensoresMeio(sensores):
            anda(v_reta,0)
            return 1
        gira('esquerda')
        return 2
    if estado == 3:
        if sensoresMeio(sensores):
            anda(v_reta,0)
            return 1
        gira('direita')
        return 3

def desvia_bloco():
    gira_angulo(90)
    anda_posicao(250)
    gira_angulo(-90)
    anda_posicao(450)
    gira_angulo(-90)
    anda_posicao(250)
    gira_angulo(90)
