# coding: utf-8

import RPi.GPIO as GPIO
import time

SOUNDER = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)

Hz = [261.6,293.7,329.6,349.2,392.0,440.0,493.9,523.2]
p = GPIO.PWM(SOUNDER, 1)
p.start(50)
for i in Hz:
    p.ChangeFrequency(i)
    time.sleep(1)
p.stop()
GPIO.cleanup()
