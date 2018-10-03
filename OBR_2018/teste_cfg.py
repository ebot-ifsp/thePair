import ConfigParser, math

cfg = ConfigParser.ConfigParser()
cfg.read('config.cfg')

diametro_roda = 30.0                   # raio da roda do robo (mm)
taco_mm = math.pi*diametro_roda/360.0  # distancia percorrida em um taco (1 grau)

sequencia = eval(cfg.get('ninja', 'sequencia'))

fator_correcao_linear = float(cfg.get('velocidades', 'fator_correcao_linear'))
v_reta = int(cfg.get('velocidades', 'v_reta'))
v_gira = int(cfg.get('velocidades', 'v_reta'))

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
pino_gyro = cfg.get('pinos', 'pino_gyro')
pino_if = cfg.get('pinos', 'pino_if')
