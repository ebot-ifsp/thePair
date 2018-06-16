#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from ev3dev.ev3 import *
from time import sleep

# beep e frequencias:
for i in range(5):
    Sound.beep()
    sleep(1)

Sound.tone([(500, 1000, 400)] * 3).wait()

Sound.speak('The book is on the table').wait()


# pisca o led do brick
Leds.set_color(Leds.RIGHT, Leds.RED)
sleep(1)
Leds.set_color(Leds.RIGHT, Leds.GREEN)
sleep(1)
Leds.set_color(Leds.LEFT, Leds.GREEN)
sleep(1)
Leds.set_color(Leds.LEFT, Leds.RED)
sleep(1)
Leds.all_off()


