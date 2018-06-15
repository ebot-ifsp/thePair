#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
import math, time
diametro_roda = 30.0		# raio da roda do robom contando a esteira (mm)
distancia_eixos = 133.6		# distancia entre os eixos em mm:
taco_grau = math.pi/360.0
taco_mm = 0.5233
fator_correcao_angulo = 0.9
fator_correcao_linear = 1.8

m_esq = ev3.LargeMotor('outA')						# motorA (lado esquerdo)
m_dir = ev3.LargeMotor('outB')						# motorB (lado direito)
ir = ev3.InfraredSensor()							# sensor IF
gyro = ev3.GyroSensor('in1')						# giroscopio no in1
gyro.mode='GYRO-ANG'
ir = ev3.InfraredSensor() 
ir.mode = 'IR-PROX'

def gira_angulo(angulo, block=True):
	taco = angulo*taco_grau
	taco = taco*fator_correcao_angulo
	m_esq.run_to_rel_pos(position_sp=taco, speed_sp=300, stop_action="brake")
	m_dir.run_to_rel_pos(position_sp=-1*taco, speed_sp=300, stop_action="brake")
	if block: 
		hold_on()

def gira_angulo_gyro(angulo, block=True):
	angulo_inicial = gyro.value()
	angulo_atual = angulo_inicial
	if angulo > 0:
		m_esq.run_forever(speed_sp=200)
		m_dir.run_forever(speed_sp=-200)
		while angulo_atual < angulo + angulo_inicial:
			time.sleep(0.01)
			angulo_atual = gyro.value()
		anda(0, 0)
	elif angulo < 0:
		m_esq.run_forever(speed_sp=-200)
		m_dir.run_forever(speed_sp=200)	
		while angulo_atual > angulo + angulo_inicial:
			time.sleep(0.01)
			angulo_atual = gyro.value()
		anda(0, 0)
	if block:
		hold_on()

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

def anda_posicao(distancia, velocidade=300, block=True):
	n_taco = distancia/taco_mm
	n_taco = n_taco*fator_correcao_linear
	m_esq.run_to_rel_pos(position_sp=n_taco, speed_sp=velocidade, stop_action="brake")
	m_dir.run_to_rel_pos(position_sp=n_taco, speed_sp=velocidade, stop_action="brake")
	if block:
		hold_on()

def parar():
	anda_posicao(0)

def hold_on():
	while len(m_esq.state) > 0 or len(m_dir.state) > 0:
		time.sleep(0.01)
