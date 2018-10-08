#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
from ev3dev.ev3 import Button
import math, time
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

diametro_roda = 30.0                   # raio da roda do robo (mm)
taco_mm = math.pi*diametro_roda/360.0  # distancia percorrida em um taco (1 grau)

gambiarra_angulo = float(cfg.get('velocidades', 'gambiarra_angulo'))
fator_correcao_linear = float(cfg.get('velocidades', 'fator_correcao_linear'))
v_reta = int(cfg.get('velocidades', 'v_reta'))
v_gira = int(cfg.get('velocidades', 'v_reta'))

limiar_if = int(cfg.get('sensor_linha', 'limiar_if'))

minimo_if = int(cfg.get('bloco', 'minimo_if'))
bloco_anda1 = int(cfg.get('bloco', 'bloco_anda1'))
bloco_anda2 = int(cfg.get('bloco', 'bloco_anda2'))
bloco_anda3 = int(cfg.get('bloco', 'bloco_anda3'))

curvaverde_anda = int(cfg.get('curvaVerde', 'curvaverde_anda'))
curvaverde_gira = int(cfg.get('curvaVerde', 'curvaverde_gira'))
volta_gira = int(cfg.get('curvaVerde', 'volta_gira'))
volta_lado = cfg.get('curvaVerde', 'volta_lado')

pino_motor_esquerda = cfg.get('pinos', 'pino_motor_esquerda')
pino_motor_direita = cfg.get('pinos', 'pino_motor_direita')
pino_if = cfg.get('pinos', 'pino_if')
pino_corE = cfg.get('pinos', 'pino_corE')
pino_corD = cfg.get('pinos', 'pino_corD')

m_esq = ev3.LargeMotor(pino_motor_esquerda)					
m_dir = ev3.LargeMotor(pino_motor_direita)					

# gyro = ev3.GyroSensor(pino_gyro)
# gyro.mode='GYRO-ANG'

ir = ev3.InfraredSensor(pino_if)
ir.mode = 'IR-PROX'

btn = Button()

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
    
def gira_angulo(angulo, block=True):
    n_taco = angulo * gambiarra_angulo
    m_esq.run_to_rel_pos(position_sp=n_taco,
                         speed_sp=100, 
                         stop_action="brake")
    m_dir.run_to_rel_pos(position_sp=-1*n_taco,
                         speed_sp=-100, 
                         stop_action="brake")
    if block:
        hold_on()

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

def viu_verde(r, g, b):
    lim_inf = 25
    lim_sup = 80
    prop = 1.5
    if (r < lim_sup and g < lim_sup and g > lim_inf):
        if g > r*prop:
            return True
    return False        
        
        
        
        
