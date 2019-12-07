import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

while True:
    print "Relay on"
    GPIO.output(24, GPIO.HIGH)
    time.sleep(1.5)
    print "Relay off"
    GPIO.output(24, GPIO.LOW)
    time.sleep(1.5)



