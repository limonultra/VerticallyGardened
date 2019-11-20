import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)  # Ignore warnings for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be output
                                          # and set initial value to low (off)

while True:
    GPIO.output(8, GPIO.HIGH)
    sleep(1)
    GPIO.output(8, GPIO.LOW)
    sleep(1)
