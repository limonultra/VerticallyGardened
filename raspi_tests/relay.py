import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

while True:
    print "Relay on"
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)
    print "Relay off"
    GPIO.output(18, GPIO.LOW)



