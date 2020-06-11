import time
import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
import time
import requests

def receiveW():
       
    firebase_url = 'https://seniordesign-e59ca.firebaseio.com/'
    user = '3xL6MRsUvrN7I2H134ejPGglGgr2'
    
    req = requests.get(firebase_url + '/users/'+ user +'/sensors/WaterInterval.json')
    d = req.json()
    return d

#Tuneables
duration = 10 # seconds
delay = 5 # minutes

#GPIO setup
Wat_GPIO = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(Wat_GPIO , GPIO.OUT)

last = datetime.now()+timedelta(minutes = delay)
try:
    while(1):
        now = datetime.now()
        delay = receiveW()
        if (delay>7) or (delay<3):
            delay = 5
        if(now>(last+timedelta(minutes = delay))):
        
            # Pump ON
            GPIO.output(Wat_GPIO , GPIO.HIGH)
            # Duration
            time.sleep(duration)
            # Pump OFF
            GPIO.output(Wat_GPIO, GPIO.LOW)

            last=now
        time.sleep(10)
        
        
except KeyboardInterrupt:
    GPIO.output(Wat_GPIO, GPIO.LOW)
    GPIO.cleanup()
    print('Water Pump Shut Off')