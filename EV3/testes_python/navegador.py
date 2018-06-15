#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import ev3dev.ev3 as ev3
from controle import *
from arduino import *
import time

inp = Arduino()
estado = 1

while 1:
	if ir.value() < 25:	# caso chegue no obstaculo
		desvia_bloco()
	sensores = inp.sensores()

	if sensores.count(True) > 4: # fim de curso - Voltar
		voltar()
	elif sensores.count(True) == 4: # cor para virar - descobrir para onde
		pass # implementar
	elif sensores.count(True) == 0:
		pass # parar() # implementar
	elif sensores.count(True) < 4 and  sensores.count(True) > 0:
		estado = segue_linha(sensores,estado)
	
	# implementar -> andar fora da linha 




'''
import time
import math
diametro_roda = 30		# raio da roda do robom contando a esteira (mm)
distancia_eixos = 133.6		# distancia entre os eixos em mm:
taco_grau = 7.5

class Navegador():
	
	def __init__(self, esq='outA', dir='outC', cor = 0.765):
		self.motE = ev3.LargeMotor(esq)
		self.motD = ev3.LargeMotor(dir)
		self.fatorC = cor
		self.a = Arduino()
	def esquerda(self):
		self.motD.run_timed(time_sp=100, speed_sp=500)
	def direita(self):
	    self.motE.run_timed(time_sp=100, speed_sp=500)
	def frente(self):
		self.motD.run_timed(time_sp=100, speed_sp=500)
		self.motE.run_timed(time_sp=100, speed_sp=500)
	def contornaLeite(self):
		self.motD.run_timed(time_sp=1400,speed_sp=500)
		time.sleep(1.4)
		self.motD.run_timed(time_sp=400,speed_sp=500)
		self.motE.run_timed(time_sp=400,speed_sp=500)
		time.sleep(0.4)
		self.motE.run_timed(time_sp=1500,speed_sp=500)
		time.sleep(1.5)
		self.motE.run_timed(time_sp=300,speed_sp=500)
		self.motD.run_timed(time_sp=300,speed_sp=500)
		time.sleep(0.3)
		self.motE.run_timed(time_sp=1300,speed_sp=500)
		time.sleep(1.3)
		self.motE.run_timed(time_sp=800,speed_sp=500)
		self.motD.run_timed(time_sp=800,speed_sp=500)
		time.sleep(0.8)
	def distancia_linear(self,angulo):
		return diametro_roda*angulo*math.pi

	def gira_angulo(self,angulo):
		angulo=self.fatorC*angulo
		taco = angulo*taco_grau
		self.motE.run_to_rel_pos(position_sp=taco, speed_sp=300, stop_action="brake")
		self.motD.run_to_rel_pos(position_sp=-1*taco, speed_sp=300, stop_action="brake")	
	def sensor(self,n):
		return self.a.le(n)>128

	def andaAteFaixa(self):
		while(not self.sensor(2) and  not self.sensor(3) and not self.sensor(4) and not self.sensor(5) and not self.sensor(6)):
			self.frente()
		
	def navegue(self):
		a=Arduino();
		if(a.le(1)>128):
			self.frente()
		if(a.le(7)>128):
			self.esquerda()
		if(a.le(4)>128):
			self.direita()
		for i in range(0,10):
			self.esquerda()
			time.sleep(0.1)
		for i in range(0,20):
			self.direita()
			time.sleep(0.1)
		for i in range(0,10):
			self.esquerda()
			time.sleep(0.1)
		for i in range(0,10):
			self.frente()
			time.sleep(0.1)
		for i in range(0,20):
			self.esquerda()
			time.sleep(0.1)
			self.frente()
			time.sleep(0.1)
'''
	
			
	
