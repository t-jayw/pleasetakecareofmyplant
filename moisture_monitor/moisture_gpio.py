# Must run as root on rpi

import RPi.GPIO as GPIO
import time

OUTPUT_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

def on_off(t=5):
    GPIO.output(OUTPUT_PIN, True)
    time.sleep(t)
    GPIO.output(OUTPUT_PIN, False)
    GPIO.cleanup()

def on():
    GPIO.output(OUTPUT_PIN, True)

def off():
    GPIO.output(OUTPUT_PIN, False)
    GPIO.cleanup()
