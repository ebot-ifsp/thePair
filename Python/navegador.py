#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import time
from ev3dev.ev3 import Leds
from ev3dev.ev3 import Button
from movimento import *
from sensores import *
from controle import *

if __name__ == '__main__':

    estado = 1
    btn = Button()

    Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)  # iniciar
    Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
    print('aguardando bt para iniciar')
    while not btn.any():                                    # esperando botao para
        time.sleep(0.01)
    Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)       # ready go
    Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)      # go go go
    print('Iniciando')
    try:
        while not btn.any():
            ############################################
            ## verifica se tem obstaculo para desviar ##
            ############################################
            if ir.value() < minimo_if:                     # caso chegue no obstaculo
                print('devia bloco')
                #desvia_bloco()                            #debug trocar
            ###################################################
            ## verificar se alguma linha verde foi encotrada ##
            ###################################################
            r, g, b = corE.red, corE.green, corE.blue
            linha_esquerda = viu_verde(r, g, b)
            r, g, b = corD.red, corD.green, corD.blue
            linha_direita = viu_verde(r, g, b)
            if linha_direita:
                print('curva direita')
                #curva_alinhar('direita', 8)
            if linha_esquerda:
                print('curva esquerda')
                #curva_alinhar('esquerda', 8)
            if linha_direita and linha_esquerda:
                print('curva voltar')
                # parar()
                # time.sleep(0.1)
                # gira_angulo(90)                             # gira 90 graus
                # time.sleep(0.1)
                # gira('direita', v_gira/2)                   # continua girando
                # while not sensoresMeio(ard.sensores()):     # ate linha chegar nomeio do
                #     time.sleep(0.1)                         # sensor
                # parar()
                estado = 1 
            sensores = ard.sensores()
            qt_preto = ard.quantidade(sensores)
            print(sensores, qt_preto)
            ##########################
            ## Seguidor de linha    ##
            ##########################
            if qt_preto > 0 and qt_preto < 4:               # linha normal
                estado = segue_linha(sensores, estado)
                print(estado, 'maquina estado')
            ##################################
            ## Sem linha - anda para frente ##
            ##################################
            elif qt_preto == 0:                             # sem linha
                anda(v_reta, 0)
                estado = 1
                print(qt_preto, 'reta')
            ################################
            ## 7 ou 8 linhas - cruzamento ##
            ################################
            elif qt_preto > 6:                              # encruzilhada
                print(qt_preto, 'cruzamento')
                anda_posicao(10)
                estado = 1
            ####################
            ## Curva 90 graus ##
            ####################  
            elif qt_preto > 2:                              # virar 90 graus
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
        Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN) 
        Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        time.sleep(1)

    except Exception as e:
        parar()
        Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN) 
        Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('except', e)
        time.sleep(1)
