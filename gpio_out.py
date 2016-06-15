# Must run as root on rpi

import RPi.GPIO as GPIO
import time

OUTPUT_PIN = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

def on_off(t=5):
    GPIO.output(OUTPUT_PIN, True)
    time.sleep(t)
    GPIO.output(OUTPUT_PIN, False)
    GPIO.cleanup()
