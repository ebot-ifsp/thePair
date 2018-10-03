#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
import math, time

diametro_roda = 30.0                   # raio da roda do robo (mm)
taco_mm = math.pi*diametro_roda/360.0  # distancia percorrida em um taco (1 grau)
fator_correcao_linear = 1.1            # correcao

v_reta = 200
v_gira = 150

m_esq = ev3.LargeMotor('outC')						# motorA (lado esquerdo)
m_dir = ev3.LargeMotor('outB')						# motorB (lado direito)

gyro = ev3.GyroSensor('in2')						# giroscopio no in1
gyro.mode='GYRO-ANG'

ir = ev3.InfraredSensor('in1') 
ir.mode = 'IR-PROX'

def anda(velocidade, direcao):
    if direcao > 0:
        speed_sp_dir = int((90 - direcao)*velocidade/90)
        speed_sp_esq = velocidade
    elif direcao < 0:
        speed_sp_esq = int((90 + direcao)*velocidade/90)
        speed_sp_dir = velocidade
    else:
        speed_sp_esq = velocidade
        speed_sp_dir = velocidade
    m_esq.run_forever(speed_sp=speed_sp_esq)
    m_dir.run_forever(speed_sp=speed_sp_dir)

def anda_posicao(distancia, velocidade=150, block=True):
    n_taco = (distancia/taco_mm)*fator_correcao_linear
    m_esq.run_to_rel_pos(position_sp=n_taco, speed_sp=velocidade, stop_action="brake")
    m_dir.run_to_rel_pos(position_sp=n_taco, speed_sp=velocidade, stop_action="brake")
    if block:
        hold_on()
    
def gira_angulo(angulo):
    gyro.mode = 'GYRO-RATE'
    gyro.mode='GYRO-ANG'
    angulo_inicial = gyro.value()
    angulo_atual = angulo_inicial
    if angulo > 0:
        m_esq.run_forever(speed_sp=v_gira)
        m_dir.run_forever(speed_sp=-v_gira)
        while angulo_atual < angulo + angulo_inicial:
            time.sleep(0.01)
            angulo_atual = gyro.value()
    elif angulo < 0:
        m_esq.run_forever(speed_sp=-v_gira)
        m_dir.run_forever(speed_sp=v_gira)
        while angulo_atual > angulo + angulo_inicial:
            time.sleep(0.01)
            angulo_atual = gyro.value()
    parar()

def gira(lado, velocidade=v_gira):
    if lado == 'direita':
        m_esq.run_forever(speed_sp=velocidade)
        m_dir.run_forever(speed_sp=-velocidade)
    elif lado == 'esquerda':
        m_esq.run_forever(speed_sp=-velocidade)
        m_dir.run_forever(speed_sp=velocidade)
        
def hold_on(time_out=20):
    t_inicial = time.clock()
    while len(m_esq.state) > 0 or len(m_dir.state) > 0:
        time.sleep(0.01)
        if time.clock() - t_inicial > time_out:
            break

def parar():
    m_esq.stop()
    m_dir.stop()
        
        
        
        
        
        
        
        
        