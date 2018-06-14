#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import math
diametro_roda = 35.6		# raio da roda do robom contando a esteira (mm)
distancia_eixos = 133.6		# distancia entre os eixos em mm:
taco_grau = 7.5

m_esq = ev3.LargeMotor('outA')						# motorA (lado esquerdo)
m_dir = ev3.LargeMotor('outB')						# motorB (lado direito)
ir = ev3.InfraredSensor()							# sensor IF

def gira_angulo(angulo):
	taco = angulo*taco_grau
	m_esq.run_to_rel_pos(position_sp=taco, speed_sp=300, stop_action="brake")
	m_dir.run_to_rel_pos(position_sp=-1*taco, speed_sp=300, stop_action="brake")

def anda(velocidade, direcao):
	if direcao > 0:
		speed_sp_dir = int((100 - direcao)*velocidade/100)
		speed_sp_esq = velocidade
	elif direcao < 0:
		speed_sp_esq = int((100 + direcao)*velocidade/100)
		speed_sp_dir = velocidade
	else:
		speed_sp_esq = velocidade
		speed_sp_dir = velocidade
	m_esq.run_forever(speed_sp=speed_sp_esq)
	m_dir.run_forever(speed_sp=speed_sp_dir)

def parar(self):
	anda(0, 0)