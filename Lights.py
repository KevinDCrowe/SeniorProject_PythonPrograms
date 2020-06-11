import time
import RPi.GPIO as GPIO
try:
    #Tuneables
    duration_h = 10 # Hours
    duration = duration_h * 3600 # Seconds
    GPIOnum = 4 # GPIO port used

    #GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIOnum, GPIO.OUT)

    # Lights ON
    GPIO.output(GPIOnum, GPIO.HIGH)
    # Duration
    time.sleep(duration)
    # Lights OFF
    GPIO.output(GPIOnum, GPIO.LOW)
    
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.output(GPIOnum,GPIO.LOW)
    GPIO.cleanup()
    print('Lights Shut off')