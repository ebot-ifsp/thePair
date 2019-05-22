from ev3dev2.motor import LargeMotor, Motor
import math, time

diametro_roda = 30.0                   # raio da roda do robo (mm)
taco_mm = math.pi*diametro_roda/360.0  # distancia percorrida em um taco (1 grau)

fator_correcao_linear = 1.1
v_reta = 300
v_gira = 150

limiar_if = 50

minimo_if = 30
bloco_anda1 = 250
bloco_anda2 = 450
bloco_anda3 = 250

curvaverde_anda = 70
curvaverde_gira = 60
volta_gira = 100
volta_lado = 'direita'

pino_motor_esquerda = 'outA'
pino_motor_direita = 'outB'
pino_motor_garra = 'outC'
pino_if = 2

m_esq = LargeMotor(pino_motor_esquerda)					
m_dir = LargeMotor(pino_motor_direita)					
m_gar = Motor(pino_motor_garra)


def movimento_garra(angulo, velocidade):
    m_gar.run_to_rel_pos(position_sp=angulo, speed_sp=velocidade, stop_action="hold")

def sobe_garra():
    movimento_garra(90,800)

def desce_garra():
    movimento_garra(-90,800)

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

  