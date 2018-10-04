#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
from movimento import *
from arduino import *
from navegador import ard

def sensoresEsquerda(s):
    return s[1] or s[2]

def sensoresMeio(s):
    return s[3] or s[4]

def sensoresDireita(s):
    return s[5] or s[6]

def voltar():
    gira_angulo(volta_gira)
    gira(volta_lado)
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

def curva_alinhar(lado):
    anda_posicao(20)
    gira(lado, v_gira/2)                        # continua girando
    while not sensoresMeio(ard.sensores()):     # ate linha chegar nomeio do
        time.sleep(0.1)

def desvia_bloco():
    # alinhar
    gira_angulo(90)
    time.sleep(0.1)
    parar()
    time.sleep(0.1)
    anda(v_reta, -40)
    while not sensoresMeio(ard.sensores()):
        time.sleep(0.05)
    print('parar')
    parar()
    # gira_angulo(90)
    # anda_posicao(bloco_anda1)
    # gira_angulo(-90)
    # anda_posicao(bloco_anda2)
    # gira_angulo(-90)
    # anda(v_reta/2, 0)
    # while not sensoresMeio(ard.sensores()):
    #     time.sleep(0.05)
    # parar()
    # curva_alinhar('direita')
