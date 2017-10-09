#!/usr/bin/python2
"""Activate GPIO Pins on Raspberry Pi for electrical system"""

test = True
while test:
  import time
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(16, GPIO.OUT)
  GPIO.output(16, GPIO.HIGH)
  time.sleep(2)
  test = False
