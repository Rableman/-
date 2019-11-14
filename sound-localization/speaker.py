# coding: utf-8

import RPi.GPIO as GPIO
import pigpio
import time

def getch():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

SOUNDER = 18
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)
#p = GPIO.PWM(SOUNDER, 1)
#p.start(50)
p = pigpio.pi()
p.set_mode(SOUNDER, pigpio.OUTPUT)
freq = 100
print("\r"+str(freq)+"Hz", end="")
while True:
    #p.ChangeFrequency(freq)
    p.hardware_PWM(SOUNDER, freq, 100000)
    key = ord(getch())
    if key == 3:
        break
    elif key == 106:
        freq -= 1
    elif key == 74:
        freq -= 100
    elif key == 107:
        freq += 1
    elif key == 75:
        freq += 100
    elif key == 108:
        freq += 10
    elif key == 104:
        freq -= 10
    else:
        print(key)

    if freq <= 1:
        freq = 1
    print("\r"+str(freq)+"Hz", end="")
print(str(freq)+"Hz")
p.set_mode(SOUNDER, pigpio.OUTPUT)
#GPIO.cleanup()
