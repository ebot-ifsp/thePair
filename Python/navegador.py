#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import time
from ev3dev.ev3 import Leds
from movimento import *
from sensores import *
from controle import *

def left(state):
    global bt_left
    if state:
        print('bt left')
        bt_left = True

def right(state):
    global bt_right
    if state:
        print('bt right')
        bt_right = True

bt_left = False
bt_right = False
btn.on_left = left
btn.on_right = right
bt_sair = False

if __name__ == '__main__':
    while True:
        Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)  # iniciar
        Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        print('aguardando bt para iniciar')
        while not btn.any():         
            time.sleep(0.01)
            if 'right' in btn.buttons_pressed:
                bt_sair = True
        if bt_sair:
            break
        Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)       # ready go
        Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)      # go go go
        print('Iniciando')
        time.sleep(1)
        buffer_cor = 0
        n_buffer_cor = 4
        cor_esquerda = []
        cor_direita = []
        bt_left = False
        while not bt_left:
            btn.process()
            ############################################
            ## verifica se tem obstaculo para desviar ##
            ############################################
            if ir.value() < minimo_if:                     # caso chegue no obstaculo
                print('desvia bloco')
                desvia_bloco()                            #debug trocar
            ###################################################
            ## verificar se alguma linha verde foi encotrada ##
            ###################################################
            linha_esquerda = viu_verde(corE.red, corE.green, corE.blue)
            linha_direita = viu_verde(corD.red, corD.green, corD.blue)
            if linha_direita or linha_esquerda:
                cor_direita.append(linha_direita)
                cor_esquerda.append(linha_esquerda)
                alinhar()
                for i in range(n_buffer_cor - 1):
                    linha_esquerda = viu_verde(corE.red, corE.green, corE.blue)
                    linha_direita = viu_verde(corD.red, corD.green, corD.blue)
                    cor_direita.append(linha_direita)
                    cor_esquerda.append(linha_esquerda)
                    anda_posicao(0.5)
                if True in cor_direita and True in cor_esquerda:
                    print('curva voltar')
                    parar()
                    time.sleep(0.1)
                    gira_angulo(90)                             # gira 90 graus
                    time.sleep(0.1)
                    gira('direita', v_gira/2)                   # continua girando
                    while not sensoresMeio(ard.sensores()):     # ate linha chegar nomeio do
                        time.sleep(0.1)                         # sensor
                    parar()     
                elif True in cor_esquerda:
                    print('curva esquerda')
                    curva_alinhar('esquerda', 8)
                elif True in cor_direita:
                    print('curva direita')
                    curva_alinhar('direita', 8)
                cor_esquerda = []
                cor_direita = []
                buffer_cor = 0

            ##########################
            ## Seguidor de linha    ##
            ##########################
            sensores_float = ard.le_todos()
            sensores_bool = ard.sensores(sensores_float)
            qt_sensores = ard.quantidade(sensores_bool)
            ## if linha normal - reta ou curva ###
            if qt_sensores > 0 and qt_sensores < 4:
                pos = ard.pos_linha(sensores_float) - 4500
                pos = pos/8
                #pos = 90*pos/4500
                if pos > 90:
                    pos = 90
                elif pos < -90:
                    pos = -90
                anda(v_reta, pos)
            ## sem linha - anda reto
            elif qt_sensores == 0:
                anda(v_reta, 0)
            ## Encruzilhada passar reto
            elif qt_sensores > 6:
                anda_posicao(5)
            ## if curva 90 graus ##
            else:
                if sensoresDireita(sensores_bool) and sensoresEsquerda(sensores_bool):
                    print('esquerda e direita - zica')
                elif sensoresDireita(sensores_bool):
                    print('Direita')
                    curva_alinhar('direita')
                elif sensoresEsquerda(sensores_bool):
                    print('Esquerda')
                    curva_alinhar('esquerda')
        parar()
    parar()
    Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    time.sleep(1)

    # except Exception as e:
    #     parar()
    #     Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    #     Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    #     print('except', e)
    #     time.sleep(1)
