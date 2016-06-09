# Must run as root on rpi

import RPi.GPIO as GPIO
import time

OUTPUT_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

def on_off(time = 25):
    GPIO.output(OUTPUT_PIN, True)
    time.sleep(time)
    GPIO.output(OUTPUT_PIN, False)
    GPIO.cleanup()
