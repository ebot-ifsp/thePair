import time

import ev3dev.ev3 as ev3
from sensores import Arduino

a = Arduino()

m_esq = ev3.LargeMotor('outC')					
m_dir = ev3.LargeMotor('outB')		

def alinha():
    pos = a.pos_linha()
    print(pos)
    if pos > 4700:
        print(pos, 'dir')
        m_esq.run_forever(speed_sp=150)
        m_dir.run_forever(speed_sp=-150)
        print('aqui')
        while pos > 4600:
            pos = a.pos_linha()
            print(pos, 'dir-while')
    elif pos < 4300:
        print(pos, 'esq')
        m_esq.run_forever(speed_sp=-150)
        m_dir.run_forever(speed_sp=150)
        while pos < 4600:
            pos = a.pos_linha()
            print(pos, 'esq-while')
        

    m_esq.stop()
    m_dir.stop()
    print('alinhado', a.pos_linha())