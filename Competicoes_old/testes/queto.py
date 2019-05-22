#!/usr/bin/env python3


import ev3dev.ev3 as ev3


m_esq = ev3.LargeMotor('outB')
m_dir = ev3.LargeMotor('outC')

m_esq.stop()
m_dir.stop()
