#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
from movimento import *
from arduino import *

def sensoresDireita(s):
    return s[1] or s[2]

def sensoresMeio(s):
    return s[3] or s[4]

def sensoresEsquerda(s):
    return s[5] or s[6]

def voltar(ard):
    gira_angulo(volta_gira)
    gira(volta_lado)
    sensores = ard.sensores()
    while not sensoresMeio(sensores):
        sensores = ard.sensores()
        time.sleep(0.01)
    estado = 1
    anda(v_reta, 0)

def curvaVerde(direcao,ard):
    anda_posicao(curvaverde_anda)
    if direcao == 'esq':
        gira_angulo(-curvaverde_gira)
        gira('esq')
    else:
        gira_angulo(curvaverde_gira)
        gira('dir')
    sensores = ard.sensores()
    while not sensoresMeio(sensores):
        sensores = ard.sensores()
        time.sleep(0.01)
    estado = 1
    anda(v_reta, 0)
    time.sleep(0.5)

def segue_linha(sensores,estado):
    if estado == 1:
        if not sensoresEsquerda(sensores) and not sensoresDireita(sensores):
            anda(v_reta, 0)
            return 1
        if sensoresDireita(sensores):
            gira('direita')
            return 2
        if sensoresEsquerda(sensores):
            gira('esquerda')
            return 3
    if estado == 2:
        if sensoresMeio(sensores):
            anda(v_reta,0)
            return 1
        gira('direita')
        return 2
    if estado == 3:
        if sensoresMeio(sensores):
            anda(v_reta,0)
            return 1
        gira('esquerda')
        return 3

def desvia_bloco():
    gira_angulo(-90)
    anda_posicao(bloco_anda1)
    gira_angulo(90)
    anda_posicao(bloco_anda2)
    gira_angulo(90)
    anda_posicao(bloco_anda3)
    gira_angulo(-90)
