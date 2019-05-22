from ev3dev2.sensor.lego import ColorSensor, InfraredSensor

pino_ir = '4'
pino_corE = '2'
pino_corD = '3'

fator_ir_distancia = 0.9

ir = InfraredSensor()
ir.mode = 'IR-PROX'

corE = ColorSensor(pino_corE)
corD = ColorSensor(pino_corD)

corE.mode = 'RGB-RAW'
corD.mode = 'RGB-RAW'

def viu_verde(r, g, b):
    lim_inf = 25
    lim_sup = 80
    prop = 1.5
    if (r < lim_sup and g < lim_sup and g > lim_inf):
        if g > r*prop:
            return True
    return False      

def le_rgb(sensor):
    return corE.red, corE.green, corE.blue

def distancia_ir():
    return ir.proximity*fator_ir_distancia