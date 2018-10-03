#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
import configparser

cfg = configparser.ConfigParser()
btn = Button()
decisoes = []

def gravar():
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    Leds.set_color(Leds.LEFT, Leds.GREEN)
    cfg.read('config.cfg')
    cfgfile = open('config.cfg', 'w')
    cfg.set('ninja', 'sequencia', str(decisoes))
    cfg.write(cfgfile)
    cfgfile.close()

def pisca_led():
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    Leds.set_color(Leds.LEFT, Leds.GREEN)
    time.sleep(0.5)
    Leds.set_color(Leds.RIGHT, Leds.RED)
    Leds.set_color(Leds.LEFT, Leds.RED)

def left(state):
    if state:
        decisoes.append('esq')
        pisca_led()

def right(state):  # neater use of 'if' follows:
    if state:
        decisoes.append('dir')
        pisca_led()

def up(state):
    if state:
        decisoes.append('reto')
        pisca_led()

def down(state):
    if state:
        decisoes.append('vol')
        pisca_led()

def enter(state):
    if state:
        decisoes.pop(-1)
        pisca_led()

def backspace(state):
    if state:
        gravar()
        sair = True
        exit()

btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
btn.on_enter = enter
btn.on_backspace = backspace

sair = False
Leds.set_color(Leds.RIGHT, Leds.GREEN)
Leds.set_color(Leds.LEFT, Leds.GREEN)
time.sleep(2)
Leds.set_color(Leds.RIGHT, Leds.RED)
Leds.set_color(Leds.LEFT, Leds.RED)
while not sair:
    btn.process()
    time.sleep(0.01)
